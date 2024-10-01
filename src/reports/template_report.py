from datetime import datetime

class ReportGenerator:
    """
    Classe responsável por gerar e atualizar o relatório de testes de modelos.
    Gera relatórios para diferentes modelos, com flexibilidade para adicionar análise e otimizações.
    """

    def __init__(self, model_name, report_file="logs/test_report.txt"):
        """
        Inicializa o gerador de relatórios com o nome do modelo e o arquivo de relatório.
        :param model_name: Nome do modelo testado (e.g., "BERT", "GPT-4").
        :param report_file: Nome do arquivo de relatório (padrão: logs/test_report.txt).
        """
        self.model_name = model_name
        self.report_file = report_file

    def create_report(self):
        """
        Gera o cabeçalho inicial do relatório se ele ainda não existir.
        Inclui as informações do modelo, tarefa e modos de injeção de prompt.
        """
        with open(self.report_file, 'w') as file:
            file.write(f"Relatório de Teste de Ataques Adversariais\n")
            file.write(f"Modelo Testado: {self.model_name}\n")
            file.write(f"Data de Início: {datetime.now()}\n")
            file.write("\nConfiguração do Teste:\n")
            file.write(f"Modelo: {self.model_name}\n")
            file.write("Tarefa: Análise de Sentimentos ou similar\n")
            file.write("Modos de Injeção de Prompt: Simple, Camouflaged, Evolving, Contradictory, Trusted\n")
            file.write("-" * 80 + "\n")
            file.write("\nResultados:\n")
            file.write("Modo de Injeção | Classe Original | Classe Após Injeção | Probabilidades Originais | Probabilidades Após Injeção\n")
            file.write("-" * 100 + "\n")

    def update_report(self, mode, original_class, injected_class, original_probs, injected_probs):
        """
        Atualiza o relatório com os resultados de cada execução de teste.
        :param mode: Modo de injeção utilizado (e.g., "Simple", "Camouflaged").
        :param original_class: Classe original antes da injeção do prompt.
        :param injected_class: Classe após a injeção do prompt.
        :param original_probs: Probabilidades originais (antes da injeção).
        :param injected_probs: Probabilidades após a injeção do prompt.
        """
        with open(self.report_file, 'a') as file:
            file.write(f"{mode:<15} | {original_class:<15} | {injected_class:<20} | {original_probs} | {injected_probs}\n")

    def add_analysis(self, analysis):
        """
        Adiciona uma seção de análise no relatório.
        :param analysis: Texto com a análise dos resultados.
        """
        with open(self.report_file, 'a') as file:
            file.write("\nAnálise dos Resultados:\n")
            file.write(f"{analysis}\n")
            file.write("-" * 100 + "\n")

    def add_optimization(self, optimization):
        """
        Adiciona uma seção de otimizações no relatório.
        :param optimization: Texto com a descrição da otimização realizada.
        """
        with open(self.report_file, 'a') as file:
            file.write("\nOtimizações Realizadas:\n")
            file.write(f"{optimization}\n")
            file.write("-" * 100 + "\n")

    def finalize_report(self):
        """
        Finaliza o relatório com a data de término.
        """
        with open(self.report_file, 'a') as file:
            file.write("\nRelatório Finalizado em: {}\n".format(datetime.now()))
            file.write("=" * 100 + "\n")
