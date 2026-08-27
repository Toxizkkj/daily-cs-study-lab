# Pilhas e Filas em C

## 1. Teoria e Complexidade

Uma **Pilha (Stack)** é uma estrutura de dados linear baseada no princípio **LIFO** (*Last-In, First-Out*), onde o último elemento inserido é o primeiro a ser removido. As operações ocorrem exclusivamente em uma extremidade chamada **Topo**. É utilizada em chamadas de funções (call stack), desfazer/refazer (undo/redo) e avaliação de expressões.

Uma **Fila (Queue)** é uma estrutura linear baseada no princípio **FIFO** (*First-In, First-Out*), onde o primeiro elemento inserido é o primeiro a ser removido. As inserções ocorrem no **Fim** (*rear*) e as remoções no **Início** (*front*). É amplamente utilizada em sistemas de impressão, escalonamento de processos e buffers de rede.

| Operação | Pilha (Tempo) | Fila (Tempo) | Espaço (Ambas) |
| :--- | :--- | :--- | :--- |
| Inserção (*Push* / *Enqueue*) | $O(1)$ | $O(1)$ | $O(N)$ |
| Remoção (*Pop* / *Dequeue*) | $O(1)$ | $O(1)$ | $O(N)$ |
| Busca / Acesso | $O(N)$ | $O(N)$ | $O(N)$ |

---

## 2. Implementacao Completa em C

```c
#include <stdio.h>
#include <stdlib.h>

// Struct do Nó
typedef struct Node {
    int data;
    struct Node* next;
} Node;

// Struct da Pilha
typedef struct {
    Node* top;
} Stack;

// Struct da Fila
typedef struct {
    Node* front;
    Node* rear;
} Queue;

// --- FUNÇÕES DA PILHA ---
Stack* create_stack() {
    Stack* s = (Stack*)malloc(sizeof(Stack));
    if (s) s->top = NULL;
    return s;
}

void push(Stack* s, int value) {
    if (!s) return;
    Node* new_node = (Node*)malloc(sizeof(Node));
    if (!new_node) return; // Falha de alocacao
    new_node->data = value;
    new_node->next = s->top;
    s->top = new_node;
}

int pop(Stack* s, int* success) {
    if (!s || !s->top) { // Underflow
        if (success) *success = 0;
        return -1;
    }
    Node* temp = s->top;
    int value = temp->data;
    s->top = temp->next;
    free(temp);
    if (success) *success = 1;
    return value;
}

void free_stack(Stack* s) {
    if (!s) return;
    Node* current = s->top;
    while (current) {
        Node* temp = current;
        current = current->next;
        free(temp);
    }
    free(s);
}

// --- FUNÇÕES DA FILA ---
Queue* create_queue() {
    Queue* q = (Queue*)malloc(sizeof(Queue));
    if (q) {
        q->front = NULL;
        q->rear = NULL;
    }
    return q;
}

void enqueue(Queue* q, int value) {
    if (!q) return;
    Node* new_node = (Node*)malloc(sizeof(Node));
    if (!new_node) return;
    new_node->data = value;
    new_node->next = NULL;
    
    if (q->rear == NULL) {
        q->front = new_node;
        q->rear = new_node;
    } else {
        q->rear->next = new_node;
        q->rear = new_node;
    }
}

int dequeue(Queue* q, int* success) {
    if (!q || !q->front) { // Underflow
        if (success) *success = 0;
        return -1;
    }
    Node* temp = q->front;
    int value = temp->data;
    q->front = q->front->next;
    
    if (q->front == NULL) {
        q->rear = NULL; // Fila ficou vazia
    }
    
    free(temp);
    if (success) *success = 1;
    return value;
}

void free_queue(Queue* q) {
    if (!q) return;
    Node* current = q->front;
    while (current) {
        Node* temp = current;
        current = current->next;
        free(temp);
    }
    free(q);
}

// --- MAIN COM TESTES ---
int main() {
    int status;

    // Teste Pilha (LIFO)
    printf("=== TESTE PILHA ===\n");
    Stack* s = create_stack();
    push(s, 10);
    push(s, 20);
    push(s, 30);

    while (s->top != NULL) {
        int val = pop(s, &status);
        if (status) printf("Pop Pilha: %d\n", val);
    }
    pop(s, &status); // Teste Underflow
    if (!status) printf("Pilha Vazia! (Underflow controlado)\n");
    free_stack(s);

    // Teste Fila (FIFO)
    printf("\n=== TESTE FILA ===\n");
    Queue* q = create_queue();
    enqueue(q, 100);
    enqueue(q, 200);
    enqueue(q, 300);

    while (q->front != NULL) {
        int val = dequeue(q, &status);
        if (status) printf("Dequeue Fila: %d\n", val);
    }
    dequeue(q, &status); // Teste Underflow
    if (!status) printf("Fila Vazia! (Underflow controlado)\n");
    free_queue(q);

    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Ponteiro Solto no Dequeue (Dangling Pointer):**
   Ao remover o último elemento de uma Fila, atualizar apenas `q->front = NULL` e esquecer de atualizar `q->rear = NULL` deixa `rear` apontando para a memória liberada pelo `free()`, causando *Undefined Behavior* na próxima inserção.

2. **Memory Leak no Pop / Dequeue:**
   Acessar `s->top = s->top->next` antes de salvar o ponteiro do nó antigo impede a execução do `free()`. A memória correspondente ao nó removido permanecerá alocada até o fim da execução do programa.

3. **Acesso Direto Sem Verificação de Underflow:**
   Fazer `int val = s->top->data` diretamente em uma função sem verificar se `s` ou `s->top` são `NULL` gera erro de desreferenciação de ponteiro nulo (*Segmentation Fault*).

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função em C chamada `int peek(Stack* s, int* status)` que retorna o elemento do topo de uma pilha dinamicamente alocada **sem removê-lo**. Caso a pilha esteja vazia (underflow) ou o ponteiro seja nulo, a função deve atribuir `0` ao ponteiro `status` e retornar `-1`. Caso contrário, atribui `1` ao `status` e retorna o valor.

**Gabarito:**

```c
int peek(Stack* s, int* status) {
    // 1. Verificacao de ponteiro da pilha e underflow
    if (s == NULL || s->top == NULL) {
        if (status != NULL) {
            *status = 0; // Sinaliza erro/vazio
        }
        return -1;
    }

    // 2. Sinaliza sucesso
    if (status != NULL) {
        *status = 1;
    }

    // 3. Retorna o dado do topo sem alterar a estrutura (sem free)
    return s->top->data;
}
```