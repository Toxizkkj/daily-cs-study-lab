# Arvores AVL em C

## 1. Teoria e Complexidade
Uma Árvore AVL é uma árvore binária de busca (BST) autobalanceada. Ela garante que a diferença de altura entre as subárvores esquerda e direita de qualquer nó — chamada de **Fator de Balanceamento (FB)** — seja no máximo $1$ ou $-1$. O cálculo é feito por: $FB = \text{altura}(Esq) - \text{altura}(Dir)$.

Se $|FB| > 1$, a árvore está desbalanceada. O rebalanceamento ocorre via rotações:
- **LL (Rotação Simples à Direita):** Inserção/Remoção no filho esquerdo da subárvore esquerda.
- **RR (Rotação Simples à Esquerda):** Inserção/Remoção no filho direito da subárvore direita.
- **LR (Rotação Dupla Esquerda-Direita):** Inserção no filho direito da subárvore esquerda (Rotação RR no filho esquerdo, depois LL no nó atual).
- **RL (Rotação Dupla Direita-Esquerda):** Inserção no filho esquerdo da subárvore direita (Rotação LL no filho direito, depois RR no nó atual).

| Operação | Caso Médio | Pior Caso | Espaço |
| :--- | :--- | :--- | :--- |
| Busca | $O(\log n)$ | $O(\log n)$ | $O(1)$ |
| Inserção | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ stack |
| Remoção | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ stack |

---

## 2. Implementacao Completa em C

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int key;
    struct Node *left;
    struct Node *right;
    int height;
} Node;

int height(Node *n) {
    return n ? n->height : 0;
}

int max(int a, int b) {
    return (a > b) ? a : b;
}

Node* create_node(int key) {
    Node *node = (Node*)malloc(sizeof(Node));
    node->key = key;
    node->left = NULL;
    node->right = NULL;
    node->height = 1;
    return node;
}

int get_balance(Node *n) {
    return n ? height(n->left) - height(n->right) : 0;
}

Node* right_rotate(Node *y) {
    Node *x = y->left;
    Node *T2 = x->right;

    x->right = y;
    y->left = T2;

    y->height = max(height(y->left), height(y->right)) + 1;
    x->height = max(height(x->left), height(x->right)) + 1;

    return x;
}

Node* left_rotate(Node *x) {
    Node *y = x->right;
    Node *T2 = y->left;

    y->left = x;
    x->right = T2;

    x->height = max(height(x->left), height(x->right)) + 1;
    y->height = max(height(y->left), height(y->right)) + 1;

    return y;
}

Node* insert(Node *node, int key) {
    if (!node) return create_node(key);

    if (key < node->key)
        node->left = insert(node->left, key);
    else if (key > node->key)
        node->right = insert(node->right, key);
    else
        return node;

    node->height = 1 + max(height(node->left), height(node->right));
    int balance = get_balance(node);

    // Casos de Desbalanceamento
    if (balance > 1 && key < node->left->key) // LL
        return right_rotate(node);

    if (balance < -1 && key > node->right->key) // RR
        return left_rotate(node);

    if (balance > 1 && key > node->left->key) { // LR
        node->left = left_rotate(node->left);
        return right_rotate(node);
    }

    if (balance < -1 && key < node->right->key) { // RL
        node->right = right_rotate(node->right);
        return left_rotate(node);
    }

    return node;
}

Node* min_value_node(Node *node) {
    Node *current = node;
    while (current->left)
        current = current->left;
    return current;
}

Node* delete_node(Node *root, int key) {
    if (!root) return root;

    if (key < root->key)
        root->left = delete_node(root->left, key);
    else if (key > root->key)
        root->right = delete_node(root->right, key);
    else {
        if (!root->left || !root->right) {
            Node *temp = root->left ? root->left : root->right;
            if (!temp) {
                temp = root;
                root = NULL;
            } else
                *root = *temp;
            free(temp);
        } else {
            Node *temp = min_value_node(root->right);
            root->key = temp->key;
            root->right = delete_node(root->right, temp->key);
        }
    }

    if (!root) return root;

    root->height = 1 + max(height(root->left), height(root->right));
    int balance = get_balance(root);

    if (balance > 1 && get_balance(root->left) >= 0) // LL
        return right_rotate(root);

    if (balance > 1 && get_balance(root->left) < 0) { // LR
        root->left = left_rotate(root->left);
        return right_rotate(root);
    }

    if (balance < -1 && get_balance(root->right) <= 0) // RR
        return left_rotate(root);

    if (balance < -1 && get_balance(root->right) > 0) { // RL
        root->right = right_rotate(root->right);
        return left_rotate(root);
    }

    return root;
}

Node* search(Node *root, int key) {
    if (!root || root->key == key)
        return root;
    if (key < root->key)
        return search(root->left, key);
    return search(root->right, key);
}

void free_tree(Node *root) {
    if (root) {
        free_tree(root->left);
        free_tree(root->right);
        free(root);
    }
}

void inorder(Node *root) {
    if (root) {
        inorder(root->left);
        printf("%d (FB: %d) ", root->key, get_balance(root));
        inorder(root->right);
    }
}

int main() {
    Node *root = NULL;

    // Teste de insercoes que forcam rebalanceamentos
    int keys[] = {10, 20, 30, 40, 50, 25};
    for (int i = 0; i < 6; i++)
        root = insert(root, keys[i]);

    printf("Em-ordem (Chave e FB):\n");
    inorder(root);
    printf("\n");

    // Teste de Busca
    int target = 25;
    Node *found = search(root, target);
    printf("Busca %d: %s\n", target, found ? "Encontrado" : "Nao encontrado");

    // Teste de Remoção
    root = delete_node(root, 30);
    printf("Apos remover 30:\n");
    inorder(root);
    printf("\n");

    free_tree(root);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Acessar nó `NULL` ao calcular Altura/FB:**
   - *Erro:* Fazer `node->left->height` sem verificar se `node->left` é `NULL`.
   - *Solução:* Use sempre a função auxiliar `height(Node *n)` que trata a verificação `n == NULL` retornando `0`.

2. **Esquecer de Atualizar Alturas nas Rotações:**
   - *Erro:* Trocar os ponteiros de pai e filho durante a rotação, mas esquecer de recalcular `node->height`.
   - *Consequência:* O FB dos ancestrais será calculado incorretamente nas chamadas recursivas superiores, quebrando o balanceamento de toda a árvore.

3. **Confundir a Ordem da Rotação Dupla (LR / RL):**
   - *Erro:* Para um nó desbalanceado à esquerda ($FB = 2$) cujo filho esquerdo tem $FB = -1$ (Caso LR), tentar aplicar a rotação no nó raiz antes de ajustar o filho.
   - *Regra:* Primeiro rotacione o **filho** na direção oposta, e depois o **pai**. (LR = Esquerda no filho, Direita no pai).

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função recursiva `int is_avl(Node *root)` que receba a raiz de uma árvore binária de busca e retorne `1` se ela for uma AVL válida (respeitando a propriedade $|FB| \le 1$ para todos os nós) ou `0` caso contrário.

**Gabarito:**

```c
int is_avl(Node *root) {
    if (!root) return 1;

    int balance = get_balance(root);

    if (balance < -1 || balance > 1)
        return 0;

    return is_avl(root->left) && is_avl(root->right);
}
```