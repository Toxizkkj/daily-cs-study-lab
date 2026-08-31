# Arvores Binarias em C

## 1. Teoria e Complexidade

Uma Árvore Binária é uma estrutura de dados hierárquica não linear onde cada nó possui no máximo dois filhos, referenciados como esquerdo (`esq`) e direito (`dir`). A navegação baseia-se em recursão: a pré-ordem processa a raiz antes dos filhos (útil para cópia); a em-ordem processa a raiz entre os filhos (gera elementos ordenados em Árvores Binárias de Busca); e a pós-ordem processa a raiz após os filhos (essencial para desalocação de memória e cálculo de altura).

A altura de uma árvore é a maior distância entre a raiz e uma folha. Operações em árvores desbalanceadas podem degenerar para o desempenho de listas encadeadas.

| Operação | Caso Médio | Pior Caso | Complexidade de Espaço (Pilha) |
| :--- | :--- | :--- | :--- |
| Busca / Inserção | $O(\log N)$ | $O(N)$ | $O(h)$ onde $h$ é a altura |
| Percursos (Pré/Em/Pós) | $O(N)$ | $O(N)$ | $O(h)$ |
| Cálculo de Altura | $O(N)$ | $O(N)$ | $O(h)$ |
| Desalocação | $O(N)$ | $O(N)$ | $O(h)$ |

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
    No *novo = (No*) malloc(sizeof(No));
    novo->chave = chave;
    novo->esq = NULL;
    novo->dir = NULL;
    return novo;
}

No* inserir(No *raiz, int chave) {
    if (raiz == NULL) return criarNo(chave);
    if (chave < raiz->chave)
        raiz->esq = inserir(raiz->esq, chave);
    else if (chave > raiz->chave)
        raiz->dir = inserir(raiz->dir, chave);
    return raiz;
}

No* buscar(No *raiz, int chave) {
    if (raiz == NULL || raiz->chave == chave) return raiz;
    if (chave < raiz->chave) return buscar(raiz->esq, chave);
    return buscar(raiz->dir, chave);
}

int altura(No *raiz) {
    if (raiz == NULL) return -1;
    int altEsq = altura(raiz->esq);
    int altDir = altura(raiz->dir);
    return (altEsq > altDir ? altEsq : altDir) + 1;
}

void preOrdem(No *raiz) {
    if (raiz != NULL) {
        printf("%d ", raiz->chave);
        preOrdem(raiz->esq);
        preOrdem(raiz->dir);
    }
}

void emOrdem(No *raiz) {
    if (raiz != NULL) {
        emOrdem(raiz->esq);
        printf("%d ", raiz->chave);
        emOrdem(raiz->dir);
    }
}

void posOrdem(No *raiz) {
    if (raiz != NULL) {
        posOrdem(raiz->esq);
        posOrdem(raiz->dir);
        printf("%d ", raiz->chave);
    }
}

void destruirArvore(No *raiz) {
    if (raiz != NULL) {
        destruirArvore(raiz->esq);
        destruirArvore(raiz->dir);
        free(raiz);
    }
}

int main() {
    No *raiz = NULL;

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
    printf("\n");

    printf("Altura da arvore: %d\n", altura(raiz));

    No *busca = buscar(raiz, 40);
    printf("Busca pelo 40: %s\n", busca ? "Encontrado" : "Nao encontrado");

    destruirArvore(raiz);
    raiz = NULL;

    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Desalocação fora da Pós-Ordem (Segmentation Fault / Use-After-Free):** Executar `free(raiz)` antes de chamar a função para `raiz->esq` ou `raiz->dir` gera comportamento indefinido, pois o programa tentará ler ponteiros de uma memória já liberada.
2. **Esquecer o caso-base `NULL`:** Não verificar `if (raiz == NULL)` no início das funções recursivas resultará em *Segmentation Fault* imediato ao tentar acessar `raiz->esq` ou `raiz->dir` em um nó folha.
3. **Não reatribuir o ponteiro no retorno da inserção:** Fazer apenas `inserir(raiz->esq, chave)` sem atribuir `raiz->esq = inserir(...)` impede que os novos nós alocados sejam conectados à árvore original.

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função recursiva `int contarNos(No *raiz)` que receba o ponteiro para a raiz de uma árvore binária e retorne a quantidade total de nós presentes nela.

**Gabarito:**

```c
int contarNos(No *raiz) {
    if (raiz == NULL) {
        return 0;
    }
    return 1 + contarNos(raiz->esq) + contarNos(raiz->dir);
}
```

**Explicação:** O caso base retorna `0` quando o ponteiro é nulo. Caso contrário, a função soma `1` (o nó atual) ao resultado das chamadas recursivas para a subárvore esquerda e direita.