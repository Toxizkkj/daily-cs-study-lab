# Arvores Binarias em C

## 1. Teoria e Complexidade

Uma Árvore Binária é uma estrutura de dados hierárquica e não linear constituída por nós. Cada nó contém um valor e no máximo dois ponteiros de referência: o filho esquerdo (`esq`) e o filho direito (`dir`). O nó base da hierarquia é chamado de *raiz*, e os nós sem filhos são chamados de *folhas*.

Os percursos determinam a ordem de visita aos nós: **Pré-ordem** (Raiz, Esquerda, Direita), **Em-ordem** (Esquerda, Raiz, Direita) e **Pós-ordem** (Esquerda, Direita, Raiz). A desalocação de memória deve obrigatoriamente usar a **Pós-ordem**, garantindo que os filhos sejam destruídos antes do pai.

| Operação | Tempo (Médio) | Tempo (Pior Caso) | Espaço Auxiliar |
| :--- | :--- | :--- | :--- |
| **Busca / Inserção (BST)** | $O(\log n)$ | $O(n)$ | $O(h)$ |
| **Percursos (Pré/Em/Pós)** | $O(n)$ | $O(n)$ | $O(h)$ |
| **Cálculo de Altura** | $O(n)$ | $O(n)$ | $O(h)$ |
| **Desalocação Completa** | $O(n)$ | $O(n)$ | $O(h)$ |

*(Onde $n$ é o número de nós e $h$ é a altura da árvore. O espaço auxiliar deve-se à pilha da recursão).*

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

No* criarNo(int chave) {
    No* novo = (No*)malloc(sizeof(No));
    novo->chave = chave;
    novo->esq = NULL;
    novo->dir = NULL;
    return novo;
}

No* inserir(No* raiz, int chave) {
    if (raiz == NULL) return criarNo(chave);
    if (chave < raiz->chave)
        raiz->esq = inserir(raiz->esq, chave);
    else if (chave > raiz->chave)
        raiz->dir = inserir(raiz->dir, chave);
    return raiz;
}

void preOrdem(No* raiz) {
    if (raiz != NULL) {
        printf("%d ", raiz->chave);
        preOrdem(raiz->esq);
        preOrdem(raiz->dir);
    }
}

void emOrdem(No* raiz) {
    if (raiz != NULL) {
        emOrdem(raiz->esq);
        printf("%d ", raiz->chave);
        emOrdem(raiz->dir);
    }
}

void posOrdem(No* raiz) {
    if (raiz != NULL) {
        posOrdem(raiz->esq);
        posOrdem(raiz->dir);
        printf("%d ", raiz->chave);
    }
}

int altura(No* raiz) {
    if (raiz == NULL) return -1;
    int altEsq = altura(raiz->esq);
    int altDir = altura(raiz->dir);
    return 1 + (altEsq > altDir ? altEsq : altDir);
}

void liberarArvore(No* raiz) {
    if (raiz != NULL) {
        liberarArvore(raiz->esq);
        liberarArvore(raiz->dir);
        free(raiz);
    }
}

int main() {
    No* raiz = NULL;

    raiz = inserir(raiz, 50);
    inserir(raiz, 30);
    inserir(raiz, 70);
    inserir(raiz, 20);
    inserir(raiz, 40);

    printf("Pre-ordem: ");
    preOrdem(raiz);
    printf("\nEm-ordem: ");
    emOrdem(raiz);
    printf("\nPos-ordem: ");
    posOrdem(raiz);

    printf("\nAltura da arvore: %d\n", altura(raiz));

    liberarArvore(raiz);
    raiz = NULL;

    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Liberar a memória em Pré-ordem**: Fazer `free(raiz)` antes de chamar a recursão para os filhos causa *Use-After-Free* ou *Segmentation Fault*, pois acessa endereços já desalocados (`raiz->esq` e `raiz->dir`). A liberação correta é sempre em **Pós-ordem**.
2. **Esquecer o caso base em funções recursivas**: Não checar `if (raiz == NULL)` no início das funções gera recursão infinita e *Stack Overflow*.
3. **Convenção de altura (Nó vs. Aresta)**: Se a questão considerar a altura em **número de arestas**, o nó `NULL` deve retornar `-1`. Se considerar **número de nós**, o `NULL` deve retornar `0`. Atente-se ao enunciado.

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função recursiva em C com a assinatura `int contarFolhas(No* raiz)` que retorne a quantidade de nós folha existentes em uma árvore binária.

**Gabarito:**

```c
int contarFolhas(No* raiz) {
    if (raiz == NULL) {
        return 0;
    }
    if (raiz->esq == NULL && raiz->dir == NULL) {
        return 1;
    }
    return contarFolhas(raiz->esq) + contarFolhas(raiz->dir);
}
```

**Explicação:** 
- **Caso base 1:** Se a árvore/subárvore estiver vazia (`NULL`), retorna `0`.
- **Caso base 2:** Se o nó atual não possui filho esquerdo nem direito (`esq == NULL && dir == NULL`), ele é um nó folha; retorna `1`.
- **Passo recursivo:** Se for um nó interno, soma o total de folhas encontradas na subárvore esquerda com o total da subárvore direita.