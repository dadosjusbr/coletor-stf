from coleta import coleta_pb2 as Coleta

from headers_keys import (CONTRACHEQUE, HEADERS)
import number
import re


def parse_employees(file, chave_coleta, month, year):
    employees = {}
    counter = 1
    for row in file:
        member = Coleta.ContraCheque()
        member.id_contra_cheque = chave_coleta + "/" + str(counter)
        member.chave_coleta = chave_coleta
        member.matricula = str(row[0])
        member.nome = row[1]
        # Quando o membro não possui função, i.e. célula NaN, não é um membro ativo
        # Usando como exemplo ROSA MARIA PIRES WEBER, ex-ministra, ainda presente no contracheque
        if not number.is_nan(row[2]):
            member.funcao = row[2]
        else:
            continue
        if not number.is_nan(row[5]):
            member.local_trabalho = row[5]
        member.tipo = Coleta.ContraCheque.Tipo.Value("MEMBRO")
        member.ativo = True
        member.remuneracoes.CopyFrom(
            create_remuneration(row, month, year)
        )

        employees[str(row[0])] = member
        counter += 1

    return employees


def create_remuneration(row, month, year):
    remuneration_array = Coleta.Remuneracoes()
    for key, value in HEADERS[CONTRACHEQUE].items():
        remuneration = Coleta.Remuneracao()
        remuneration.natureza = Coleta.Remuneracao.Natureza.Value("R")
        remuneration.categoria = CONTRACHEQUE
        remuneration.item = key
        
        # Caso o valor seja negativo, ele vai transformar em positivo:
        valor = re.sub("[R$] ?", "", row[value]) # Tirando o "R$" da string
        remuneration.valor = float(abs(number.format_value(valor)))

        if value in [16, 17, 19, 20]:
            remuneration.valor = remuneration.valor * (-1)
            remuneration.natureza = Coleta.Remuneracao.Natureza.Value("D")
        elif value in [7, 8, 9, 10, 13]:
            remuneration.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("B")
        else:
            remuneration.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("O")
        remuneration_array.remuneracao.append(remuneration)

    # O item "Auxílio Moradia" passou a ser disponibilizado a partir de setembro de 2020
    if int(year) > 2020 or int(year) == 2020 and int(month) >= 9:
        remuneration = Coleta.Remuneracao()
        remuneration.natureza = Coleta.Remuneracao.Natureza.Value("R")
        remuneration.categoria = CONTRACHEQUE
        remuneration.item = "Auxílio Moradia"
        
        # Caso o valor seja negativo, ele vai transformar em positivo:
        valor = re.sub("[R$] ?", "", row[27]) # Tirando o "R$" da string
        remuneration.valor = float(abs(number.format_value(valor)))
        
        remuneration.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("O")
        remuneration_array.remuneracao.append(remuneration)
    return remuneration_array


def parse(data, chave_coleta):
    employees = {}
    payroll = Coleta.FolhaDePagamento()

    employees.update(parse_employees(data.contracheques, chave_coleta, data.month, data.year))

    for i in employees.values():
        payroll.contra_cheque.append(i)
    return payroll
