# Arvores Binarias em C

## 1. Teoria e Complexidade

Uma árvore binária é uma estrutura de dados hierárquica e não linear composta por nós, onde cada nó contém um valor (chave) e no máximo dois ponteiros para seus filhos: esquerdo (`esq`) e direito (`dir`). O nó raiz é o ponto de entrada da árvore, e nós sem filhos são chamados de folhas. 

A navegação e o processamento dos dados ocorrem via recursão através de percursos: **Pré-ordem** (Visita Nó -> Esquerda -> Direita), **Em-ordem** (Esquerda -> Visita Nó -> Direita) e **Pós-ordem** (Esquerda -> Direita -> Visita Nó). O percurso em pós-ordem é essencial para a desalocação de memória, pois garante que os filhos sejam liberados antes do nó pai.

| Operação | Caso Médio | Pior Caso | Espaço (Pilha Recursiva) |
| :--- | :--- | :--- | :--- |
| Inserção / Busca (Árvore de Busca) | $O(\log n)$ | $O(n)$ | $O(h)$ |
| Percursos (Pré, Em, Pós-ordem) | $O(n)$ | $O(n)$ | $O(h)$ |
| Cálculo de Altura | $O(n)$ | $O(n)$ | $O(h)$ |
| Desalocação | $O(n)$ | $O(n)$ | $O(h)$ |

*(Onde $n$ é o número de nós e $h$ é a altura da árvore).*

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
    int hEsq = altura(raiz->esq);
    int hDir = altura(raiz->dir);
    return (hEsq > hDir ? hEsq : hDir) + 1;
}

No* buscar(No* raiz, int chave) {
    if (raiz == NULL || raiz->chave == chave) return raiz;
    if (chave < raiz->chave) return buscar(raiz->esq, chave);
    return buscar(raiz->dir, chave);
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

    printf("Pre-ordem: "); preOrdem(raiz); printf("\n");
    printf("Em-ordem:  "); emOrdem(raiz); printf("\n");
    printf("Pos-ordem: "); posOrdem(raiz); printf("\n");

    printf("Altura da arvore: %d\n", altura(raiz));

    No* encontrado = buscar(raiz, 30);
    printf("Busca (30): %s\n", encontrado ? "Encontrado" : "Nao encontrado");

    liberarArvore(raiz);
    raiz = NULL;

    return 0;
}
```

## 3. Pegadinhas de Prova

1. **Liberação Precoce de Memória (Memory Leak/Segfault):** Tentar fazer `free(raiz)` antes de chamar a função de liberação para `raiz->esq` e `raiz->dir`. Ao dar `free` primeiro, o acesso aos ponteiros dos filhos gera um comportamento indefinido ou *Segmentation Fault*. A liberação **deve** usar a ordem Pós-Ordem.
2. **Esquecer o Caso Base em Recursão:** Não testar `if (raiz == NULL)` no início de funções de travessia ou cálculo de altura. Acessar `raiz->esq` em um ponteiro nulo causará *Segmentation Fault* imediatamente.
3. **Ponteiro Solto (Dangling Pointer) após a Liberação:** Chamar `liberarArvore(raiz)` desaloca a memória, mas a variável local `raiz` na função chamadora continuará apontando para o endereço antigo. Deve-se explicitamente atribuir `raiz = NULL;` após a liberação.

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função recursiva em C com a assinatura `int contarNos(No* raiz)` que receba o ponteiro para a raiz de uma árvore binária e retorne a quantidade total de nós presentes na árvore.

**Gabarito:**

```c
int contarNos(No* raiz) {
    if (raiz == NULL) {
        return 0;
    }
    return 1 + contarNos(raiz->esq) + contarNos(raiz->dir);
}
```

*Explicação:* O caso base retorna `0` quando o nó for `NULL`. Caso contrário, a função conta `1` (o próprio nó atual) e soma recursivamente com o total de nós da subárvore esquerda e da subárvore direita.