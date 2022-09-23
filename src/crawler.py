import requests
import sys
import os
import pathlib


def download(url, file_path):
    try:
        headers = {
            "authority": "egesp-portal.stf.jus.br",
            "method": "GET",
            "path": "/assets/1.jpg",
            "scheme": "https",
            "accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "cookie": "_ga=GA1.3.1173173078.1662485968; _gid=GA1.3.466465446.1663772947; _portal_session=spfjVrF0ffFO2nuYEug1PJMJ5S6Hbpw1vW37AT9dZX0dgyHNIIxm4CncLNDdCn3MJZueoeSo%2FQfj9DC2NJV3fGI2mrBWMkO7iV%2B1RIFnEcjm295RS9ZA7gyLZb2PdsjOy2r53jyuXoNxTCGQV84%3D--Xik7jqZFhRzqMm9Z--LRYqvBf6y5q91sB3JFAPUg%3D%3D; _gat_gtag_UA_149216086_6=1; Cookie-full-lb-prod=srv-funE+GAHukG8ebv6sc2KaA|Yys6i",
            "if-none-match": "afd175d4ab65ec7b2f2731b4ebd5c4a7ad31dbbc3b5a1eb555466cb2f97da8f8",
            "referer": url,
            "sec-ch-ua": '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux",
            "sec-fetch-dest": "image",
            "sec-fetch-mode": "no-cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        }
        response = requests.get(url, allow_redirects=False, headers=headers)
        with open(file_path, "wb") as file:
            file.write(response.content)
        file.close()
    except Exception as excep:
        sys.stderr.write("Não foi possível fazer o download do arquivo: " +
                         file_path + '. O seguinte erro foi gerado: ' + str(excep))
        os._exit(1)


def crawl(year, month, output_path):
    pathlib.Path(output_path).mkdir(exist_ok=True)
    filename = f'membros-ativos-contracheques-{month}-{year}.html'
    file_path = [f'{output_path}/{filename}']
    url = f'https://egesp-portal.stf.jus.br/transparencia/rendimento_folha?utf8=%E2%9C%93&tipo_relatorio=XLSX&q%5Bano_eq%5D={year}&q%5Bmes_eq%5D={int(month)}&q%5Bid_aux_eq%5D=0&q%5Bcdg_ordem_in%5D%5B%5D=&q%5Bcdg_cargo_efetivo_in%5D%5B%5D=&q%5Bcdg_cargo_comissionado_in%5D%5B%5D=&q%5Bcdg_funcao_in%5D%5B%5D=&q%5Bcdg_unidade_in%5D%5B%5D=&q%5Bcdg_sitfunc_eq%5D=12&button='
    download(url, file_path[0])

    return file_path
