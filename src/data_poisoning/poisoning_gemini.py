import google.generativeai as genai
import poisoning_utils as utils
import os
import logging
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import src.reports.data_poisoning_report_template as report_template  

API_KEY = "API_KEY"
MODEL_NAME = "gemini-1.5-flash"

def configure_gemini_api(api_key: str) -> None:
    """
    Configura a API do modelo Gemini.
    
    Args:
        api_key (str): Chave de API para autenticação.
    """
    genai.configure(api_key=api_key)
    print("API Gemini configurada com sucesso.")

def generate_gemini_response(model_name: str, input_text: str, max_tokens: int) -> str:
    """
    Gera a resposta do modelo Gemini para um texto de entrada, aplicando uma limitação de tokens na pós-processamento.
    
    Args:
        model_name (str): Nome do modelo a ser usado.
        input_text (str): Texto que será passado para o modelo.
        max_tokens (int): Número máximo de tokens na resposta.
        
    Returns:
        str: Resposta gerada pelo modelo.
    """
    model = genai.GenerativeModel(model_name=model_name)
    response = model.generate_content(input_text)
    
    if response and response.text:
        words = response.text.split()
        limited_response = " ".join(words[:max_tokens])
        return limited_response
    return ""

def execute_data_poisoning_attack(dataset_path: str, poison_type: str = None, max_records: int = 10, max_tokens: int = 5000) -> None:
    """
    Executa o ataque de Data Poisoning no modelo Gemini usando um dataset específico.
    
    Args:
        dataset_path (str): Caminho para o arquivo CSV contendo o dataset de Data Poisoning.
        poison_type (str, optional): Tipo específico de envenenamento para filtrar (e.g., 'bias', 'misinformation').
        max_records (int, optional): Número máximo de registros a serem processados.
        max_tokens (int, optional): Número máximo de tokens para cada resposta do modelo.
    """
    configure_gemini_api(API_KEY)
    
    data = utils.load_poisoning_data(dataset_path)
    filtered_data = utils.filter_poisoning_data(data, poison_type)
    
    responses = []
    
    for i, (_, row) in enumerate(filtered_data.iterrows()):
        if i >= max_records:
            print(f"Limite de {max_records} registros atingido. Parando a execução.")
            break
        
        record_id = row['id']
        input_text = row['input_text']
        expected_response = row['model_response_expected']
        
        model_response = generate_gemini_response(MODEL_NAME, input_text, max_tokens)
        
        utils.log_model_response(record_id, input_text, model_response, expected_response)
        responses.append({
            "record_id": record_id,
            "input_text": input_text,
            "model_response": model_response,
            "expected_response": expected_response
        })
    
    results = utils.evaluate_poisoning_success(responses)
    utils.summarize_poisoning_results(results)
    report_template.generate_report(
        model_name=MODEL_NAME,
        poison_type=poison_type if poison_type else "all",
        responses=responses,
        results_summary=results
    )

if __name__ == "__main__":
    dataset_path = "data/data_poisoning_dataset.csv" 
    execute_data_poisoning_attack(dataset_path, poison_type="misinformation", max_records=10, max_tokens=5000)
