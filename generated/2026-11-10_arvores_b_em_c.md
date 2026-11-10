# Arvores B em C

## 1. Teoria e Complexidade

Uma **Árvore B** é uma estrutura de dados de busca auto-balanceada projetada para funcionar de forma eficiente em sistemas de armazenamento secundário (discos/SSDs). Diferente das árvores binárias, cada nó de uma Árvore B de ordem $m$ pode conter múltiplos elementos (chaves) e ter até $m$ filhos (multi-caminho). Todas as folhas permanecem estritamente no mesmo nível de profundidade.

As regras fundamentais para uma Árvore B de ordem $m$ (ou grau mínimo $t$, onde $m = 2t$) são:
- Cada nó possui no máximo $m-1$ chaves e $m$ filhos.
- Qualquer nó interno (exceto a raiz) possui no mínimo $\lceil m/2 \rceil - 1$ chaves.
- O **Split** (divisão de nó) ocorre de baixo para cima quando um nó atinge o limite máximo de chaves, promovendo a chave mediana para o nó pai.
- A **Busca** realiza uma busca binária ou sequencial dentro da página do nó atual para decidir qual ponteiro de filho seguir.

| Operação | Complexidade de Tempo (Médio/Pior Caso) | Complexidade de Espaço |
| :--- | :--- | :--- |
| **Busca** | $O(\log_m N)$ | $O(1)$ auxiliar |
| **Inserção** | $O(\log_m N)$ | $O(\log_m N)$ |
| **Remoção** | $O(\log_m N)$ | $O(\log_m N)$ |
| **Espaço Total** | $O(N)$ | $O(N)$ |

---

## 2. Implementacao Completa em C

Código completo baseado em grau mínimo $T = 2$ (Ordem $m = 4$: Máximo de 3 chaves e 4 filhos por nó).

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define T 2
#define MAX_KEYS (2 * T - 1) // 3
#define MAX_CHILDREN (2 * T) // 4
#define MIN_KEYS (T - 1)     // 1

typedef struct BTreeNode {
    int keys[MAX_KEYS];
    struct BTreeNode *children[MAX_CHILDREN];
    int num_keys;
    bool is_leaf;
} BTreeNode;

BTreeNode *create_node(bool is_leaf) {
    BTreeNode *node = (BTreeNode *)malloc(sizeof(BTreeNode));
    node->num_keys = 0;
    node->is_leaf = is_leaf;
    for (int i = 0; i < MAX_CHILDREN; i++) {
        node->children[i] = NULL;
    }
    return node;
}

BTreeNode *search(BTreeNode *root, int key) {
    if (!root) return NULL;
    int i = 0;
    while (i < root->num_keys && key > root->keys[i]) i++;
    if (i < root->num_keys && key == root->keys[i]) return root;
    if (root->is_leaf) return NULL;
    return search(root->children[i], key);
}

void split_child(BTreeNode *parent, int i, BTreeNode *child) {
    BTreeNode *new_node = create_node(child->is_leaf);
    new_node->num_keys = MIN_KEYS;

    for (int j = 0; j < MIN_KEYS; j++) {
        new_node->keys[j] = child->keys[j + T];
    }

    if (!child->is_leaf) {
        for (int j = 0; j < T; j++) {
            new_node->children[j] = child->children[j + T];
        }
    }

    child->num_keys = MIN_KEYS;

    for (int j = parent->num_keys; j >= i + 1; j--) {
        parent->children[j + 1] = parent->children[j];
    }
    parent->children[i + 1] = new_node;

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
        while (i >= 0 && key < node->keys[i]) i--;
        i++;
        if (node->children[i]->num_keys == MAX_KEYS) {
            split_child(node, i, node->children[i]);
            if (key > node->keys[i]) i++;
        }
        insert_non_full(node->children[i], key);
    }
}

void insert(BTreeNode **root, int key) {
    BTreeNode *r = *root;
    if (!r) {
        *root = create_node(true);
        (*root)->keys[0] = key;
        (*root)->num_keys = 1;
        return;
    }
    if (r->num_keys == MAX_KEYS) {
        BTreeNode *s = create_node(false);
        *root = s;
        s->children[0] = r;
        split_child(s, 0, r);
        insert_non_full(s, key);
    } else {
        insert_non_full(r, key);
    }
}

void merge(BTreeNode *node, int idx) {
    BTreeNode *child = node->children[idx];
    BTreeNode *sibling = node->children[idx + 1];

    child->keys[MIN_KEYS] = node->keys[idx];
    for (int i = 0; i < sibling->num_keys; ++i) {
        child->keys[i + T] = sibling->keys[i];
    }
    if (!child->is_leaf) {
        for (int i = 0; i <= sibling->num_keys; ++i) {
            child->children[i + T] = sibling->children[i];
        }
    }
    for (int i = idx + 1; i < node->num_keys; ++i) {
        node->keys[i - 1] = node->keys[i];
    }
    for (int i = idx + 2; i <= node->num_keys; ++i) {
        node->children[i - 1] = node->children[i];
    }
    child->num_keys += sibling->num_keys + 1;
    node->num_keys--;
    free(sibling);
}

