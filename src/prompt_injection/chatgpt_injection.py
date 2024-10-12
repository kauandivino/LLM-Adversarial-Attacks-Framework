import openai
import os
import csv
import random
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from openai import OpenAI
from src.utils.log_utils import log_response
from src.reports.template_ethics_report import EthicsReportGenerator

client = OpenAI(api_key="OPENAI_KEY")

def load_prompts(csv_path):
    prompts = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            prompts.append(row)
    return prompts

def generate_chatgpt_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini", 
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=5000
    )
    return response.choices[0].message.content 

def get_random_prompts(prompts, num_tests):
    return random.sample(prompts, min(num_tests, len(prompts)))

report = EthicsReportGenerator(model_name="ChatGPT GPT-4", report_file="logs/chatgpt_ethics_report.txt")
report.create_report()

csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'prompts_ethics_dataset.csv'))
prompts = load_prompts(csv_path)

num_tests_per_mode = 10 

for prompt_data in get_random_prompts(prompts, num_tests_per_mode):
    base_prompt = prompt_data['base_prompt']
    injected_prompt = prompt_data['specific_injection']

    original_response = generate_chatgpt_response(base_prompt)
    print(f"Resposta original: {original_response}")

    injected_response = generate_chatgpt_response(injected_prompt)
    print(f"Resposta após injeção: {injected_response}")

    log_response(injected_prompt, f"Resposta original: {original_response}, Resposta após injeção: {injected_response}")

    report.update_report("Prompt Injection", original_response, injected_response)

report.finalize_report()

print("Testes concluídos e relatório gerado com sucesso.")
