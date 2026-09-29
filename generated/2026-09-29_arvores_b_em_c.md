# Arvores B em C

## 1. Teoria e Complexidade

Uma Árvore B é uma estrutura de dados de busca multi-caminho auto-balanceada projetada para otimizar operações de leitura e escrita em blocos de memória secundária (como discos e SSDs). Diferente de árvores binárias, cada nó (chamado de página) em uma Árvore B de ordem $m$ pode conter múltiplos elementos (chaves) e ter até $m$ filhos.

**Regras Fundamentais de uma Árvore B de Ordem $m$:**
1. **Capacidade de Chaves:** Cada nó contém no máximo $m - 1$ chaves. Exceto a raiz, todo nó interno possui no mínimo $\lceil m/2 \rceil - 1$ chaves.
2. **Capacidade de Filhos:** Um nó não-folha com $k$ chaves possui exatamente $k + 1$ ponteiros para filhos.
3. **Propriedade de Balanceamento:** Todas as folhas estão rigorosamente no mesmo nível de profundidade.
4. **Algoritmo de Split:** Quando uma chave é inserida em uma página cheia ($m - 1$ chaves), a página é dividida (split): a chave mediana sobe para o nó pai, e as metades restante e superior formam duas novas páginas irmãs.

| Operação | Caso Médio | Pior Caso | Complexidade de Espaço |
| :--- | :--- | :--- | :--- |
| **Busca** | $O(\log_m n)$ | $O(\log_m n)$ | $O(n)$ |
| **Inserção** | $O(\log_m n)$ | $O(\log_m n)$ | $O(n)$ |
| **Remoção** | $O(\log_m n)$ | $O(\log_m n)$ | $O(n)$ |

---

## 2. Implementacao Completa em C

Código compilável demonstrando uma Árvore B com grau mínimo $T = 2$ (Ordem $m = 4$, até 3 chaves por nó).

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define T 2 // Grau minimo (Ordem m = 2*T = 4)

typedef struct BTreeNode {
    int keys[2 * T - 1];
    struct BTreeNode* children[2 * T];
    int num_keys;
    bool leaf;
} BTreeNode;

BTreeNode* createNode(bool leaf) {
    BTreeNode* node = (BTreeNode*)malloc(sizeof(BTreeNode));
    node->leaf = leaf;
    node->num_keys = 0;
    for (int i = 0; i < 2 * T; i++) {
        node->children[i] = NULL;
    }
    return node;
}

void traverse(BTreeNode* root) {
    if (root == NULL) return;
    int i;
    for (i = 0; i < root->num_keys; i++) {
        if (!root->leaf) traverse(root->children[i]);
        printf("%d ", root->keys[i]);
    }
    if (!root->leaf) traverse(root->children[i]);
}

BTreeNode* search(BTreeNode* root, int k) {
    if (root == NULL) return NULL;
    int i = 0;
    while (i < root->num_keys && k > root->keys[i]) i++;
    if (i < root->num_keys && root->keys[i] == k) return root;
    if (root->leaf) return NULL;
    return search(root->children[i], k);
}

