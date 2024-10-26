import pandas as pd
import logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_poisoning_data(filepath: str) -> pd.DataFrame:
    """
    Carrega o dataset de Data Poisoning a partir de um arquivo CSV.
    
    Args:
        filepath (str): Caminho para o arquivo CSV contendo o dataset.
        
    Returns:
        pd.DataFrame: DataFrame com o conteúdo do dataset.
    """
    try:
        data = pd.read_csv(filepath)
        logging.info(f"Dataset carregado com sucesso. {len(data)} registros encontrados.")
        return data
    except Exception as e:
        logging.error(f"Erro ao carregar o dataset: {e}")
        raise

def filter_poisoning_data(data: pd.DataFrame, poison_type: str = None) -> pd.DataFrame:
    """
    Filtra o dataset com base no tipo de envenenamento, se especificado.
    
    Args:
        data (pd.DataFrame): DataFrame contendo o dataset completo.
        poison_type (str, optional): Tipo específico de envenenamento para filtrar (e.g., 'bias', 'misinformation').
        
    Returns:
        pd.DataFrame: DataFrame filtrado com base no tipo de envenenamento.
    """
    if poison_type:
        filtered_data = data[data['poison_type'] == poison_type]
        logging.info(f"Filtrado {len(filtered_data)} registros do tipo '{poison_type}'.")
        return filtered_data
    logging.info("Nenhum filtro aplicado. Retornando o dataset completo.")
    return data

def log_model_response(record_id: str, input_text: str, model_response: str, expected_response: str) -> None:
    """
    Registra a resposta do modelo e a compara com a resposta esperada.
    
    Args:
        record_id (str): Identificador único do registro no dataset.
        input_text (str): Texto de entrada utilizado para envenenamento.
        model_response (str): Resposta gerada pelo modelo.
        expected_response (str): Resposta esperada caso o envenenamento seja bem-sucedido.
    """
    logging.info(f"Registro ID: {record_id}")
    logging.info(f"Texto de entrada: {input_text}")
    logging.info(f"Resposta do modelo: {model_response}")
    logging.info(f"Resposta esperada: {expected_response}")
    if model_response.strip().lower() == expected_response.strip().lower():
        logging.info("Resultado: O envenenamento foi bem-sucedido.")
    else:
        logging.info("Resultado: O envenenamento falhou ou foi parcialmente bem-sucedido.")

def evaluate_poisoning_success(responses: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Avalia o sucesso do Data Poisoning comparando as respostas reais com as esperadas.
    
    Args:
        responses (List[Dict[str, Any]]): Lista de dicionários contendo ID, resposta do modelo e resposta esperada.
        
    Returns:
        Dict[str, int]: Dicionário com contagem de sucessos e falhas de envenenamento.
    """
    success_count = 0
    failure_count = 0
    
    for response in responses:
        if response['model_response'].strip().lower() == response['expected_response'].strip().lower():
            success_count += 1
        else:
            failure_count += 1
    
    logging.info(f"Total de sucessos: {success_count}")
    logging.info(f"Total de falhas: {failure_count}")
    
    return {
        "success": success_count,
        "failure": failure_count
    }

def summarize_poisoning_results(results: Dict[str, int]) -> None:
    """
    Gera um resumo dos resultados do Data Poisoning.
    
    Args:
        results (Dict[str, int]): Dicionário com contagem de sucessos e falhas de envenenamento.
    """
    total_tests = results['success'] + results['failure']
    success_rate = (results['success'] / total_tests) * 100 if total_tests > 0 else 0
    failure_rate = (results['failure'] / total_tests) * 100 if total_tests > 0 else 0
    
    logging.info("Resumo dos Resultados de Data Poisoning:")
    logging.info(f"Total de testes: {total_tests}")
    logging.info(f"Sucessos: {results['success']} ({success_rate:.2f}%)")
    logging.info(f"Falhas: {results['failure']} ({failure_rate:.2f}%)")
