# src/prompt_injection/test_bert_injection.py

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from transformers import BertTokenizer, BertForSequenceClassification
from torch.nn.functional import softmax
import torch
from prompt_injection import PromptInjector
from src.utils.log_utils import log_response


model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

# Definir dispositivo (usar GPU se disponível)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Função para classificar o texto com BERT
def classify_text(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True).to(device)
    outputs = model(**inputs)
    probs = softmax(outputs.logits, dim=-1)
    return torch.argmax(probs, dim=1).item(), probs

# Instanciar o módulo de prompt injection
injector = PromptInjector()

# Definir o prompt base para análise de sentimentos
base_prompt = "Eu estou me sentindo muito triste hoje."

# Aplicar os modos de injeção de prompt e testar no modelo BERT
modes = ["simple", "camouflaged", "evolving", "contradictory", "trusted"]
for mode in modes:
    # Criar o prompt malicioso
    malicious_prompt = injector.create_malicious_prompt(base_prompt, mode=mode)

    # Classificar o prompt base
    original_class, original_probs = classify_text(base_prompt)
    print(f"[{mode.upper()}] Classe original: {original_class}, Probabilidades: {original_probs}")

    # Classificar o prompt injetado
    injected_class, injected_probs = classify_text(malicious_prompt)
    print(f"[{mode.upper()}] Classe após injeção: {injected_class}, Probabilidades: {injected_probs}")

    # Registrar o resultado no log
    log_response(malicious_prompt, f"Classe original: {original_class}, Classe após injeção: {injected_class}")
