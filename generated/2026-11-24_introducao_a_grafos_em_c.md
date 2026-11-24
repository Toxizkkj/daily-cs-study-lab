# Introducao a Grafos em C

## 1. Teoria e Complexidade

Um **Grafo** $G = (V, E)$ é uma estrutura de dados formada por um conjunto de vértices ($V$) e um conjunto de arestas ($E$) que conectam esses vértices. Na **Lista de Adjacência**, o grafo é representado por um vetor de ponteiros onde cada elemento aponta para uma lista encadeada contendo seus vizinhos diretos. Essa abordagem é ideal para grafos esparsos, pois otimiza a memória.

Para percorrer o grafo, utilizam-se dois algoritmos fundamentais:
- **Busca em Largura (BFS)**: Explora o grafo nível por nível a partir da origem, utilizando uma **Fila (FIFO)**. É ideal para encontrar o menor caminho em grafos não ponderados.
- **Busca em Profundidade (DFS)**: Explora cada ramo o mais fundo possível antes de fazer o *backtracking*, utilizando **recursão** (pilha de execução).

| Operação / Algoritmo | Complexidade de Tempo | Complexidade de Espaço |
| :--- | :--- | :--- |
| Representação (Espaço Total) | - | $O(V + E)$ |
| Inserção de Aresta | $O(1)$ | $O(1)$ |
| Busca em Largura (BFS) | $O(V + E)$ | $O(V)$ |
| Busca em Profundidade (DFS) | $O(V + E)$ | $O(V)$ |

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

Node* createNode(int v) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    newNode->dest = v;
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
    // Aresta de src para dest
    Node* newNode = createNode(dest);
    newNode->next = graph->adjLists[src];
    graph->adjLists[src] = newNode;

    // Aresta de dest para src (Grafo Nao-Direcionado)
    newNode = createNode(src);
    newNode->next = graph->adjLists[dest];
    graph->adjLists[dest] = newNode;
}

void resetVisited(Graph* graph) {
    for (int i = 0; i < graph->numVertices; i++) {
        graph->visited[i] = 0;
    }
}

void DFS(Graph* graph, int vertex) {
    graph->visited[vertex] = 1;
    printf("%d ", vertex);

    Node* temp = graph->adjLists[vertex];
    while (temp) {
        int adjVertex = temp->dest;
        if (!graph->visited[adjVertex]) {
            DFS(graph, adjVertex);
        }
        temp = temp->next;
    }
}

void BFS(Graph* graph, int startVertex) {
    int queue[100];
    int front = 0, rear = 0;

    graph->visited[startVertex] = 1;
    queue[rear++] = startVertex;

    while (front < rear) {
        int current = queue[front++];
        printf("%d ", current);

        Node* temp = graph->adjLists[current];
        while (temp) {
            int adj = temp->dest;
            if (!graph->visited[adj]) {
                graph->visited[adj] = 1;
                queue[rear++] = adj;
            }
            temp = temp->next;
        }
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
    addEdge(graph, 1, 3);
    addEdge(graph, 1, 4);

    printf("Percurso DFS (inicio em 0): ");
    DFS(graph, 0);
    printf("\n");

    resetVisited(graph);

    printf("Percurso BFS (inicio em 0): ");
    BFS(graph, 0);
    printf("\n");

    freeGraph(graph);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Reaproveitamento do vetor `visited` sem reset:** Executar BFS e DFS sequencialmente no mesmo grafo sem zerar o vetor `visited` entre as chamadas faz com que a segunda busca termine imediatamente sem visitar nenhum nó.
2. **Memory Leak ao liberar o grafo:** Liberar a estrutura `Graph` ou o vetor `adjLists` antes de percorrer e dar `free()` em cada `Node` de cada lista encadeada gera vazamento de memória grave.
3. **Loop Infinito em Grafos com Ciclos:** Esquecer de marcar o nó como visitado **antes** de empilhar (BFS) ou de fazer a chamada recursiva (DFS) causa recursão infinita ou estouro de memória da fila.

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função em C chamada `hasPath` que recebe um grafo, um vértice de origem (`src`) e um vértice de destino (`dest`), e retorna `1` se existir um caminho entre eles ou `0` caso contrário, utilizando DFS. Assuma que o vetor `visited` foi previamente zerado.

**Gabarito:**

```c
int hasPath(Graph* graph, int src, int dest) {
    if (src == dest) return 1;
    
    graph->visited[src] = 1;
    Node* temp = graph->adjLists[src];
    
    while (temp) {
        int adj = temp->dest;
        if (!graph->visited[adj]) {
            if (hasPath(graph, adj, dest)) {
                return 1;
            }
        }
        temp = temp->next;
    }
    
    return 0;
}
```