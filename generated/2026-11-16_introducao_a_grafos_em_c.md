# Introducao a Grafos em C

## 1. Teoria e Complexidade

Um grafo é uma estrutura de dados não linear composta por um conjunto de vértices (ou nós) $V$ e um conjunto de arestas $E$ que conectam esses vértices. A **Lista de Adjacência** representa o grafo como um vetor de listas encadeadas, onde o índice do vetor representa um vértice e os nós da lista contêm seus vizinhos diretos. É a representação mais eficiente em memória para grafos esparsos ($|E| \ll |V|^2$).

Os dois algoritmos fundamentais de exploração são:
* **BFS (Breadth-First Search / Busca em Largura):** Explora o grafo em níveis a partir de um nó inicial, utilizando uma estrutura de **Fila (FIFO)**. É ideal para encontrar o menor caminho em grafos não ponderados.
* **DFS (Depth-First Search / Busca em Profundidade):** Explora o máximo possível ao longo de cada ramo antes de fazer o *backtracking*, implementado naturalmente por **Recursão (Pilha de Chamadas)**.

| Operação / Algoritmo | Complexidade de Tempo | Complexidade de Espaço |
| :--- | :--- | :--- |
| Alocação do Grafo | $O(V)$ | $O(V + E)$ |
| Inserção de Aresta | $O(1)$ | $O(1)$ |
| Percurso BFS | $O(V + E)$ | $O(V)$ |
| Percurso DFS | $O(V + E)$ | $O(V)$ |

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
    int num_vertices;
    No** listas;
    int* visitado;
} Grafo;

typedef struct Fila {
    int itens[100];
    int frente;
    int tras;
} Fila;

Fila* criar_fila() {
    Fila* f = (Fila*)malloc(sizeof(Fila));
    f->frente = -1;
    f->tras = -1;
    return f;
}

int esta_vazia(Fila* f) {
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

No* criar_no(int v) {
    No* novo = (No*)malloc(sizeof(No));
    novo->vertice = v;
    novo->prox = NULL;
    return novo;
}

Grafo* criar_grafo(int vertices) {
    Grafo* g = (Grafo*)malloc(sizeof(Grafo));
    g->num_vertices = vertices;
    g->listas = (No**)malloc(vertices * sizeof(No*));
    g->visitado = (int*)malloc(vertices * sizeof(int));

    for (int i = 0; i < vertices; i++) {
        g->listas[i] = NULL;
        g->visitado[i] = 0;
    }
    return g;
}

void adicionar_aresta(Grafo* g, int src, int dest) {
    No* novo = criar_no(dest);
    novo->prox = g->listas[src];
    g->listas[src] = novo;

    novo = criar_no(src);
    novo->prox = g->listas[dest];
    g->listas[dest] = novo;
}

void resetar_visitados(Grafo* g) {
    for (int i = 0; i < g->num_vertices; i++) {
        g->visitado[i] = 0;
    }
}

void bfs(Grafo* g, int inicio) {
    resetar_visitados(g);
    Fila* f = criar_fila();

    g->visitado[inicio] = 1;
    enfileirar(f, inicio);

    printf("BFS a partir do vertice %d: ", inicio);
    while (!esta_vazia(f)) {
        int v_atual = desenfileirar(f);
        printf("%d ", v_atual);

        No* temp = g->listas[v_atual];
        while (temp) {
            int adj = temp->vertice;
            if (!g->visitado[adj]) {
                g->visitado[adj] = 1;
                enfileirar(f, adj);
            }
            temp = temp->prox;
        }
    }
    printf("\n");
    free(f);
}

void dfs_recursivo(Grafo* g, int v) {
    g->visitado[v] = 1;
    printf("%d ", v);

    No* temp = g->listas[v];
    while (temp) {
        int adj = temp->vertice;
        if (!g->visitado[adj]) {
            dfs_recursivo(g, adj);
        }
        temp = temp->prox;
    }
}

void dfs(Grafo* g, int inicio) {
    resetar_visitados(g);
    printf("DFS a partir do vertice %d: ", inicio);
    dfs_recursivo(g, inicio);
    printf("\n");
}

void liberar_grafo(Grafo* g) {
    for (int i = 0; i < g->num_vertices; i++) {
        No* temp = g->listas[i];
        while (temp) {
            No* aux = temp;
            temp = temp->prox;
            free(aux);
        }
    }
    free(g->listas);
    free(g->visitado);
    free(g);
}

int main() {
    Grafo* g = criar_grafo(5);

    adicionar_aresta(g, 0, 1);
    adicionar_aresta(g, 0, 2);
    adicionar_aresta(g, 1, 3);
    adicionar_aresta(g, 1, 4);

    bfs(g, 0);
    dfs(g, 0);

    liberar_grafo(g);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Vazamento de Memória na Desalocação (Memory Leak):** Liberar apenas o ponteiro principal `free(g)` ou o vetor `free(g->listas)` deixa todas as listas encadeadas de adjacência perdidas na memória heap. É obrigatório iterar sobre cada índice e dar `free` nó por nó.
2. **Reaproveitamento de Estado (`visitado` sujo):** Chamar BFS e logo em seguida DFS sem zerar o vetor `visitado` faz com que a segunda busca termine imediatamente ou ignore a maior parte do grafo, pois os vértices ainda constam como marcados.
3. **Estouro de Pilha no DFS Recursivo (Stack Overflow):** Em grafos muito profundos (ex: uma linha com $10^5$ vértices), a chamada recursiva do DFS consumirá toda a pilha do sistema. Em cenários de alta escala, o correto é usar um DFS iterativo com pilha manual no heap.

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função em C `int calcular_grau(Grafo* g, int v)` que receba um grafo e o índice de um vértice `v` e retorne o seu grau (número de conexões diretas).

**Gabarito:**

```c
int calcular_grau(Grafo* g, int v) {
    if (v < 0 || v >= g->num_vertices) {
        return -1; // Vertice invalido
    }
    
    int grau = 0;
    No* temp = g->listas[v];
    
    while (temp != NULL) {
        grau++;
        temp = temp->prox;
    }
    
    return grau;
}
```