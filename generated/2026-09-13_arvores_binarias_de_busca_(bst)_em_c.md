# Arvores Binarias de Busca (BST) em C

## 1. Teoria e Complexidade

Uma Árvore Binária de Busca (BST) é uma estrutura de dados hierárquica baseada em nós. Sua **propriedade de ordenação** estabelece que, para qualquer nó $X$:
- Todas as chaves na subárvore **esquerda** são estritamente menores que a chave de $X$ ($\text{esq} < X$).
- Todas as chaves na subárvore **direita** são estritamente maiores que a chave de $X$ ($\text{dir} > X$).

As operações primárias dependem diretamente da altura $h$ da árvore, resultando em complexidade $O(h)$. Em árvores balanceadas $h = \log n$, mas no pior caso (inserção ordenada) a árvore degenera em uma lista encadeada onde $h = n$.

| Operação | Caso Médio (Balanceada) | Pior Caso (Degenerada) | Espaço (Auxiliar) |
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

No* criar_no(int chave) {
    No* novo = (No*)malloc(sizeof(No));
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
    if (raiz == NULL || raiz->chave == chave) 
        return raiz;
    if (chave < raiz->chave) 
        return buscar(raiz->esq, chave);
    return buscar(raiz->dir, chave);
}

No* menor_no(No* raiz) {
    No* atual = raiz;
    while (atual && atual->esq != NULL)
        atual = atual->esq;
    return atual;
}

No* remover(No* raiz, int chave) {
    if (raiz == NULL) return raiz;

    if (chave < raiz->chave) {
        raiz->esq = remover(raiz->esq, chave);
    } else if (chave > raiz->chave) {
        raiz->dir = remover(raiz->dir, chave);
    } else {
        // Caso 1: Sem filhos (folha) / Caso 2: 1 filho
        if (raiz->esq == NULL) {
            No* temp = raiz->dir;
            free(raiz);
            return temp;
        } else if (raiz->dir == NULL) {
            No* temp = raiz->esq;
            free(raiz);
            return temp;
        }
        // Caso 3: 2 filhos (Sucessor Em-Ordem: menor da subárvore direita)
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

void liberar_arvore(No* raiz) {
    if (raiz == NULL) return;
    liberar_arvore(raiz->esq);
    liberar_arvore(raiz->dir);
    free(raiz);
}

int main() {
    No* raiz = NULL;

    // Insercao
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
    int alvo = 40;
    No* buscado = buscar(raiz, alvo);
    printf("Busca %d: %s\n", alvo, buscado ? "Encontrado" : "Nao encontrado");

    // Remocao Caso 1: Folha (20)
    raiz = remover(raiz, 20);
    // Remocao Caso 2: 1 Filho (Supondo que tiramos e sobrou 1)
    raiz = remover(raiz, 30); 
    // Remocao Caso 3: 2 Filhos (50 - Raiz)
    raiz = remover(raiz, 50);

    printf("Em-ordem apos remocoes: ");
    em_ordem(raiz);
    printf("\n");

    liberar_arvore(raiz);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Esquecer de reatribuir os retornos das funções recursivas**:
   - *Erro*: Escrever `remover(raiz->esq, chave);` em vez de `raiz->esq = remover(raiz->esq, chave);`.
   - *Consequência*: O ponteiro do pai continua apontando para a memória desalocada do filho (ponteiro solto/dangling pointer), causando comportamento indefinido ou *Segmentation Fault*.

2. **Copiar o nó em vez de apenas o valor no Caso 3 de remoção**:
   - *Erro*: Ao remover um nó com 2 filhos, tentar trocar os ponteiros `raiz = temp` em vez de apenas copiar o valor da chave `raiz->chave = temp->chave`.
   - *Consequência*: Quebra de encadeamento da árvore e destruição da estrutura do pai original.

3. **Memory Leak na remoção de nós com 1 ou 0 filhos**:
   - *Erro*: Retornar o filho diretamente (`return raiz->dir;`) sem executar `free(raiz)`.
   - *Consequência*: O nó original permanece alocado no *heap* sem nenhuma referência apontando para ele.

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função recursiva em C com a assinatura `int altura(No* raiz)` que retorne a altura de uma BST. Considere a altura de uma árvore vazia (`NULL`) como `-1` e de uma árvore com apenas a raiz como `0`.

**Gabarito:**

```c
int max(int a, int b) {
    return (a > b) ? a : b;
}

int altura(No* raiz) {
    if (raiz == NULL) {
        return -1; // Base: arvore vazia tem altura -1
    }
    
    int alt_esq = altura(raiz->esq);
    int alt_dir = altura(raiz->dir);
    
    return 1 + max(alt_esq, alt_dir);
}
```

*Explicação:* A função desce recursivamente até as folhas. O caso base retorna `-1`. À medida que a pilha desfaz, cada nível adiciona `1` ao máximo retornado entre as subárvores esquerda e direita. Um único nó resulta em `1 + max(-1, -1) = 0`.