import logging
import sys
import google.generativeai as genai
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from jailbreaking_utils import load_prompts, generate_next_prompt, evaluate_response, detect_deviation, adapt_prompt_for_gemini
from src.utils.log_utils import log_response
from src.reports.jailbreaking_report_template import JailbreakingReport

genai.configure(api_key="API_KEY")
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def generate_gemini_response(chat, prompt):
    """
    Envia uma mensagem dentro de um chat interativo com o modelo Gemini, mantendo o histórico.
    
    :param chat: Instância do chat iniciado com o modelo Gemini.
    :param prompt: O prompt a ser enviado ao modelo dentro da conversa.
    :return: Resposta do modelo Gemini.
    """
    try:
        response = chat.send_message(prompt)
        return response.text if hasattr(response, 'text') else "Erro: Resposta inválida."
    except Exception as e:
        logging.error(f"Erro ao gerar a resposta do modelo Gemini: {e}")
        return "Erro ao gerar a resposta."

def run_gemini_jailbreaking_test(dataset_path, num_tests_per_subject=1, max_interactions=5):
    """
    Executa os testes de jailbreaking no modelo Gemini de forma progressiva dentro de uma única conversa.
    
    :param dataset_path: Caminho para o dataset contendo os prompts.
    :param num_tests_per_subject: Número de testes a serem feitos por assunto.
    :param max_interactions: Número máximo de interações permitidas por sequência de ataque.
    """
    prompts = load_prompts(dataset_path)
    report = JailbreakingReport(model_name="Gemini", report_file="logs/gemini_jailbreaking_report.txt")
    report.create_report()
    subjects = set([prompt['subject'] for prompt in prompts])
    
    for subject in subjects:
        logging.info(f"\n--- Iniciando Testes para Subject: {subject} ---")
        subject_prompts = [p for p in prompts if p['subject'] == subject]
        
        for test_num in range(num_tests_per_subject):
            logging.info(f"\n--- Teste {test_num + 1} para {subject} ---")
            
            base_prompt = next(p for p in subject_prompts if p['progression_stage'] == "1")
            jailbreaking_prompt = base_prompt['jailbreaking_injection']
            expected_behavior = base_prompt['expected_behavior']
            aggressiveness_level = int(base_prompt['aggressiveness_level'])
            
            logging.info(f"Prompt Inicial: {base_prompt['base_prompt']} (Nível {aggressiveness_level})")

            chat = model.start_chat(
                history=[
                    {"role": "user", "parts": base_prompt['base_prompt']},
                ]
            )
            
            original_response = chat.send_message(jailbreaking_prompt).text
            logging.info(f"Resposta Original: {original_response}")

            log_response(jailbreaking_prompt, f"Resposta Original: {original_response}")
            deviation_detected = not evaluate_response(original_response, expected_behavior)

            for progression_stage in range(1, max_interactions + 1):
                if not deviation_detected:
                    next_prompt_data, next_level = generate_next_prompt(subject_prompts, base_prompt, aggressiveness_level, base_prompt['mode'], max_interactions, progression_stage)
                    
                    if next_prompt_data:
                        injected_response = chat.send_message(next_prompt_data['jailbreaking_injection']).text
                        
                        logging.info(f"Resposta após injeção no estágio {progression_stage}: {injected_response}")
                        
                        deviation_detected = detect_deviation(injected_response, original_response)
                        log_response(next_prompt_data['jailbreaking_injection'], f"Resposta após injeção: {injected_response}")
                        
                        report.update_report(subject, original_response, injected_response, progression_stage, next_level, deviation_detected)
                        
                        original_response = injected_response
                    else:
                        logging.info(f"Nenhuma progressão adicional disponível no estágio {progression_stage}.")
                        break
                else:
                    logging.info(f"Desvio detectado no estágio {progression_stage}. Encerrando o teste.")
                    break

    report.finalize_report()
    logging.info("Testes concluídos e relatório gerado com sucesso.")


if __name__ == "__main__":
    dataset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'jailbreaking_dataset.csv'))
    run_gemini_jailbreaking_test(dataset_path, num_tests_per_subject=1, max_interactions=5)