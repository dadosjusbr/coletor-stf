from coleta import coleta_pb2 as Coleta

from headers_keys import (CONTRACHEQUE, HEADERS)
import number


def parse_employees(file, chave_coleta):
    employees = {}
    counter = 1
    for row in file:
        member = Coleta.ContraCheque()
        member.id_contra_cheque = chave_coleta + "/" + str(counter)
        member.chave_coleta = chave_coleta
        member.matricula = str(row[0])
        member.nome = row[1]
        member.funcao = row[2]
        member.local_trabalho = row[5]
        member.tipo = Coleta.ContraCheque.Tipo.Value("MEMBRO")
        member.ativo = True
        member.remuneracoes.CopyFrom(
            create_remuneration(row)
        )

        employees[str(row[0])] = member
        counter += 1
            
    return employees


def create_remuneration(row):
    remuneration_array = Coleta.Remuneracoes()
    for key, value in HEADERS[CONTRACHEQUE].items():
        remuneration = Coleta.Remuneracao()
        remuneration.natureza = Coleta.Remuneracao.Natureza.Value("R")
        remuneration.categoria = CONTRACHEQUE
        remuneration.item = key
        # Caso o valor seja negativo, ele vai transformar em positivo:
        remuneration.valor = float(abs(number.format_value(row[value])))

        if value in [16, 17, 19, 20]:
            remuneration.valor = remuneration.valor * (-1)
            remuneration.natureza = Coleta.Remuneracao.Natureza.Value("D")

        if value in [4]:
            remuneration.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("B")
        elif value in [8, 9, 10, 13, 22, 23, 24, 25, 26, 27]:
            remuneration.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("O")

        remuneration_array.remuneracao.append(remuneration)

    return remuneration_array


def update_employees(fn, employees, categoria):
    for row in fn:
        nome = row[0]
        if nome in employees.keys():
            emp = employees[nome]
            remu = create_remuneration(row, categoria)
            emp.remuneracoes.MergeFrom(remu)
            employees[nome] = emp
    return employees


def parse(data, chave_coleta, month, year):
    employees = {}
    folha = Coleta.FolhaDePagamento()

    # Puts all parsed employees in the big map
    if year == "2018" or year == "2019":
        employees.update(parse_employees(data.contracheque, chave_coleta, CONTRACHEQUE_2019))
    else:
        employees.update(parse_employees(data.contracheque, chave_coleta, CONTRACHEQUE))

    update_employees(data.indenizatorias, employees, INDENIZACOES)

    for i in employees.values():
        folha.contra_cheque.append(i)
    return folha