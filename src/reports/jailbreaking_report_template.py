import os
import logging
from datetime import datetime

class JailbreakingReport:
    """
    Classe responsável por gerar e gerenciar o relatório dos testes de Jailbreaking.
    O relatório é gerado dinamicamente e contém todas as informações necessárias para avaliar o sucesso ou falha dos ataques.
    """
    
    def __init__(self, model_name, report_file="jailbreaking_report.txt"):
        """
        Inicializa o relatório.
        
        :param model_name: Nome do modelo de linguagem testado (ex: GPT-4).
        :param report_file: Caminho do arquivo de relatório onde os resultados serão armazenados.
        """
        self.model_name = model_name
        self.report_file = report_file
        self.start_time = datetime.now()
        self.results = []  # Armazena os resultados de cada teste

    def create_report(self):
        """
        Cria o arquivo de relatório e escreve o cabeçalho com informações iniciais.
        """
        try:
            with open(self.report_file, 'w', encoding='utf-8') as f:
                f.write(f"--- Relatório de Testes de Jailbreaking ---\n")
                f.write(f"Modelo de Linguagem: {self.model_name}\n")
                f.write(f"Data de Início: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"{'-'*50}\n\n")
            logging.info("Arquivo de relatório criado com sucesso.")
        except Exception as e:
            logging.error(f"Erro ao criar o arquivo de relatório: {e}")

    def update_report(self, subject, original_response, injected_response, progression_stage, aggressiveness_level, deviation_detected):
        """
        Atualiza o relatório com os detalhes de cada teste.
        
        :param subject: O assunto sob teste (ex: Privacidade de Dados).
        :param original_response: Resposta original do modelo sem o ataque.
        :param injected_response: Resposta após a injeção do ataque.
        :param progression_stage: O estágio atual da progressão do ataque.
        :param aggressiveness_level: Nível de agressividade do ataque.
        :param deviation_detected: Flag indicando se houve desvio na resposta após o ataque.
        """
        entry = {
            'subject': subject,
            'progression_stage': progression_stage,
            'aggressiveness_level': aggressiveness_level,
            'original_response': original_response,
            'injected_response': injected_response,
            'deviation_detected': deviation_detected
        }
        self.results.append(entry)
        
        try:
            with open(self.report_file, 'a', encoding='utf-8') as f:
                f.write(f"--- Teste para Assunto: {subject} ---\n")
                f.write(f"Estágio de Progressão: {progression_stage}\n")
                f.write(f"Nível de Agressividade: {aggressiveness_level}\n")
                f.write(f"Resposta Original: {original_response}\n")
                f.write(f"Resposta após Injeção: {injected_response}\n")
                f.write(f"Desvio Detectado: {'Sim' if deviation_detected else 'Não'}\n")
                f.write(f"{'-'*50}\n\n")
            logging.info(f"Relatório atualizado com sucesso para o assunto {subject}.")
        except Exception as e:
            logging.error(f"Erro ao atualizar o relatório: {e}")
    
    def finalize_report(self):
        """
        Finaliza o relatório com um resumo e dados estatísticos sobre os testes realizados.
        """
        end_time = datetime.now()
        duration = end_time - self.start_time
        total_tests = len(self.results)
        successful_attacks = sum(1 for r in self.results if r['deviation_detected'])
        success_rate = (successful_attacks / total_tests) * 100 if total_tests > 0 else 0
        
        try:
            with open(self.report_file, 'a', encoding='utf-8') as f:
                f.write(f"\n--- Resumo Final ---\n")
                f.write(f"Data de Término: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Duração Total dos Testes: {duration}\n")
                f.write(f"Total de Testes Realizados: {total_tests}\n")
                f.write(f"Total de Ataques Bem-Sucedidos: {successful_attacks}\n")
                f.write(f"Taxa de Sucesso dos Ataques: {success_rate:.2f}%\n")
                f.write(f"{'='*50}\n")
            logging.info("Relatório finalizado com sucesso.")
        except Exception as e:
            logging.error(f"Erro ao finalizar o relatório: {e}")

    def generate_summary_table(self):
        """
        Gera uma tabela resumo das principais informações dos testes realizados para facilitar a visualização dos resultados.
        """
        try:
            with open(self.report_file, 'a', encoding='utf-8') as f:
                f.write(f"\n--- Tabela Resumo dos Testes ---\n")
                f.write(f"{'Subject':<20}{'Stage':<10}{'Agressiveness':<15}{'Deviation':<10}\n")
                f.write(f"{'-'*50}\n")
                for result in self.results:
                    subject = result['subject']
                    stage = result['progression_stage']
                    aggressiveness = result['aggressiveness_level']
                    deviation = 'Sim' if result['deviation_detected'] else 'Não'
                    f.write(f"{subject:<20}{stage:<10}{aggressiveness:<15}{deviation:<10}\n")
                f.write(f"{'='*50}\n")
            logging.info("Tabela resumo gerada com sucesso.")
        except Exception as e:
            logging.error(f"Erro ao gerar a tabela resumo: {e}")
