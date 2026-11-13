# Arvores Binarias de Busca (BST) em C

## 1. Teoria e Complexidade

Uma **Árvore Binária de Busca (BST)** é uma estrutura de dados hierárquica na qual cada nó possui no máximo dois filhos (esquerdo e direito). A **propriedade de ordenação** estabelece que, para qualquer nó $X$:
- Todos os elementos na subárvore à **esquerda** possuem chaves **menores** que a chave de $X$.
- Todos os elementos na subárvore à **direita** possuem chaves **maiores** que a chave de $X$.

As operações cruciais de busca, inserção e remoção dependem diretamente da altura $h$ da árvore. A remoção lida com três cenários:
1. **Nó folha (0 filhos):** É removido diretamente liberando a memória.
2. **Nó com 1 filho:** O nó é removido e seu filho único ocupa a sua posição.
3. **Nó com 2 filhos:** O nó é substituído pelo seu **sucessor em-ordem** (o menor valor da subárvore direita), e então o sucessor original é removido.

| Operação | Caso Médio | Pior Caso (Degenerada) | Espaço (Auxiliar Recursivo) |
| :--- | :--- | :--- | :--- |
| Busca | $O(\log n)$ | $O(n)$ | $O(h)$ |
| Inserção | $O(\log n)$ | $O(n)$ | $O(h)$ |
| Remoção | $O(\log n)$ | $O(n)$ | $O(h)$ |

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
    No* novo = (No*) malloc(sizeof(No));
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
    if (raiz == NULL) return NULL;

    if (chave < raiz->chave) {
        raiz->esq = remover(raiz->esq, chave);
    } else if (chave > raiz->chave) {
        raiz->dir = remover(raiz->dir, chave);
    } else {
        // Caso 1 e 2: 0 ou 1 filho
        if (raiz->esq == NULL) {
            No* temp = raiz->dir;
            free(raiz);
            return temp;
        } else if (raiz->dir == NULL) {
            No* temp = raiz->esq;
            free(raiz);
            return temp;
        }
        // Caso 3: 2 filhos (substitui pelo sucessor)
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

    // Insercoes
    raiz = inserir(raiz, 50);
    raiz = inserir(raiz, 30);
    raiz = inserir(raiz, 70);
    raiz = inserir(raiz, 20);
    raiz = inserir(raiz, 40);
    raiz = inserir(raiz, 60);
    raiz = inserir(raiz, 80);

    printf("Em-ordem inicial: ");
    em_ordem(raiz);
    printf("\n");

    // Busca
    No* b = buscar(raiz, 40);
    printf("Busca 40: %s\n", b ? "Encontrado" : "Nao encontrado");

    // Remocao Caso 1: Folha (20)
    raiz = remover(raiz, 20);
    // Remocao Caso 2: 1 filho (supor remocao que deixa 1 filho)
    raiz = remover(raiz, 30);
    // Remocao Caso 3: 2 filhos (raiz 50)
    raiz = remover(raiz, 50);

    printf("Em-ordem apos remocoes (20, 30, 50): ");
    em_ordem(raiz);
    printf("\n");

    liberar(raiz);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Perda de Ponteiros no Retorno Recursivo:** Esquecer de atualizar o ponteiro no retorno (`raiz->esq = remover(raiz->esq, val);`). Se fizer apenas `remover(raiz->esq, val);`, a alteração no ponteiro pai não persiste e gera um ponteiro solto (*dangling pointer*).
2. **Memory Leak no Caso 3 de Remoção:** Liberar o nó diretamente no caso de 2 filhos desconecta a árvore. O correto é copiar a chave do sucessor para o nó atual e chamar a remoção recursiva **apenas** para a chave duplicada na subárvore direita.
3. **Pior Caso O(n) por Inserção Ordenada:** Se elementos forem inseridos em ordem crescente (ex: 1, 2, 3, 4), a BST degenera em uma Lista Encadeada simples, transformando busca e inserção de $O(\log n)$ em $O(n)$.

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função em C `int contar_folhas(No* raiz)` que retorna a quantidade total de nós folha (nós sem filhos esquerdos e sem filhos direitos) em uma BST.

**Gabarito:**

```c
int contar_folhas(No* raiz) {
    if (raiz == NULL) 
        return 0;
    
    // Se nao tem filho esquerdo nem direito, e um no folha
    if (raiz->esq == NULL && raiz->dir == NULL) 
        return 1;
    
    // Soma as folhas da subarvore esquerda e direita
    return contar_folhas(raiz->esq) + contar_folhas(raiz->dir);
}
```