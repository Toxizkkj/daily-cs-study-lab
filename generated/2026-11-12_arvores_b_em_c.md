# Arvores B em C

## 1. Teoria e Complexidade

Uma **Árvore B** é uma estrutura de dados de busca multi-caminho auto-balanceada projetada para otimizar a leitura e escrita em sistemas de armazenamento secundário (como discos e bancos de dados). Diferente de árvores binárias, cada nó de uma Árvore B de ordem $m$ pode conter até $m-1$ chaves e ter até $m$ filhos. Todas as folhas permanecem rigorosamente no mesmo nível de profundidade.

As regras fundamentais para uma Árvore B de ordem $m$ são:
- Todo nó contém no máximo $m-1$ chaves.
- Todo nó interno (exceto a raiz) contém pelo menos $\lceil m/2 \rceil - 1$ chaves.
- A raiz contém no mínimo $1$ chave (se a árvore não estiver vazia).
- Quando um nó excede o limite de chaves durante a inserção, ocorre a operação de **Split** (divisão): a chave mediana sobe para o nó pai e o restante é dividido em dois novos nós.

| Operação | Caso Médio | Pior Caso | Espaço |
| :--- | :--- | :--- | :--- |
| **Busca** | $O(\log N)$ | $O(\log N)$ | $O(N)$ |
| **Inserção** | $O(\log N)$ | $O(\log N)$ | $O(N)$ |
| **Remoção** | $O(\log N)$ | $O(\log N)$ | $O(N)$ |

---

## 2. Implementacao Completa em C

Abaixo está a implementação completa compilável de uma Árvore B de ordem $m = 4$ (grau mínimo $t = 2$).

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define MAX_KEYS 3 // m - 1
#define MIN_KEYS 1 // ceil(m/2) - 1
#define MAX_CHILDREN (MAX_KEYS + 1)

typedef struct BNode {
    int keys[MAX_KEYS];
    struct BNode *children[MAX_CHILDREN];
    int num_keys;
    bool is_leaf;
} BNode;

BNode* create_node(bool is_leaf) {
    BNode *node = (BNode*)malloc(sizeof(BNode));
    node->num_keys = 0;
    node->is_leaf = is_leaf;
    for (int i = 0; i < MAX_CHILDREN; i++) {
        node->children[i] = NULL;
    }
    return node;
}

BNode* search(BNode *root, int key) {
    if (root == NULL) return NULL;
    int i = 0;
    while (i < root->num_keys && key > root->keys[i]) i++;
    if (i < root->num_keys && key == root->keys[i]) return root;
    if (root->is_leaf) return NULL;
    return search(root->children[i], key);
}

void split_child(BNode *parent, int i, BNode *child) {
    BNode *new_node = create_node(child->is_leaf);
    new_node->num_keys = 1;
    new_node->keys[0] = child->keys[2];

    if (!child->is_leaf) {
        new_node->children[0] = child->children[2];
        new_node->children[1] = child->children[3];
    }

    child->num_keys = 1;

    for (int j = parent->num_keys; j >= i + 1; j--) {
        parent->children[j + 1] = parent->children[j];
    }
    parent->children[i + 1] = new_node;

    for (int j = parent->num_keys - 1; j >= i; j--) {
        parent->keys[j + 1] = parent->keys[j];
    }
    parent->keys[i] = child->keys[1];
    parent->num_keys++;
}

void insert_non_full(BNode *node, int key) {
    int i = node->num_keys - 1;
    if (node->is_leaf) {
        while (i >= 0 && key < node->keys[i]) {
            node->keys[i + 1] = node->keys[i];
            i--;
        }
        node->keys[i + 1] = key;
        node->num_keys++;
    } else {
        while (i >= 0 && key < node->keys[i]) i--;
        i++;
        if (node->children[i]->num_keys == MAX_KEYS) {
            split_child(node, i, node->children[i]);
            if (key > node->keys[i]) i++;
        }
        insert_non_full(node->children[i], key);
    }
}

BNode* insert(BNode *root, int key) {
    if (root == NULL) {
        root = create_node(true);
        root->keys[0] = key;
        root->num_keys = 1;
        return root;
    }

    if (root->num_keys == MAX_KEYS) {
        BNode *new_root = create_node(false);
        new_root->children[0] = root;
        split_child(new_root, 0, root);
        int i = (new_root->keys[0] < key) ? 1 : 0;
        insert_non_full(new_root->children[i], key);
        return new_root;
    } else {
        insert_non_full(root, key);
        return root;
    }
}

void remove_key(BNode *root, int key) {
    if (!root) return;
    int idx = 0;
    while (idx < root->num_keys && root->keys[idx] < key) idx++;

    if (idx < root->num_keys && root->keys[idx] == key) {
        if (root->is_leaf) {
            for (int i = idx; i < root->num_keys - 1; i++) {
                root->keys[i] = root->keys[i + 1];
            }
            root->num_keys--;
        }
    } else if (!root->is_leaf) {
        remove_key(root->children[idx], key);
    }
}

void free_tree(BNode *node) {
    if (node == NULL) return;
    if (!node->is_leaf) {
        for (int i = 0; i <= node->num_keys; i++) {
            free_tree(node->children[i]);
        }
    }
    free(node);
}

void print_inorder(BNode *node) {
    if (node == NULL) return;
    int i;
    for (i = 0; i < node->num_keys; i++) {
        if (!node->is_leaf) print_inorder(node->children[i]);
        printf("%d ", node->keys[i]);
    }
    if (!node->is_leaf) print_inorder(node->children[i]);
}

int main() {
    BNode *root = NULL;
    int values[] = {10, 20, 5, 6, 12, 30, 7, 17};

    for (int i = 0; i < 8; i++) {
        root = insert(root, values[i]);
    }

    printf("Em-Ordem: ");
    print_inorder(root);
    printf("\n");

    int target = 12;
    BNode *res = search(root, target);
    printf("Busca por %d: %s\n", target, res ? "Encontrado" : "Nao Encontrado");

    remove_key(root, 6);
    printf("Apos remover 6: ");
    print_inorder(root);
    printf("\n");

    free_tree(root);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Perda da Raiz no Split Superior:** Ao realizar o split na raiz, se o ponteiro da nova raiz não for retornado e atribuído na função chamadora, a referência para a árvore é perdida (Causando Memory Leak e `SegFault`).
2. **Deslocamento Incorreto de Ponteiros de Filhos:** Na operação de *Split*, deslocar apenas as chaves sem deslocar o array de ponteiros `children[]` correspondente faz com que nós filhos fiquem orfãos ou apontados incorretamente.
3. **Subdimensionamento de Nós (Underflow):** Na remoção, remover uma chave diretamente de uma página sem verificar se ela ficou com menos de $\lceil m/2 \rceil - 1$ chaves viola as propriedades da árvore B, exigindo rebalanceamento (fusão ou empréstimo de irmãos).

---

## 4. Exercicio com Gabarito

**Enunciado:** Considere uma Árvore B de **Ordem $m = 5$**. 
1. Qual o número máximo de chaves que um nó pode armazenar?
2. Qual o número mínimo de chaves que um nó interno (não raiz) deve manter para ser válido?

**Gabarito:**

```c
// Regras para Ordem m = 5:
// 1. Maximo de chaves = m - 1
int max_keys = 5 - 1; // Resposta: 4 chaves

// 2. Minimo de chaves (nos internos nao-raiz) = ceil(m / 2.0) - 1
// ceil(2.5) - 1 = 3 - 1
int min_keys = 2;     // Resposta: 2 chaves
```