# Pilhas e Filas em C

## 1. Teoria e Complexidade

Pilhas (LIFO - *Last In, First Out*) são estruturas onde o último elemento inserido é o primeiro a ser removido. As operações ocorrem exclusivamente em uma extremidade chamada **topo**. Filas (FIFO - *First In, First Out*) são estruturas onde o primeiro elemento inserido é o primeiro a ser removido. A inserção ocorre na **cauda** (fim) e a remoção ocorre na **cabeça** (início).

Ambas podem ser implementadas dinamicamente usando ponteiros e structs (`Node`). Na pilha, mantemos apenas o ponteiro para o `topo`. Na fila, mantemos ponteiros para o `inicio` e `fim`, garantindo que inserções e remoções sejam executadas em tempo constante sem a necessidade de deslocar elementos na memória.

| Operação | Pilha (Tempo) | Fila (Tempo) | Espaço (Ambos) |
| :--- | :--- | :--- | :--- |
| Inserção (`push` / `enqueue`) | $O(1)$ | $O(1)$ | $O(n)$ |
| Remoção (`pop` / `dequeue`) | $O(1)$ | $O(1)$ | $O(n)$ |
| Consulta Topo/Início (`peek`) | $O(1)$ | $O(1)$ | $O(n)$ |
| Busca por Valor | $O(n)$ | $O(n)$ | $O(n)$ |

---

## 2. Implementação Completa em C

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node* next;
} Node;

typedef struct {
    Node* topo;
} Pilha;

typedef struct {
    Node* inicio;
    Node* fim;
} Fila;

// --- OPERAÇÕES DA PILHA ---
void push(Pilha* p, int val) {
    Node* novo = (Node*)malloc(sizeof(Node));
    if (!novo) return; // Falha de alocação
    novo->data = val;
    novo->next = p->topo;
    p->topo = novo;
}

int pop(Pilha* p, int* erro) {
    if (p->topo == NULL) { // Underflow
        *erro = 1;
        return -1;
    }
    *erro = 0;
    Node* temp = p->topo;
    int val = temp->data;
    p->topo = temp->next;
    free(temp);
    return val;
}

void free_pilha(Pilha* p) {
    Node* atual = p->topo;
    while (atual != NULL) {
        Node* temp = atual;
        atual = atual->next;
        free(temp);
    }
    p->topo = NULL;
}

// --- OPERAÇÕES DA FILA ---
void enqueue(Fila* f, int val) {
    Node* novo = (Node*)malloc(sizeof(Node));
    if (!novo) return; // Falha de alocação
    novo->data = val;
    novo->next = NULL;
    if (f->fim == NULL) {
        f->inicio = f->fim = novo;
    } else {
        f->fim->next = novo;
        f->fim = novo;
    }
}

int dequeue(Fila* f, int* erro) {
    if (f->inicio == NULL) { // Underflow
        *erro = 1;
        return -1;
    }
    *erro = 0;
    Node* temp = f->inicio;
    int val = temp->data;
    f->inicio = f->inicio->next;
    if (f->inicio == NULL) f->fim = NULL; // Fila ficou vazia
    free(temp);
    return val;
}

void free_fila(Fila* f) {
    Node* atual = f->inicio;
    while (atual != NULL) {
        Node* temp = atual;
        atual = atual->next;
        free(temp);
    }
    f->inicio = f->fim = NULL;
}

int main() {
    int erro;
    Pilha p = {NULL};
    Fila f = {NULL, NULL};

    // Teste Pilha (LIFO)
    push(&p, 10);
    push(&p, 20);
    push(&p, 30);
    printf("Pilha Pop: %d\n", pop(&p, &erro)); // Imprime 30

    // Teste Fila (FIFO)
    enqueue(&f, 100);
    enqueue(&f, 200);
    enqueue(&f, 300);
    printf("Fila Dequeue: %d\n", dequeue(&f, &erro)); // Imprime 100

    // Liberacao de Memoria
    free_pilha(&p);
    free_fila(&f);

    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Memory Leak no Pop/Dequeue**: Liberar a estrutura da pilha/fila ou avançar o ponteiro principal sem dar `free()` no nó removido. O nó fica inacessível na memória Heap.
2. **Esquecer de Atualizar `fim` na Fila Vazia**: Ao remover o último elemento de uma fila dinâmica (`dequeue`), `f->inicio` torna-se `NULL`, mas se `f->fim` não for atualizado para `NULL`, ele se torna um ponteiro pendente (*dangling pointer*), causando *Segmentation Fault* nas inserções futuras.
3. **Não Tratar Underflow**: Acessar `p->topo->data` ou `f->inicio->data` quando a pilha/fila está vazia (`NULL`) gera travamento imediato do programa por falha de segmentação.

---

## 4. Exercício com Gabarito

**Enunciado:** Escreva uma função em C `void inverter_fila(Fila* f)` que inverte a ordem dos elementos de uma fila existente utilizando uma pilha auxiliar dinâmica. Assuma que as funções `push`, `pop`, `enqueue` e `dequeue` já estão implementadas.

### Gabarito Explicado

```c
void inverter_fila(Fila* f) {
    Pilha p = {NULL};
    int erro = 0;

    // 1. Desenfileira tudo da Fila e empilha na Pilha (inverte a ordem natural)
    while (f->inicio != NULL) {
        int val = dequeue(f, &erro);
        push(&p, val);
    }

    // 2. Desempilha da Pilha e enfileira de volta na Fila
    while (p.topo != NULL) {
        int val = pop(&p, &erro);
        enqueue(f, val);
    }

    // 3. Garante desalocação da pilha auxiliar (caso de sobram de memória)
    free_pilha(&p);
}
```
*Explicação:* Ao remover da Fila (FIFO) e inserir na Pilha (LIFO), a sequência de dados é invertida. Ao remover da Pilha e re-inserir na Fila, a Fila final conterá todos os elementos originais em ordem invertida.