# Arvores B em C

## 1. Teoria e Complexidade

Uma **Árvore B** é uma estrutura de dados de busca multi-caminho auto-balanceada, projetada para otimizar operações de leitura e escrita em sistemas de armazenamento em bloco (como discos e bancos de dados). Em uma Árvore B de ordem $m$ (ou grau mínimo $t$, onde $m = 2t$), cada nó pode conter múltiplas chaves e ponteiros para filhos. Todas as folhas permanecem no mesmo nível, garantindo que a altura da árvore cresça de forma logarítmica estrita.

Regras fundamentais para uma Árvore B de grau mínimo $t \ge 2$:
- **Chaves por nó**: Mínimo de $t - 1$ chaves (exceto raiz) e máximo de $2t - 1$ chaves.
- **Filhos por nó**: Todo nó interno tem $k + 1$ filhos, onde $k$ é a quantidade de chaves do nó.
- **Split**: Quando um nó atinge $2t - 1$ chaves e precisa receber mais uma, ele é dividido ao meio. A chave mediana é promovida para o nó pai, e as metades esquerda e direita viram nós irmãos.

### Complexidade

| Operação | Tempo (Médio) | Tempo (Pior Caso) | Espaço |
| :--- | :--- | :--- | :--- |
| Busca | $O(\log n)$ | $O(\log n)$ | $O(n)$ |
| Inserção | $O(\log n)$ | $O(\log n)$ | $O(n)$ |
| Remoção | $O(\log n)$ | $O(\log n)$ | $O(n)$ |

---

## 2. Implementacao Completa em C

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define T 2 // Grau minimo (Max chaves = 2T - 1 = 3, Max filhos = 2T = 4)

typedef struct BNode {
    int keys[2 * T - 1];
    struct BNode *children[2 * T];
    int num_keys;
    bool leaf;
} BNode;

BNode *create_node(bool leaf) {
    BNode *node = (BNode *)malloc(sizeof(BNode));
    node->leaf = leaf;
    node->num_keys = 0;
    for (int i = 0; i < 2 * T; i++) {
        node->children[i] = NULL;
    }
    return node;
}

BNode *search(BNode *root, int key) {
    if (!root) return NULL;
    int i = 0;
    while (i < root->num_keys && key > root->keys[i]) i++;
    if (i < root->num_keys && root->keys[i] == key) return root;
    if (root->leaf) return NULL;
    return search(root->children[i], key);
}

void split_child(BNode *parent, int i, BNode *child) {
    BNode *z = create_node(child->leaf);
    z->num_keys = T - 1;

    for (int j = 0; j < T - 1; j++) {
        z->keys[j] = child->keys[j + T];
    }

    if (!child->leaf) {
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

void insert_non_full(BNode *node, int key) {
    int i = node->num_keys - 1;

    if (node->leaf) {
        while (i >= 0 && node->keys[i] > key) {
            node->keys[i + 1] = node->keys[i];
            i--;
        }
        node->keys[i + 1] = key;
        node->num_keys++;
    } else {
        while (i >= 0 && node->keys[i] > key) i--;
        i++;
        if (node->children[i]->num_keys == 2 * T - 1) {
            split_child(node, i, node->children[i]);
            if (node->keys[i] < key) i++;
        }
        insert_non_full(node->children[i], key);
    }
}

void insert(BNode **root, int key) {
    BNode *r = *root;
    if (!r) {
        *root = create_node(true);
        (*root)->keys[0] = key;
        (*root)->num_keys = 1;
        return;
    }
    if (r->num_keys == 2 * T - 1) {
        BNode *s = create_node(false);
        *root = s;
        s->children[0] = r;
        split_child(s, 0, r);
        insert_non_full(s, key);
    } else {
        insert_non_full(r, key);
    }
}

bool remove_leaf(BNode *node, int key) {
    int idx = -1;
    for (int i = 0; i < node->num_keys; i++) {
        if (node->keys[i] == key) { idx = i; break; }
    }
    if (idx == -1) return false;
    for (int i = idx; i < node->num_keys - 1; i++) {
        node->keys[i] = node->keys[i + 1];
    }
    node->num_keys--;
    return true;
}

void free_tree(BNode *node) {
    if (!node) return;
    if (!node->leaf) {
        for (int i = 0; i <= node->num_keys; i++) {
            free_tree(node->children[i]);
        }
    }
    free(node);
}

void print_inorder(BNode *node) {
    if (!node) return;
    int i;
    for (i = 0; i < node->num_keys; i++) {
        if (!node->leaf) print_inorder(node->children[i]);
        printf("%d ", node->keys[i]);
    }
    if (!node->leaf) print_inorder(node->children[i]);
}

int main(void) {
    BNode *root = NULL;
    int keys[] = {10, 20, 5, 6, 12, 30, 7, 17};
    int n = sizeof(keys) / sizeof(keys[0]);

    for (int i = 0; i < n; i++) {
        insert(&root, keys[i]);
    }

    printf("Em-ordem: ");
    print_inorder(root);
    printf("\n");

    int target = 12;
    BNode *res = search(root, target);
    printf("Busca por %d: %s\n", target, res ? "Encontrado" : "Nao encontrado");

    if (res && res->leaf) {
        remove_leaf(res, 5);
        printf("Apos remover 5 (folha): ");
        print_inorder(root);
        printf("\n");
    }

    free_tree(root);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Acesso Além do Limite dos Filhos (`Index Out of Bounds`)**:
   Um nó com $k$ chaves possui exatamente $k+1$ filhos ativos. Tentar percorrer `children` até `MAX_KEYS` em vez de `num_keys` causa **Segmentation Fault** ao acessar ponteiros nulos ou não inicializados.

2. **Perda da Raiz durante o Split**:
   Quando a raiz fica cheia, a criação da nova raiz exige que o ponteiro principal da árvore seja atualizado (`*root = s`). Passar a raiz por valor (`BNode *root`) em vez de ponteiro duplo (`BNode **root`) faz com que a alteração do nível superior seja perdida na função chamadora.

3. **Memory Leak na Liberação Recursiva**:
   Liberar o nó pai com `free(node)` *antes* de percorrer iterativamente ou recursivamente os ponteiros em `node->children[i]` invalida a leitura da memória, impedindo a liberação dos nós descendentes.

---

## 4. Exercicio com Gabarito

**Enunciado:**  
Considere uma Árvore B de grau mínimo $t=2$ (máximo de 3 chaves por nó) inicialmente vazia. Desenhe a estrutura resultante após a inserção sequencial das chaves: **10, 20, 30, 40, 50**.

---

**Gabarito Explícito:**

1. Insere **10, 20, 30**: A raiz fica cheia com 3 chaves: `[10, 20, 30]`.
2. Insere **40**: A raiz cheia sofre **split**. A chave mediana **20** sobe para uma nova raiz.
   - Raiz: `[20]`
   - Filho esquerdo: `[10]`
   - Filho direito: `[30, 40]`
3. Insere **50**: Inserida no filho direito, que passa a ter: `[30, 40, 50]`.

**Estrutura Final:**
```text
        [20]
       /    \
   [10]      [30, 40, 50]
```