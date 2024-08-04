#%%
import requests
import pandas as pd
import pandas.api.types as ptypes
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
    """Realiza uma requisição GET no link informado junto de outros parâmetros. Ele retorna um objeto BeautifulSoup com o html obtido.

    Arguments:
        url {str} -- URL da embrapa que irá receber a requisição
        aba {str} -- Chave do dicionário "abas". Informe com base em qual aba do site da embrapa gostaria de fazer a requisição.
        subopcao {Optional[str]} -- Se este parâmetro for informado, adicona o parâmetro "subopcao" na requisição.
        ano {Optional[str]} -- Se este parâmetro for informado, adicona o parâmetro "ano" na requisição.
    """
    response = requests.get(url, params= {'opcao': abas[aba], 'subopcao': subopcao, 'ano': ano})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def get_available_suboptions(embrapa_url: str, aba: str) -> dict[str,str]:
    """Realiza requisição GET na url informada e, para a aba da página mencionada, retorna os valores existentes de subabas (subopções).
    O dicionário retornado contém o nome da subopção conforme seria utilizado na forma de parâmetro durante uma requisição, e o nome como é exibido na página do navegador.

    Arguments:
        url {str} -- URL da embrapa que irá receber a requisição
        aba {str} -- Chave do dicionário "abas". Informe com base em qual aba do site da embrapa gostaria de fazer a requisição.
    """
    soup = http_get(embrapa_url, aba)
    sub_options = {f'subopt_0{n +1}': sub_option.text for n, sub_option in enumerate(soup.find_all('button', 'btn_sopt'))}
    
    assert sub_options, f'Subopções da aba {aba} não encontradas'
    return sub_options

def get_available_years(embrapa_url: str, aba: str, subopcao: Optional[str]  = None):
    """Realiza requisição GET na url informada com parâmetros adicionados e retorna a faixa de anos em que há dados disponíveis

    Arguments:
        embrapa_url {str} -- URL da embrapa que irá receber a requisição
        aba {str} -- Chave do dicionário "abas". Informe com base em qual aba do site da embrapa gostaria de fazer a requisição.
        subopcao {Optional[str]} -- Se este parâmetro for informado, adicona o parâmetro "subopcao" na requisição.
    """
    soup = http_get(embrapa_url, aba, subopcao)
    periodo_busca = soup.find_all('label','lbl_pesq')[0].text
    ano_inicio, ano_fim = re.findall(r'\[(\d{4})-(\d{4})\]', periodo_busca)[0]
    
    return ano_inicio, ano_fim

def structure_table(soup: BeautifulSoup, table_attr: str) -> pd.DataFrame:
    """Gera um dataframe com dados da tabela de uma página.

    Arguments:
        soup {BeautifulSoup} -- Objeto BeautifulSoup gerado a partir de uma requisição e html do site da Embrapa
        table_attr {str} -- Nome do elemento tabela, escrito no html obtido de uma requisição.
    """
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
    """ Gera um dataframe com dados de tabelas de todos os anos disponíveis, da aba produção do site da Embrapa.
    """
    aba = 'producao'
    dfs = []
    ano_inicio, ano_fim = get_available_years(embrapa_url = embrapa_url, aba = aba)
    
    # Iteração para cada ano, lendo dados da tabela na página e concatenando resultados
    for ano in range(int(ano_inicio), int(ano_fim) + 1):
        soup = http_get(url =embrapa_url, aba = aba, ano = ano)
        df = structure_table(soup = soup, table_attr = "tb_base tb_dados").assign(ano = ano)
        dfs.append(df)
    dfs = pd.concat(dfs)
    
    assert dfs.shape[0] > 1, f'Tabela de dados da aba {aba} está vazia'
    assert list(dfs.columns) == ['Produto', 'Quantidade (L.)', 'ano'], 'Nomes de colunas obtidas do site não satisfazem os valores padrão de "Produto", "Quantidade (L.)", e "ano"'
    assert ptypes.is_string_dtype(dfs['Produto']), 'Tipo da coluna Produto não é string'
    assert ptypes.is_string_dtype(dfs['Quantidade (L.)']), 'Tipo da coluna Quantidade não é string'
    assert ptypes.is_numeric_dtype(dfs['ano']), 'Tipo da coluna ano não é numérico'
    return dfs


