# Pilhas e Filas em C

## 1. Teoria e Complexidade

Uma **Pilha (Stack)** é uma estrutura de dados linear baseada no princípio **LIFO** (*Last In, First Out*), onde o último elemento inserido é o primeiro a ser removido. Todas as operações de inserção (`push`) e remoção (`pop`) ocorrem em uma única extremidade chamada **topo**.

Uma **Fila (Queue)** é uma estrutura linear baseada no princípio **FIFO** (*First In, First Out*), onde o primeiro elemento inserido é o primeiro a ser removido. As inserções (`enqueue`) ocorrem no **fim** da fila, enquanto as remoções (`dequeue`) ocorrem no **início**.

| Operação | Pilha (Tempo) | Fila (Tempo) | Espaço (Ambas) |
| :--- | :--- | :--- | :--- |
| Inserção (`push` / `enqueue`) | O(1) | O(1) | O(1) por nó |
| Remoção (`pop` / `dequeue`) | O(1) | O(1) | O(1) |
| Busca | O(n) | O(n) | O(n) total |

---

## 2. Implementacao Completa em C

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct No {
    int valor;
    struct No* prox;
} No;

typedef struct {
    No* topo;
} Pilha;

typedef struct {
    No* inicio;
    No* fim;
} Fila;

// --- PILHA ---
Pilha* criar_pilha() {
    Pilha* p = (Pilha*)malloc(sizeof(Pilha));
    if (p) p->topo = NULL;
    return p;
}

void push(Pilha* p, int val) {
    if (!p) return;
    No* novo = (No*)malloc(sizeof(No));
    if (!novo) return;
    novo->valor = val;
    novo->prox = p->topo;
    p->topo = novo;
}

int pop(Pilha* p, int* ok) {
    if (!p || !p->topo) {
        if (ok) *ok = 0; // Underflow
        return -1;
    }
    No* temp = p->topo;
    int val = temp->valor;
    p->topo = temp->prox;
    free(temp);
    if (ok) *ok = 1;
    return val;
}

void liberar_pilha(Pilha* p) {
    if (!p) return;
    No* atual = p->topo;
    while (atual) {
        No* temp = atual;
        atual = atual->prox;
        free(temp);
    }
    free(p);
}

// --- FILA ---
Fila* criar_fila() {
    Fila* f = (Fila*)malloc(sizeof(Fila));
    if (f) { f->inicio = NULL; f->fim = NULL; }
    return f;
}

void enqueue(Fila* f, int val) {
    if (!f) return;
    No* novo = (No*)malloc(sizeof(No));
    if (!novo) return;
    novo->valor = val;
    novo->prox = NULL;
    if (f->fim == NULL) {
        f->inicio = novo;
        f->fim = novo;
    } else {
        f->fim->prox = novo;
        f->fim = novo;
    }
}

int dequeue(Fila* f, int* ok) {
    if (!f || !f->inicio) {
        if (ok) *ok = 0; // Underflow
        return -1;
    }
    No* temp = f->inicio;
    int val = temp->valor;
    f->inicio = temp->prox;
    if (f->inicio == NULL) f->fim = NULL;
    free(temp);
    if (ok) *ok = 1;
    return val;
}

void liberar_fila(Fila* f) {
    if (!f) return;
    No* atual = f->inicio;
    while (atual) {
        No* temp = atual;
        atual = atual->prox;
        free(temp);
    }
    free(f);
}

int main() {
    int ok;

    Pilha* p = criar_pilha();
    push(p, 10);
    push(p, 20);
    printf("Pilha Pop: %d\n", pop(p, &ok)); // Imprime 20

    Fila* f = criar_fila();
    enqueue(f, 100);
    enqueue(f, 200);
    printf("Fila Dequeue: %d\n", dequeue(f, &ok)); // Imprime 100

    liberar_pilha(p);
    liberar_fila(f);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Underflow sem verificação (`Segmentation Fault`):** Tentar desreferenciar `p->topo->valor` ou `f->inicio->valor` quando a estrutura estiver vazia (`NULL`). Sempre verifique se o ponteiro principal e o nó atual não são nulos antes de acessar seus campos.
2. **Ponteiro Solto (*Dangling Pointer*) ao esvaziar a Fila:** Ao remover o último elemento de uma fila no `dequeue`, alterar apenas `f->inicio = NULL` e esquecer de atualizar `f->fim = NULL`. O ponteiro `fim` continuará apontando para uma memória já liberada por `free()`.
3. **Vazamento de Memória (*Memory Leak*):** Executar apenas `free(pilha)` ou `free(fila)` sem iterar sobre a lista encadeada interna para desalocar cada elemento `No` individualmente.

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função em C chamada `int peek_pilha(Pilha* p, int* out)` que consulta o elemento do topo de uma pilha dinamicamente alocada **sem removê-lo**. A função deve tratar underflow e retornar `1` em caso de sucesso ou `0` se a pilha estiver vazia ou nula.

**Gabarito:**

```c
int peek_pilha(Pilha* p, int* out) {
    // Verifica se a pilha existe e se possui ao menos um nó
    if (!p || !p->topo || !out) {
        return 0; // Falha / Underflow
    }
    
    *out = p->topo->valor; // Copia o valor sem alterar a estrutura
    return 1; // Sucesso
}
```