void remove_node(BTreeNode *root, int key) {
    if (!root) return;
    int idx = 0;
    while (idx < root->num_keys && root->keys[idx] < key) idx++;

    if (idx < root->num_keys && root->keys[idx] == key) {
        if (root->is_leaf) {
            for (int i = idx + 1; i < root->num_keys; ++i) root->keys[i - 1] = root->keys[i];
            root->num_keys--;
        } else {
            if (root->children[idx]->num_keys >= T) {
                BTreeNode *cur = root->children[idx];
                while (!cur->is_leaf) cur = cur->children[cur->num_keys];
                int pred = cur->keys[cur->num_keys - 1];
                root->keys[idx] = pred;
                remove_node(root->children[idx], pred);
            } else if (root->children[idx + 1]->num_keys >= T) {
                BTreeNode *cur = root->children[idx + 1];
                while (!cur->is_leaf) cur = cur->children[0];
                int succ = cur->keys[0];
                root->keys[idx] = succ;
                remove_node(root->children[idx + 1], succ);
            } else {
                merge(root, idx);
                remove_node(root->children[idx], key);
            }
        }
    } else {
        if (root->is_leaf) return;
        bool flag = (idx == root->num_keys);
        if (root->children[idx]->num_keys < T) {
            if (idx != 0 && root->children[idx - 1]->num_keys >= T) {
                BTreeNode *child = root->children[idx];
                BTreeNode *sibling = root->children[idx - 1];
                for (int i = child->num_keys - 1; i >= 0; --i) child->keys[i + 1] = child->keys[i];
                if (!child->is_leaf) {
                    for (int i = child->num_keys; i >= 0; --i) child->children[i + 1] = child->children[i];
                }
                child->keys[0] = root->keys[idx - 1];
                if (!child->is_leaf) child->children[0] = sibling->children[sibling->num_keys];
                root->keys[idx - 1] = sibling->keys[sibling->num_keys - 1];
                child->num_keys++;
                sibling->num_keys--;
            } else if (idx != root->num_keys && root->children[idx + 1]->num_keys >= T) {
                BTreeNode *child = root->children[idx];
                BTreeNode *sibling = root->children[idx + 1];
                child->keys[child->num_keys] = root->keys[idx];
                if (!child->is_leaf) child->children[child->num_keys + 1] = sibling->children[0];
                root->keys[idx] = sibling->keys[0];
                for (int i = 1; i < sibling->num_keys; ++i) sibling->keys[i - 1] = sibling->keys[i];
                if (!sibling->is_leaf) {
                    for (int i = 1; i <= sibling->num_keys; ++i) sibling->children[i - 1] = sibling->children[i];
                }
                child->num_keys++;
                sibling->num_keys--;
            } else {
                if (idx != root->num_keys) merge(root, idx);
                else merge(root, idx - 1);
            }
        }
        if (flag && idx > root->num_keys) remove_node(root->children[idx - 1], key);
        else remove_node(root->children[idx], key);
    }
}

void print_tree(BTreeNode *root, int level) {
    if (!root) return;
    printf("Nivel %d [%d chaves]: ", level, root->num_keys);
    for (int i = 0; i < root->num_keys; i++) printf("%d ", root->keys[i]);
    printf("\n");
    for (int i = 0; i <= root->num_keys; i++) {
        print_tree(root->children[i], level + 1);
    }
}

void free_tree(BTreeNode *node) {
    if (!node) return;
    if (!node->is_leaf) {
        for (int i = 0; i <= node->num_keys; i++) {
            free_tree(node->children[i]);
        }
    }
    free(node);
}

int main(void) {
    BTreeNode *root = NULL;
    int keys[] = {10, 20, 5, 6, 12, 30, 7, 17};
    int n = sizeof(keys) / sizeof(keys[0]);

    for (int i = 0; i < n; i++) insert(&root, keys[i]);

    printf("--- Estrutura da Arvore B ---\n");
    print_tree(root, 0);

    int target = 6;
    printf("\nBusca por %d: %s\n", target, search(root, target) ? "Encontrado" : "Nao encontrado");

    printf("\nRemovendo chave 6...\n");
    remove_node(root, 6);
    if (root->num_keys == 0) {
        BTreeNode *tmp = root;
        root = root->is_leaf ? NULL : root->children[0];
        free(tmp);
    }

    print_tree(root, 0);

    free_tree(root);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Incompatibilidade do tamanho de vetores (*Off-by-One*):** Um nó de Árvore B com $K$ chaves possui obrigatoriamente $K+1$ ponteiros para filhos. Declarar `children[MAX_KEYS]` em vez de `children[MAX_KEYS + 1]` causa estouro de buffer (*Segmentation Fault*) durante o split.
2. **Ignorar Atualização da Raiz no Split Superior:** Quando a raiz atual fica cheia, o split cria uma nova raiz acima dela. Se a função de inserção não receber o ponteiro da raiz por referência (`BTreeNode **root`) ou não retornar a nova raiz, o ponteiro original apontará para um nó antigo, corrompendo a árvore.
3. **Liberação de Memória Incompleta (*Memory Leak*):** Na desalocação (`free_tree`), é necessário percorrer **todos os $K+1$ filhos válidos** antes de liberar o nó atual. Executar `free(node)` antes do laço faz com que os ponteiros dos filhos sejam perdidos na memória.

---

## 4. Exercicio com Gabarito

**Enunciado:** Considere uma Árvore B de grau mínimo $T = 3$. Suponha que um nó folha que já possui 5 chaves receba a tentativa de inserção de mais uma chave. 
1. Quantas chaves este nó passará a ter temporariamente antes do *split*?
2. Quantas chaves ficarão no nó original, quantas subirão para o pai e quantas irão para o novo nó irmão após o *split*?

---

### Gabarito Explicado

1. **Capacidade Máxima:** Em uma Árvore B com $T = 3$, o número máximo de chaves por nó é $2T - 1 = 5$. Ao tentar inserir a 6ª chave, o nó estoura temporariamente com **6 chaves**.
2. **Divisão (Split):**
   - A chave de índice mediano (posição $T - 1 = 2$, considerando índice 0) é selecionada para subir.
   - **1 chave** (a mediana) sobe para o nó pai.
   - **2 chaves** (à esquerda da mediana) permanecem no nó original.
   - **3 chaves** (à direita da mediana) são movidas para o novo nó irmão à direita.