# Arvores B em C

## 1. Teoria e Complexidade

A **Árvore B** é uma estrutura de dados auto-balanceada de busca multi-caminho, projetada para otimizar operações de leitura/escrita em blocos de memória secundária (como discos e bancos de dados). Em uma Árvore B de ordem $m$, cada nó pode conter no máximo $m-1$ chaves e $m$ ponteiros para filhos. Exceto a raiz, todos os nós internos possuem pelo menos $\lceil m/2 \rceil$ filhos. Todas as folhas permanecem estritamente no mesmo nível de profundidade.

O processo de **Split** ocorre quando uma inserção estoura a capacidade máxima de uma página ($m-1$ chaves). O elemento mediano dessa página é promovido para o nó pai, e a página original é dividida em dois novos nós de tamanho igual. A busca percorre as chaves ordenadas dentro do nó para decidir qual ponteiro de filho seguir, mantendo a altura da árvore em $O(\log_m n)$.

| Operação | Caso Médio | Pior Caso | Espaço |
| :--- | :--- | :--- | :--- |
| **Busca** | $O(\log n)$ | $O(\log n)$ | $O(1)$ |
| **Inserção** | $O(\log n)$ | $O(\log n)$ | $O(1)$ |
| **Remoção** | $O(\log n)$ | $O(\log n)$ | $O(1)$ |
| **Espaço Total** | $O(n)$ | $O(n)$ | $O(n)$ |

---

## 2. Implementacao Completa em C

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define T 2 // Grau minimo (Ordem m = 2*T = 4). Max chaves = 3, Max filhos = 4

typedef struct BTreeNode {
    int keys[2 * T - 1];
    struct BTreeNode *children[2 * T];
    int num_keys;
    bool is_leaf;
} BTreeNode;

typedef struct BTree {
    BTreeNode *root;
} BTree;

BTreeNode* create_node(bool is_leaf) {
    BTreeNode *node = (BTreeNode*)malloc(sizeof(BTreeNode));
    node->num_keys = 0;
    node->is_leaf = is_leaf;
    for (int i = 0; i < 2 * T; i++) {
        node->children[i] = NULL;
    }
    return node;
}

BTree* create_tree() {
    BTree *tree = (BTree*)malloc(sizeof(BTree));
    tree->root = create_node(true);
    return tree;
}

BTreeNode* search(BTreeNode *node, int key) {
    int i = 0;
    while (i < node->num_keys && key > node->keys[i]) {
        i++;
    }
    if (i < node->num_keys && key == node->keys[i]) {
        return node;
    }
    if (node->is_leaf) {
        return NULL;
    }
    return search(node->children[i], key);
}

void split_child(BTreeNode *parent, int i, BTreeNode *child) {
    BTreeNode *z = create_node(child->is_leaf);
    z->num_keys = T - 1;

    for (int j = 0; j < T - 1; j++) {
        z->keys[j] = child->keys[j + T];
    }

    if (!child->is_leaf) {
        for (int j = 0; j < T; j++) {
            z->children[j] = child->children[j + T];
        }
    }

    child->num_keys = T - 1;

    for (int j = parent->num_keys; j >= i + 1; j--) {
        parent->children[j + 1] = parent->children[j];
    }
    parent->children[i + 1] = z;

    for (int j = parent->num_keys - 1; j >= i; j--) {
        parent->keys[j + 1] = parent->keys[j];
    }
    parent->keys[i] = child->keys[T - 1];
    parent->num_keys++;
}

void insert_non_full(BTreeNode *node, int key) {
    int i = node->num_keys - 1;

    if (node->is_leaf) {
        while (i >= 0 && key < node->keys[i]) {
            node->keys[i + 1] = node->keys[i];
            i--;
        }
        node->keys[i + 1] = key;
        node->num_keys++;
    } else {
        while (i >= 0 && key < node->keys[i]) {
            i--;
        }
        i++;
        if (node->children[i]->num_keys == 2 * T - 1) {
            split_child(node, i, node->children[i]);
            if (key > node->keys[i]) {
                i++;
            }
        }
        insert_non_full(node->children[i], key);
    }
}

void insert(BTree *tree, int key) {
    BTreeNode *root = tree->root;
    if (root->num_keys == 2 * T - 1) {
        BTreeNode *s = create_node(false);
        tree->root = s;
        s->children[0] = root;
        split_child(s, 0, root);
        insert_non_full(s, key);
    } else {
        insert_non_full(root, key);
    }
}

void traverse(BTreeNode *node) {
    int i;
    for (i = 0; i < node->num_keys; i++) {
        if (!node->is_leaf) {
            traverse(node->children[i]);
        }
        printf("%d ", node->keys[i]);
    }
    if (!node->is_leaf) {
        traverse(node->children[i]);
    }
}

void free_node(BTreeNode *node) {
    if (node == NULL) return;
    if (!node->is_leaf) {
        for (int i = 0; i <= node->num_keys; i++) {
            free_node(node->children[i]);
        }
    }
    free(node);
}

void free_tree(BTree *tree) {
    if (tree == NULL) return;
    free_node(tree->root);
    free(tree);
}

int main() {
    BTree *tree = create_tree();

    int keys[] = {10, 20, 5, 6, 12, 30, 7, 17};
    int n = sizeof(keys) / sizeof(keys[0]);

    for (int i = 0; i < n; i++) {
        insert(tree, keys[i]);
    }

    printf("Em-Ordem: ");
    traverse(tree->root);
    printf("\n");

    int search_key = 6;
    BTreeNode *res = search(tree->root, search_key);
    printf("Busca %d: %s\n", search_key, res != NULL ? "Encontrado" : "Nao Encontrado");

    free_tree(tree);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Aumento de Altura pela Raiz:** A altura de uma Árvore B cresce exclusivamente de baixo para cima. Ocorre **apenas** quando a raiz atual enche e é dividida (`split_child`), criando uma nova raiz com $1$ chave e $2$ filhos. Tentar dividir folhas sem propagar para o pai gera perda de referências e *Segmentation Fault*.
2. **Atualização do `num_keys` pós-Split:** Ao dividir um nó com $2T-1$ chaves, o nó original fica com $T-1$ chaves, o novo nó recebe $T-1$ chaves e $1$ chave sobe para o pai. Esquecer de atualizar `num_keys` de **todos** os três nós envolvidos corrompe a iteração e causa acessos inválidos de memória.
3. **Liberação Recursiva de Memória (Memory Leak):** Dar `free(node)` antes de percorrer os ponteiros `children[]` invalida o acesso aos nós filhos. A desalocação deve usar o percurso em Pós-Ordem (liberar todos os filhos primeiro e o nó atual por último).

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função recursiva `int count_keys(BTreeNode *root)` que retorne o total de chaves armazenadas na Árvore B.

**Gabarito:**

```c
int count_keys(BTreeNode *root) {
    if (root == NULL) return 0;
    
    int total = root->num_keys;
    
    if (!root->is_leaf) {
        for (int i = 0; i <= root->num_keys; i++) {
            total += count_keys(root->children[i]);
        }
    }
    
    return total;
}
```