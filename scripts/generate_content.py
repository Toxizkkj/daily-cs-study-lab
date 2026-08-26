import os
import random
import time
from datetime import datetime, date
from google import genai
from google.genai import types

def get_current_ed_topic():
    # Cronograma estruturado por semanas (Segunda a Domingo)
    start_date = date(2026, 8, 24)
    today = date.today()
    
    days_diff = (today - start_date).days
    week_index = max(0, days_diff // 7)

    schedule = [
        # Semana 1 (24/08 a 30/08)
        ("Pilhas e Filas em C", 
         "implementacao de Pilhas (LIFO) ou Filas (FIFO) dinamicas com structs e ponteiros, funcoes push/pop ou enqueue/dequeue, tratamento de underflow, verificacao de NULL e liberacao total de memoria free()"),
        
        # Semana 2 (31/08 a 06/09)
        ("Arvores Binarias em C", 
         "definicao de nos com struct e ponteiros esquerdo/direito, percursos recursivos em Pre-ordem, Em-ordem e Pos-ordem, calculo de altura e desalocacao recursiva em pos-ordem"),
        
        # Semana 3 (07/09 a 13/09)
        ("Arvores Binarias de Busca (BST) em C", 
         "propriedade de ordenacao em BST, insercao, busca binaria, remocao nos 3 casos (sem filhos, 1 filho e 2 filhos com sucessor) e complexidade O(h)"),
        
        # Semana 4 (14/09 a 20/09)
        ("Arvores AVL em C", 
         "fator de balanceamento (FB), deteccao de desbalanceamento, rotacoes simples e duplas (LL, RR, LR, RL) e manutencao do O(log n)"),
        
        # Semana 5 (21/09 a 27/09)
        ("Introducao a Grafos em C", 
         "representacao por Lista de Adjacencia com ponteiros, percursos de Busca em Largura (BFS com fila) e Busca em Profundidade (DFS recursiva)"),
        
        # Semana 6 (28/09 a 04/10)
        ("Arvores B em C", 
         "arvores multi-caminho balanceadas, ordem m, regras de chaves por pagina, algoritmo de split e busca eficiente"),
        
        # Semana 7 (05/10 a 11/10)
        ("Tabelas Hash em Memoria em C", 
         "funcoes de dispersao modular, tratamento de colisoes por Encadeamento Separado (vetor de listas encadeadas) e Enderecamento Aberto"),
        
        # Semana 8 (12/10 a 18/10)
        ("Tabelas Hash em Disco e Indexacao em C", 
         "arquivos binarios (fopen rb/wb, fseek, fread, fwrite), hashing estatico/extensivel em arquivo e reducao de I/O em disco")
    ]

    if week_index < len(schedule):
        title, details = schedule[week_index]
        return title, details, f"Semana {week_index + 1}"
    else:
        title, details = random.choice(schedule)
        return title, details, "Revisao Avancada"

def generate_daily_study():
    print("Iniciando geracao de conteudo de ED em C...")
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Chave GEMINI_API_KEY nao configurada.")

    client = genai.Client(api_key=api_key)

    override = os.environ.get("OVERRIDE_TOPIC", "").strip()

    if override:
        topic_title = f"{override}"
        topic_details = f"implementacao pratica e fundamentos de {override} em C com foco em ponteiros e memoria"
        week_tag = "Personalizado"
    else:
        topic_title, topic_details, week_tag = get_current_ed_topic()

    print(f"Topico selecionado [{week_tag}]: {topic_title}")

    prompt = f"""
    Crie uma licao tecnica e direta de Estrutura de Dados em C sobre: {topic_title}.
    Foco do dia: {topic_details}.

    REGRAS DE FORMATAÇÃO:
    - NAO inclua cabecalhos academicos (como nome de professor, disciplina, universidade, data, etc.).
    - Va direto ao conteudo comeco pelo titulo `# {topic_title}`.
    - Seja conciso e focado para que a resposta NUNCA seja cortada no meio.

    ESTRUTURA OBRIGATÓRIA:
    # {topic_title}

    ## 1. Teoria e Complexidade
    - Explicacao direta do conceito (maximo 2 paragrafos).
    - Tabela de complexidade Big-O (tempo e espaco).

    ## 2. Implementacao Completa em C
    - Codigo C 100% completo e compilavel em um unico bloco.
    - Structs com typedef.
    - Funcoes principais (insercao, remocao, busca, liberacao total com free).
    - Funcao main() com testes claros e prints.
    - Codigo limpo, sem comentarios excessivos para caber perfeitamente.

    ## 3. Pegadinhas de Prova
    - 2 ou 3 erros comuns (segfault, memory leak, ponteiro solto).

    ## 4. Exercicio com Gabarito
    - Enunciado pratico curto.
    - Codigo ou solucao explicada do gabarito.
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
                        max_output_tokens=8192,
                        temperature=0.4
                    )
                )
                if response and response.text:
                    print(f"Sucesso com o modelo: {model_name}!")
                    break
            except Exception as e:
                print(f"Aviso [{model_name}]: {e}")
                time.sleep(2)
        
        if response and response.text:
            break

    if not response or not response.text:
        raise RuntimeError("Falha ao gerar conteudo com os modelos.")

    print("Salvando arquivo...")
    os.makedirs("generated", exist_ok=True)
    today_str = datetime.now().strftime("%Y-%m-%d")
    clean_name = topic_title.split(':')[0].replace(' ', '_').replace('/', '_').lower()
    filename = f"generated/{today_str}_{clean_name}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(response.text)

    print(f"Licao salva com sucesso em: {filename}")

if __name__ == "__main__":
    generate_daily_study()
