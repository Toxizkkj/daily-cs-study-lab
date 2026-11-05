# Introducao a Grafos em C

## 1. Teoria e Complexidade

Um grafo $G = (V, E)$ é uma estrutura de dados composta por um conjunto de vértices ($V$) e um conjunto de arestas ($E$) que conectam esses vértices. A representação por **Lista de Adjacência** utiliza um vetor de ponteiros onde cada posição representa um vértice e aponta para uma lista encadeada contendo seus vizinhos diretos. Essa abordagem é ideal para grafos esparsos ($|E| \ll |V|^2$), pois economiza memória comparada à Matriz de Adjacência.

Os percursos fundamentais em grafos são:
- **Busca em Largura (BFS)**: Explora o grafo nível por nível a partir de uma origem, utilizando uma estrutura de dados de Fila (FIFO). É ideal para encontrar o caminho mínimo em grafos não ponderados.
- **Busca em Profundidade (DFS)**: Explora o grafo avançando o máximo possível ao longo de cada ramo antes de retroceder (*backtracking*), sendo implementada nativamente via recursão (Pilha de execução).

| Operação / Algoritmo | Complexidade de Tempo | Complexidade de Espaço |
| :--- | :--- | :--- |
| **Representação (Espaço Total)** | - | $O(V + E)$ |
| **Inserção de Aresta** | $O(1)$ | $O(1)$ |
| **Remoção de Aresta** | $O(\text{grau}(V))$ | $O(1)$ |
| **Busca em Largura (BFS)** | $O(V + E)$ | $O(V)$ |
| **Busca em Profundidade (DFS)** | $O(V + E)$ | $O(V)$ |

---

## 2. Implementacao Completa em C

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct No {
    int vertice;
    struct No* prox;
} No;

typedef struct Grafo {
    int numVertices;
    No** adj;
} Grafo;

typedef struct Fila {
    int itens[100];
    int frente;
    int tras;
} Fila;

Fila* criarFila() {
    Fila* f = (Fila*)malloc(sizeof(Fila));
    f->frente = -1;
    f->tras = -1;
    return f;
}

int estaVazia(Fila* f) {
    return f->tras == -1;
}

void enfileirar(Fila* f, int valor) {
    if (f->frente == -1) f->frente = 0;
    f->tras++;
    f->itens[f->tras] = valor;
}

int desenfileirar(Fila* f) {
    int item = f->itens[f->frente];
    f->frente++;
    if (f->frente > f->tras) {
        f->frente = f->tras = -1;
    }
    return item;
}

No* criarNo(int v) {
    No* novo = (No*)malloc(sizeof(No));
    novo->vertice = v;
    novo->prox = NULL;
    return novo;
}

Grafo* criarGrafo(int vertices) {
    Grafo* g = (Grafo*)malloc(sizeof(Grafo));
    g->numVertices = vertices;
    g->adj = (No**)malloc(vertices * sizeof(No*));
    for (int i = 0; i < vertices; i++) {
        g->adj[i] = NULL;
    }
    return g;
}

void adicionarAresta(Grafo* g, int src, int dest) {
    No* novo = criarNo(dest);
    novo->prox = g->adj[src];
    g->adj[src] = novo;

    novo = criarNo(src);
    novo->prox = g->adj[dest];
    g->adj[dest] = novo;
}

void removerAresta(Grafo* g, int src, int dest) {
    for (int i = 0; i < 2; i++) {
        int u = (i == 0) ? src : dest;
        int v = (i == 0) ? dest : src;
        
        No* temp = g->adj[u];
        No* ant = NULL;

        while (temp != NULL && temp->vertice != v) {
            ant = temp;
            temp = temp->prox;
        }

        if (temp != NULL) {
            if (ant == NULL) g->adj[u] = temp->prox;
            else ant->prox = temp->prox;
            free(temp);
        }
    }
}

void bfs(Grafo* g, int inicio) {
    int* visitado = (int*)calloc(g->numVertices, sizeof(int));
    Fila* f = criarFila();

    visitado[inicio] = 1;
    enfileirar(f, inicio);

    printf("BFS (%d): ", inicio);
    while (!estaVazia(f)) {
        int atual = desenfileirar(f);
        printf("%d ", atual);

        No* temp = g->adj[atual];
        while (temp != NULL) {
            int adjV = temp->vertice;
            if (!visitado[adjV]) {
                visitado[adjV] = 1;
                enfileirar(f, adjV);
            }
            temp = temp->prox;
        }
    }
    printf("\n");
    free(visitado);
    free(f);
}

void dfsRec(Grafo* g, int v, int* visitado) {
    visitado[v] = 1;
    printf("%d ", v);

    No* temp = g->adj[v];
    while (temp != NULL) {
        if (!visitado[temp->vertice]) {
            dfsRec(g, temp->vertice, visitado);
        }
        temp = temp->prox;
    }
}

void dfs(Grafo* g, int inicio) {
    int* visitado = (int*)calloc(g->numVertices, sizeof(int));
    printf("DFS (%d): ", inicio);
    dfsRec(g, inicio, visitado);
    printf("\n");
    free(visitado);
}

void liberarGrafo(Grafo* g) {
    for (int i = 0; i < g->numVertices; i++) {
        No* temp = g->adj[i];
        while (temp != NULL) {
            No* aux = temp;
            temp = temp->prox;
            free(aux);
        }
    }
    free(g->adj);
    free(g);
}

int main() {
    Grafo* g = criarGrafo(5);

    adicionarAresta(g, 0, 1);
    adicionarAresta(g, 0, 2);
    adicionarAresta(g, 1, 3);
    adicionarAresta(g, 2, 4);

    bfs(g, 0);
    dfs(g, 0);

    printf("Removendo aresta (0, 2)...\n");
    removerAresta(g, 0, 2);

    bfs(g, 0);

    liberarGrafo(g);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Vazamento na Desalocação Encadeada (`Memory Leak`)**: Liberar a estrutura do grafo `free(g)` ou o vetor de listas `free(g->adj)` sem antes iterar e dar `free()` em cada nó de cada lista encadeada deixa todos os nós órfãos na memória.
2. **Esquecer de Marcar o Vértice como Visitado ao Enfileirar na BFS**: Se o vértice for marcado como visitado apenas no momento da remoção da fila (em vez de no momento do enfileiramento), o mesmo nó pode ser inserido múltiplas vezes na fila, causando estouro de memória ou redundância no percurso.
3. **Estouro de Pilha (*Stack Overflow*) na DFS Recursiva**: Em grafos densos ou muito profundos (ex: lista encadeada longa de $10^5$ nós), a DFS recursiva pode estourar a pilha de execução do sistema. Nesses cenários, deve-se usar uma DFS iterativa com pilha explícita alocada na *heap*.

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função recursiva baseada em DFS com a assinatura `int existeCaminho(Grafo* g, int u, int v, int* visitado)` que retorna `1` se existe um caminho entre os vértices `u` e `v`, e `0` caso contrário.

**Gabarito:**

```c
int existeCaminho(Grafo* g, int u, int v, int* visitado) {
    if (u == v) return 1;
    
    visitado[u] = 1;
    No* temp = g->adj[u];
    
    while (temp != NULL) {
        int vizinho = temp->vertice;
        if (!visitado[vizinho]) {
            if (existeCaminho(g, vizinho, v, visitado)) {
                return 1;
            }
        }
        temp = temp->prox;
    }
    
    return 0;
}
```