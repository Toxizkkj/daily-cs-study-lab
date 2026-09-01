# Arvores Binarias em C

## 1. Teoria e Complexidade

Uma Árvore Binária é uma estrutura hierárquica na qual cada nó possui no máximo dois filhos, chamados de ponteiro esquerdo (`esq`) e ponteiro direito (`dir`). As árvores de busca binária (BST - *Binary Search Tree*) mantêm a propriedade de ordenação: elementos menores que o nó pai ficam à esquerda, e elementos maiores ficam à direita.

Os percursos definem a ordem de visitação dos nós:
- **Pré-ordem (Raiz, Esq, Dir):** Útil para clonar/copiar a árvore.
- **Em-ordem (Esq, Raiz, Dir):** Visita os nós em ordem crescente (em BST).
- **Pós-ordem (Esq, Dir, Raiz):** Útil para desalocação de memória e cálculo de altura.

| Operação | Caso Médio | Pior Caso | Espaço (Pilha Recursiva) |
| :--- | :--- | :--- | :--- |
| Busca / Inserção / Remoção | $O(\log n)$ | $O(n)$ | $O(h)$ |
| Percursos (Pré/Em/Pós) | $O(n)$ | $O(n)$ | $O(h)$ |
| Cálculo de Altura | $O(n)$ | $O(n)$ | $O(h)$ |

*(Nota: $h$ é a altura da árvore. No pior caso de uma árvore desbalanceada, $h = n$).*

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
    if (chave < raiz->chave) raiz->esq = inserir(raiz->esq, chave);
    else if (chave > raiz->chave) raiz->dir = inserir(raiz->dir, chave);
    return raiz;
}

No* buscar(No* raiz, int chave) {
    if (raiz == NULL || raiz->chave == chave) return raiz;
    if (chave < raiz->chave) return buscar(raiz->esq, chave);
    return buscar(raiz->dir, chave);
}

No* menorNo(No* raiz) {
    No* atual = raiz;
    while (atual && atual->esq != NULL) atual = atual->esq;
    return atual;
}

No* remover(No* raiz, int chave) {
    if (raiz == NULL) return NULL;
    if (chave < raiz->chave) raiz->esq = remover(raiz->esq, chave);
    else if (chave > raiz->chave) raiz->dir = remover(raiz->dir, chave);
    else {
        if (raiz->esq == NULL) {
            No* temp = raiz->dir;
            free(raiz);
            return temp;
        } else if (raiz->dir == NULL) {
            No* temp = raiz->esq;
            free(raiz);
            return temp;
        }
        No* temp = menorNo(raiz->dir);
        raiz->chave = temp->chave;
        raiz->dir = remover(raiz->dir, temp->chave);
    }
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
    raiz = inserir(raiz, 30);
    raiz = inserir(raiz, 70);
    raiz = inserir(raiz, 20);
    raiz = inserir(raiz, 40);

    printf("Pre-ordem: "); preOrdem(raiz); printf("\n");
    printf("Em-ordem:  "); emOrdem(raiz); printf("\n");
    printf("Pos-ordem: "); posOrdem(raiz); printf("\n");

    printf("Altura da arvore: %d\n", altura(raiz));

    No* buscado = buscar(raiz, 30);
    printf("Busca 30: %s\n", buscado ? "Encontrado" : "Nao encontrado");

    raiz = remover(raiz, 30);
    printf("Em-ordem apos remover 30: "); emOrdem(raiz); printf("\n");

    liberarArvore(raiz);
    raiz = NULL;

    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Desalocação fora do percurso Pós-ordem (Use-After-Free / Segfault):**
   Liberar a memória (`free(raiz)`) antes de percorrer os filhos esquerdos e direitos resulta em comportamento indefinido, pois você tenta acessar subponteiros (`raiz->esq`) de uma região de memória já liberada. A liberação **deve** ser em pós-ordem.

2. **Perda de referência da Raiz na Inserção:**
   Passar o ponteiro por valor (`No* raiz`) sem retornar o novo ponteiro atualizado faz com que a atribuição na `main` não persista (a raiz continua `NULL`). Deve-se retornar o ponteiro atualizado ou usar ponteiro duplo (`No** raiz`).

3. **Cálculo da Altura (Convenção de Base):**
   Retornar `0` para `raiz == NULL` calcula a altura com base no *número de nós* do maior caminho. Retornar `-1` calcula a altura com base no *número de arestas* (convenção clássica da ciência da computação). Fique atento à exigência da questão.

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função recursiva `int contarFolhas(No* raiz)` em C que receba o ponteiro para a raiz de uma árvore binária e retorne a quantidade total de nós folha (nós que não possuem filho esquerdo nem filho direito).

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

*Explicação:* Se o nó for `NULL`, retorna 0 (caso base). Se ambos os filhos forem `NULL`, o nó atual é uma folha e retorna 1. Caso contrário, soma recursivamente as folhas da subárvore esquerda e da subárvore direita.