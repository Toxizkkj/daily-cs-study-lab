# Arvores AVL em C

## 1. Teoria e Complexidade

Uma Árvore AVL é uma Árvore Binária de Busca (BST) autobalanceada. Para cada nó da árvore, a diferença entre a altura da subárvore esquerda e a altura da subárvore direita — chamada de **Fator de Balanceamento (FB)** — deve ser estritamente igual a **-1, 0 ou 1** ($FB = h_{esq} - h_{dir}$). Caso o módulo do FB seja maior que 1 após uma inserção ou remoção, a árvore aplica rotações para reestabelecer o equilíbrio.

As rotações mantêm a propriedade de busca e reorganizam os ponteiros em tempo constante $O(1)$. Existem quatro tipos de rebalanceamento: **Rotação Simples à Direita (LL)**, **Rotação Simples à Esquerda (RR)**, **Rotação Dupla à Direita (LR)** e **Rotação Dupla à Esquerda (RL)**. Garantindo que a altura $h$ permaneça $O(\log n)$, a árvore previne a degradação para uma lista encadeada no pior caso.

| Operação | Caso Médio | Pior Caso | Espaço |
| :--- | :--- | :--- | :--- |
| Busca | $O(\log n)$ | $O(\log n)$ | $O(n)$ |
| Inserção | $O(\log n)$ | $O(\log n)$ | $O(n)$ |
| Remoção | $O(\log n)$ | $O(\log n)$ | $O(n)$ |

---

## 2. Implementacao Completa em C

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct No {
    int chave;
    int altura;
    struct No *esq;
    struct No *dir;
} No;

int altura(No *n) {
    return n ? n->altura : 0;
}

int max(int a, int b) {
    return (a > b) ? a : b;
}

int obterFB(No *n) {
    return n ? altura(n->esq) - altura(n->dir) : 0;
}

No* criarNo(int chave) {
    No *no = (No*)malloc(sizeof(No));
    no->chave = chave;
    no->altura = 1;
    no->esq = NULL;
    no->dir = NULL;
    return no;
}

No* rotDireita(No *y) {
    No *x = y->esq;
    No *T2 = x->dir;

    x->dir = y;
    y->esq = T2;

    y->altura = max(altura(y->esq), altura(y->dir)) + 1;
    x->altura = max(altura(x->esq), altura(x->dir)) + 1;

    return x;
}

No* rotEsquerda(No *x) {
    No *y = x->dir;
    No *T2 = y->esq;

    y->esq = x;
    x->dir = T2;

    x->altura = max(altura(x->esq), altura(x->dir)) + 1;
    y->altura = max(altura(y->esq), altura(y->dir)) + 1;

    return y;
}

No* rebalancear(No *no) {
    no->altura = 1 + max(altura(no->esq), altura(no->dir));
    int fb = obterFB(no);

    // Caso LL
    if (fb > 1 && obterFB(no->esq) >= 0)
        return rotDireita(no);

    // Caso LR
    if (fb > 1 && obterFB(no->esq) < 0) {
        no->esq = rotEsquerda(no->esq);
        return rotDireita(no);
    }

    // Caso RR
    if (fb < -1 && obterFB(no->dir) <= 0)
        return rotEsquerda(no);

    // Caso RL
    if (fb < -1 && obterFB(no->dir) > 0) {
        no->dir = rotDireita(no->dir);
        return rotEsquerda(no);
    }

    return no;
}

No* inserir(No *no, int chave) {
    if (!no) return criarNo(chave);

    if (chave < no->chave)
        no->esq = inserir(no->esq, chave);
    else if (chave > no->chave)
        no->dir = inserir(no->dir, chave);
    else
        return no; // Chaves duplicadas não são permitidas

    return rebalancear(no);
}

No* menorValorNo(No *no) {
    No *atual = no;
    while (atual->esq != NULL)
        atual = atual->esq;
    return atual;
}

No* remover(No *raiz, int chave) {
    if (!raiz) return raiz;

    if (chave < raiz->chave)
        raiz->esq = remover(raiz->esq, chave);
    else if (chave > raiz->chave)
        raiz->dir = remover(raiz->dir, chave);
    else {
        if (!raiz->esq || !raiz->dir) {
            No *temp = raiz->esq ? raiz->esq : raiz->dir;
            if (!temp) {
                temp = raiz;
                raiz = NULL;
            } else {
                *raiz = *temp;
            }
            free(temp);
        } else {
            No *temp = menorValorNo(raiz->dir);
            raiz->chave = temp->chave;
            raiz->dir = remover(raiz->dir, temp->chave);
        }
    }

    if (!raiz) return raiz;

    return rebalancear(raiz);
}

No* buscar(No *raiz, int chave) {
    if (!raiz || raiz->chave == chave)
        return raiz;
    if (chave < raiz->chave)
        return buscar(raiz->esq, chave);
    return buscar(raiz->dir, chave);
}

void liberarArvore(No *raiz) {
    if (raiz) {
        liberarArvore(raiz->esq);
        liberarArvore(raiz->dir);
        free(raiz);
    }
}

void emOrdem(No *raiz) {
    if (raiz) {
        emOrdem(raiz->esq);
        printf("%d (FB: %d) ", raiz->chave, obterFB(raiz));
        emOrdem(raiz->dir);
    }
}

int main() {
    No *raiz = NULL;

    raiz = inserir(raiz, 10);
    raiz = inserir(raiz, 20);
    raiz = inserir(raiz, 30); // Provoca rotação RR
    raiz = inserir(raiz, 40);
    raiz = inserir(raiz, 50); // Provoca rotação RR
    raiz = inserir(raiz, 25); // Provoca rotação RL

    printf("Em-Ordem apos insercoes:\n");
    emOrdem(raiz);
    printf("\n");

    printf("Busca do 25: %s\n", buscar(raiz, 25) ? "Encontrado" : "Nao encontrado");

    raiz = remover(raiz, 30);
    printf("Em-Ordem apos remover 30:\n");
    emOrdem(raiz);
    printf("\n");

    liberarArvore(raiz);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Acessar ponteiros nulos no cálculo de altura:** Tentar acessar `no->esq->altura` diretamente quando `esq` é `NULL` resulta em **Segmentation Fault**. É obrigatório utilizar uma função auxiliar (`altura(No*)`) que trate `NULL` retornando `0`.
2. **Atualização incorreta da ordem das alturas nas rotações:** Na rotação, a altura do nó filho que sobe deve ser recalculada **depois** da altura do nó pai que desce. Inverter essa ordem corrompe a propriedade de balanceamento da árvore.
3. **Perda de ponteiros e Memory Leak na remoção:** Ao remover um nó com dois filhos substituindo-o pelo menor nó da subárvore direita, esquecer de encadear o retorno de `remover(raiz->dir, temp->chave)` de volta em `raiz->dir` desconecta a subárvore e causa vazamento de memória.

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função recursiva em C `int ehAVL(No *raiz)` que retorna `1` se uma dada árvore atende a todas as regras de uma Árvore AVL (módulo do FB $\le 1$ para todos os nós) ou `0` caso contrário.

**Gabarito:**

```c
int ehAVL(No *raiz) {
    if (!raiz) return 1;

    int fb = obterFB(raiz);
    if (fb < -1 || fb > 1)
        return 0;

    return ehAVL(raiz->esq) && ehAVL(raiz->dir);
}
```