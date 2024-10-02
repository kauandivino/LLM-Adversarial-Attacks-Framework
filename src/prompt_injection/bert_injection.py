import sys
import os
import csv
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from transformers import BertTokenizer, BertForSequenceClassification
from torch.nn.functional import softmax
import torch
from prompt_injection import PromptInjector
from src.utils.log_utils import log_response
from src.reports.template_report import ReportGenerator

model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def classify_text(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True).to(device)
    outputs = model(**inputs)
    probs = softmax(outputs.logits, dim=-1)
    return torch.argmax(probs, dim=1).item(), probs

def load_prompts(csv_path):
    prompts = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            prompts.append(row)
    return prompts

def get_random_prompts_by_mode(prompts, mode, num_tests):
    mode_prompts = [prompt for prompt in prompts if prompt['mode'] == mode]
    return random.sample(mode_prompts, min(num_tests, len(mode_prompts)))

report = ReportGenerator(model_name="BERT Multilingual (nlptown/bert-base-multilingual-uncased-sentiment)", report_file="logs/bert_report.txt")
report.create_report()

injector = PromptInjector()

csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'prompts_injection_dataset.csv'))
prompts = load_prompts(csv_path)

modes = ["simple", "camouflaged", "evolving", "contradictory", "trusted"]
num_tests_per_mode = 3

for mode in modes:
    print(f"\n--- Testando Modo: {mode.upper()} ---")
    selected_prompts = get_random_prompts_by_mode(prompts, mode, num_tests_per_mode)
    
    for prompt_data in selected_prompts:
        base_prompt = prompt_data['base_prompt']
        malicious_prompt = prompt_data['specific_injection']
        original_class, original_probs = classify_text(base_prompt)
        print(f"[{mode.upper()}] Classe original: {original_class}, Probabilidades: {original_probs}")

        injected_class, injected_probs = classify_text(malicious_prompt)
        print(f"[{mode.upper()}] Classe após injeção: {injected_class}, Probabilidades: {injected_probs}")

        log_response(malicious_prompt, f"Classe original: {original_class}, Classe após injeção: {injected_class}")
        report.update_report(mode, original_class, injected_class, original_probs, injected_probs)

report.finalize_report()

print("Testes concluídos e relatório gerado com sucesso.")