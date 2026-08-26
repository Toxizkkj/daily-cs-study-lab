# 📚 Estrutura de Dados em C [Semana 1]: Pilhas e Filas em C

**Disciplina:** Estrutura de Dados I  
**Docente:** Prof. Dr. [Nome do Professor]  
**Curso:** Bacharelado em Sistemas de Informação (3º Período) — Universidade Federal  

---

## 🎯 1. Fundamentacao Teorica & Intuicao

Sejam bem-vindos à nossa aula. Hoje estudaremos duas das estruturas de dados lineares mais fundamentais da Ciência da Computação: **Pilhas (Stacks)** e **Filas (Queues)**.

A diferença crucial entre elas não reside na forma como os dados são armazenados na memória física, mas sim na **política de acesso e remoção** dos elementos.

```
       PILHA (LIFO)                     FILA (FIFO)
  Last-In, First-Out               First-In, First-Out

     |  Elemento C  | Topo            Início                   Fim
     |--------------|               +---+   +---+   +---+   +---+
     |  Elemento B  |               | A |-->| B |-->| C |-->| D |
     |--------------|               +---+   +---+   +---+   +---+
     |  Elemento A  | Base          [Sai]                   [Entra]
     +--------------+
```

### 1.1. Pilhas (LIFO - *Last-In, First-Out*)
O último elemento a entrar é obrigatoriamente o primeiro a sair.
* **Inserção (Push):** Adiciona um elemento no **topo**.
* **Remoção (Pop):** Remove o elemento do **topo**.
* **Estática vs. Dinâmica:**
  * *Estática (Vetores):* Tamanho fixo ($N$). Risco de **Overflow** (pilha cheia ao tentar dar `push`).
  * *Dinâmica (Ponteiros/Lista Encadeada):* Cresce conforme a memória RAM disponível (*Heap*). Sem risco de overflow físico até que a memória do sistema se esgote.
  * *Underflow:* Ocorre em ambas ao tentar dar `pop` em uma pilha vazia.

### 1.2. Filas (FIFO - *First-In, First-Out*)
O primeiro elemento a entrar é obrigatoriamente o primeiro a sair.
* **Inserção (Enqueue):** Adiciona no **fim** (*rear/tail*).
* **Remoção (Dequeue):** Remove do **início** (*front/head*).
* **Fila Circular Estática:** Para evitar o deslocamento constante de elementos ($O(N)$) em vetores, utilizamos aritmética modular (`(fim + 1) % CAPACIDADE`) para reutilizar posições liberadas no início do vetor.
* **Fila Dinâmica:** Mantém dois ponteiros principais: `inicio` e `fim`.

### 1.3. Análise de Complexidade Assintótica (Big-O)

| Operação | Pilha Estática | Pilha Dinâmica | Fila Estática (Circular) | Fila Dinâmica |
| :--- | :---: | :---: | :---: | :---: |
| **Push / Enqueue** | $O(1)$ | $O(1)$ | $O(1)$ | $O(1)$ |
| **Pop / Dequeue** | $O(1)$ | $O(1)$ | $O(1)$ | $O(1)$ |
| **Consulta (Peek)**| $O(1)$ | $O(1)$ | $O(1)$ | $O(1)$ |
| **Busca (Search)** | $O(N)$ | $O(N)$ | $O(N)$ | $O(N)$ |
| **Espaço (Space)** | $O(N)$ fixo | $O(N)$ proporcional | $O(N)$ fixo | $O(N)$ proporcional |

*Nota acadêmica:* O consumo de memória na abordagem dinâmica tem um *overhead* extra devido ao ponteiro de encadeamento (`sizeof(Node*)` bytes por nó).

### 1.4. Aplicações Práticas em Engenharia de Software
* **Pilhas:**
  * Gerenciamento de pilha de chamadas de funções (*Call Stack*) da JVM, GCC e execução de código recursivo.
  * Algoritmos de *Undo/Redo* (Ctrl+Z) em editores de texto.
  * AVALIAÇÃO DE EXPRESSÕES MATEMÁTICAS (conversão da notação Infixa para Pós-fixa / Polonesa Reversa).
  * Algoritmos de navegação em Grafos (DFS - *Depth-First Search*).
