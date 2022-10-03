from coleta import coleta_pb2 as Coleta


def captura(month, year):
    metadado = Coleta.Metadados()
    metadado.nao_requer_login = True
    metadado.nao_requer_captcha = True
    metadado.acesso = Coleta.Metadados.FormaDeAcesso.ACESSO_DIRETO
    metadado.extensao = Coleta.Metadados.Extensao.HTML
    metadado.estritamente_tabular = True
    metadado.tem_matricula = True
    metadado.tem_lotacao = True
    metadado.tem_cargo = True
    metadado.receita_base = Coleta.Metadados.OpcoesDetalhamento.DETALHADO
    metadado.despesas = Coleta.Metadados.OpcoesDetalhamento.DETALHADO
    metadado.formato_consistente = True
    metadado.outras_receitas = Coleta.Metadados.OpcoesDetalhamento.SUMARIZADO
    # O item "Auxílio Moradia" passou a ser disponibilizado a partir de setembro de 2020
    if (year == 2020 and month == 9):
        metadado.formato_consistente = False
        
    return metadado