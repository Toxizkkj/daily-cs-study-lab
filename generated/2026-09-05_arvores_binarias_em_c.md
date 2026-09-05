# Arvores Binarias em C

## 1. Teoria e Complexidade

Uma Árvore Binária é uma estrutura de dados hierárquica não linear onde cada elemento (chamado de nó) possui no máximo dois filhos: o filho esquerdo e o filho direito. O primeiro nó é a raiz. Quando organizada de forma que valores menores fiquem à esquerda e maiores à direita, temos uma Árvore Binária de Busca (BST).

Os percursos determinam a ordem de visita aos nós:
- **Pré-ordem (Nó, Esquerda, Direita):** Processa a raiz antes dos filhos. Útil para clonar árvores.
- **Em-ordem (Esquerda, Nó, Direita):** Visita os nós em ordem crescente (em BSTs).
- **Pós-ordem (Esquerda, Direita, Nó):** Processa os filhos antes da raiz. Usado para desalocação de memória e cálculo de altura.

| Operação | Tempo (Médio) | Tempo (Pior Caso) | Espaço (Pior Caso) |
| :--- | :--- | :--- | :--- |
| Busca | $O(\log n)$ | $O(n)$ | $O(h)$ |
| Inserção | $O(\log n)$ | $O(n)$ | $O(h)$ |
| Remoção | $O(\log n)$ | $O(n)$ | $O(h)$ |
| Percursos | $O(n)$ | $O(n)$ | $O(h)$ |

*Nota: $n$ é o número de nós e $h$ é a altura da árvore. O pior caso ocorre quando a árvore se degenera em uma lista encadeada.*

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

No* criarNo(int valor) {
    No* novo = (No*)malloc(sizeof(No));
    novo->chave = valor;
    novo->esq = NULL;
    novo->dir = NULL;
    return novo;
}

No* inserir(No* raiz, int valor) {
    if (raiz == NULL) return criarNo(valor);
    if (valor < raiz->chave)
        raiz->esq = inserir(raiz->esq, valor);
    else if (valor > raiz->chave)
        raiz->dir = inserir(raiz->dir, valor);
    return raiz;
}

No* buscar(No* raiz, int valor) {
    if (raiz == NULL || raiz->chave == valor) return raiz;
    if (valor < raiz->chave) return buscar(raiz->esq, valor);
    return buscar(raiz->dir, valor);
}

No* menorNo(No* no) {
    No* atual = no;
    while (atual && atual->esq != NULL)
        atual = atual->esq;
    return atual;
}

No* remover(No* raiz, int valor) {
    if (raiz == NULL) return raiz;

    if (valor < raiz->chave)
        raiz->esq = remover(raiz->esq, valor);
    else if (valor > raiz->chave)
        raiz->dir = remover(raiz->dir, valor);
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
    int altEsq = altura(raiz->esq);
    int altDir = altura(raiz->dir);
    return (altEsq > altDir ? altEsq : altDir) + 1;
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
    raiz = inserir(raiz, 30);
    raiz = inserir(raiz, 70);
    raiz = inserir(raiz, 20);
    raiz = inserir(raiz, 40);

    printf("Pre-ordem: ");
    preOrdem(raiz);
    printf("\nEm-ordem: ");
    emOrdem(raiz);
    printf("\nPos-ordem: ");
    posOrdem(raiz);

    printf("\nAltura da arvore: %d\n", altura(raiz));

    printf("Busca (40): %s\n", buscar(raiz, 40) ? "Encontrado" : "Nao encontrado");

    raiz = remover(raiz, 30);
    printf("Em-ordem apos remover 30: ");
    emOrdem(raiz);
    printf("\n");

    destruirArvore(raiz);
    raiz = NULL;

    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Liberar o nó raiz antes das subárvores (Memory Leak):**
   Fazer `free(raiz)` no topo da função de liberação antes de chamar a recursão para `esq` e `dir` gera comportamento indefinido e vazamento de memória. A liberação **exige** o percurso em **Pós-ordem**.
   *Errado:*
   ```c
   free(raiz);
   destruir(raiz->esq); // Erro: acesso a ponteiro invalido!
   ```

2. **Acesso a ponteiro `NULL` (Segmentation Fault):**
   Acessar `raiz->esq` sem verificar previamente se `raiz == NULL`. O caso base da recursão (`if (raiz == NULL)`) deve sempre vir antes de qualquer acesso aos campos do `struct`.

3. **Perder a referência no retorno da Inserção/Remoção:**
   Esquecer de reatribuir o retorno das funções recursivas ao ponteiro do nó pai (`raiz->esq = inserir(raiz->esq, val)`). Sem isso, as alterações feitas na subárvore não são encadeadas na árvore original.

---

## 4. Exercicio com Gabarito

**Enunciado:**
Escreva uma função recursiva em C com a assinatura `int contarNos(No* raiz)` que receba o ponteiro para a raiz de uma árvore binária e retorne a quantidade total de nós presentes na árvore.

**Gabarito:**

```c
int contarNos(No* raiz) {
    // Caso base: arvore vazia tem 0 nos
    if (raiz == NULL) {
        return 0;
    }
    // Soma 1 (no atual) + nos da esquerda + nos da direita
    return 1 + contarNos(raiz->esq) + contarNos(raiz->dir);
}
```

**Explicação:** A função utiliza uma abordagem recursiva (baseada no percurso em pós-ordem). Se o nó atual for nulo, retorna `0`. Caso contrário, calcula recursivamente o total de nós da subárvore esquerda, o total da subárvore direita e soma `1` (referente ao próprio nó).