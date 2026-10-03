# Arvores B em C

## 1. Teoria e Complexidade

Uma Árvore B é uma estrutura de dados de busca auto-balanceada e multi-caminho (multi-way) projetada para otimizar operações em sistemas de armazenamento secundário (disco/SSD). Em uma Árvore B de ordem $m$ (ou grau mínimo $t$, onde $m = 2t$), cada nó interno contém no máximo $m - 1$ chaves e no mínimo $\lceil m/2 \rceil - 1$ chaves (exceto a raiz). Os nós possuem até $m$ ponteiros para filhos. Todas as folhas residem obrigatoriamente no mesmo nível de profundidade.

A inserção segue o princípio de *bottom-up*: as chaves são inseridas em nós folha. Quando uma folha atinge a capacidade máxima ($m - 1$ chaves), ocorre o algoritmo de **Split** (divisão): a chave mediana sobe para o nó pai e as chaves restantes dividem-se em dois novos nós. A busca percorre as chaves do nó atual (linearmente ou via busca binária) para selecionar o ponteiro de subárvore correto, garantindo complexidade logarítmica mesmo para volumes massivos de dados.

| Operação | Complexidade de Tempo (Médio) | Complexidade de Tempo (Pior) | Espaço |
| :--- | :--- | :--- | :--- |
| **Busca** | $O(\log_m n)$ | $O(\log_m n)$ | $O(n)$ |
| **Inserção** | $O(\log_m n)$ | $O(\log_m n)$ | $O(n)$ |
| **Remoção** | $O(\log_m n)$ | $O(\log_m n)$ | $O(n)$ |

---

## 2. Implementacao Completa em C

O código abaixo implementa uma Árvore B com grau mínimo $t=2$ (ordem $m=4$). Cada nó armazena no máximo 3 chaves e até 4 filhos.

