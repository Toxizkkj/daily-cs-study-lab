import os
import random
import time
from datetime import datetime
from google import genai
from google.genai import types

def generate_daily_study():
    print("Iniciando geracao de conteudo alinhado a ementa federal de BSI...")
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Chave GEMINI_API_KEY nao configurada.")

    client = genai.Client(api_key=api_key)

    # Topicos baseados na ementa padrao do 3º periodo de BSI em Federais
    topics = [
        # --- ESTRUTURA DE DADOS EM C (BSI - 3º PERÍODO) ---
        "Estrutura de Dados em C: Aritmetica de Ponteiros e Passagem por Referencia (* e &)",
        "Estrutura de Dados em C: Alocacao Dinamica de Vetores e Matrizes com malloc, calloc, realloc e free",
        "Estrutura de Dados em C: Criacao e Modularizacao de TADs (Tipos Abstratos de Dados em .h e .c)",
        "Estrutura de Dados em C: Listas Encadeadas Simples (Insercao no Inicio, Fim, Busca e Remocao)",
        "Estrutura de Dados em C: Listas Duplamente Encadeadas e Listas Circulares",
        "Estrutura de Dados em C: Pilhas (Stacks) com implementacao encadeada e aplicacao pratica (avaliar expressoes)",
        "Estrutura de Dados em C: Filas (Queues) com implementacao circular estatica e encadeada",
        "Estrutura de Dados em C: Arvores Binarias de Busca (BST) - Insercao, Busca e Percursos (Pre, Em e Pos-ordem)",
        "Estrutura de Dados em C: Metodos de Ordenacao Elementares vs Eficientes (Bubble, Insertion, QuickSort)",
        "Estrutura de Dados em C: Analise de Complexidade Assintotica (Notacao Big-O, O(1), O(n), O(n log n))",

        # --- FUNDAMENTOS DE ESTATISTICA E PROBABILIDADE (BSI - 3º PERÍODO) ---
        "Estatistica Descritiva: Medidas de Tendencia Central (Media, Mediana, Moda) e Sensibilidade a Outliers",
        "Estatistica Descritiva: Medidas de Dispersao (Variancia Amostral vs Populacional, Desvio Padrao e CV%)",
        "Estatistica Descritiva: Analise Exploratoria com Boxplot, Quartis e Deteccao de Outliers por IQR",
        "Probabilidade: Regra da Soma, do Produto e Probabilidade Condicional com Teorema de Bayes",
        "Variaveis Aleatorias Discretas: Distribuicao Binomial aplicada a falhas de transmissao/sistemas",
        "Variaveis Aleatorias Discretas: Distribuicao de Poisson aplicada a chegada de requisicoes/filas",
        "Variaveis Aleatorias Continuas: Distribuicao Normal, Padronizacao Z e Calculo de Probabilidades",
        "Amostragem e Inferencia: Teorema do Limite Central e Distribuicao das Medias Amostrais",
        "Inferencia Estatistica: Intervalo de Confianca para a Media com Desvio Padrao Conhecido e Desconhecido (t-Student)",
        "Testes de Hipotese: Formulacao de H0 e H1, Nivel de Significancia (alpha), Erros Tipo I/II e p-valor"
    ]
    
    selected_topic = random.choice(topics)
    print(f"Topico sorteado: {selected_topic}")

    prompt = f"""
    Voce e um professor titular de Ciencia da Computacao e Estatistica em uma Universidade Federal, lecionando para o 3º periodo de Sistemas de Informacao.
    Crie uma licao de estudo aprofundada, didatica, tecnica e completa sobre: {selected_topic}.

    Siga rigorosamente este formato Markdown:
    # 📚 Licao de BSI: {selected_topic}
    
    ## 🎯 1. Fundamentacao Teorica e Intuicao
    - Explicacao clara do conceito focada em Sistemas de Informacao e Computacao.
    - Por que este topico cai em provas e onde ele e aplicado na engenharia de software / ciencia de dados.
    
    ## 💻 2. Implementacao Pratica Completa
    - SE FOR ESTRUTURA DE DADOS EM C:
      * Codigo em C modular, legivel e moderno.
      * Demonstre explicitamente o gerenciamento de memoria: checagem de ponteiro nulo (NULL check) e 'free()' ao final.
      * Inclua a funcao main() pronta para compilacao via gcc sem erros.
    - SE FOR ESTATISTICA:
      * Formulas matematicas detalhadas.
      * Script em Python utilizando numpy, scipy ou pandas para resolver um exemplo computacional com dados simulados.
    
    ## ⚠️ 3. Pegadinhas Classicas de Provas da Federal
    - Quais sao os erros conceituais ou de sintaxe que mais reprovam alunos nesse topico (ex: vazamento de memoria por perder ponteiro de cabeca, divisao por zero em variancia n-1, interpretacao errada do p-valor).
    
    ## 🧠 4. Exercicio Pratico de Fixacao com Gabarito
    - Enunciado de um exercicio no estilo de prova universitaria.
    - Solucao comentada e gabarito logo abaixo com explicacao passo a passo.
    """

    models_to_try = ["gemini-3.6-flash", "gemini-3.1-pro-preview"]
    response = None

    for model_name in models_to_try:
        for attempt in range(3):
            try:
                print(f"Tentando {model_name} (tentativa {attempt + 1}/3)...")
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        max_output_tokens=4000,
                        temperature=0.7
                    )
                )
                if response and response.text:
                    print(f"Sucesso com o modelo: {model_name}!")
                    break
            except Exception as e:
                print(f"Aviso [{model_name}]: {e}")
                time.sleep(3)
        
        if response and response.text:
            break

    if not response or not response.text:
        raise RuntimeError("Falha ao gerar conteudo com todos os modelos disponiveis.")

    print("Salvando arquivo Markdown...")
    os.makedirs("generated", exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    clean_topic_name = selected_topic.split(':')[0].replace(' ', '_').lower()
    filename = f"generated/{today}_{clean_topic_name}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(response.text)

    print(f"Licao salva com sucesso em: {filename}")

if __name__ == "__main__":
    generate_daily_study()
