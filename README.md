# Supremo Tribunal Federal (STF)

Este coletor tem como objetivo a recuperação de informações sobre folhas de pagamentos dos membros ativos do Supremo Tribunal Federal. O site com as informações de **Rendimentos** pode ser acessado **[aqui](https://egesp-portal.stf.jus.br/transparencia/rendimento_folha)**.

O coletor será estruturado como uma CLI. Uma vez passado como argumentos mês e ano, será feito o download de uma planilha, no formato HTML:

A planilha segue o seguinte formato:
|Campo|Descrição|
|-----|---------|
|**Matrícula (String)**| Matrícula do funcionário.|
|**Nome (String)**| Nome completo do funcionário.|
|**Cargo (String)**| Cargo do funcionário dentro do MP.|
|**Lotação (String)**| Local (cidade, departamento, promotoria) em que o funcionário trabalha.|
|**Vencimentos / Subsídios**| Vencimento do cargo efetivo, acrescido das vantagens pecuniárias permanentes estabelecidas em lei ou subsídio dos membros. |
|**Vantagens Pessoais**| Adicionais de Qualificação, vantagem pessoal nominalmente identificada - VPNI (Lei nº 9.624/98), adicional por tempo de serviço, pagamentos decorrentes de decisão judicial ou extensões administrativas. |
|**Vantagens de natureza periódica/eventual ou relativas às lotações dos servidores** | Serviço extraordinário (hora-extra), substituição, adicional de insalubridade, adicional de periculosidade, adicional noturno, gratificação de instrutória, gratificação pelo exercício cumulativo de ofício. |
|**Exercício de cargo em comissão/função comissionada**| retribuição pelo(a) cargo/função exercido(a) pelo servidor; |
|**Abono de Permanência**| O servidor titular de cargo efetivo que tenha completado as exigências para a aposentadoria voluntária e que opte por permanecer em atividade poderá fazer jus ao abono equivalente, no máximo, ao valor da sua contribuição previdenciária, até completar a idade para aposentadoria compulsória. |
|**Contribuição previdenciária**| Contribuição social do servidor público. |
|**Imposto de Renda**| Imposto sobre Renda Retido na Fonte (IRRF)|
|**Abate teto**| O teto remuneratório dos servidores corresponde ao subsídio dos Ministros do Supremo Tribunal Federal (Art. 37, XI, da CF).|
|**Descontos diversos**| Descontos de diversas naturezas.|
|**Férias**| Parcelas pagas a título de adicional de 1/3 (terço) de férias bem como adiantamento de férias, ou devolução de adiantamento.|
|**Gratificação natalina e antecipação**| Parcelas pagas a título de Gratificação Natalina ou antecipação de 50% da mesma.|
|**Auxílios e benefícios**| Pagamentos de valores a título de auxílios, como alimentação, pré- escolar, natalidade, transporte e etc.|
|**Indenizações**| Indenizações de férias, indenizações de transporte e outras situações previstas em lei.|
|**Exercícios Anteriores e licença prêmio convertida em pecúnia**| Pagamento de licença prêmio.|
|**Auxílio Moradia**| Pagamento de Auxílio Moradia.|


## Como usar

### Executando com Docker

 - Inicialmente é preciso instalar o [Docker](https://docs.docker.com/install/). 
 - A imagem do contêiner do coletor poderá ser construída ou baixada. 

 - Construção da imagem:

     ```sh
    $ docker build --pull --rm -t coletor-stf:latest .
     ```
 - Download da imagem:

    ```sh
    $ docker pull ghcr.io/dadosjusbr/coletor-stf:main
    ```
 - Execução:
 
    ```sh
    $ docker run -i --rm -e YEAR=2021 -e MONTH=03 -e OUTPUT_FOLDER=/output --name coletor-stf --mount type=bind,src=/tmp/coletor-stf,dst=/output coletor-stf
    ```

### Execução sem Docker:

- Para executar o script é necessário rodar o seguinte comando, a partir do diretório mpma, adicionando às variáveis seus respectivos valores, a depender da consulta desejada. É válido lembrar que faz-se necessario ter o [Python 3.8+](https://www.python.org/downloads/) instalado, bem como o chromedriver compatível com a versão do seu Google Chrome. Ele pode ser baixado [aqui](https://chromedriver.chromium.org/downloads).
 
    ```sh
    $ YEAR=2021 MONTH=03 DRIVER_PATH=/chromedriver GIT_COMMIT=$(git rev-list -1 HEAD) python3 src/main.py
    ```
- Para que a execução do script possa ser corretamente executada é necessário que todos os requirements sejam devidamente instalados. Para isso, executar o [PIP](https://pip.pypa.io/en/stable/installing/) passando o arquivo requiments.txt, por meio do seguinte comando:
   
   ```sh
    $ pip install -r requirements.txt
   ```