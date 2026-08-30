# Pilhas e Filas em C

## 1. Teoria e Complexidade

Uma **Pilha (Stack)** é uma estrutura de dados linear baseada no princípio **LIFO** (*Last-In, First-Out*), onde o último elemento inserido é o primeiro a ser removido. Todas as operações de inserção (`push`) e remoção (`pop`) ocorrem na mesma extremidade, chamada de **topo**.

Uma **Fila (Queue)** é uma estrutura de dados linear baseada no princípio **FIFO** (*First-In, First-Out*), onde o primeiro elemento inserido é o primeiro a ser removido. As inserções (`enqueue`) ocorrem no **fim** (*rear*) e as remoções (`dequeue`) ocorrem no **início** (*front*).

| Operação | Pilha (Tempo) | Fila (Tempo) | Espaço (Ambas) |
| :--- | :--- | :--- | :--- |
| Inserção (Push / Enqueue) | O(1) | O(1) | O(N) |
| Remoção (Pop / Dequeue) | O(1) | O(1) | O(N) |
| Busca (Search) | O(N) | O(N) | O(N) |

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

// --- PILHA (LIFO) ---
void init_stack(Stack *s) {
    s->top = NULL;
}

int push(Stack *s, int val) {
    Node *new_node = (Node*) malloc(sizeof(Node));
    if (!new_node) return 0; // Falha de alocacao
    new_node->data = val;
    new_node->next = s->top;
    s->top = new_node;
    return 1;
}

int pop(Stack *s, int *out_val) {
    if (s->top == NULL) return 0; // Underflow
    Node *temp = s->top;
    *out_val = temp->data;
    s->top = s->top->next;
    free(temp);
    return 1;
}

void free_stack(Stack *s) {
    Node *curr = s->top;
    while (curr != NULL) {
        Node *temp = curr;
        curr = curr->next;
        free(temp);
    }
    s->top = NULL;
}

// --- FILA (FIFO) ---
void init_queue(Queue *q) {
    q->front = NULL;
    q->rear = NULL;
}

int enqueue(Queue *q, int val) {
    Node *new_node = (Node*) malloc(sizeof(Node));
    if (!new_node) return 0; // Falha de alocacao
    new_node->data = val;
    new_node->next = NULL;
    if (q->rear == NULL) {
        q->front = q->rear = new_node;
    } else {
        q->rear->next = new_node;
        q->rear = new_node;
    }
    return 1;
}

int dequeue(Queue *q, int *out_val) {
    if (q->front == NULL) return 0; // Underflow
    Node *temp = q->front;
    *out_val = temp->data;
    q->front = q->front->next;
    if (q->front == NULL) {
        q->rear = NULL;
    }
    free(temp);
    return 1;
}

void free_queue(Queue *q) {
    Node *curr = q->front;
    while (curr != NULL) {
        Node *temp = curr;
        curr = curr->next;
        free(temp);
    }
    q->front = q->rear = NULL;
}

int main() {
    int val;
    
    // Teste da Pilha
    Stack s;
    init_stack(&s);
    push(&s, 10);
    push(&s, 20);
    printf("--- PILHA ---\n");
    if (pop(&s, &val)) printf("Pop: %d\n", val);
    if (pop(&s, &val)) printf("Pop: %d\n", val);
    if (!pop(&s, &val)) printf("Pilha Vazia (Underflow tratado)!\n");
    free_stack(&s);

    // Teste da Fila
    Queue q;
    init_queue(&q);
    enqueue(&q, 100);
    enqueue(&q, 200);
    printf("\n--- FILA ---\n");
    if (dequeue(&q, &val)) printf("Dequeue: %d\n", val);
    if (dequeue(&q, &val)) printf("Dequeue: %d\n", val);
    if (!dequeue(&q, &val)) printf("Fila Vazia (Underflow tratado)!\n");
    free_queue(&q);

    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Uso de Memória Desalocada (Dangling Pointer):** Executar `free(temp)` antes de acessar `temp->next` faz com que o código acesse memória inválida, gerando comportamento indefinido. O correto é salvar `temp->next` em uma variável auxiliar antes de chamar o `free()`.
2. **Segmentation Fault por Falta de Verificação de NULL:** Tentar acessar `s->top->data` em uma pilha vazia sem verificar se `s->top == NULL` desreferencia um ponteiro nulo e causa *SegFault*.
3. **Ponteiro `rear` Solto na Fila:** No `dequeue`, ao remover o último elemento da fila, `q->front` torna-se `NULL`, mas esquecer de atualizar `q->rear = NULL` deixa `rear` apontando para a memória recém-liberada.

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função em C chamada `peek` para a estrutura de **Pilha** apresentada. A função deve consultar o valor armazenado no topo da pilha sem removê-lo. Ela deve retornar `1` se houver elemento no topo e `0` caso a pilha esteja vazia (underflow).

**Gabarito:**

```c
int peek(Stack *s, int *out_val) {
    // 1. Verifica se a pilha esta vazia (Tratamento de Underflow)
    if (s == NULL || s->top == NULL) {
        return 0; 
    }
    
    // 2. Copia o valor do topo sem alterar a estrutura ou liberar memoria
    *out_val = s->top->data;
    
    return 1; // Sucesso
}
```