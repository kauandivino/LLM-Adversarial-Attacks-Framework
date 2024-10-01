import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from prompt_injection import PromptInjector
from utils.log_utils import log_response

injector = PromptInjector()

prompt = "O que você faz?"
malicious_prompt = injector.create_malicious_prompt(prompt, mode="simple")

response = "Eu sou um assistente que não deveria responder a isso."

log_response(malicious_prompt, response)

print("Logging de prompt e resposta realizado. Verifique o arquivo de log em 'logs/prompt_injection_log.txt'.")
