import sys
import os
import numpy

import pandas as pd

# Se for erro de não existir planilhas, o retorno vai ser esse:
STATUS_DATA_UNAVAILABLE = 4
# Caso o erro for a planilha, que é invalida por algum motivo, o retorno vai ser esse:
STATUS_INVALID_FILE = 5


def _read(file):
    try:
        data = pd.read_html(file)
        data = numpy.array(data[1])

    except Exception as excep:
        print(f"Erro lendo as planilhas: {excep}", file=sys.stderr)
        if "html5lib not found, please install it" in str(excep):
            sys.exit(STATUS_DATA_UNAVAILABLE)
        sys.exit(STATUS_INVALID_FILE)
    return data


def load(file_name, year, month, output_path):
    """Carrega os arquivos passados como parâmetros.
    
     :param file_name: slice contendo o arquivo baixado pelo coletor.
    O nome do arquivo deve seguir uma convenção e começar com 
    membros-ativos-contracheques
     :param year e month: usados para fazer a validação na planilha de controle de dados
     :return um objeto Data() pronto para operar com os arquivos
    """
    contracheques = _read(file_name)

    return Data(contracheques, year, month, output_path)

class Data:
    def __init__(self, contracheques, year, month, output_path):
        self.year = year
        self.month = month
        self.output_path = output_path
        self.contracheques = contracheques

    def validate(self):
        """
         Validação inicial do arquivo passado como parâmetro.
        Aborta a execução do script caso não encontre o arquivo,
        retornando o codigo 4, esse codigo significa que não 
        existe dados para a data pedida.
        """

        if not (
            os.path.isfile(
                f"{self.output_path}/membros-ativos-contracheques-{self.month}-{self.year}.html"
            )
        ):
            sys.stderr.write(f"Não existe planilha para {self.month}/{self.year}.")
            sys.exit(STATUS_DATA_UNAVAILABLE)