# Arvores Binarias em C

## 1. Teoria e Complexidade

Uma árvore binária é uma estrutura de dados hierárquica não linear composta por nós, onde cada nó contém um valor e ponteiros para no máximo dois filhos: esquerdo (`esq`) e direito (`dir`). O primeiro nó é a **raiz**. Nos sem filhos são chamados de **folhas**. Em Árvores Binárias de Busca (BST), a propriedade fundamental é que todos os nós à esquerda de um nó pai possuem valores menores que ele, e os nós à direita possuem valores maiores.

A navegação na árvore é feita recursivamente. Os percursos definem a ordem de visitação dos nós: **Pré-ordem** (Raiz, Esquerda, Direita), **Em-ordem** (Esquerda, Raiz, Direita - resulta nos dados ordenados em uma BST) e **Pós-ordem** (Esquerda, Direita, Raiz - essencial para liberação de memória). A **altura** de um nó é o maior número de arestas até uma folha.

| Operação | Tempo (Médio) | Tempo (Pior Caso) | Espaço (Recursão Pior Caso) |
| :--- | :--- | :--- | :--- |
| Busca | $O(\log n)$ | $O(n)$ | $O(n)$ |
| Inserção | $O(\log n)$ | $O(n)$ | $O(n)$ |
| Altura | $O(n)$ | $O(n)$ | $O(n)$ |
| Percursos | $O(n)$ | $O(n)$ | $O(n)$ |

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

No* criar_no(int valor) {
    No* novo = (No*) malloc(sizeof(No));
    if (novo == NULL) exit(1);
    novo->chave = valor;
    novo->esq = NULL;
    novo->dir = NULL;
    return novo;
}

No* inserir(No* raiz, int valor) {
    if (raiz == NULL) return criar_no(valor);
    if (valor < raiz->chave) {
        raiz->esq = inserir(raiz->esq, valor);
    } else if (valor > raiz->chave) {
        raiz->dir = inserir(raiz->dir, valor);
    }
    return raiz;
}

No* buscar(No* raiz, int valor) {
    if (raiz == NULL || raiz->chave == valor) return raiz;
    if (valor < raiz->chave) return buscar(raiz->esq, valor);
    return buscar(raiz->dir, valor);
}

int max(int a, int b) {
    return (a > b) ? a : b;
}

int altura(No* raiz) {
    if (raiz == NULL) return -1; // Altura por arestas (árvore com 1 nó tem altura 0)
    return 1 + max(altura(raiz->esq), altura(raiz->dir));
}

void pre_ordem(No* raiz) {
    if (raiz != NULL) {
        printf("%d ", raiz->chave);
        pre_ordem(raiz->esq);
        pre_ordem(raiz->dir);
    }
}

void em_ordem(No* raiz) {
    if (raiz != NULL) {
        em_ordem(raiz->esq);
        printf("%d ", raiz->chave);
        em_ordem(raiz->dir);
    }
}

void pos_ordem(No* raiz) {
    if (raiz != NULL) {
        pos_ordem(raiz->esq);
        pos_ordem(raiz->dir);
        printf("%d ", raiz->chave);
    }
}

void destruir_arvore(No* raiz) {
    if (raiz != NULL) {
        destruir_arvore(raiz->esq);
        destruir_arvore(raiz->dir);
        free(raiz);
    }
}

int main() {
    No* raiz = NULL;

    // Inserção de dados
    raiz = inserir(raiz, 50);
    raiz = inserir(raiz, 30);
    raiz = inserir(raiz, 70);
    raiz = inserir(raiz, 20);
    raiz = inserir(raiz, 40);

    printf("Pre-ordem: ");
    pre_ordem(raiz);
    printf("\n");

    printf("Em-ordem: ");
    em_ordem(raiz);
    printf("\n");

    printf("Pos-ordem: ");
    pos_ordem(raiz);
    printf("\n");

    printf("Altura da arvore: %d\n", altura(raiz));

    int valor_busca = 30;
    No* encontrado = buscar(raiz, valor_busca);
    if (encontrado != NULL) {
        printf("Valor %d encontrado na arvore.\n", valor_busca);
    } else {
        printf("Valor %d nao encontrado.\n", valor_busca);
    }

    // Desalocação completa
    destruir_arvore(raiz);
    raiz = NULL;

    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Dereferenciação de Ponteiro Nulo (`Segmentation Fault`)**:
   Tentar acessar `raiz->esq` sem verificar previamente se `raiz == NULL`. A checagem do caso base (`if (raiz == NULL)`) **deve sempre vir em primeiro lugar** na recursão.

2. **Ordem Incorreta na Desalocação (`Use-After-Free` / `Memory Leak`)**:
   Liberar a memória da raiz com `free(raiz)` antes de visitar as subárvores filhas. Se a raiz for liberada primeiro, os ponteiros `raiz->esq` e `raiz->dir` tornam-se inválidos (dangling pointers), tornando impossível desalocar os filhos com segurança. **A liberação DEVE usar Pós-ordem**.

3. **Cálculo da Altura (Convenção Nula vs. Folha)**:
   Retornar `0` para `raiz == NULL` altera a definição da altura. Retornar `0` no nó nulo define altura por quantidade de nós. Retornar `-1` define a altura pelo número de **arestas**. Atente-se ao enunciado da prova para saber qual convenção é exigida.

---

## 4. Exercicio com Gabarito

**Enunciado**: Escreva uma função recursiva em C chamada `contar_folhas` que receba o ponteiro para a raiz de uma árvore binária e retorne a quantidade total de nós folha presentes na árvore.

**Gabarito**:

```c
int contar_folhas(No* raiz) {
    // Caso base 1: Árvore vazia
    if (raiz == NULL) return 0;
    
    // Caso base 2: Nó atual é uma folha
    if (raiz->esq == NULL && raiz->dir == NULL) return 1;
    
    // Passo recursivo: Soma das folhas da subárvore esquerda e direita
    return contar_folhas(raiz->esq) + contar_folhas(raiz->dir);
}
```

**Explicação**: Se o nó for `NULL`, ele contribui com `0`. Se não tiver filhos à esquerda nem à direita, é uma folha e retorna `1`. Caso contrário, a função delega a contagem recursivamente para o filho esquerdo e direito, somando os resultados.