* **Filas:**
  * Escalonador de processos do Sistema Operacional (Round-Robin, filas de pronto CPU).
  * Buffers de E/S (Sockets de rede, drivers de teclado, streaming de áudio/vídeo).
  * Spool de impressão (Queue de documentos aguardando a impressora).
  * Algoritmos de navegação em Grafos (BFS - *Breadth-First Search*).

---

## 💻 2. Implementacao Completa em C (Compilavel)

Abaixo está a implementação robusta de uma **Pilha Dinâmica** e de uma **Fila Dinâmica** em um único arquivo C compilável. O código atende a todos os critérios de produção e boas práticas exigidos em avaliações acadêmicas.

```c
/**
 * @file estruturas_lineares.c
 * @brief Implementacao robusta de Pilha e Fila Dinamicas em C.
 * @author Prof. Dr. Estrutura de Dados
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

/* ========================================================================== */
/*                         ESTRUTURA DA PILHA DINÂMICA                        */
/* ========================================================================== */

typedef struct NodePilha {
    int dado;
    struct NodePilha* proximo;
} NodePilha;

typedef struct {
    NodePilha* topo;
    size_t tamanho;
} Pilha;

/**
 * @brief Inicializa a estrutura da Pilha.
 */
Pilha* criar_pilha(void) {
    Pilha* p = (Pilha*) malloc(sizeof(Pilha));
    if (p == NULL) {
        fprintf(stderr, "Erro critico: Falha de alocacao de memoria para a Pilha!\n");
        exit(EXIT_FAILURE);
    }
    p->topo = NULL;
    p->tamanho = 0;
    return p;
}

/**
 * @brief Verifica se a pilha esta vazia.
 */
bool pilha_vazia(const Pilha* p) {
    return (p == NULL || p->topo == NULL);
}

/**
 * @brief Insere um elemento no topo da pilha (Push).
 */
bool push(Pilha* p, int valor) {
    if (p == NULL) return false;

    NodePilha* novo = (NodePilha*) malloc(sizeof(NodePilha));
    if (novo == NULL) {
        fprintf(stderr, "Erro: Falha ao alocar memoria para novo no da Pilha.\n");
        return false; // Trata estouro de memoria da Heap
    }

    novo->dado = valor;
    novo->proximo = p->topo;
    p->topo = novo;
    p->tamanho++;
    return true;
}

/**
 * @brief Remove e retorna o elemento do topo da pilha (Pop).
 */
bool pop(Pilha* p, int* valor_out) {
    if (pilha_vazia(p)) {
        fprintf(stderr, "Alerta [Underflow]: Tentativa de Pop em pilha vazia!\n");
        return false;
    }

    NodePilha* temp = p->topo;
    *valor_out = temp->dado;
    p->topo = temp->proximo;
    
    free(temp); // Libera o nó desalocado
    temp = NULL; // Previne dangling pointer local

    p->tamanho--;
    return true;
}

/**
 * @brief Destroi a pilha e libera toda a memoria alocada.
 */
void destruir_pilha(Pilha** p) {
    if (p == NULL || *p == NULL) return;

    NodePilha* atual = (*p)->topo;
    while (atual != NULL) {
        NodePilha* aux = atual->proximo;
        free(atual);
        atual = aux;
    }

    free(*p);
    *p = NULL; // Evita ponteiro pendente no escopo do chamador
    printf("Memoria da Pilha liberada com sucesso.\n");
}


/* ========================================================================== */
/*                         ESTRUTURA DA FILA DINÂMICA                         */
/* ========================================================================== */

typedef struct NodeFila {
    int dado;
    struct NodeFila* proximo;
} NodeFila;

typedef struct {
    NodeFila* inicio;
    NodeFila* fim;
    size_t tamanho;
} Fila;

/**
 * @brief Inicializa a Fila.
 */
Fila* criar_fila(void) {
    Fila* f = (Fila*) malloc(sizeof(Fila));
    if (f == NULL) {
        fprintf(stderr, "Erro critico: Falha de alocacao para a Fila!\n");
        exit(EXIT_FAILURE);
    }
    f->inicio = NULL;
    f->fim = NULL;
    f->tamanho = 0;
    return f;
}

/**
 * @brief Verifica se a fila esta vazia.
 */
bool fila_vazia(const Fila* f) {
    return (f == NULL