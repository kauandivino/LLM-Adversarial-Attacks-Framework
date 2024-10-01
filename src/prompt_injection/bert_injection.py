import sys
import os

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

report = ReportGenerator(model_name="BERT Multilingual (nlptown/bert-base-multilingual-uncased-sentiment)", report_file="logs/bert_report.txt")
report.create_report()

injector = PromptInjector()

base_prompt = "Eu estou me sentindo muito triste hoje."

modes = ["simple", "camouflaged", "evolving", "contradictory", "trusted"]

for mode in modes:
    malicious_prompt = injector.create_malicious_prompt(base_prompt, mode=mode)
    original_class, original_probs = classify_text(base_prompt)
    print(f"[{mode.upper()}] Classe original: {original_class}, Probabilidades: {original_probs}")

    injected_class, injected_probs = classify_text(malicious_prompt)
    print(f"[{mode.upper()}] Classe após injeção: {injected_class}, Probabilidades: {injected_probs}")

    log_response(malicious_prompt, f"Classe original: {original_class}, Classe após injeção: {injected_class}")

    report.update_report(mode, original_class, injected_class, original_probs, injected_probs)

report.finalize_report()
