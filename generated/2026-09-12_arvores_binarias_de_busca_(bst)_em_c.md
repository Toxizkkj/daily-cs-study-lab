# Arvores Binarias de Busca (BST) em C

## 1. Teoria e Complexidade

Uma Árvore Binária de Busca (BST) é uma estrutura de dados hierárquica baseada em nós. Ela segue estritamente a **propriedade de ordenação**: para qualquer nó $N$, todas as chaves na subárvore à sua esquerda são estritamente menores que a chave de $N$, e todas as chaves na subárvore à sua direita são estritamente maiores. Isso permite a execução de busca binária diretamente sobre a estrutura encadeada.

A eficiência das operações de busca, inserção e remoção depende diretamente da altura $h$ da árvore. Em uma árvore balanceada, a altura é $h = O(\log n)$. No pior caso, quando os elementos são inseridos em ordem crescente ou decrescente, a árvore degenera em uma lista encadeada, resultando em $h = O(n)$.

| Operação | Caso Médio | Pior Caso | Complexidade de Espaço |
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

No* buscar(No* raiz, int chave) {
    if (raiz == NULL || raiz->chave == chave) return raiz;
    if (chave < raiz->chave) return buscar(raiz->esq, chave);
    return buscar(raiz->dir, chave);
}

No* menorNo(No* raiz) {
    No* atual = raiz;
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
        // Caso 1: Sem filhos ou Caso 2: Apenas 1 filho (direita)
        if (raiz->esq == NULL) {
            No* temp = raiz->dir;
            free(raiz);
            return temp;
        }
        // Caso 2: Apenas 1 filho (esquerda)
        else if (raiz->dir == NULL) {
            No* temp = raiz->esq;
            free(raiz);
            return temp;
        }
        // Caso 3: 2 filhos (substitui pelo menor nó da subárvore direita / sucessor)
        No* temp = menorNo(raiz->dir);
        raiz->chave = temp->chave;
        raiz->dir = remover(raiz->dir, temp->chave);
    }
    return raiz;
}

void liberar(No* raiz) {
    if (raiz != NULL) {
        liberar(raiz->esq);
        liberar(raiz->dir);
        free(raiz);
    }
}

void emOrdem(No* raiz) {
    if (raiz != NULL) {
        emOrdem(raiz->esq);
        printf("%d ", raiz->chave);
        emOrdem(raiz->dir);
    }
}

int main() {
    No* raiz = NULL;
    raiz = inserir(raiz, 50);
    raiz = inserir(raiz, 30);
    raiz = inserir(raiz, 20);
    raiz = inserir(raiz, 40);
    raiz = inserir(raiz, 70);
    raiz = inserir(raiz, 60);
    raiz = inserir(raiz, 80);

    printf("Impressao em-ordem: ");
    emOrdem(raiz);
    printf("\n");

    printf("Buscando 40: %s\n", buscar(raiz, 40) ? "Encontrado" : "Nao encontrado");

    raiz = remover(raiz, 20); // Caso 1: Folha
    raiz = remover(raiz, 30); // Caso 2: 1 filho
    raiz = remover(raiz, 50); // Caso 3: 2 filhos

    printf("Apos remocoes (20, 30, 50): ");
    emOrdem(raiz);
    printf("\n");

    liberar(raiz);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Perda de ponteiro na remoção de 2 filhos**: Ao remover um nó com dois filhos, copiar o valor do sucessor não basta; é obrigatório chamar a remoção recursiva na subárvore correta (`raiz->dir = remover(raiz->dir, temp->chave)`). Caso contrário, o nó sucessor original ficará duplicado na árvore.
2. **Esquecer de atualizar os ponteiros pai**: Em chamadas recursivas como `raiz->esq = inserir(raiz->esq, chave)`, esquecer a atribuição `raiz->esq = ...` quebra a ligação dos nós atualizados com a árvore.
3. **Desreferenciar ponteiros NULL durante a busca**: Tentar acessar `raiz->chave` antes de validar se `raiz == NULL` causa *Segmentation Fault*. A verificação de base deve vir sempre primeiro na condição.

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função recursiva em C com a assinatura `int contarFolhas(No* raiz)` que retorne o número total de nós folha (nós sem filhos à esquerda nem à direita) em uma BST.

**Gabarito:**

```c
int contarFolhas(No* raiz) {
    if (raiz == NULL) 
        return 0;
    if (raiz->esq == NULL && raiz->dir == NULL) 
        return 1;
    return contarFolhas(raiz->esq) + contarFolhas(raiz->dir);
}
```