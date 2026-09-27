# Introducao a Grafos em C

## 1. Teoria e Complexidade

Um grafo $G = (V, E)$ é uma estrutura de dados não linear composta por um conjunto de vértices $V$ e um conjunto de arestas $E$. A representação por **Lista de Adjacência** utiliza um vetor de ponteiros para listas encadeadas, onde cada posição $i$ do vetor contém a lista de vértices vizinhos ao vértice $i$. Essa abordagem é ideal para grafos esparsos, otimizando o uso de memória em comparação à Matriz de Adjacência $O(V^2)$.

A exploração do grafo é feita por dois algoritmos fundamentais: **Busca em Largura (BFS)**, que utiliza uma Fila para explorar os vértices por camadas de distância, e **Busca em Profundidade (DFS)**, que utiliza recursão (Pilha de Chamadas) para avançar até o ponto mais distante antes de retornar (*backtracking*).

| Operação / Algoritmo | Complexidade de Tempo | Complexidade de Espaço |
| :--- | :--- | :--- |
| Representação (Estrutura) | - | $O(V + E)$ |
| Inserção de Aresta | $O(1)$ | $O(1)$ |
| Remoção de Aresta | $O(V)$ | $O(1)$ |
| Busca em Largura (BFS) | $O(V + E)$ | $O(V)$ |
| Busca em Profundidade (DFS)| $O(V + E)$ | $O(V)$ |

---

## 2. Implementacao Completa em C

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct No {
    int destino;
    struct No* prox;
} No;

typedef struct Grafo {
    int numVertices;
    No** listasAdj;
} Grafo;

typedef struct Fila {
    int itens[100];
    int frente;
    int tras;
} Fila;

No* criarNo(int dest) {
    No* novo = (No*)malloc(sizeof(No));
    novo->destino = dest;
    novo->prox = NULL;
    return novo;
}

Grafo* criarGrafo(int vertices) {
    Grafo* g = (Grafo*)malloc(sizeof(Grafo));
    g->numVertices = vertices;
    g->listasAdj = (No**)malloc(vertices * sizeof(No*));
    for (int i = 0; i < vertices; i++) {
        g->listasAdj[i] = NULL;
    }
    return g;
}

void adicionarAresta(Grafo* g, int orig, int dest) {
    No* novo = criarNo(dest);
    novo->prox = g->listasAdj[orig];
    g->listasAdj[orig] = novo;

    novo = criarNo(orig);
    novo->prox = g->listasAdj[dest];
    g->listasAdj[dest] = novo;
}

void removerAresta(Grafo* g, int orig, int dest) {
    for (int i = 0; i < 2; i++) {
        int u = (i == 0) ? orig : dest;
        int v = (i == 0) ? dest : orig;
        No* atual = g->listasAdj[u];
        No* ant = NULL;

        while (atual != NULL && atual->destino != v) {
            ant = atual;
            atual = atual->prox;
        }
        if (atual != NULL) {
            if (ant == NULL) g->listasAdj[u] = atual->prox;
            else ant->prox = atual->prox;
            free(atual);
        }
    }
}

void bfs(Grafo* g, int inicio) {
    bool visitado[100] = {false};
    Fila q = {.frente = 0, .tras = 0};

    visitado[inicio] = true;
    q.itens[q.tras++] = inicio;

    printf("BFS (%d): ", inicio);
    while (q.frente < q.tras) {
        int v = q.itens[q.frente++];
        printf("%d ", v);

        No* temp = g->listasAdj[v];
        while (temp != NULL) {
            int adj = temp->destino;
            if (!visitado[adj]) {
                visitado[adj] = true;
                q.itens[q.tras++] = adj;
            }
            temp = temp->prox;
        }
    }
    printf("\n");
}

void dfsRecursivo(Grafo* g, int v, bool visitado[]) {
    visitado[v] = true;
    printf("%d ", v);

    No* temp = g->listasAdj[v];
    while (temp != NULL) {
        int adj = temp->destino;
        if (!visitado[adj]) {
            dfsRecursivo(g, adj, visitado);
        }
        temp = temp->prox;
    }
}

void dfs(Grafo* g, int inicio) {
    bool visitado[100] = {false};
    printf("DFS (%d): ", inicio);
    dfsRecursivo(g, inicio, visitado);
    printf("\n");
}

void destruirGrafo(Grafo* g) {
    if (!g) return;
    for (int i = 0; i < g->numVertices; i++) {
        No* atual = g->listasAdj[i];
        while (atual != NULL) {
            No* temp = atual;
            atual = atual->prox;
            free(temp);
        }
    }
    free(g->listasAdj);
    free(g);
}

int main() {
    Grafo* g = criarGrafo(5);

    adicionarAresta(g, 0, 1);
    adicionarAresta(g, 0, 2);
    adicionarAresta(g, 1, 3);
    adicionarAresta(g, 1, 4);
    adicionarAresta(g, 2, 4);

    bfs(g, 0);
    dfs(g, 0);

    removerAresta(g, 1, 4);
    printf("Apos remover aresta (1,4):\n");
    bfs(g, 0);

    destruirGrafo(g);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Vazamento de Memória ao Liberar o Grafo (`free` incompleto)**:
   * *Erro:* Chamar `free(g->listasAdj)` e `free(g)` sem percorrer cada lista encadeada individualmente.
   * *Consequência:* Os nós dinamicos do tipo `No` continuam alocados na Heap (Memory Leak).

2. **Esquecer de Marcar o Vértice como Visitado no Enfileiramento na BFS**:
   * *Erro:* Marcar `visitado[v] = true` apenas ao desenfileirar o vértice em vez de marcá-lo no momento da inserção na fila.
   * *Consequência:* O mesmo vértice é inserido múltiplas vezes na fila por caminhos diferentes, causando estouro da fila ou redundância $O(2^E)$.

3. **Loop Infinito em Grafos Não Direcionados**:
   * *Erro:* Omitir o vetor de controle de visitados `visited[]` nos algoritmos de percurso.
   * *Consequência:* Pela natureza bidirecional da aresta ($A \to B$ e $B \to A$), a DFS/BFS entra em recursão infinita e estoura a pilha (*Stack Overflow*).

---

## 4. Exercicio com Gabarito

**Enunciado:**
Escreva uma função em C chamada `bool existeCaminho(Grafo* g, int orig, int dest)` que retorna `true` se existir ao menos um caminho entre os vértices `orig` e `dest`, e `false` caso contrário. Utilize Busca em Profundidade (DFS).

**Gabarito:**

```c
bool auxExisteCaminho(Grafo* g, int v, int dest, bool visitado[]) {
    if (v == dest) return true;
    visitado[v] = true;

    No* temp = g->listasAdj[v];
    while (temp != NULL) {
        int adj = temp->destino;
        if (!visitado[adj]) {
            if (auxExisteCaminho(g, adj, dest, visitado)) {
                return true;
            }
        }
        temp = temp->prox;
    }
    return false;
}

bool existeCaminho(Grafo* g, int orig, int dest) {
    bool visitado[100] = {false};
    return auxExisteCaminho(g, orig, dest, visitado);
}
```