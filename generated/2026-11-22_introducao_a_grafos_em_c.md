# Introducao a Grafos em C

## 1. Teoria e Complexidade

Um Grafo $G = (V, E)$ é uma estrutura não linear formada por um conjunto de vértices ($V$) e arestas ($E$). A representação por **Lista de Adjacência** utiliza um vetor de listas encadeadas onde cada posição $i$ contém os vizinhos do vértice $i$. É a escolha ideal para grafos esparsos ($|E| \ll |V|^2$), pois economiza memória em comparação à Matriz de Adjacência.

A **Busca em Largura (BFS)** explora o grafo nível por nível a partir de uma origem, utilizando uma **Fila (FIFO)**. É perfeita para encontrar o caminho mais curto em grafos não ponderados. A **Busca em Profundidade (DFS)** explora o grafo indo o mais fundo possível ao longo de cada ramo antes de retroceder (backtracking), implementada nativamente via **Recursão** (Pilha do sistema).

| Operação / Algoritmo | Complexidade de Tempo | Complexidade de Espaço |
| :--- | :--- | :--- |
| Espaço Total (Grafo) | - | $O(V + E)$ |
| Inserção de Aresta | $O(1)$ | $O(1)$ |
| Busca em Largura (BFS) | $O(V + E)$ | $O(V)$ |
| Busca em Profundidade (DFS)| $O(V + E)$ | $O(V)$ |

---

## 2. Implementacao Completa em C

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int dest;
    struct Node* next;
} Node;

typedef struct Graph {
    int numVertices;
    Node** adjLists;
} Graph;

typedef struct Queue {
    int items[100];
    int front;
    int rear;
} Queue;

Node* createNode(int d) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    newNode->dest = d;
    newNode->next = NULL;
    return newNode;
}

Graph* createGraph(int vertices) {
    Graph* graph = (Graph*)malloc(sizeof(Graph));
    graph->numVertices = vertices;
    graph->adjLists = (Node**)malloc(vertices * sizeof(Node*));
    for (int i = 0; i < vertices; i++) {
        graph->adjLists[i] = NULL;
    }
    return graph;
}

void addEdge(Graph* graph, int src, int dest) {
    Node* newNode = createNode(dest);
    newNode->next = graph->adjLists[src];
    graph->adjLists[src] = newNode;

    newNode = createNode(src);
    newNode->next = graph->adjLists[dest];
    graph->adjLists[dest] = newNode;
}

Queue* createQueue() {
    Queue* q = (Queue*)malloc(sizeof(Queue));
    q->front = -1;
    q->rear = -1;
    return q;
}

int isEmpty(Queue* q) {
    return q->rear == -1;
}

void enqueue(Queue* q, int value) {
    if (q->rear == 99) return;
    if (q->front == -1) q->front = 0;
    q->rear++;
    q->items[q->rear] = value;
}

int dequeue(Queue* q) {
    int item;
    if (isEmpty(q)) return -1;
    item = q->items[q->front];
    q->front++;
    if (q->front > q->rear) {
        q->front = q->rear = -1;
    }
    return item;
}

void bfs(Graph* graph, int startVertex) {
    Queue* q = createQueue();
    int* visited = (int*)calloc(graph->numVertices, sizeof(int));

    visited[startVertex] = 1;
    enqueue(q, startVertex);

    printf("BFS (%d): ", startVertex);
    while (!isEmpty(q)) {
        int current = dequeue(q);
        printf("%d ", current);

        Node* temp = graph->adjLists[current];
        while (temp) {
            int adjVertex = temp->dest;
            if (visited[adjVertex] == 0) {
                visited[adjVertex] = 1;
                enqueue(q, adjVertex);
            }
            temp = temp->next;
        }
    }
    printf("\n");
    free(visited);
    free(q);
}

void dfsRecursive(Graph* graph, int vertex, int* visited) {
    visited[vertex] = 1;
    printf("%d ", vertex);

    Node* temp = graph->adjLists[vertex];
    while (temp) {
        int connectedVertex = temp->dest;
        if (!visited[connectedVertex]) {
            dfsRecursive(graph, connectedVertex, visited);
        }
        temp = temp->next;
    }
}

void dfs(Graph* graph, int startVertex) {
    int* visited = (int*)calloc(graph->numVertices, sizeof(int));
    printf("DFS (%d): ", startVertex);
    dfsRecursive(graph, startVertex, visited);
    printf("\n");
    free(visited);
}

void freeGraph(Graph* graph) {
    for (int i = 0; i < graph->numVertices; i++) {
        Node* temp = graph->adjLists[i];
        while (temp) {
            Node* toFree = temp;
            temp = temp->next;
            free(toFree);
        }
    }
    free(graph->adjLists);
    free(graph);
}

int main() {
    Graph* graph = createGraph(5);
    addEdge(graph, 0, 1);
    addEdge(graph, 0, 2);
    addEdge(graph, 1, 3);
    addEdge(graph, 1, 4);
    addEdge(graph, 2, 4);

    bfs(graph, 0);
    dfs(graph, 0);

    freeGraph(graph);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Vazamento de Memória ao Liberar o Grafo**: Dar `free(graph->adjLists)` ou `free(graph)` sem percorrer cada nó (`Node*`) de cada lista encadeada resulta em *memory leak* massivo dos nós alocados dinamicamente.
2. **Ciclos Infinitos por Falta de Marcação Prévia**: No BFS, marcar o nó como visitado apenas no momento de desempilhar/desenfileirar (em vez de marcar no momento da inserção na fila) faz com que o mesmo nó seja inserido múltiplas vezes na fila, gerando estouro de memória ou redundância severa.
3. **Reaproveitamento Negligente do Vetor `visited`**: Executar BFS e DFS em sequência usando o mesmo ponteiro de `visited` sem zerar os valores (`calloc` ou `memset`) faz com que o segundo algoritmo termine instantaneamente sem visitar os vértices.

---

## 4. Exercicio com Gabarito

**Enunciado**: Escreva uma função em C `int countComponents(Graph* graph)` que retorne a quantidade de componentes conexos existentes em um grafo não direcionado.

**Gabarito**:

```c
void dfsComponent(Graph* graph, int vertex, int* visited) {
    visited[vertex] = 1;
    Node* temp = graph->adjLists[vertex];
    while (temp) {
        if (!visited[temp->dest]) {
            dfsComponent(graph, temp->dest, visited);
        }
        temp = temp->next;
    }
}

int countComponents(Graph* graph) {
    int components = 0;
    int* visited = (int*)calloc(graph->numVertices, sizeof(int));

    for (int v = 0; v < graph->numVertices; v++) {
        if (!visited[v]) {
            dfsComponent(graph, v, visited);
            components++; // Incrementa cada vez que inicia uma nova busca
        }
    }

    free(visited);
    return components;
}
```