```c
#include <stdio.h>
#include <stdlib.h>

#define T 2 // Grau minimo: no pode ter no maximo 2*T - 1 = 3 chaves

typedef struct BTreeNode {
    int keys[2 * T - 1];
    struct BTreeNode *C[2 * T];
    int n;
    int leaf;
} BTreeNode;

typedef struct BTree {
    BTreeNode *root;
} BTree;

BTreeNode *createNode(int leaf) {
    BTreeNode *node = (BTreeNode *)malloc(sizeof(BTreeNode));
    node->leaf = leaf;
    node->n = 0;
    for (int i = 0; i < 2 * T; i++) {
        node->C[i] = NULL;
    }
    return node;
}

BTree *createBTree() {
    BTree *tree = (BTree *)malloc(sizeof(BTree));
    tree->root = NULL;
    return tree;
}

BTreeNode *search(BTreeNode *root, int k) {
    if (root == NULL) return NULL;
    int i = 0;
    while (i < root->n && k > root->keys[i]) i++;
    if (i < root->n && root->keys[i] == k) return root;
    if (root->leaf) return NULL;
    return search(root->C[i], k);
}

void splitChild(BTreeNode *x, int i, BTreeNode *y) {
    BTreeNode *z = createNode(y->leaf);
    z->n = T - 1;

    for (int j = 0; j < T - 1; j++) {
        z->keys[j] = y->keys[j + T];
    }
    if (!y->leaf) {
        for (int j = 0; j < T; j++) {
            z->C[j] = y->C[j + T];
        }
    }
    y->n = T - 1;

    for (int j = x->n; j >= i + 1; j--) {
        x->C[j + 1] = x->C[j];
    }
    x->C[i + 1] = z;

    for (int j = x->n - 1; j >= i; j--) {
        x->keys[j + 1] = x->keys[j];
    }
    x->keys[i] = y->keys[T - 1];
    x->n++;
}

void insertNonFull(BTreeNode *x, int k) {
    int i = x->n - 1;
    if (x->leaf) {
        while (i >= 0 && x->keys[i] > k) {
            x->keys[i + 1] = x->keys[i];
            i--;
        }
        x->keys[i + 1] = k;
        x->n++;
    } else {
        while (i >= 0 && x->keys[i] > k) i--;
        i++;
        if (x->C[i]->n == 2 * T - 1) {
            splitChild(x, i, x->C[i]);
            if (x->keys[i] < k) i++;
        }
        insertNonFull(x->C[i], k);
    }
}

void insert(BTree *tree, int k) {
    BTreeNode *root = tree->root;
    if (root == NULL) {
        tree->root = createNode(1);
        tree->root->keys[0] = k;
        tree->root->n = 1;
    } else {
        if (root->n == 2 * T - 1) {
            BTreeNode *s = createNode(0);
            s->C[0] = root;
            splitChild(s, 0, root);
            int i = (s->keys[0] < k) ? 1 : 0;
            insertNonFull(s->C[i], k);
            tree->root = s;
        } else {
            insertNonFull(root, k);
        }
    }
}

void traverse(BTreeNode *root) {
    if (root != NULL) {
        int i;
        for (i = 0; i < root->n; i++) {
            if (!root->leaf) traverse(root->C[i]);
            printf("%d ", root->keys[i]);
        }
        if (!root->leaf) traverse(root->C[i]);
    }
}

void freeNode(BTreeNode *node) {
    if (node == NULL) return;
    if (!node->leaf) {
        for (int i = 0; i <= node->n; i++) {
            freeNode(node->C[i]);
        }
    }
    free(node);
}

void freeTree(BTree *tree) {
    if (tree != NULL) {
        freeNode(tree->root);
        free(tree);
    }
}

int main() {
    BTree *tree = createBTree();

    int keys[] = {10, 20, 5, 6, 12, 30, 7, 17};
    int n = sizeof(keys) / sizeof(keys[0]);

    for (int i = 0; i < n; i++) {
        insert(tree, keys[i]);
    }

    printf("Em-ordem das chaves inseridas: ");
    traverse(tree->root);
    printf("\n");

    int target = 6;
    BTreeNode *res = search(tree->root, target);
    if (res != NULL) printf("Chave %d ENCONTRADA na arvore.\n", target);
    else printf("Chave %d NAO encontrada.\n", target);

    target = 99;
    res = search(tree->root, target);
    if (res != NULL) printf("Chave %d ENCONTRADA na arvore.\n", target);
    else printf("Chave %d NAO encontrada.\n", target);

    freeTree(tree);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Desbalanceamento de Índices ($n$ chaves vs $n+1$ ponteiros):**
   - **Erro:** Fazer um laço iterando até `i <= node->n` ao acessar o vetor de chaves (`keys[i]`).
   - **Consequência:** *Buffer Overflow* ou *Segmentation Fault*. Lembre-se: em um nó com `n` chaves, os índices válidos de `keys` vão de `0` a `n - 1`, enquanto os índices válidos do vetor de ponteiros para filhos `C` vão de `0` a `n`.

2. **Perda da Raiz na Divisão (Split da Raiz):**
   - **Erro:** Executar a divisão no nó raiz sem reatribuir o ponteiro da estrutura principal (`tree->root`).
   - **Consequência:** A chave mediana promovida é alocada em um novo nó pai, mas se `tree->root` continuar apontando para a antiga raiz, a nova estrutura da árvore é perdida na memória (*Memory Leak* e dados inacessíveis).

3. **Acesso Inválido a Ponteiros Filhos em Nós Folha:**
   - **Erro:** Tentar descer na recursão acessando `node->C[i]` sem antes verificar a flag `node->leaf == 0`.
   - **Consequência:** Leitura de ponteiros nulos ou uninitialized (`NULL`), causando *Segfault*. Folhas não possuem subárvores.

---

## 4. Exercicio com Gabarito

**Enunciado:**
Escreva uma função recursiva em C com a seguinte assinatura: `int countTotalKeys(BTreeNode *root)`. A função deve retornar o número total de chaves armazenadas em toda a Árvore B a partir de um nó de origem.

**Gabarito:**

```c
int countTotalKeys(BTreeNode *root) {
    if (root == NULL) return 0;

    int total = root->n; // Soma as chaves do no atual

    // Se nao for folha, soma recursivamente as chaves de todos os filhos
    if (!root->leaf) {
        for (int i = 0; i <= root->n; i++) {
            total += countTotalKeys(root->C[i]);
        }
    }

    return total;
}
```
*Explicação:* A função acumula o valor do campo `n` do nó corrente. Se o nó não for folha, ela percorre recursivamente os `n + 1` ponteiros de subárvores (`C[0]` até `C[n]`), somando as chaves de cada nível até atingir as folhas base.