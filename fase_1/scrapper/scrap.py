import requests
import pandas as pd
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
import re
from typing import Optional

embrapa_url = "http://vitibrasil.cnpuv.embrapa.br"

abas = {
        'producao': 'opt_02',
        'processamento': 'opt_03',
        'comercializacao': 'opt_04',
        'importacao': 'opt_05',
        'exportacao': 'opt_06',
}

def http_get(url: str, aba: str, subopcao: Optional[str]  = None, ano: Optional[str] = None) -> BeautifulSoup:
    response = requests.get(url, params= {'opcao': abas[aba], 'subopcao': subopcao, 'ano': ano})
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def get_available_suboptions(embrapa_url: str, aba: str) -> dict[str,str]:
    soup = http_get(embrapa_url, aba)
    return {f'subopt_0{n +1}': sub_option.text for n, sub_option in enumerate(soup.find_all('button', 'btn_sopt'))}

def get_available_years(embrapa_url: str, aba: str, subopcao: Optional[str]  = None):
    soup = http_get(embrapa_url, aba, subopcao)
    periodo_busca = soup.find_all('label','lbl_pesq')[0].text
    ano_inicio, ano_fim = re.findall(r'\[(\d{4})-(\d{4})\]', periodo_busca)[0]
    return ano_inicio, ano_fim

def structure_table(soup: BeautifulSoup, table_attr: str) -> pd.DataFrame:
    linhas_com_valores = []
    
    # Iteração dentro da tabela, para cada linha
    for tabela in soup.find_all('table', attrs = table_attr):
        linhas = tabela.find_all("tr")
        
        for n, linha in enumerate(linhas):
            # Encontra e salva nomes das colunas
            if linha.findChildren('th'):
                colunas = [coluna.text.strip() for coluna in linha.findChildren('th')]
                continue
            
            # Detecta se linha é o total (última linha), e interrompe o looping antes de adicionar ela nas outras linhas
            if n == len(linhas) -1 :
                break
            
            linhas_com_valores.append([valor.text.strip() for valor in linha.findChildren('td')])
        
        # Criação de dataframe
        df = {colunas[id_coluna]: [valor[id_coluna] for valor in linhas_com_valores] for id_coluna in range(len(colunas))}
        df = pd.DataFrame(df)
        return df
    

def scrap_producao() -> pd.DataFrame:
    aba = 'producao'
    dfs = []
    ano_inicio, ano_fim = get_available_years(embrapa_url = embrapa_url, aba = aba)
    
    # Iteração para cada ano, lendo dados da tabela na página e concatenando resultados
    for ano in range(int(ano_inicio), int(ano_fim) + 1):
        soup = http_get(url =embrapa_url, aba = aba, ano = ano)
        df = structure_table(soup = soup, table_attr = "tb_base tb_dados").assign(ano = ano)
        dfs.append(df)
    
    return pd.concat(dfs)


def scrap_processamento() -> pd.DataFrame:
    aba = 'processamento'
    dfs = []
    
    sub_options = get_available_suboptions(embrapa_url, aba)
    
    # Iteração para cada sub aba
    for sub_option in sub_options.keys():
        ano_inicio, ano_fim = get_available_years(embrapa_url = embrapa_url, aba = aba, subopcao = sub_option)
    
        # Iteração para cada ano de cada sub aba, lendo dados da tabela na página e concatenando resultados
        for ano in range(int(ano_inicio), int(ano_fim) + 1):
            soup = http_get(url =embrapa_url, aba = aba, subopcao = sub_option, ano = ano)
            df = structure_table(soup = soup, table_attr = "tb_base tb_dados").assign(ano = ano) \
                                                                              .assign(classificacao_uva = sub_options[sub_option])
            
            # Altera nome de coluna diferente para o mesmo nome que aparece em outras abas
            if 'Sem definição' in df.columns:
                df = df.rename(columns = {'Sem definição':'Cultivar'})
                
            dfs.append(df)
    
    return pd.concat(dfs)


def scrap_comercializacao() -> pd.DataFrame:
    aba = 'comercializacao'
    dfs = []
    ano_inicio, ano_fim = get_available_years(embrapa_url = embrapa_url, aba = aba)
    
    # Iteração para cada ano, lendo dados da tabela na página e concatenando resultados
    for ano in range(int(ano_inicio), int(ano_fim) + 1):
        soup = http_get(url =embrapa_url, aba = aba, ano = ano)
        df = structure_table(soup = soup, table_attr = "tb_base tb_dados").assign(ano = ano)
        dfs.append(df)
    
    return pd.concat(dfs)


def scrap_importacao() -> pd.DataFrame:
    aba = 'importacao'
    dfs = []
    
    sub_options = get_available_suboptions(embrapa_url, aba)
    
    # Iteração para cada sub aba
    for sub_option in sub_options.keys():
        ano_inicio, ano_fim = get_available_years(embrapa_url = embrapa_url, aba = aba, subopcao = sub_option)
    
        # Iteração para cada ano de cada sub aba, lendo dados da tabela na página e concatenando resultados
        for ano in range(int(ano_inicio), int(ano_fim) + 1):
            soup = http_get(url =embrapa_url, aba = aba, subopcao = sub_option, ano = ano)
            df = structure_table(soup = soup, table_attr = "tb_base tb_dados").assign(ano = ano).assign(classificacao_derivado = sub_options[sub_option])
                
            dfs.append(df)
    
    return pd.concat(dfs)


def scrap_exportacao() -> pd.DataFrame:
    aba = 'exportacao'
    dfs = []
    
    sub_options = get_available_suboptions(embrapa_url, aba)
    
    # Iteração para cada sub aba
    for sub_option in sub_options.keys():
        ano_inicio, ano_fim = get_available_years(embrapa_url = embrapa_url, aba = aba, subopcao = sub_option)
    
        # Iteração para cada ano de cada sub aba, lendo dados da tabela na página e concatenando resultados
        for ano in range(int(ano_inicio), int(ano_fim) + 1):
            soup = http_get(url =embrapa_url, aba = aba, subopcao = sub_option, ano = ano)
            df = structure_table(soup = soup, table_attr = "tb_base tb_dados").assign(ano = ano).assign(classificacao_derivado = sub_options[sub_option])
                
            dfs.append(df)
    
    return pd.concat(dfs)