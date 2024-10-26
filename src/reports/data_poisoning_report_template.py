import os
from datetime import datetime
from typing import List, Dict

LOG_DIR = "logs"

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def generate_report(model_name: str, poison_type: str, responses: List[Dict[str, str]], results_summary: Dict[str, int]) -> str:
    """
    Gera um relatório detalhado dos resultados do Data Poisoning.
    
    Args:
        model_name (str): Nome do modelo que foi testado.
        poison_type (str): Tipo de envenenamento realizado (e.g., 'bias', 'misinformation').
        responses (List[Dict[str, str]]): Lista de dicionários contendo as respostas de cada entrada.
        results_summary (Dict[str, int]): Resumo com contagem de sucessos e falhas.
    
    Returns:
        str: Caminho para o arquivo de relatório gerado.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    report_filename = f"{model_name}_{poison_type}_test_report_{timestamp}.txt"
    report_path = os.path.join(LOG_DIR, report_filename)
    
    total_tests = results_summary['success'] + results_summary['failure']
    success_rate = (results_summary['success'] / total_tests) * 100 if total_tests > 0 else 0

    report_content = [
        "----------------------------------------",
        "Relatório de Teste de Data Poisoning",
        "----------------------------------------",
        f"Modelo: {model_name}",
        f"Tipo de Envenenamento: {poison_type}",
        f"Data do Teste: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Total de Registros Testados: {total_tests}",
        "----------------------------------------",
        "Resultados Individuais",
        "----------------------------------------"
    ]
    
    for response in responses:
        result = "Sucesso" if response['model_response'].strip().lower() == response['expected_response'].strip().lower() else "Falha"
        report_content.extend([
            f"\nID: {response['record_id']}",
            f"Texto de Entrada: \"{response['input_text']}\"",
            f"Resposta do Modelo: \"{response['model_response']}\"",
            f"Resposta Esperada: \"{response['expected_response']}\"",
            f"Resultado: {result}"
        ])
    
    report_content.extend([
        "\n----------------------------------------",
        "Resumo Final",
        "----------------------------------------",
        f"Total de Sucessos: {results_summary['success']}",
        f"Total de Falhas: {results_summary['failure']}",
        f"Taxa de Sucesso: {success_rate:.2f}%",
        "\nObservação:",
        "Nenhuma observação adicional."
        "\n----------------------------------------",
        "Fim do Relatório",
        "----------------------------------------"
    ])
    
    with open(report_path, 'w', encoding="utf-8") as file:
        file.write("\n".join(report_content))
    
    print(f"Relatório gerado: {report_path}")
    return report_path
