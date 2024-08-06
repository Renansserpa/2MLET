import pytest
import pandas.api.types as ptypes
from scrapper.scrap import scrap_producao, scrap_processamento, scrap_comercializacao, scrap_importacao, scrap_exportacao

# ------------- Armazenamento de dados extraídos -------------
@pytest.fixture(scope="session")
def producao_data():
    df = scrap_producao()
    return df

@pytest.fixture(scope="session")
def processamento_data():
    df = scrap_processamento()
    return df

@pytest.fixture(scope="session")
def comercializacao_data():
    df = scrap_comercializacao()
    return df

@pytest.fixture(scope="session")
def importacao_data():
    df = scrap_importacao()
    return df

@pytest.fixture(scope="session")
def exportacao_data():
    df = scrap_exportacao()
    return df

# ------------- Testes com dados da aba produção -------------
def test_producao(producao_data):
    
    aba = 'producao'
    
    required_columns = {
        "Produto": ptypes.is_string_dtype,
        "Quantidade (L.)": ptypes.is_string_dtype,
        "ano": ptypes.is_numeric_dtype
    }
    
    # Valida se dataframe não está vazio
    assert producao_data.shape[0] > 1, f'Tabela da aba {aba} está vazia'
    
    # Valida se colunas necessárias estão presentes e na mesma ordem necessária no dataset
    assert list(producao_data.columns) == list(required_columns.keys()), (
    f"Ordem de colunas na aba {aba} não está correta. "
    f"A ordem resultante é {list(producao_data.columns)} quando deveria ser {list(required_columns.keys())}"
    )
    
    #Itera para cada coluna necessária e valida se o tipo de dado está correto.
    for col_name, format_verification_funct in required_columns.items():
        assert format_verification_funct(producao_data[col_name]), f"Coluna {col_name} dos dados da aba {aba} falhou na função de validar o tipo de dado: {format_verification_funct}"
        

# ------------- Testes com dados da aba processamento -------------
def test_processamento(processamento_data):
    
    aba = 'processamento'
    
    required_columns = {
        "Cultivar": ptypes.is_string_dtype,
        "Quantidade (Kg)": ptypes.is_string_dtype,
        "ano": ptypes.is_numeric_dtype,
        "classificacao_uva": ptypes.is_string_dtype
    }
    
    # Valida se dataframe não está vazio
    assert processamento_data.shape[0] > 1, f'Tabela da aba {aba} está vazia'
    
    # Valida se colunas necessárias estão presentes e na mesma ordem necessária no dataset
    assert list(processamento_data.columns) == list(required_columns.keys()), (
    f"Ordem de colunas na aba {aba} não está correta. "
    f"A ordem resultante é {list(processamento_data.columns)} quando deveria ser {list(required_columns.keys())}"
    )
    
    #Itera para cada coluna necessária e valida se o tipo de dado está correto.
    for col_name, format_verification_funct in required_columns.items():
        assert format_verification_funct(processamento_data[col_name]), f"Coluna {col_name} dos dados da aba {aba} falhou na função de validar o tipo de dado: {format_verification_funct}"
        
        
# ------------- Testes com dados da aba comercialização -------------
def test_comercializacao(comercializacao_data):
    
    aba = 'comercializacao'
    
    required_columns = {
        "Produto": ptypes.is_string_dtype,
        "Quantidade (L.)": ptypes.is_string_dtype,
        "ano": ptypes.is_numeric_dtype
    }
    
    # Valida se dataframe não está vazio
    assert comercializacao_data.shape[0] > 1, f'Tabela da aba {aba} está vazia'
    
    # Valida se colunas necessárias estão presentes e na mesma ordem necessária no dataset
    assert list(comercializacao_data.columns) == list(required_columns.keys()), (
    f"Ordem de colunas na aba {aba} não está correta. "
    f"A ordem resultante é {list(comercializacao_data.columns)} quando deveria ser {list(required_columns.keys())}"
    )
    
    #Itera para cada coluna necessária e valida se o tipo de dado está correto.
    for col_name, format_verification_funct in required_columns.items():
        assert format_verification_funct(comercializacao_data[col_name]), f"Coluna {col_name} dos dados da aba {aba} falhou na função de validar o tipo de dado: {format_verification_funct}"
        
        
# ------------- Testes com dados da aba importação -------------
def test_importacao(importacao_data):
    
    aba = 'importacao'
    
    required_columns = {
        "Países": ptypes.is_string_dtype,
        "Quantidade (Kg)": ptypes.is_string_dtype,
        "Valor (US$)": ptypes.is_string_dtype,
        "ano": ptypes.is_numeric_dtype,
        "classificacao_derivado": ptypes.is_string_dtype
    }
    
    # Valida se dataframe não está vazio
    assert importacao_data.shape[0] > 1, f'Tabela da aba {aba} está vazia'
    
    # Valida se colunas necessárias estão presentes e na mesma ordem necessária no dataset
    assert list(importacao_data.columns) == list(required_columns.keys()), (
    f"Ordem de colunas na aba {aba} não está correta. "
    f"A ordem resultante é {list(importacao_data.columns)} quando deveria ser {list(required_columns.keys())}"
    )
    
    #Itera para cada coluna necessária e valida se o tipo de dado está correto.
    for col_name, format_verification_funct in required_columns.items():
        assert format_verification_funct(importacao_data[col_name]), f"Coluna {col_name} dos dados da aba {aba} falhou na função de validar o tipo de dado: {format_verification_funct}"
        
        
# ------------- Testes com dados da aba exportacao -------------
def test_exportacao(exportacao_data):
    
    aba = 'exportacao'
    
    required_columns = {
        "Países": ptypes.is_string_dtype,
        "Quantidade (Kg)": ptypes.is_string_dtype,
        "Valor (US$)": ptypes.is_string_dtype,
        "ano": ptypes.is_numeric_dtype,
        "classificacao_derivado": ptypes.is_string_dtype
    }
    
    # Valida se dataframe não está vazio
    assert exportacao_data.shape[0] > 1, f'Tabela da aba {aba} está vazia'
    
    # Valida se colunas necessárias estão presentes e na mesma ordem necessária no dataset
    assert list(exportacao_data.columns) == list(required_columns.keys()), (
    f"Ordem de colunas na aba {aba} não está correta. "
    f"A ordem resultante é {list(exportacao_data.columns)} quando deveria ser {list(required_columns.keys())}"
    )
    
    #Itera para cada coluna necessária e valida se o tipo de dado está correto.
    for col_name, format_verification_funct in required_columns.items():
        assert format_verification_funct(exportacao_data[col_name]), f"Coluna {col_name} dos dados da aba {aba} falhou na função de validar o tipo de dado: {format_verification_funct}"