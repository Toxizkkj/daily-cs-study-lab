# Arvores Binarias de Busca (BST) em C

## 1. Teoria e Complexidade

Uma Árvore Binária de Busca (BST) é uma estrutura hierárquica baseada em nós. A propriedade fundamental de ordenação estabelece que: para qualquer nó $N$, todos os elementos na subárvore esquerda possuem chaves estritamente menores que a chave de $N$, e todos os elementos na subárvore direita possuem chaves estritamente maiores.

Todas as operações principais (busca, inserção e remoção) percorrem um caminho da raiz até uma folha, tornando o custo proporcional à altura da árvore ($h$). Em árvores balanceadas, $h = O(\log n)$. No pior caso (inserção de elementos já ordenados), a árvore se degrada em uma lista encadeada onde $h = O(n)$.

| Operação | Caso Médio | Pior Caso | Espaço (Pilha de Recursão) |
| :--- | :--- | :--- | :--- |
| **Busca** | $O(\log n)$ | $O(n)$ | $O(h)$ |
| **Inserção** | $O(\log n)$ | $O(n)$ | $O(h)$ |
| **Remoção** | $O(\log n)$ | $O(n)$ | $O(h)$ |

---

## 2. Implementacao Completa em C

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct No {
    int chave;
    struct No *esq;
    struct No *dir;
} No;

No* criar_no(int chave) {
    No* novo = (No*)malloc(sizeof(No));
    novo->chave = chave;
    novo->esq = NULL;
    novo->dir = NULL;
    return novo;
}

No* inserir(No* raiz, int chave) {
    if (raiz == NULL) return criar_no(chave);
    if (chave < raiz->chave)
        raiz->esq = inserir(raiz->esq, chave);
    else if (chave > raiz->chave)
        raiz->dir = inserir(raiz->dir, chave);
    return raiz;
}

No* buscar(No* raiz, int chave) {
    if (raiz == NULL || raiz->chave == chave) return raiz;
    if (chave < raiz->chave) return buscar(raiz->esq, chave);
    return buscar(raiz->dir, chave);
}

No* menor_no(No* no) {
    No* atual = no;
    while (atual && atual->esq != NULL)
        atual = atual->esq;
    return atual;
}

No* remover(No* raiz, int chave) {
    if (raiz == NULL) return raiz;

    if (chave < raiz->chave)
        raiz->esq = remover(raiz->esq, chave);
    else if (chave > raiz->chave)
        raiz->dir = remover(raiz->dir, chave);
    else {
        // Caso 1: Folha (0 filhos) ou Caso 2: 1 filho
        if (raiz->esq == NULL) {
            No* temp = raiz->dir;
            free(raiz);
            return temp;
        } else if (raiz->dir == NULL) {
            No* temp = raiz->esq;
            free(raiz);
            return temp;
        }
        // Caso 3: 2 filhos -> Sucessor em-ordem (menor da subárvore direita)
        No* temp = menor_no(raiz->dir);
        raiz->chave = temp->chave;
        raiz->dir = remover(raiz->dir, temp->chave);
    }
    return raiz;
}

void em_ordem(No* raiz) {
    if (raiz != NULL) {
        em_ordem(raiz->esq);
        printf("%d ", raiz->chave);
        em_ordem(raiz->dir);
    }
}

void liberar(No* raiz) {
    if (raiz != NULL) {
        liberar(raiz->esq);
        liberar(raiz->dir);
        free(raiz);
    }
}

int main() {
    No* raiz = NULL;
    
    // Inserções
    raiz = inserir(raiz, 50);
    inserir(raiz, 30);
    inserir(raiz, 20);
    inserir(raiz, 40);
    inserir(raiz, 70);
    inserir(raiz, 60);
    inserir(raiz, 80);

    printf("Em-ordem: ");
    em_ordem(raiz);
    printf("\n");

    // Busca
    No* b = buscar(raiz, 40);
    printf("Busca 40: %s\n", b ? "Encontrado" : "Nao encontrado");

    // Remocao Caso 1: Folha (20)
    raiz = remover(raiz, 20);
    
    // Remocao Caso 2: 1 filho (30 tem apenas o 40)
    raiz = remover(raiz, 30);

    // Remocao Caso 3: 2 filhos (50 - raiz)
    raiz = remover(raiz, 50);

    printf("Pos-remocoes: ");
    em_ordem(raiz);
    printf("\n");

    liberar(raiz);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Esquecer de reatribuir o ponteiro retornado na remoção/inserção:**
   Fazer apenas `remover(raiz->esq, chave)` sem reatribuir `raiz->esq = remover(raiz->esq, chave)` gera ponteiros soltos (*dangling pointers*) ou falha na atualização dos nós pais quando subárvores mudam de lugar.

2. **Ordem de liberação de memória em desalocações:**
   Ao desalocar a árvore inteira, tentar fazer `free(raiz)` antes de chamar `liberar(raiz->esq)` e `liberar(raiz->dir)` resulta em *Segmentation Fault* ou *Memory Leak*, pois os ponteiros dos filhos deixam de ser acessíveis após o `free` do pai.

3. **Substituição incorreta no caso de 2 filhos:**
   Ao remover um nó com 2 filhos, copiar diretamente os ponteiros do sucessor em vez de apenas **copiar o valor do sucessor** e depois chamar a remoção recursiva na subárvore para apagar o nó duplicado real.

---

## 4. Exercicio com Gabarito

**Enunciado:**
Escreva uma função recursiva `int contar_folhas(No* raiz)` que receba o ponteiro para a raiz de uma BST e retorne a quantidade total de nós folha (nós que não possuem filhos).

**Gabarito:**

```c
int contar_folhas(No* raiz) {
    if (raiz == NULL) 
        return 0;
    
    // É folha se não tem filho esquerdo nem direito
    if (raiz->esq == NULL && raiz->dir == NULL) 
        return 1;
        
    return contar_folhas(raiz->esq) + contar_folhas(raiz->dir);
}
```