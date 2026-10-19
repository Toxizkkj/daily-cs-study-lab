# Arvores Binarias em C

## 1. Teoria e Complexidade

Uma árvore binária é uma estrutura de dados hierárquica na qual cada nó possui no máximo dois filhos, referenciados como filho esquerdo (`esq`) e filho direito (`dir`). A alocação de memória é dinâmica, utilizando ponteiros para conectar os nós. A navegação na estrutura é feita tipicamente via recursão, onde a condição de parada é o ponteiro nulo (`NULL`).

A eficiência do acesso aos dados depende diretamente da altura da árvore ($h$). Em árvores binárias de busca (BST) balanceadas, a altura é $O(\log n)$, enquanto no pior caso (árvore degenerada em lista) a altura é $O(n)$. A desalocação da memória exige obrigatoriamente um percurso em Pós-ordem para evitar a perda de ponteiros para os subfilhos antes da liberação do nó pai.

| Operação | Tempo (Médio) | Tempo (Pior Caso) | Espaço (Recursão - Pior Caso) |
| :--- | :--- | :--- | :--- |
| **Busca / Inserção** | $O(\log n)$ | $O(n)$ | $O(n)$ |
| **Percursos (Pré, Em, Pós)** | $O(n)$ | $O(n)$ | $O(n)$ |
| **Cálculo de Altura** | $O(n)$ | $O(n)$ | $O(n)$ |
| **Desalocação Total** | $O(n)$ | $O(n)$ | $O(n)$ |

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

int calcularAltura(No* raiz) {
    if (raiz == NULL) return -1;
    int altEsq = calcularAltura(raiz->esq);
    int altDir = calcularAltura(raiz->dir);
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
    printf("\nEm-ordem:  ");
    emOrdem(raiz);
    printf("\nPos-ordem: ");
    posOrdem(raiz);
    printf("\n");

    printf("Altura da arvore: %d\n", calcularAltura(raiz));

    int valorBusca = 40;
    No* encontrado = buscar(raiz, valorBusca);
    if (encontrado != NULL)
        printf("Chave %d encontrada na arvore.\n", valorBusca);
    else
        printf("Chave %d nao encontrada.\n", valorBusca);

    liberarArvore(raiz);
    raiz = NULL;

    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Desalocação Incorreta (Memory Leak / Use-After-Free):** Executar `free(raiz)` **antes** de chamar a função para os subfilhos esquerdo e direito. Ao dar `free` no nó pai, o acesso aos ponteiros `raiz->esq` e `raiz->dir` passa a ser um comportamento indefinido (ponteiro solto/dangling pointer). A liberação DEVE ser em pós-ordem.
2. **Esquecer a Verificação do Caso Base (`NULL`):** Tentar acessar `raiz->chave` ou fazer chamadas recursivas sem verificar se `raiz == NULL` gera erro de segfault (*Segmentation Fault*).
3. **Perda de Referência na Inserção:** Não reatribuir o retorno da chamada recursiva (`raiz->esq = inserir(...)`). Se o retorno for ignorado, as novas subárvores não serão conectadas aos nós pais.

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função recursiva em C chamada `contarFolhas` que receba o ponteiro para a raiz de uma árvore binária e retorne a quantidade total de nós folha (nós que não possuem filho esquerdo nem direito).

**Gabarito:**

```c
int contarFolhas(No* raiz) {
    // Caso base 1: arvore ou subarvore vazia
    if (raiz == NULL) return 0;
    
    // Caso base 2: o no e' uma folha (nao tem subfilhos)
    if (raiz->esq == NULL && raiz->dir == NULL) return 1;
    
    // Passo recursivo: soma folhas da esquerda e da direita
    return contarFolhas(raiz->esq) + contarFolhas(raiz->dir);
}
```