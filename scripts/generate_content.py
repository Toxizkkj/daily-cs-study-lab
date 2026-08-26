import os
import random
import time
from datetime import datetime, date
from google import genai
from google.genai import types

def get_current_ed_topic():
    # Cronograma estruturado por semanas (Segunda a Domingo)
    # Semana 1 iniciada na Segunda-feira, 24 de Agosto de 2026
    start_date = date(2026, 8, 24)
    today = date.today()
    
    # Calcula a semana atual com base na data de inicio
    days_diff = (today - start_date).days
    week_index = max(0, days_diff // 7)

    schedule = [
        # Semana 1 (24/08 a 30/08)
        ("Pilhas e Filas em C", 
         "implementacao estatica (vetores) e encadeada (dinamica com ponteiros), operacoes push, pop, enqueue, dequeue, verificacao de underflow/overflow, liberacao total de memoria free() e aplicacoes praticas como avaliacao de expressoes e simulacao de buffers"),
        
        # Semana 2 (31/08 a 06/09)
        ("Arvores Binarias em C", 
         "definicao de nos com struct e ponteiros esquerdo/direito, criacao de nos, percursos recursivos em Pre-ordem, Em-ordem e Pos-ordem, calculo de altura, contagem de nos e desalocacao recursiva pos-ordem"),
        
        # Semana 3 (07/09 a 13/09)
        ("Arvores Binarias de Busca (BST) em C", 
         "propriedade fundamental de ordenacao em BST, insercao recursiva/iterativa, busca binaria, remocao de nos considerando os 3 casos (sem filhos, 1 filho e 2 filhos com sucessor/antecessor) e analise de complexidade O(h)"),
        
        # Semana 4 (14/09 a 20/09)
        ("Arvores AVL em C", 
         "fator de balanceamento (FB = h_esq - h_dir), deteccao de desbalanceamento, rotacoes simples a esquerda e direita (RR, LL), rotacoes duplas (RL, LR) e manutencao da complexidade O(log n) nas operacoes"),
        
        # Semana 5 (21/09 a 27/09)
        ("Introducao a Grafos em C", 
         "representacao por Matriz de Adjacencia vs Lista de Adjacencia com ponteiros, percursos e buscas: Busca em Largura (BFS usando fila) e Busca em Profundidade (DFS recursiva/usando pilha)"),
        
        # Semana 6 (28/09 a 04/10)
        ("Arvores B em C", 
         "conceito de arvores multi-caminho balanceadas, ordem m, capacidade minima e maxima de chaves por pagina, algoritmo de divisao de no (split) na insercao e navegacao entre paginas"),
        
        # Semana 7 (05/10 a 11/10)
        ("Tabelas Hash em Memoria em C", 
         "funcoes de dispersao (hashing modular, multiplicativo), tratamento de colisoes por Encadeamento Separado (vetor de listas encadeadas) e Enderecamento Aberto (sondagem linear/quadratica), calculo do fator de carga"),
        
        # Semana 8 (12/10 a 18/10)
        ("Tabelas Hash em Disco e Indexacao em C", 
         "manipulacao de arquivos binarios (fopen com rb/wb, fseek, fread, fwrite), hashing estatico e extensivel em arquivo, buckets em disco e tecnicas de indexacao para minimizar operacoes de I/O")
    ]

    if week_index < len(schedule):
        title, details = schedule[week_index]
        return title, details, f"Semana {week_index + 1}"
    else:
        # Apos as 8 semanas, entra em ciclo de revisao avancada de ED
        title, details = random.choice(schedule)
        return title, details, "Revisao Avancada de ED"

def generate_daily_study():
    print("Iniciando processo de geracao de conteudo (Foco 100% Estrutura de Dados em C)...")
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Chave GEMINI_API_KEY nao configurada.")

    client = genai.Client(api_key=api_key)

    # Permite sobrescrever o topico pelo GitHub Actions caso queira adiantar algo
    override = os.environ.get("OVERRIDE_TOPIC", "").strip()

    if override:
        topic_title = f"Foco Especial: {override}"
        topic_details = f"Topico customizado focado em {override} para Estrutura de Dados em C"
        week_tag = "Personalizado"
    else:
        topic_title, topic_details, week_tag = get_current_ed_topic()

    print(f"Topico de hoje [{week_tag}]: {topic_title}")

    prompt = f"""
    Voce e um professor titular de Estrutura de Dados em C em uma Universidade Federal (curso de Sistemas de Informacao - 3º Periodo).
    Crie uma aula/licao completa, aprofundada, didatica e com codigo robusto em C sobre: {topic_title}.
    Foco especifico de hoje: {topic_details}.

    Siga rigorosamente esta estrutura em Markdown:
    # 📚 Estrutura de Dados em C [{week_tag}]: {topic_title}
    
    ## 🎯 1. Fundamentacao Teorica & Intuicao
    - Explicacao clara do conceito, estruturas de dados envolvidas e complexidade assintotica (Big-O de tempo e espaco).
    - Por que essa estrutura e crucial e onde ela e aplicada na pratica em engenharia de software / sistemas reais.
    
    ## 💻 2. Implementacao Completa em C (Compilavel)
    - Codigo em C completo, limpo e didatico pronto para compilar com gcc.
    - Definicao explicita das structs com typedef.
    - Tratamento obrigatorio de ponteiros: verificacao de alocacao nula (`if (ptr == NULL)`), manipulacao segura de ponteiro duplo (`**`) onde aplicavel e funcao explicita de liberacao de memoria (`free()`) para evitar vazamentos (memory leak).
    - Funcao `main()` demonstrando o uso com saidas impressas via `printf`.
    
    ## ⚠️ 3. Pegadinhas Classicas de Prova da Federal
    - Erros mais comuns que reprovam alunos em provas praticas e teoricas (ex: dangling pointers, segfault ao acessar ponteiro nulo, esquecer de atualizar o ponteiro anterior em remocoes, perda do noh raiz).
    
    ## 🧠 4. Exercicio Pratico de Prova com Gabarito
    - Enunciado de uma questao discursiva/pratica no estilo de prova universitaria federal.
    - Solucao comentada e implementada passo a passo logo abaixo.
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
        raise RuntimeError("Falha ao gerar conteudo com os modelos disponiveis.")

    print("Salvando arquivo...")
    os.makedirs("generated", exist_ok=True)
    today_str = datetime.now().strftime("%Y-%m-%d")
    clean_name = topic_title.split(':')[0].replace(' ', '_').replace('/', '_').lower()
    filename = f"generated/{today_str}_{clean_name}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(response.text)

    print(f"Licao de ED salva com sucesso em: {filename}")

if __name__ == "__main__":
    generate_daily_study()
