# Pilhas e Filas em C

## 1. Teoria e Complexidade

Pilhas (**LIFO** - *Last In, First Out*) inserem e removem elementos exclusivamente no topo. Filas (**FIFO** - *First In, First Out*) inserem no final e removem do início. Ambas as estruturas podem ser implementadas dinamicamente via nós encadeados (`struct`), permitindo crescimento contínuo na memória sem a necessidade de redimensionamento de vetores (*realloc*).

A alocação dinâmica exige gerenciamento manual do ponteiro para a pilha ou fila, além do controle rigoroso das operações de alocação (`malloc`) e desalocação (`free`) para evitar *memory leaks* (vazamento de memória) ou desreferenciamento de ponteiros nulos (*segmentation fault*).

| Operação | Pilha (LIFO) | Fila (FIFO) | Complexidade de Espaço |
| :--- | :--- | :--- | :--- |
| Inserção (*Push / Enqueue*) | O(1) | O(1) | O(1) por nó |
| Remoção (*Pop / Dequeue*) | O(1) | O(1) | O(1) liberado |
| Busca / Acesso | O(n) | O(n) | O(n) total |

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

// PILHA (LIFO)
void push(Stack *s, int val) {
    Node *new_node = (Node*) malloc(sizeof(Node));
    if (!new_node) return;
    new_node->data = val;
    new_node->next = s->top;
    s->top = new_node;
}

int pop(Stack *s, int *out) {
    if (s->top == NULL) return 0; // Underflow
    Node *temp = s->top;
    *out = temp->data;
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

// FILA (FIFO)
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

int dequeue(Queue *q, int *out) {
    if (q->front == NULL) return 0; // Underflow
    Node *temp = q->front;
    *out = temp->data;
    q->front = q->front->next;
    if (q->front == NULL) q->rear = NULL;
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

int main(void) {
    int val;
    
    // Teste da Pilha
    Stack s = {NULL};
    push(&s, 10);
    push(&s, 20);
    printf("--- PILHA ---\n");
    while (pop(&s, &val)) {
        printf("Pop: %d\n", val);
    }
    free_stack(&s);

    // Teste da Fila
    Queue q = {NULL, NULL};
    enqueue(&q, 100);
    enqueue(&q, 200);
    printf("--- FILA ---\n");
    while (dequeue(&q, &val)) {
        printf("Dequeue: %d\n", val);
    }
    free_queue(&q);

    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Acesso Após Liberação (*Use-After-Free*):** Ler `node->next` após ter executado `free(node)`. O correto é salvar o ponteiro do próximo elemento em uma variável temporária antes de desalocar o nó atual:
   ```c
   // ERRO COMUM:
   free(temp);
   curr = temp->next; // Segfault ou Comportamento Indefinido!
   ```

2. **Perda do Ponteiro `rear` na Fila:** Esquecer de atualizar `q->rear = NULL` quando o último elemento é removido (`q->front == NULL`). Isso deixa um ponteiro pendente (*dangling pointer*) no final da fila.

3. **Falso Esvaziamento (*Memory Leak*):** Redefinir `s->top = NULL` ou `q->front = NULL` para "limpar" a estrutura sem percorrer a lista encadeada executando `free()`. A memória alocada permanece inacessível até o término da execução do processo.

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função em C chamada `peek_stack` que retorne o valor contido no topo da pilha sem removê-lo. A função deve tratar a condição de *underflow* retornando `1` para sucesso e `0` caso a pilha esteja vazia.

**Gabarito:**

```c
int peek_stack(const Stack *s, int *out) {
    // Verificacao de underflow / ponteiro nulo
    if (s == NULL || s->top == NULL) {
        return 0; // Pilha vazia ou invalida
    }
    
    // Copia o valor do topo sem alterar a estrutura
    *out = s->top->data;
    return 1; // Sucesso
}
```

*Explicação:* A função apenas inspeciona o nó apontado por `s->top`. Não há alocação, alteração de ponteiros ou uso de `free()`, garantindo complexidade $O(1)$ de tempo e espaço mantendo a integridade da pilha.