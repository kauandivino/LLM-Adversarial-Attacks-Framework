import logging
import os

if not os.path.exists('logs'):
    os.makedirs('logs')
    
logging.basicConfig(
    filename='logs/prompt_injection_log.txt',  
    level=logging.INFO,  
    format='%(asctime)s - %(levelname)s - %(message)s' 
)

def log_response(prompt: str, response: str):
    """
    Função que registra o prompt injetado e a resposta gerada pelo modelo no arquivo de log.
    
    :param prompt: O prompt injetado no modelo.
    :param response: A resposta gerada pelo modelo após o prompt.
    """
    logging.info(f"Prompt Injetado: {prompt}\nResposta: {response}\n")
