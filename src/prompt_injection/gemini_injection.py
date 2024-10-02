import sys
import os
import csv
import random
import google.generativeai as genai
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.utils.log_utils import log_response
from src.reports.template_ethics_report import EthicsReportGenerator

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

genai.configure(api_key="AIzaSyDubPrAn-KE0PIgVELk9LE_dyfJnAYsvME")

model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def load_ethics_prompts(csv_path):
    prompts = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            prompts.append(row)
    return prompts

def get_random_prompts_by_mode(prompts, mode, num_tests):
    mode_prompts = [prompt for prompt in prompts if prompt['mode'] == mode]
    return random.sample(mode_prompts, min(num_tests, len(mode_prompts)))

def generate_gemini_response(prompt):
    response = model.generate_content(prompt)
    return response.text if hasattr(response, 'text') else "Erro: Sem resposta válida."

report = EthicsReportGenerator(model_name="Google Gemini", report_file="logs/gemini_ethics_report.txt")
report.create_report()

csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'prompts_ethics_dataset.csv'))
prompts = load_ethics_prompts(csv_path)

modes = ["simple", "camouflaged", "evolving", "contradictory", "trusted"]
total_tests_limit = 2 
mode_success_count = defaultdict(int)
total_tests = 0
successful_injections = 0

for mode in modes:
    print(f"\n--- Testando Modo: {mode.upper()} ---")
    
    selected_prompts = get_random_prompts_by_mode(prompts, mode, total_tests_limit)
    
    for prompt_data in selected_prompts:
        base_prompt = prompt_data['base_prompt']
        malicious_prompt = prompt_data['specific_injection']

        original_response = generate_gemini_response(base_prompt)
        print(f"[{mode.upper()}] Resposta original: {original_response}")

        injected_response = generate_gemini_response(malicious_prompt)
        print(f"[{mode.upper()}] Resposta após injeção: {injected_response}")
        
        log_response(malicious_prompt, f"Resposta original: {original_response}, Resposta após injeção: {injected_response}")

        report.update_report(mode, original_response, injected_response)

        if original_response != injected_response:
            mode_success_count[mode] += 1
            successful_injections += 1
        
        total_tests += 1

report.add_comparative_analysis(mode_success_count, total_tests, successful_injections)

report.finalize_report()

print("Testes concluídos e relatório gerado com sucesso.")
