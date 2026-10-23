# Pilhas e Filas em C

## 1. Teoria e Complexidade
A **Pilha (Stack)** é uma estrutura de dados linear baseada na política **LIFO** (*Last In, First Out*), onde o último elemento inserido é o primeiro a ser removido. Suas operações ocorrem exclusivamente no topo. A **Fila (Queue)** segue a política **FIFO** (*First In, First Out*), onde o primeiro elemento inserido é o primeiro a ser removido. As inserções ocorrem no fim (*rear*) e as remoções no início (*front*).

A implementação dinâmica utilizando ponteiros e `structs` aloca memória no *heap* sob demanda para cada nó. Isso elimina o tamanho limite fixo das estruturas estáticas (vetores), exigindo rigor no controle de alocação (`malloc`), tratamento de subfluxo (*underflow* ao tentar remover de uma estrutura vazia) e desalocação total (`free`).

| Estrutura | Operação | Complexidade Temporal | Complexidade Espacial |
| :--- | :--- | :--- | :--- |
| **Pilha** | Push / Pop / Top | $O(1)$ | $O(N)$ |
| **Fila** | Enqueue / Dequeue | $O(1)$ | $O(N)$ |
| **Ambas** | Busca / Varredura | $O(N)$ | $O(N)$ |

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

// --- PILHA (STACK) ---
Stack* create_stack() {
    Stack* s = (Stack*)malloc(sizeof(Stack));
    if (s) s->top = NULL;
    return s;
}

void push(Stack* s, int val) {
    if (!s) return;
    Node* new_node = (Node*)malloc(sizeof(Node));
    if (!new_node) return;
    new_node->data = val;
    new_node->next = s->top;
    s->top = new_node;
}

int pop(Stack* s, int* ok) {
    if (!s || !s->top) {
        if (ok) *ok = 0; // Underflow
        return -1;
    }
    Node* temp = s->top;
    int val = temp->data;
    s->top = s->top->next;
    free(temp);
    if (ok) *ok = 1;
    return val;
}

void free_stack(Stack* s) {
    if (!s) return;
    Node* curr = s->top;
    while (curr) {
        Node* temp = curr;
        curr = curr->next;
        free(temp);
    }
    free(s);
}

// --- FILA (QUEUE) ---
Queue* create_queue() {
    Queue* q = (Queue*)malloc(sizeof(Queue));
    if (q) { q->front = NULL; q->rear = NULL; }
    return q;
}

void enqueue(Queue* q, int val) {
    if (!q) return;
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

int dequeue(Queue* q, int* ok) {
    if (!q || !q->front) {
        if (ok) *ok = 0; // Underflow
        return -1;
    }
    Node* temp = q->front;
    int val = temp->data;
    q->front = q->front->next;
    if (q->front == NULL) q->rear = NULL;
    free(temp);
    if (ok) *ok = 1;
    return val;
}

void free_queue(Queue* q) {
    if (!q) return;
    Node* curr = q->front;
    while (curr) {
        Node* temp = curr;
        curr = curr->next;
        free(temp);
    }
    free(q);
}

int main() {
    int status;

    // Teste da Pilha
    Stack* s = create_stack();
    push(s, 10);
    push(s, 20);
    printf("Pilha Pop: %d\n", pop(s, &status)); // Imprime 20
    printf("Pilha Pop: %d\n", pop(s, &status)); // Imprime 10
    pop(s, &status);
    if (!status) printf("Pilha Underflow detectado!\n");
    free_stack(s);

    // Teste da Fila
    Queue* q = create_queue();
    enqueue(q, 100);
    enqueue(q, 200);
    printf("Fila Dequeue: %d\n", dequeue(q, &status)); // Imprime 100
    printf("Fila Dequeue: %d\n", dequeue(q, &status)); // Imprime 200
    dequeue(q, &status);
    if (!status) printf("Fila Underflow detectado!\n");
    free_queue(q);

    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Ponteiro Solto (*Dangling Pointer*) no `rear` da Fila**: Ao desenfileirar o último elemento de uma fila, o ponteiro `front` avança para `NULL`, mas se o ponteiro `rear` não for explicitamente atualizado para `NULL`, ele continuará apontando para o nó que acabou de ser liberado com `free()`.
2. **Segmentation Fault por Falta de Verificação de Underflow**: Tentar ler `s->top->data` ou `q->front->data` sem checar se `s->top` ou `q->front` são `NULL`. Se a estrutura estiver vazia, o programa tentará desreferenciar um ponteiro nulo.
3. **Memory Leak na Remoção**: Avançar o ponteiro do topo ou do início (ex: `s->top = s->top->next`) sem salvar o endereço do nó anterior em um ponteiro auxiliar `temp`. Sem o ponteiro auxiliar, torna-se impossível executar o `free(temp)`, causando vazamento de memória.

---

## 4. Exercicio com Gabarito

**Enunciado:** Implemente uma função `int peek(Stack* s, int* val)` para a Pilha. A função deve consultar o elemento do topo sem removê-lo. Se a pilha estiver vazia, deve retornar `0` (*underflow*). Se houver elemento, deve atribuir o valor à variável apontada por `val` e retornar `1`.

**Gabarito:**

```c
int peek(Stack* s, int* val) {
    // 1. Verifica se a estrutura ou o topo sao nulos (Underflow)
    if (!s || !s->top) {
        return 0;
    }
    
    // 2. Copia o valor sem alterar os ponteiros da pilha
    if (val) {
        *val = s->top->data;
    }
    
    return 1; // Sucesso
}
```