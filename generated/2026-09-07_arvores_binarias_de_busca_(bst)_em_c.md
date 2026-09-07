# Arvores Binarias de Busca (BST) em C

## 1. Teoria e Complexidade

Uma Árvore Binária de Busca (BST) é uma estrutura de dados hierárquica baseada em nós, definida pela **propriedade de ordenação**: para qualquer nó $N$, todas as chaves na subárvore esquerda são estritamente menores que $N.chave$, e todas as chaves na subárvore direita são estritamente maiores que $N.chave$. Essa propriedade garante que o percurso *em-ordem* (in-order) visite os elementos de forma perfeitamente ordenada.

A eficiência de todas as operações fundamentais (busca, inserção e remoção) depende diretamente da altura $h$ da árvore, resultando em complexidade $O(h)$. Em uma árvore balanceada, $h = O(\log n)$. No entanto, se os elementos forem inseridos de forma ordenada, a árvore degenera em uma lista encadeada, levando a $h = O(n)$.

| Operação | Caso Médio | Pior Caso | Espaço (Auxiliar) |
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

No* minimo(No* raiz) {
    No* atual = raiz;
    while (atual && atual->esq != NULL)
        atual = atual->esq;
    return atual;
}

No* remover(No* raiz, int chave) {
    if (raiz == NULL) return NULL;

    if (chave < raiz->chave)
        raiz->esq = remover(raiz->esq, chave);
    else if (chave > raiz->chave)
        raiz->dir = remover(raiz->dir, chave);
    else {
        // Casos 1 e 2: Sem filhos ou apenas 1 filho
        if (raiz->esq == NULL) {
            No* temp = raiz->dir;
            free(raiz);
            return temp;
        } else if (raiz->dir == NULL) {
            No* temp = raiz->esq;
            free(raiz);
            return temp;
        }
        // Caso 3: 2 filhos -> Obter o sucessor em-ordem (menor da subárvore direita)
        No* temp = minimo(raiz->dir);
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
    if (raiz != NULL) {
        liberar_arvore(raiz->esq);
        liberar_arvore(raiz->dir);
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
    int alvo = 40;
    No* b = buscar(raiz, alvo);
    printf("Busca %d: %s\n", alvo, b ? "Encontrado" : "Nao encontrado");

    // Remocao Caso 1: Folha (20)
    raiz = remover(raiz, 20);
    // Remocao Caso 2: 1 Filho (assumindo estrutura resultante)
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

1. **Perda do ponteiro do pai ao retornar da recursão**:
   Esquecer de atribuir o retorno das funções de inserção e remoção aos ponteiros dos filhos (`raiz->esq = remover(raiz->esq, val)`). Fazer apenas `remover(raiz->esq, val)` sem reatribuir resulta na perda da alteração da estrutura da árvore (ponteiros soltos ou desatualizados).

2. **Memory Leak no Caso 3 da Remoção**:
   Tentar desalocar (`free`) o nó com dois filhos diretamente em vez de trocar a chave com a do sucessor/antecessor e chamar a remoção recursiva. A troca de ponteiros diretos em nós com dois filhos é propensa a vazamento de memória e perda de subárvores inteiras.

3. **Segmentation Fault em Ponteiros Nulos (Base Case)**:
   Acessar `raiz->chave`, `raiz->esq` ou `raiz->dir` antes de checar se `raiz == NULL`. A verificação de `NULL` deve ser sempre a primeira instrução em funções recursivas sobre árvores.

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função recursiva em C com a assinatura `int contar_folhas(No* raiz)` que calcule e retorne a quantidade total de nós folha (nós que não possuem filho esquerdo e nem filho direito) em uma BST.

**Gabarito:**

```c
int contar_folhas(No* raiz) {
    if (raiz == NULL)
        return 0;
    
    // Se não possui filho esquerdo nem direito, é uma folha
    if (raiz->esq == NULL && raiz->dir == NULL)
        return 1;
    
    // Soma os nós folha da subárvore esquerda e direita
    return contar_folhas(raiz->esq) + contar_folhas(raiz->dir);
}
```

*Explicação:* A função lida primeiro com o caso base (`NULL`, retornando `0`). Em seguida, verifica se o nó atual atende ao critério de folha (ambos os filhos nulos), retornando `1`. Caso contrário, divide o problema somando recursivamente o número de folhas das subárvores esquerda e direita.