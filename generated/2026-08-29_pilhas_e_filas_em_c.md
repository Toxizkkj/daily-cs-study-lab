# Pilhas e Filas em C

## 1. Teoria e Complexidade

Pilhas (LIFO - *Last In, First Out*) e Filas (FIFO - *First In, First Out*) são estruturas de dados lineares fundamentais. Na Pilha, o último elemento inserido é o primeiro a ser removido (operações no `topo`). Na Fila, o primeiro elemento inserido é o primeiro a ser removido (inserção no `fim`/`tail` e remoção no `inicio`/`head`).

A implementação dinâmica com ponteiros e `structs` permite expandir e contrair a memória em tempo de execução conforme a demanda, eliminando a limitação de tamanho fixo dos vetores estáticos, ao custo de um *overhead* de memória adicional para armazenar os ponteiros de encadeamento.

### Tabela de Complexidade (Big-O)

| Operação | Pilha (LIFO) Dynamic | Fila (FIFO) Dynamic | Vetor Estático (Pior Caso) |
| :--- | :--- | :--- | :--- |
| **Inserção (Push / Enqueue)** | $O(1)$ | $O(1)$ | $O(1)$ / $O(n)$ |
| **Remoção (Pop / Dequeue)** | $O(1)$ | $O(1)$ | $O(n)$ (sem índice circular) |
| **Busca / Acesso** | $O(n)$ | $O(n)$ | $O(n)$ |
| **Espaço (Memória)** | $O(n)$ | $O(n)$ | $O(N_{max})$ |

---

## 2. Implementacao Completa em C

Código compilável demonstrando a implementação de uma **Pilha Dinâmica** com tratamento de erro, prevenção de *underflow* e liberação completa de memória.

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct No {
    int dado;
    struct No *prox;
} No;

typedef struct {
    No *topo;
} Pilha;

Pilha* criar_pilha(void) {
    Pilha *p = (Pilha*) malloc(sizeof(Pilha));
    if (p != NULL) {
        p->topo = NULL;
    }
    return p;
}

int esta_vazia(Pilha *p) {
    return (p == NULL || p->topo == NULL);
}

int push(Pilha *p, int valor) {
    if (p == NULL) return 0;
    No *novo = (No*) malloc(sizeof(No));
    if (novo == NULL) return 0; // Trata falha de alocacao
    
    novo->dado = valor;
    novo->prox = p->topo;
    p->topo = novo;
    return 1;
}

int pop(Pilha *p, int *valor_out) {
    if (esta_vazia(p)) {
        printf("[ERRO] Underflow: Tentativa de remover de pilha vazia.\n");
        return 0;
    }
    No *temp = p->topo;
    *valor_out = temp->dado;
    p->topo = temp->prox;
    free(temp);
    return 1;
}

void liberar_pilha(Pilha *p) {
    if (p == NULL) return;
    No *atual = p->topo;
    while (atual != NULL) {
        No *temp = atual;
        atual = atual->prox;
        free(temp);
    }
    free(p);
}

void imprimir(Pilha *p) {
    if (esta_vazia(p)) {
        printf("Pilha Vazia.\n");
        return;
    }
    No *atual = p->topo;
    printf("Topo -> ");
    while (atual != NULL) {
        printf("[%d] -> ", atual->dado);
        atual = atual->prox;
    }
    printf("NULL\n");
}

int main(void) {
    Pilha *p = criar_pilha();

    push(p, 10);
    push(p, 20);
    push(p, 30);
    imprimir(p);

    int valor;
    if (pop(p, &valor)) printf("Removido: %d\n", valor);
    if (pop(p, &valor)) printf("Removido: %d\n", valor);
    imprimir(p);

    liberar_pilha(p);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Acesso após o `free` (Dangling Pointer / Ponteiro Solto):**
   * *Erro:* Fazer `p->topo = p->topo->prox; free(p->topo);` sem salvar o ponteiro antigo. Ao avançar `p->topo` antes de liberar, você perde o ponteiro original ou libera o elemento errado.
   * *Correção:* Salvar o nó a ser removido em uma variável auxiliar (`No *temp = p->topo`), atualizar o ponteiro principal e só então chamar `free(temp)`.

2. **Vazamento de Memória (*Memory Leak*) ao Desalocar a Estrutura:**
   * *Erro:* Chamar apenas `free(pilha)` achando que a memória encadeada inteira será liberada.
   * *Correção:* É obrigatório percorrer nó por nó com um laço `while`, liberando cada nó individualmente antes de liberar a ponteiro da `struct` descritora.

3. **Segment fault por desreferenciação de NULL (Underflow indevido):**
   * *Erro:* Acessar `p->topo->dado` sem checar se `p` é `NULL` ou se `p->topo` é `NULL`.
   * *Correção:* Sempre validar a condição de estrutura vazia (*underflow*) antes de realizar a operação de remoção ou leitura.

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva a função `int enqueue(Fila *f, int valor)` para uma **Fila Dinâmica** em C. A fila é representada pelas estruturas abaixo. A função deve retornar `1` em caso de sucesso e `0` em caso de falha de alocação.

```c
typedef struct No {
    int dado;
    struct No *prox;
} No;

typedef struct {
    No *inicio;
    No *fim;
} Fila;
```

---

### Gabarito

```c
int enqueue(Fila *f, int valor) {
    if (f == NULL) return 0;
    
    No *novo = (No*) malloc(sizeof(No));
    if (novo == NULL) return 0; // Falha de alocacao
    
    novo->dado = valor;
    novo->prox = NULL;
    
    if (f->fim == NULL) { // Fila estava vazia
        f->inicio = novo;
        f->fim = novo;
    } else {
        f->fim->prox = novo;
        f->fim = novo;
    }
    return 1;
}
```

**Explicação:** O elemento é sempre inserido no final da fila. Se a fila estiver vazia (`f->fim == NULL`), o novo nó torna-se simultaneamente o `inicio` e o `fim`. Caso contrário, encadeia-se o novo nó após o `fim` atual e atualiza-se o ponteiro `f->fim`.