void splitChild(BTreeNode* parent, int i, BTreeNode* child) {
    BTreeNode* z = createNode(child->leaf);
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

void insertNonFull(BTreeNode* node, int k) {
    int i = node->num_keys - 1;
    if (node->leaf) {
        while (i >= 0 && node->keys[i] > k) {
            node->keys[i + 1] = node->keys[i];
            i--;
        }
        node->keys[i + 1] = k;
        node->num_keys++;
    } else {
        while (i >= 0 && node->keys[i] > k) i--;
        i++;
        if (node->children[i]->num_keys == 2 * T - 1) {
            splitChild(node, i, node->children[i]);
            if (node->keys[i] < k) i++;
        }
        insertNonFull(node->children[i], k);
    }
}

void insert(BTreeNode** root, int k) {
    BTreeNode* r = *root;
    if (r == NULL) {
        *root = createNode(true);
        (*root)->keys[0] = k;
        (*root)->num_keys = 1;
        return;
    }
    if (r->num_keys == 2 * T - 1) {
        BTreeNode* s = createNode(false);
        *root = s;
        s->children[0] = r;
        splitChild(s, 0, r);
        insertNonFull(s, k);
    } else {
        insertNonFull(r, k);
    }
}

void removeFromLeaf(BTreeNode* node, int idx) {
    for (int i = idx + 1; i < node->num_keys; ++i) {
        node->keys[i - 1] = node->keys[i];
    }
    node->num_keys--;
}

void removeKey(BTreeNode* node, int k) {
    if (!node) return;
    int idx = 0;
    while (idx < node->num_keys && node->keys[idx] < k) idx++;
    if (idx < node->num_keys && node->keys[idx] == k) {
        if (node->leaf) {
            removeFromLeaf(node, idx);
        }
    } else if (!node->leaf) {
        removeKey(node->children[idx], k);
    }
}

void freeTree(BTreeNode* node) {
    if (node == NULL) return;
    if (!node->leaf) {
        for (int i = 0; i <= node->num_keys; i++) {
            freeTree(node->children[i]);
        }
    }
    free(node);
}

int main() {
    BTreeNode* root = NULL;
    int keys[] = {10, 20, 5, 6, 12, 30, 7, 17};
    int n = sizeof(keys) / sizeof(keys[0]);

    for (int i = 0; i < n; i++) insert(&root, keys[i]);

    printf("Em-ordem: ");
    traverse(root);
    printf("\n");

    int searchKey = 12;
    printf("Busca %d: %s\n", searchKey, search(root, searchKey) ? "Encontrado" : "Nao encontrado");

    removeKey(root, 6);
    printf("Apos remover 6: ");
    traverse(root);
    printf("\n");

    freeTree(root);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Atualização da Raiz no Split Superior:** Na inserção, quando a raiz estoura a capacidade máxima ($2T - 1$ chaves), uma nova raiz deve ser alocada e o ponteiro principal da árvore deve ser atualizado (`*root = s`). Esquecer de passar `BTreeNode**` impede que a mudança da raiz se propague para fora da função, gerando acesso a memória inválida.
2. **Confusão entre Ordem $m$ e Grau Mínimo $t$:** Questões costumam misturar $m$ e $t$. Se a ordem é $m$, o nó tem no máximo $m-1$ chaves. Se é definido pelo grau mínimo $t$, o nó tem no máximo $2t-1$ chaves e $2t$ filhos. Confundir esses limites causa estouro de buffer (out-of-bounds) em arrays estáticos de nós.
3. **Liberar Memória sem Descer nos Filhos Restantes:** Como um nó com $k$ chaves possui $k+1$ ponteiros válidos de filhos, iterar apenas até `i < num_keys` ao dar `free` deixa o último filho (`children[num_keys]`) sem liberação, resultando em *memory leak*.

---

## 4. Exercicio com Gabarito

**Enunciado:** Considere uma Árvore B de Ordem $m = 3$ (capacidade máxima de 2 chaves por nó). A árvore está inicialmente vazia.
Insira sequencialmente as chaves **10, 20 e 30**. Descreva a estrutura resultante do nó raiz e de seus filhos após o término da última inserção.

---

**Gabarito/Solução:**

1. **Inserção de 10 e 20:** Ambas couberam no mesmo nó folha.
   - Estado: `[10, 20]` (Nó com 2 chaves).
2. **Inserção de 30:** O nó estoura a capacidade ($3$ chaves: `[10, 20, 30]`). Ocorre um **split**:
   - A chave mediana (**20**) sobe e torna-se a nova **raiz**.
   - O elemento à esquerda (**10**) torna-se o filho esquerdo da raiz.
   - O elemento à direita (**30**) torna-se o filho direito da raiz.

**Estrutura Final:**
- **Raiz:** Contém a chave `[20]`
- **Filho Esquerdo:** Contém a chave `[10]`
- **Filho Direito:** Contém a chave `[30]`