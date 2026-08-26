import os
import random
import time
from datetime import datetime
from google import genai
from google.genai import types

def generate_daily_study():
    print("Iniciando processo de geracao de conteudo...")
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Chave GEMINI_API_KEY nao configurada.")

    print("Conectando a API do Gemini...")
    client = genai.Client(api_key=api_key)

    topics = [
        "Estrutura de Dados em C: Alocacao Dinamica (malloc, free) e Ponteiros",
        "Estrutura de Dados em C: Listas Simplesmente Encadeadas",
        "Estrutura de Dados em C: Pilhas (Stacks) e Filas (Queues)",
        "Estrutura de Dados em C: Arvores Binarias de Busca (BST)",
        "Estrutura de Dados em C: Algoritmos de Ordenacao (Quicksort e Mergesort)",
        "Estatistica Descritiva: Media, Mediana, Desvio Padrao e IQR",
        "Probabilidade: Distribuicao Normal e Calculo de Z-Score",
        "Inferencia Estatistica: Teorema do Limite Central e Intervalos de Confianca",
        "Testes de Hipotese: Teste t de Student e p-valor",
        "Regressao Linear Simples: Coeficiente de Determinacao (R2) e Residuos"
    ]
    
    selected_topic = random.choice(topics)
    print(f"Topico selecionado: {selected_topic}")

    prompt = f"""
    Voce e um professor universitario de Ciencia da Computacao e Estatistica.
    Crie uma licao de estudo concisa e didatica sobre: {selected_topic}.

    Siga esta estrutura Markdown:
    # 📚 Licao do Dia: {selected_topic}
    
    ## 🎯 1. Conceito Central
    Explicacao direta ao ponto (maximo 2 paragrafos).
    
    ## 💻 2. Codigo Exemplo
    - Se C: codigo enxuto, comentado, com liberacao de memoria (free).
    - Se Estatistica: script breve em Python (numpy/scipy).
    
    ## ⚠️ 3. Pegadinha Comum
    O principal erro em provas sobre isso.
    
    ## 🧠 4. Mini-Desafio
    Uma questao rapida de fixacao.
    """

    # Modelos em ordem de preferencia
    models_to_try = ["gemini-2.5-flash", "gemini-2.5-pro"]
    response = None

    for model_name in models_to_try:
        try:
            print(f"Tentando gerar com o modelo: {model_name}...")
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=1500,
                    temperature=0.7
                )
            )
            if response and response.text:
                print(f"Sucesso com o modelo: {model_name}!")
                break
        except Exception as e:
            print(f"Falha com {model_name}: {e}. Tentando proximo modelo...")
            time.sleep(2)

    if not response or not response.text:
        raise RuntimeError("Nao foi possivel gerar conteudo com nenhum dos modelos disponiveis.")

    print("Salvando arquivo...")
    os.makedirs("generated", exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    clean_topic_name = selected_topic.split(':')[0].replace(' ', '_').lower()
    filename = f"generated/{today}_{clean_topic_name}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(response.text)

    print(f"Licao salva com sucesso em: {filename}")

if __name__ == "__main__":
    generate_daily_study()