def scrap_processamento() -> pd.DataFrame:
    """ Gera um dataframe com dados de tabelas de todos os anos e subabas disponíveis, da aba processamento do site da Embrapa.
    """
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
    dfs = pd.concat(dfs)
    
    assert dfs.shape[0] > 1, f'Tabela de dados da aba {aba} está vazia'
    assert list(dfs.columns) == ['Cultivar', 'Quantidade (Kg)', 'ano', 'classificacao_uva'], 'Nomes de colunas obtidas do site não satisfazem os valores padrão de "Cultivar", "Quantidade (Kg)", "ano", e "classificacao_uva"'
    assert ptypes.is_string_dtype(dfs['Cultivar']), 'Tipo da coluna Cultivar não é string'
    assert ptypes.is_string_dtype(dfs['Quantidade (Kg)']), 'Tipo da coluna Quantidade não é string'
    assert ptypes.is_numeric_dtype(dfs['ano']), 'Tipo da coluna ano não é numérico'
    assert ptypes.is_string_dtype(dfs['classificacao_uva']), 'Tipo da coluna classificacao_uva não é string'
    return dfs


def scrap_comercializacao() -> pd.DataFrame:
    """ Gera um dataframe com dados de tabelas de todos os anos, da aba comercialização do site da Embrapa.
    """
    aba = 'comercializacao'
    dfs = []
    ano_inicio, ano_fim = get_available_years(embrapa_url = embrapa_url, aba = aba)
    
    # Iteração para cada ano, lendo dados da tabela na página e concatenando resultados
    for ano in range(int(ano_inicio), int(ano_fim) + 1):
        soup = http_get(url =embrapa_url, aba = aba, ano = ano)
        df = structure_table(soup = soup, table_attr = "tb_base tb_dados").assign(ano = ano)
        dfs.append(df)
    dfs = pd.concat(dfs)
    
    assert dfs.shape[0] > 1, f'Tabela de dados da aba {aba} está vazia'
    assert list(dfs.columns) == ['Produto', 'Quantidade (L.)', 'ano'], 'Nomes de colunas obtidas do site não satisfazem os valores padrão de "Produto", "Quantidade (L.)", e "ano"'
    assert ptypes.is_string_dtype(dfs['Produto']), 'Tipo da coluna Produto não é string'
    assert ptypes.is_string_dtype(dfs['Quantidade (L.)']), 'Tipo da coluna Quantidade não é string'
    assert ptypes.is_numeric_dtype(dfs['ano']), 'Tipo da coluna ano não é numérico'
    return dfs


def scrap_importacao() -> pd.DataFrame:
    """ Gera um dataframe com dados de tabelas de todos os anos e subabas disponíveis, da aba importação do site da Embrapa.
    """
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
    dfs = pd.concat(dfs)
    
    assert dfs.shape[0] > 1, f'Tabela de dados da aba {aba} está vazia'
    assert list(dfs.columns) == ['Países', 'Quantidade (Kg)', 'Valor (US$)', 'ano','classificacao_derivado'], 'Nomes de colunas obtidas do site não satisfazem os valores padrão de "Países", "Quantidade (Kg)", "Valor (US$)", "ano" e "classificacao_derivado"'
    assert ptypes.is_string_dtype(dfs['Países']), 'Tipo da coluna Países não é string'
    assert ptypes.is_string_dtype(dfs['Quantidade (Kg)']), 'Tipo da coluna Quantidade não é string'
    assert ptypes.is_string_dtype(dfs['Valor (US$)']), 'Tipo da coluna Valor (US$) não é string'
    assert ptypes.is_numeric_dtype(dfs['ano']), 'Tipo da coluna ano não é numérico'
    assert ptypes.is_string_dtype(dfs['classificacao_derivado']), 'Tipo da coluna classificacao_derivado não é string'
    return dfs


def scrap_exportacao() -> pd.DataFrame:
    """ Gera um dataframe com dados de tabelas de todos os anos e subabas disponíveis, da aba exportação do site da Embrapa.
    """
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
    dfs = pd.concat(dfs)
    
    assert dfs.shape[0] > 1, f'Tabela de dados da aba {aba} está vazia'
    assert list(dfs.columns) == ['Países', 'Quantidade (Kg)', 'Valor (US$)', 'ano','classificacao_derivado'], 'Nomes de colunas obtidas do site não satisfazem os valores padrão de "Países", "Quantidade (Kg)", "Valor (US$)", "ano" e "classificacao_derivado"'
    assert ptypes.is_string_dtype(dfs['Países']), 'Tipo da coluna Países não é string'
    assert ptypes.is_string_dtype(dfs['Quantidade (Kg)']), 'Tipo da coluna Quantidade não é string'
    assert ptypes.is_string_dtype(dfs['Valor (US$)']), 'Tipo da coluna Valor (US$) não é string'
    assert ptypes.is_numeric_dtype(dfs['ano']), 'Tipo da coluna ano não é numérico'
    assert ptypes.is_string_dtype(dfs['classificacao_derivado']), 'Tipo da coluna classificacao_derivado não é string'
    return dfs