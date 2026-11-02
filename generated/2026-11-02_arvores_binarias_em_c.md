# Arvores Binarias em C

## 1. Teoria e Complexidade

Uma **Árvore Binária** é uma estrutura de dados hierárquica e não linear. Cada elemento é denominado nó, contendo um valor (chave) e no máximo dois ponteiros para subárvores: `esq` (esquerda) e `dir` (direita). O nó inicial é a *raiz*. Se um nó não possui filhos, é chamado de *folha*.

Os percursos recursivos definem a ordem de visita aos nós: **Pré-ordem** (Raiz, Esquerda, Direita), **Em-ordem** (Esquerda, Raiz, Direita) e **Pós-ordem** (Esquerda, Direita, Raiz). A desalocação de memória **deve** obrigatoriamente ser feita em **Pós-ordem**, garantindo que os filhos sejam liberados da memória antes do pai, evitando o erro de acesso a memória já liberada (*use-after-free*).

| Operação | Caso Médio | Pior Caso | Espaço (Pilha) |
| :--- | :--- | :--- | :--- |
| Busca | $O(\log n)$ | $O(n)$ | $O(h)$ |
| Inserção | $O(\log n)$ | $O(n)$ | $O(h)$ |
| Remoção | $O(\log n)$ | $O(n)$ | $O(h)$ |
| Percurso | $O(n)$ | $O(n)$ | $O(h)$ |

*(Nota: $n$ é o número de nós e $h$ é a altura da árvore).*

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
    No* novo = (No*) malloc(sizeof(No));
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
    int hEsq = altura(raiz->esq);
    int hDir = altura(raiz->dir);
    return 1 + (hEsq > hDir ? hEsq : hDir);
}

void destruirArvore(No* raiz) {
    if (raiz != NULL) {
        destruirArvore(raiz->esq);
        destruirArvore(raiz->dir);
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

    printf("Pre-ordem: "); preOrdem(raiz); printf("\n");
    printf("Em-ordem: "); emOrdem(raiz); printf("\n");
    printf("Pos-ordem: "); posOrdem(raiz); printf("\n");

    printf("Altura da arvore: %d\n", altura(raiz));

    No* busca = buscar(raiz, 40);
    printf("Busca (40): %s\n", busca ? "Encontrado" : "Nao encontrado");

    destruirArvore(raiz);
    raiz = NULL;

    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Liberar o Nó em Pré-ordem (Segmentation Fault):** Chamar `free(raiz)` antes de chamar `destruirArvore(raiz->esq)` invalida o ponteiro `raiz`. O acesso subsequente a `raiz->esq` gera comportamento indefinido ou crash. A liberação **exige** Pós-ordem.
2. **Esquecer o Caso Base (`raiz == NULL`):** Tentar acessar `raiz->chave` ou `raiz->esq` sem verificar se `raiz` é nulo resulta em estouro de memória ou falha de segmentação ao atingir um nó folha.
3. **Perder o Retorno na Inserção:** Fazer apenas `inserir(raiz->esq, chave);` sem atribuir o retorno (`raiz->esq = inserir(...)`) impede que novos nós alocados sejam vinculados à árvore original.

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função em C chamada `int contarNos(No* raiz)` que calcule e retorne a quantidade total de nós presentes na árvore binária.

**Gabarito:**

```c
int contarNos(No* raiz) {
    if (raiz == NULL) return 0;
    return 1 + contarNos(raiz->esq) + contarNos(raiz->dir);
}
```

**Explicação:** O caso base retorna `0` quando a subárvore é vazia (`NULL`). No passo recursivo, a função soma `1` (o próprio nó atual) com a quantidade de nós retornada da subárvore esquerda e da subárvore direita.