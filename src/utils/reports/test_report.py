# src/reports/test_report.py

from datetime import datetime

class ReportGenerator:
    """
    Classe responsável por gerar e atualizar o relatório de testes com base nos resultados.
    """
    def __init__(self, report_file="logs/bert_test_report.txt"):
        self.report_file = report_file

    def create_report(self):
        """
        Gera o cabeçalho inicial do relatório, se ele ainda não existir.
        """
        with open(self.report_file, 'w') as file:
            file.write("Relatório de Teste de Ataques Adversariais em BERT\n")
            file.write(f"Data de Início: {datetime.now()}\n")
            file.write("\nConfiguração do Teste:\n")
            file.write("Modelo: BERT Multilingual (nlptown/bert-base-multilingual-uncased-sentiment)\n")
            file.write("Tarefa: Análise de Sentimentos\n")
            file.write("Modos de Injeção de Prompt: Simple, Camouflaged, Evolving, Contradictory, Trusted\n")
            file.write("\nResultados:\n")
            file.write("Modo de Injeção | Classe Original | Classe Após Injeção | Probabilidades Originais | Probabilidades Após Injeção\n")
            file.write("-" * 90 + "\n")

    def update_report(self, mode, original_class, injected_class, original_probs, injected_probs):
        """
        Atualiza o relatório com os resultados de cada execução de teste.
        """
        with open(self.report_file, 'a') as file:
            file.write(f"{mode:<15} | {original_class:<15} | {injected_class:<20} | {original_probs} | {injected_probs}\n")

    def add_analysis(self, analysis):
        """
        Adiciona uma análise dos resultados ao relatório.
        """
        with open(self.report_file, 'a') as file:
            file.write("\nAnálise dos Resultados:\n")
            file.write(f"{analysis}\n")
            file.write("-" * 90 + "\n")

    def add_optimization(self, optimization):
        """
        Adiciona a descrição de uma otimização feita ao relatório.
        """
        with open(self.report_file, 'a') as file:
            file.write("\nOtimizações Realizadas:\n")
            file.write(f"{optimization}\n")
            file.write("-" * 90 + "\n")
