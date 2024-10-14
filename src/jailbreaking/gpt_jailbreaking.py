import openai
import os
import logging
import sys
import csv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from jailbreaking_utils import load_prompts, evaluate_response, generate_next_prompt, detect_deviation
from src.utils.log_utils import log_response
from src.reports.jailbreaking_report_template import JailbreakingReport
from openai import OpenAI

openai.api_key = os.getenv("OPENAI_KEY")
client = openai

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def generate_gpt_response(prompt, client):
    """
    Função que envia um prompt para o modelo GPT da OpenAI e retorna a resposta.
    
    :param prompt: O prompt a ser enviado para o modelo.
    :param client: Cliente da OpenAI para fazer a chamada à API.
    :return: Resposta gerada pelo modelo GPT.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7
        )
        return response.choices[0].message.content 
    except Exception as e:
        logging.error(f"Erro ao gerar resposta do GPT: {e}")
        return "Erro: Resposta inválida."

def run_gpt_jailbreaking_test(dataset_path, num_tests_per_subject=3):
    """
    Função que executa os testes de jailbreaking no modelo GPT de forma progressiva.

    :param dataset_path: Caminho para o dataset contendo os prompts.
    :param num_tests_per_subject: Número de testes a serem realizados por assunto.
    """
    prompts = load_prompts(dataset_path)
    
    report = JailbreakingReport(model_name="gpt-4o-mini", report_file="logs/gpt_jailbreaking_report.txt")
    report.create_report()

    subjects = set([prompt['subject'] for prompt in prompts])
    
    for subject in subjects:
        logging.info(f"\n--- Iniciando Testes para Subject: {subject} ---")
        subject_prompts = [p for p in prompts if p['subject'] == subject]
        
        for test_num in range(num_tests_per_subject):
            logging.info(f"\n--- Teste {test_num + 1} para {subject} ---")
            base_prompt = next(p for p in subject_prompts if p['progression_stage'] == "1")
            initial_prompt = base_prompt['base_prompt']
            jailbreaking_prompt = base_prompt['jailbreaking_injection']
            expected_behavior = base_prompt['expected_behavior']
            aggressiveness_level = base_prompt['aggressiveness_level']

            logging.info(f"Prompt Inicial: {initial_prompt} (Nível {aggressiveness_level})")
            original_response = generate_gpt_response(initial_prompt, client)
            logging.info(f"Resposta Original: {original_response}")

            if not evaluate_response(original_response, expected_behavior):
                logging.warning(f"A resposta inicial do modelo já está fora do comportamento esperado!")
            
            for progression_stage in range(1, 6): 
                next_prompt, next_level = generate_next_prompt(
                    subject_prompts, 
                    base_prompt, 
                    progression_stage, 
                    base_prompt['mode'], 
                    max_interactions=5, 
                    current_interaction=progression_stage
                )

                if next_prompt:
                    injected_prompt = next_prompt['jailbreaking_injection']
                    logging.info(f"Progredindo para o Estágio {progression_stage + 1}: {injected_prompt}")

                    injected_response = generate_gpt_response(injected_prompt, client)
                    logging.info(f"Resposta após injeção no estágio {progression_stage + 1}: {injected_response}")

                    deviation_detected = detect_deviation(injected_response, original_response)
                    logging.info(f"Desvio detectado: {deviation_detected}")

                    log_response(injected_prompt, f"Resposta Original: {original_response}, Resposta após injeção: {injected_response}")
                    
                    report.update_report(
                        subject, 
                        original_response, 
                        injected_response, 
                        progression_stage, 
                        aggressiveness_level, 
                        deviation_detected
                    )

                    original_response = injected_response 
                else:
                    logging.info(f"Nenhuma progressão adicional disponível no estágio {progression_stage}.")
                    break

    report.finalize_report()
    logging.info("Testes concluídos e relatório gerado com sucesso.")

if __name__ == "__main__":
    dataset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'jailbreaking_dataset.csv'))
    run_gpt_jailbreaking_test(dataset_path, num_tests_per_subject=1)
