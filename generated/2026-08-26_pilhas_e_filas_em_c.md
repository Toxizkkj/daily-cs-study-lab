# Pilhas e Filas em C

## 1. Teoria e Complexidade

Pilhas (LIFO - *Last In, First Out*) e Filas (FIFO - *First In, First Out*) são estruturas de dados lineares dinâmicas. Na pilha, a inserção (*push*) e a remoção (*pop*) ocorrem na mesma extremidade (topo). Na fila, a inserção (*enqueue*) ocorre no fim (*rear*) e a remoção (*dequeue*) ocorre no início (*front*). Ambas são implementadas dinamicamente usando alocação de nós encadeados via ponteiros em C, permitindo crescimento sob demanda limitado apenas pela memória do sistema.

Tratamentos críticos incluem a verificação de **underflow** (tentar remover de uma estrutura vazia) e validação de alocação de memória (checar se `malloc` retornou `NULL`). A liberação completa da memória exige a iteração nó a nó para evitar vazamentos de memória (*memory leaks*).

| Operação | Pilha (Tempo) | Fila (Tempo) | Espaço |
| :--- | :--- | :--- | :--- |
| Inserção (Push / Enqueue) | $O(1)$ | $O(1)$ | $O(N)$ |
| Remoção (Pop / Dequeue) | $O(1)$ | $O(1)$ | $O(N)$ |
| Busca / Acesso | $O(N)$ | $O(N)$ | $O(N)$ |

---

## 2. Implementacao Completa em C

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node* next;
} Node;

typedef struct {
    Node* top;
} Stack;

typedef struct {
    Node* front;
    Node* rear;
} Queue;

// Operacoes da Pilha
void push(Stack* s, int val) {
    Node* new_node = (Node*)malloc(sizeof(Node));
    if (!new_node) return;
    new_node->data = val;
    new_node->next = s->top;
    s->top = new_node;
}

int pop(Stack* s, int* val) {
    if (s->top == NULL) return 0; // Underflow
    Node* temp = s->top;
    *val = temp->data;
    s->top = s->top->next;
    free(temp);
    return 1;
}

void free_stack(Stack* s) {
    Node* curr = s->top;
    while (curr) {
        Node* temp = curr;
        curr = curr->next;
        free(temp);
    }
    s->top = NULL;
}

// Operacoes da Fila
void enqueue(Queue* q, int val) {
    Node* new_node = (Node*)malloc(sizeof(Node));
    if (!new_node) return;
    new_node->data = val;
    new_node->next = NULL;
    if (q->rear == NULL) {
        q->front = q->rear = new_node;
        return;
    }
    q->rear->next = new_node;
    q->rear = new_node;
}

int dequeue(Queue* q, int* val) {
    if (q->front == NULL) return 0; // Underflow
    Node* temp = q->front;
    *val = temp->data;
    q->front = q->front->next;
    if (q->front == NULL) q->rear = NULL; // Trata ponteiro preso
    free(temp);
    return 1;
}

void free_queue(Queue* q) {
    Node* curr = q->front;
    while (curr) {
        Node* temp = curr;
        curr = curr->next;
        free(temp);
    }
    q->front = q->rear = NULL;
}

int main() {
    Stack s = {NULL};
    Queue q = {NULL, NULL};
    int val;

    // Teste Pilha
    push(&s, 10);
    push(&s, 20);
    if (pop(&s, &val)) printf("Pilha Pop: %d\n", val); // 20

    // Teste Fila
    enqueue(&q, 100);
    enqueue(&q, 200);
    if (dequeue(&q, &val)) printf("Fila Dequeue: %d\n", val); // 100

    free_stack(&s);
    free_queue(&q);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Ponteiro Solto em Fila Vazia (*Dangling Pointer*):**
   No `dequeue`, ao remover o último nó, se você atualizar apenas `q->front = NULL` sem atualizar `q->rear = NULL`, o ponteiro `rear` continuará apontando para uma memória que já foi liberada com `free()`.
2. **Segmentation Fault em Underflow:**
   Tentar desreferenciar `s->top->data` ou `s->top->next` quando `s->top == NULL` gera *Segmentation Fault*. Sempre cheque se o ponteiro é nulo antes do acesso.
3. **Vazamento de Memória ao Desempilhar/Desenfileirar:**
   Avançar o ponteiro de topo (`s->top = s->top->next`) sem salvar o nó anterior em uma variável temporária para executar o `free()` resulta em nós órfãos ocupando RAM permanentemente.

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função em C chamada `peek` para a estrutura de Pilha. A função deve consultar o elemento do topo sem removê-lo, retornando `1` em caso de sucesso ou `0` se a pilha estiver vazia (*underflow*).

**Gabarito:**

```c
int peek(Stack* s, int* val) {
    if (s == NULL || s->top == NULL) {
        return 0; // Tratamento de underflow / ponteiro nulo
    }
    *val = s->top->data; // Obtém o valor do topo sem alterar s->top
    return 1;
}
```