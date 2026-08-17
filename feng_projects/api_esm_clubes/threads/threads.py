import threading
import importlib

# Lista explícita de pipelines a serem executadas
pipeline_names = [
    "orders",
    "users",
]

def run_pipeline(name, results):
    """
    Executa a pipeline especificada sem exibir logs internos.
    Registra apenas True/False em `results`.
    """
    try:
        module = importlib.import_module(f"pipelines.{name}.main")
        module.main()
        results[name] = True
    except Exception:
        results[name] = False


def execute_all():
    """
    Dispara todas as pipelines em threads separadas e retorna um dicionário
    com o status de cada uma (True = sucesso, False = falha).
    """
    results = {}
    threads = []

    for name in pipeline_names:
        thread = threading.Thread(
            target=run_pipeline,
            args=(name, results),
            name=name
        )
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return results