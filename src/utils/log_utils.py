import logging
import os

if not os.path.exists('logs'):
    os.makedirs('logs')

def setup_logging(model_name, attack_type="prompt_injection"):
    """
    Configura o logger para criar arquivos de log específicos para cada modelo e tipo de ataque.
    :param model_name: Nome do modelo (e.g., 'BERT', 'GPT-4') para diferenciar os arquivos de log.
    :param attack_type: Tipo de ataque, e.g., 'prompt_injection', 'jailbreaking' para diferenciar os ataques.
    """
    log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, f'{model_name.lower()}_{attack_type}_log.txt')

    logging.basicConfig(
        filename=log_file,
        filemode='a',
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

def log_response(prompt, response, stage=None):
    """
    Loga o prompt injetado e a resposta do modelo, além de informações adicionais como a fase do ataque.
    :param prompt: O prompt que foi injetado.
    :param response: A resposta do modelo após o prompt ser injetado.
    :param stage: Fase ou progressão do ataque (se aplicável).
    """
    if stage:
        logging.info(f"Fase {stage}:")
    logging.info(f"Prompt Injetado: {prompt}")
    logging.info(f"Resposta: {response}")
