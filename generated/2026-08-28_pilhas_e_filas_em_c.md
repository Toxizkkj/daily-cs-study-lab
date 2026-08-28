# Pilhas e Filas em C

## 1. Teoria e Complexidade

**Pilha (Stack - LIFO)**: Estrutura do tipo *Last In, First Out* (o último a entrar é o primeiro a sair). As inserções (`push`) e remoções (`pop`) ocorrem exclusivamente em uma extremidade chamada **topo**.

**Fila (Queue - FIFO)**: Estrutura do tipo *First In, First Out* (o primeiro a entrar é o primeiro a sair). As inserções (`enqueue`) ocorrem no **fim** e as remoções (`dequeue`) ocorrem no **início** da estrutura.

| Operação | Pilha (LIFO) | Fila (FIFO) |
| :--- | :--- | :--- |
| Inserção (Push / Enqueue) | O(1) | O(1) |
| Remoção (Pop / Dequeue) | O(1) | O(1) |
| Busca | O(n) | O(n) |
| Espaço Auxiliar | O(n) | O(n) |

---

## 2. Implementacao Completa em C

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node *next;
} Node;

typedef struct {
    Node *top;
} Stack;

typedef struct {
    Node *front;
    Node *rear;
} Queue;

// --- PILHA (STACK) ---
void push(Stack *s, int val) {
    Node *new_node = (Node*) malloc(sizeof(Node));
    if (!new_node) return;
    new_node->data = val;
    new_node->next = s->top;
    s->top = new_node;
}

int pop(Stack *s, int *out) {
    if (!s || !s->top) return 0; // Underflow
    Node *temp = s->top;
    *out = temp->data;
    s->top = s->top->next;
    free(temp);
    return 1;
}

void free_stack(Stack *s) {
    Node *curr = s->top;
    while (curr) {
        Node *temp = curr;
        curr = curr->next;
        free(temp);
    }
    s->top = NULL;
}

// --- FILA (QUEUE) ---
void enqueue(Queue *q, int val) {
    Node *new_node = (Node*) malloc(sizeof(Node));
    if (!new_node) return;
    new_node->data = val;
    new_node->next = NULL;
    if (!q->rear) {
        q->front = q->rear = new_node;
    } else {
        q->rear->next = new_node;
        q->rear = new_node;
    }
}

int dequeue(Queue *q, int *out) {
    if (!q || !q->front) return 0; // Underflow
    Node *temp = q->front;
    *out = temp->data;
    q->front = q->front->next;
    if (!q->front) q->rear = NULL;
    free(temp);
    return 1;
}

void free_queue(Queue *q) {
    Node *curr = q->front;
    while (curr) {
        Node *temp = curr;
        curr = curr->next;
        free(temp);
    }
    q->front = q->rear = NULL;
}

int main() {
    int val;

    // Teste Pilha
    Stack s = {NULL};
    push(&s, 10);
    push(&s, 20);
    if (pop(&s, &val)) printf("Pilha Pop: %d\n", val);
    free_stack(&s);

    // Teste Fila
    Queue q = {NULL, NULL};
    enqueue(&q, 100);
    enqueue(&q, 200);
    if (dequeue(&q, &val)) printf("Fila Dequeue: %d\n", val);
    free_queue(&q);

    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Uso de Memória Desalocada (Use-After-Free)**: Fazer `free(temp)` antes de ler `temp->data` ou `temp->next`. Sempre salve o valor ou o próximo ponteiro em variáveis auxiliares antes de chamar `free()`.
2. **Esquecer de Atualizar `rear` na Fila**: Ao remover o último elemento da fila (`dequeue`), se `q->front` tornar-se `NULL`, o ponteiro `q->rear` deve ser explicitamente atualizado para `NULL`. Caso contrário, ele vira um *dangling pointer*.
3. **Segmentation Fault em Underflow**: Tentar acessar `s->top->data` ou `q->front->data` sem verificar se a ponteiro `top` ou `front` é `NULL` causa falha de segmentação ao tentar desreferenciar um ponteiro nulo.

---

## 4. Exercicio com Gabarito

**Enunciado**: Escreva uma função `int peek(Stack *s, int *out)` que consulta o elemento do topo de uma pilha sem removê-lo. A função deve retornar `1` em caso de sucesso e `0` se houver underflow (pilha vazia ou ponteiro nulo).

**Gabarito**:

```c
int peek(Stack *s, int *out) {
    if (!s || !s->top) {
        return 0; // Pilha vazia ou invalida (Underflow)
    }
    *out = s->top->data; // Copia o valor sem alterar s->top
    return 1;
}
```
*Explicação*: A consulta (*peek*) apenas acessa `s->top->data` se a pilha não for nula nem estiver vazia. Nenhuma memória é liberada e nenhum ponteiro da estrutura é alterado, preservando o estado da pilha.