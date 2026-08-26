import os
import random
import time
from datetime import datetime, date, timedelta
from google import genai
from google.genai import types

def get_current_ed_topic():
    # Cronograma estruturado por semanas (Segunda a Domingo)
    # Semana 1 iniciada na Segunda-feira, 24 de Agosto de 2026
    start_date = date(2026, 8, 24)
    today = date.today()
    
    # Calcula quantas semanas completas se passaram desde o início
    days_diff = (today - start_date).days
    week_index = max(0, days_diff // 7)

    schedule = [
        "Pilhas e Filas em C (implementacao estatica, circular e encadeada, operacoes push, pop, enqueue, dequeue e analise de vazamento)",
        "Arvores Binarias em C (estruturacao de nos, percursos em Pre-ordem, Em-ordem e Pos-ordem com recursao e desalocacao)",
        "Arvores Binarias de Busca (BST) em C (insercao, busca binaria, remocao com 0, 1 e 2 filhos e complexidade O(h))",
        "Arvores AVL em C (fator de balanceamento, rotacoes simples e duplas a esquerda e direita, mantendo O(log n))",
        "Introducao a Grafos em C (Matriz de Adjacencia vs Lista de Adjacencia, busca em largura BFS e busca em profundidade DFS)",
        "Arvores B em C (conceito de ordem m, divisao de nos split, busca e insercao eficiente)",
        "Tabelas Hash em Memoria em C (funcoes hash, tratamento de colisoes por encadeamento separado e enderecamento aberto)",
        "Tabelas Hash em Disco e Indexacao em C (acesso a arquivos binarios, hashing extensivel e reducao de I/O em disco)"
    ]

    # Se passar das 8 semanas, faz um ciclo das estruturas mais importantes
    if week_index < len(schedule):
        return schedule[week_index], f"Semana {week_index + 1}"
    else:
        chosen = random.choice(schedule)
        return chosen, "Revisao Avancada de ED"

def generate_daily_study():
    print("Iniciando processo de geracao de conteudo...")
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Chave GEMINI_API_KEY nao configurada.")

    client = genai.Client(api_key=api_key)

    # Verifica se o usuario passou um topico manual via GitHub Actions
    override = os.environ.get("OVERRIDE_TOPIC", "").strip()

    stat_topics = [
        "Estatistica Descritiva: Medidas de Posicao (Media, Mediana, Moda) e Sensibilidade a Outliers",
        "Estatistica Descritiva: Medidas de Dispersao (Variancia Amostral n-1, Desvio Padrao e Coeficiente de Variacao)",
        "Analise Exploratoria: Boxplot, Calculo de Quartis e Deteccao de Outliers por IQR",
        "Probabilidade: Regra da Soma, Produto e Probabilidade Condicional com Teorema de Bayes",
        "Variaveis Aleatorias Discretas: Distribuicao Binomial aplicada a falhas e testes de sistemas",
        "Variaveis Aleatorias Discretas: Distribuicao de Poisson para modelagem de requisicoes por segundo",
        "Variaveis Aleatorias Continuas: Distribuicao Normal e Padronizacao Z-score",
        "Inferencia Estatistica: Teorema do Limite Central e Distribuicao Amostral da Media",
        "Inferencia Estatistica: Intervalos de Confianca para a Media (t-Student vs Z)",
        "Testes de Hipotese: Formulacao de H0 e H1, Nivel de Significancia alpha, p-valor e Erros Tipo I/II"
    ]

    today = date.today()
    
    if override:
        selected_topic = f"Foco Especial: {override}"
        module_name = "Modulo Personalizado"
    else:
        # Alterna entre o tema de ED da semana e Estatistica com base no dia do mes
        ed_topic, week_label = get_current_ed_topic()
        if today.day % 2 == 1:
            selected_topic = f"Estrutura de Dados em C [{week_label}]: {ed_topic}"
            module_name = "Estrutura de Dados em C"
        else:
            chosen_stat = random.choice(stat_topics)
            selected_topic = f"Fundamentos de Estatistica: {chosen_stat}"
            module_name = "Fundamentos de Estatistica"

    print(f"Topico de hoje: {selected_topic}")

    prompt = f"""
    Voce e um professor universitario de Ciencia da Computacao e Estatistica em uma Universidade Federal (BSI - 3º Periodo).
    Crie uma aula/licao completa, altamente didatica e aprofundada sobre o tema: {selected_topic}.

    Siga rigorosamente esta estrutura Markdown:
    # 📚 Licao de BSI: {selected_topic}
    
    ## 🎯 1. Fundamentacao Teorica & Intuicao
    - Explicacao direta ao ponto focada em Sistemas de Informacao / Computacao.
    - Por que este conceito e fundamental e onde ele e cobrado em provas/entrevistas.
    
    ## 💻 2. Implementacao Pratica Completa
    - SE FOR ESTRUTURA DE DADOS EM C:
      * Codigo em C modular, compilavel e bem documentado.
      * Mostre o gerenciamento de memoria explicito (malloc, free, checagem de NULL) e a funcao main().
    - SE FOR ESTATISTICA:
      * Formulas matematicas explicadas passo a passo.
      * Script executavel em Python (numpy/scipy) com dados simulados.
    
    ## ⚠️ 3. Pegadinhas Classicas de Provas da Federal
    - Erros mais comuns cometidos por alunos que geram perda de pontos ou falhas criticas (ex: segfault, vazamento de nos, distorcao de metricas estatisticas).
    
    ## 🧠 4. Exercicio de Fixacao com Gabarito
    - Enunciado no estilo de prova universitaria.
    - Solucao comentada passo a passo logo em seguida.
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

    os.makedirs("generated", exist_ok=True)
    today_str = datetime.now().strftime("%Y-%m-%d")
    clean_name = module_name.replace(' ', '_').lower()
    filename = f"generated/{today_str}_{clean_name}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(response.text)

    print(f"Licao salva com sucesso em: {filename}")

if __name__ == "__main__":
    generate_daily_study()
