import os
import random
from datetime import datetime
from google import genai

def generate_daily_study():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Chave GEMINI_API_KEY não configurada.")

    client = genai.Client(api_key=api_key)

    topics = [
        "Estrutura de Dados em C: Alocação Dinâmica e Gerenciamento de Memória (malloc, free, realloc)",
        "Estrutura de Dados em C: Listas Simplesmente e Duplamente Encadeadas com manipulação de ponteiros",
        "Estrutura de Dados em C: Pilhas (Stacks) e Filas (Queues) com tratamento de underflow/overflow",
        "Estrutura de Dados em C: Árvores Binárias de Busca (BST) e Árvores AVL com balanceamento",
        "Estrutura de Dados em C: Algoritmos de Ordenação (Quicksort, Mergesort) e busca binária",
        "Estatística Descritiva: Média, Mediana, Moda, Variância, Desvio Padrão e Amplitude Interquartil (IQR)",
        "Probabilidade: Distribuição Normal, Binomial, Poisson e Cálculo de Z-Score",
        "Inferência Estatística: Teorema do Limite Central, Intervalos de Confiança e Erro Padrão",
        "Testes de Hipótese: Teste t de Student, Teste Qui-Quadrado, p-valor e Nível de Significância",
        "Regressão Linear Simples: Coeficiente de Determinação (R²), Correlação de Pearson e Resíduos"
    ]
    
    selected_topic = random.choice(topics)

    prompt = f"""
    Você é um professor universitário sênior de Ciência da Computação e Estatística.
    Crie uma lição de estudo aprofundada, clara e altamente didática sobre: {selected_topic}.

    Siga rigorosamente esta estrutura em Markdown:
    # 📚 Lição do Dia: [Nome do Tópico]
    
    ## 🎯 1. Conceito Central & Intuição
    Explique o que é, por que existe e qual problema resolve na prática.
    
    ## 💻 2. Código Prático & Análise Detalhada
    - Se for de C: código completo, compilável, com foco em segurança de ponteiros e memória (mostre quando desalocar).
    - Se for de Estatística: fórmula matemática explicada e um script prático em Python (com numpy/scipy) demonstrando o cálculo.
    
    ## ⚠️ 3. Pegadinhas Comuns & Casos de Borda
    Quais erros os alunos mais cometem em provas ou entrevistas técnicas sobre isso? (ex: segfault, vazamento, interpretação errada de p-valor).
    
    ## 🧠 4. Mini-Desafio do Dia
    Um exercício conceitual ou de código para fixação.
    """

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    os.makedirs("generated", exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"generated/{today}_{selected_topic.split(':')[0].replace(' ', '_').lower()}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(response.text)

    print(f"Lição gerada com sucesso em: {filename}")

if __name__ == "__main__":
    generate_daily_study()
