# Introducao a Grafos em C

## 1. Teoria e Complexidade

Um Grafo $G = (V, E)$ é uma estrutura de dados não linear formada por um conjunto de vértices ($V$) e arestas ($E$). A **Lista de Adjacência** representa o grafo mantendo um array de listas encadeadas: cada posição $i$ do array representa o vértice $i$, e sua lista encadeada armazena os vértices adjacentes a ele. É a representação mais eficiente em memória para grafos esparsos ($|E| \ll |V|^2$).

A **Busca em Largura (BFS)** explora o grafo em níveis (camadas de vizinhos mais próximos primeiro) utilizando uma **Fila (FIFO)**. A **Busca em Profundidade (DFS)** explora o grafo indo o mais fundo possível em um ramo antes de realizar o *backtracking*, sendo implementada de forma nativa com **recursão** (Pilha). Ambas utilizam um vetor `visited` para evitar loops em grafos com ciclos.

| Operação / Representação | Complexidade de Tempo | Complexidade de Espaço |
| :--- | :--- | :--- |
| Representação (Espaço Total) | — | $O(V + E)$ |
| Inserção de Aresta | $O(1)$ | $O(1)$ |
| Percurso BFS | $O(V + E)$ | $O(V)$ |
| Percurso DFS | $O(V + E)$ | $O(V)$ |

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
    int* visited;
} Graph;

typedef struct Queue {
    int items[100];
    int front;
    int rear;
} Queue;

Node* createNode(int dest) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    newNode->dest = dest;
    newNode->next = NULL;
    return newNode;
}

Graph* createGraph(int vertices) {
    Graph* graph = (Graph*)malloc(sizeof(Graph));
    graph->numVertices = vertices;
    graph->adjLists = (Node**)malloc(vertices * sizeof(Node*));
    graph->visited = (int*)malloc(vertices * sizeof(int));

    for (int i = 0; i < vertices; i++) {
        graph->adjLists[i] = NULL;
        graph->visited[i] = 0;
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

void resetVisited(Graph* graph) {
    for (int i = 0; i < graph->numVertices; i++) {
        graph->visited[i] = 0;
    }
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
    if (q->front == -1) q->front = 0;
    q->rear++;
    q->items[q->rear] = value;
}

int dequeue(Queue* q) {
    int item = q->items[q->front];
    q->front++;
    if (q->front > q->rear) {
        q->front = q->rear = -1;
    }
    return item;
}

void BFS(Graph* graph, int startVertex) {
    Queue* q = createQueue();
    graph->visited[startVertex] = 1;
    enqueue(q, startVertex);

    printf("BFS (%d): ", startVertex);
    while (!isEmpty(q)) {
        int currentVertex = dequeue(q);
        printf("%d ", currentVertex);

        Node* temp = graph->adjLists[currentVertex];
        while (temp) {
            int adjVertex = temp->dest;
            if (graph->visited[adjVertex] == 0) {
                graph->visited[adjVertex] = 1;
                enqueue(q, adjVertex);
            }
            temp = temp->next;
        }
    }
    printf("\n");
    free(q);
}

void DFS(Graph* graph, int vertex) {
    Node* adjList = graph->adjLists[vertex];
    Node* temp = adjList;

    graph->visited[vertex] = 1;
    printf("%d ", vertex);

    while (temp != NULL) {
        int connectedVertex = temp->dest;
        if (graph->visited[connectedVertex] == 0) {
            DFS(graph, connectedVertex);
        }
        temp = temp->next;
    }
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
    free(graph->visited);
    free(graph);
}

int main() {
    Graph* graph = createGraph(5);

    addEdge(graph, 0, 1);
    addEdge(graph, 0, 2);
    addEdge(graph, 1, 2);
    addEdge(graph, 1, 3);
    addEdge(graph, 2, 4);

    BFS(graph, 0);

    resetVisited(graph);
    printf("DFS (0): ");
    DFS(graph, 0);
    printf("\n");

    freeGraph(graph);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Memory Leak no Dealloc do Grafo**: Liberar `free(graph->adjLists)` ou `free(graph)` sem antes iterar por cada lista encadeada e liberar nó por nó causa vazamento de memória gravíssimo.
2. **Ciclos Infinitos por Falta do Vetor `visited`**: Em grafos não-direcionados ou com ciclos, esquecer de marcar `visited[v] = 1` *antes* de empilhar/enfileirar gera estouro de pilha (*Stack Overflow*) na DFS ou *Loop Infinito* na BFS.
3. **Não Resetar o Vetor `visited`**: Executar a BFS e, logo em seguida, a DFS no mesmo grafo sem zerar o vetor `visited` fará com que a segunda busca não visite nenhum nó, pois todos já constam como visitados.

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função recursiva `int hasPath(Graph* g, int src, int dest)` que retorna `1` se existir um caminho entre o vértice `src` e o vértice `dest`, ou `0` caso contrário, reutilizando o vetor `visited` do próprio grafo.

**Gabarito:**

```c
int hasPath(Graph* g, int src, int dest) {
    if (src == dest) return 1;

    g->visited[src] = 1;
    Node* temp = g->adjLists[src];

    while (temp != NULL) {
        int neighbor = temp->dest;
        if (!g->visited[neighbor]) {
            if (hasPath(g, neighbor, dest)) {
                return 1;
            }
        }
        temp = temp->next;
    }
    return 0;
}
```