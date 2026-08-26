# Pilhas e Filas em C

## 1. Teoria e Complexidade

Uma **Pilha (Stack)** é uma estrutura de dados linear do tipo **LIFO** (*Last-In, First-Out*), onde o último elemento inserido é o primeiro a ser removido. Todas as operações de inserção (`push`) e remoção (`pop`) ocorrem na mesma extremidade, chamada de **topo**.

Uma **Fila (Queue)** é uma estrutura linear do tipo **FIFO** (*First-In, First-Out*), onde o primeiro elemento inserido é o primeiro a ser removido. Inserções (`enqueue`) ocorrem no **fim** (*rear*) e remoções (`dequeue`) ocorrem no **início** (*front*). A alocação dinâmica com `struct` e ponteiros permite que ambas cresçam e encolham sob demanda sem desperdício de memória.

| Operação | Pilha (Push/Pop) | Fila (Enqueue/Dequeue) | Espaço (Ambas) |
| :--- | :--- | :--- | :--- |
| **Inserção** | O(1) | O(1) | O(n) |
| **Remoção** | O(1) | O(1) | O(n) |
| **Busca** | O(n) | O(n) | O(n) |

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

// --- OPERAÇÕES DE PILHA ---
Stack* create_stack() {
    Stack *s = (Stack*) malloc(sizeof(Stack));
    s->top = NULL;
    return s;
}

void push(Stack *s, int val) {
    Node *new_node = (Node*) malloc(sizeof(Node));
    if (!new_node) return;
    new_node->data = val;
    new_node->next = s->top;
    s->top = new_node;
}

int pop(Stack *s) {
    if (s->top == NULL) {
        printf("Underflow na Pilha!\n");
        return -1;
    }
    Node *temp = s->top;
    int val = temp->data;
    s->top = s->top->next;
    free(temp);
    return val;
}

void free_stack(Stack *s) {
    Node *curr = s->top;
    while (curr != NULL) {
        Node *temp = curr;
        curr = curr->next;
        free(temp);
    }
    free(s);
}

// --- OPERAÇÕES DE FILA ---
Queue* create_queue() {
    Queue *q = (Queue*) malloc(sizeof(Queue));
    q->front = q->rear = NULL;
    return q;
}

void enqueue(Queue *q, int val) {
    Node *new_node = (Node*) malloc(sizeof(Node));
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

int dequeue(Queue *q) {
    if (q->front == NULL) {
        printf("Underflow na Fila!\n");
        return -1;
    }
    Node *temp = q->front;
    int val = temp->data;
    q->front = q->front->next;
    if (q->front == NULL) {
        q->rear = NULL;
    }
    free(temp);
    return val;
}

void free_queue(Queue *q) {
    Node *curr = q->front;
    while (curr != NULL) {
        Node *temp = curr;
        curr = curr->next;
        free(temp);
    }
    free(q);
}

int main() {
    Stack *pilha = create_stack();
    push(pilha, 10);
    push(pilha, 20);
    printf("Pop Pilha: %d\n", pop(pilha)); // Imprime 20

    Queue *fila = create_queue();
    enqueue(fila, 100);
    enqueue(fila, 200);
    printf("Dequeue Fila: %d\n", dequeue(fila)); // Imprime 100

    free_stack(pilha);
    free_queue(fila);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Uso de Memória Acessada Após `free()` (Dangling Pointer):** Executar `free(temp)` antes de ler `temp->next` resulta em comportamento indefinido (Segfault). Sempre guarde a referência do próximo nó *antes* de desalocar o atual.
2. **Esquecer de atualizar `rear` no Dequeue da Fila:** Se a fila tiver apenas 1 elemento e ele for removido, `q->front` vira `NULL`, mas se `q->rear` continuar apontando para o nó liberado, o ponteiro fica solto (*dangling pointer*).
3. **Vazamento de Memória (Memory Leak) na Desalocação:** Liberar a estrutura da Pilha/Fila (`free(s)` ou `free(q)`) sem iterar e dar `free()` em todos os nós dinâmicos criados individualmente com `malloc()`.

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função em C chamada `int peek(Stack *s)` que retorna o valor do topo da pilha **sem removê-lo**. A função deve verificar se a pilha está vazia (Underflow) e retornar `-1` caso esteja.

**Gabarito:**

```c
int peek(Stack *s) {
    // 1. Verificação de ponteiros nulos/Underflow
    if (s == NULL || s->top == NULL) {
        printf("Erro: Pilha vazia ou nao inicializada.\n");
        return -1;
    }
    // 2. Retorna o valor sem alterar a estrutura ou remover o no
    return s->top->data;
}
```

*Explicação:* Diferente do `pop()`, o `peek()` apenas inspeciona o valor no ponteiro `s->top`. Nenhum `free()` é chamado e o ponteiro `s->top` permanece inalterado.