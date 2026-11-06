# Arvores AVL em C

## 1. Teoria e Complexidade

A Árvore AVL é uma Árvore Binária de Busca (ABB) auto-balanceada. Para cada nó, a diferença entre as alturas de suas subárvores esquerda e direita — chamada de **Fator de Balanceamento (FB)** — deve estar estritamente no conjunto $\{-1, 0, 1\}$, onde $FB = \text{altura}(Esq) - \text{altura}(Dir)$. Se $|FB| > 1$, a árvore está desbalanceada e exige reestruturação via rotações.

O rebalanceamento é feito por 4 tipos de rotações:
- **Simples à Direita (LL):** Nó desbalanceado com $FB = +2$ e filho esquerdo com $FB \ge 0$.
- **Simples à Esquerda (RR):** Nó desbalanceado com $FB = -2$ e filho direito com $FB \le 0$.
- **Dupla Esquerda-Direita (LR):** Nó desbalanceado com $FB = +2$ e filho esquerdo com $FB = -1$ (Rotação RR no filho, depois LL no nó).
- **Dupla Direita-Esquerda (RL):** Nó desbalanceado com $FB = -2$ e filho direito com $FB = +1$ (Rotação LL no filho, depois RR no nó).

Esse rigor mantém a altura da árvore sempre limitada a $O(\log n)$, garantindo que as operações não degenerem para $O(n)$ como em ABBs comuns.

| Operação | Caso Médio | Pior Caso | Espaço (Memória) |
| :--- | :--- | :--- | :--- |
| Busca | $O(\log n)$ | $O(\log n)$ | $O(1)$ iterativo / $O(\log n)$ pilha |
| Inserção | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ pilha recursiva |
| Remoção | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ pilha recursiva |

---

## 2. Implementacao Completa em C

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int key;
    int height;
    struct Node *left;
    struct Node *right;
} Node;

int height(Node *n) {
    return n ? n->height : 0;
}

int max(int a, int b) {
    return (a > b) ? a : b;
}

Node* createNode(int key) {
    Node* node = (Node*)malloc(sizeof(Node));
    node->key = key;
    node->height = 1;
    node->left = NULL;
    node->right = NULL;
    return node;
}

int getBalance(Node *n) {
    return n ? height(n->left) - height(n->right) : 0;
}

Node* rightRotate(Node *y) {
    Node *x = y->left;
    Node *T2 = x->right;

    x->right = y;
    y->left = T2;

    y->height = max(height(y->left), height(y->right)) + 1;
    x->height = max(height(x->left), height(x->right)) + 1;

    return x;
}

Node* leftRotate(Node *x) {
    Node *y = x->right;
    Node *T2 = y->left;

    y->left = x;
    x->right = T2;

    x->height = max(height(x->left), height(x->right)) + 1;
    y->height = max(height(y->left), height(y->right)) + 1;

    return y;
}

Node* insert(Node* node, int key) {
    if (!node) return createNode(key);

    if (key < node->key)
        node->left = insert(node->left, key);
    else if (key > node->key)
        node->right = insert(node->right, key);
    else
        return node;

    node->height = 1 + max(height(node->left), height(node->right));
    int balance = getBalance(node);

    // Caso LL
    if (balance > 1 && key < node->left->key)
        return rightRotate(node);

    // Caso RR
    if (balance < -1 && key > node->right->key)
        return leftRotate(node);

    // Caso LR
    if (balance > 1 && key > node->left->key) {
        node->left = leftRotate(node->left);
        return rightRotate(node);
    }

    // Caso RL
    if (balance < -1 && key < node->right->key) {
        node->right = rightRotate(node->right);
        return leftRotate(node);
    }

    return node;
}

Node* minValueNode(Node* node) {
    Node* current = node;
    while (current->left != NULL)
        current = current->left;
    return current;
}

Node* deleteNode(Node* root, int key) {
    if (!root) return root;

    if (key < root->key)
        root->left = deleteNode(root->left, key);
    else if (key > root->key)
        root->right = deleteNode(root->right, key);
    else {
        if (!root->left || !root->right) {
            Node *temp = root->left ? root->left : root->right;
            if (!temp) {
                temp = root;
                root = NULL;
            } else {
                *root = *temp;
            }
            free(temp);
        } else {
            Node* temp = minValueNode(root->right);
            root->key = temp->key;
            root->right = deleteNode(root->right, temp->key);
        }
    }

    if (!root) return root;

    root->height = 1 + max(height(root->left), height(root->right));
    int balance = getBalance(root);

    // Caso LL
    if (balance > 1 && getBalance(root->left) >= 0)
        return rightRotate(root);

    // Caso LR
    if (balance > 1 && getBalance(root->left) < 0) {
        root->left = leftRotate(root->left);
        return rightRotate(root);
    }

    // Caso RR
    if (balance < -1 && getBalance(root->right) <= 0)
        return leftRotate(root);

    // Caso RL
    if (balance < -1 && getBalance(root->right) > 0) {
        root->right = rightRotate(root->right);
        return leftRotate(root);
    }

    return root;
}

Node* search(Node* root, int key) {
    if (!root || root->key == key) return root;
    if (key < root->key) return search(root->left, key);
    return search(root->right, key);
}

void freeTree(Node* root) {
    if (!root) return;
    freeTree(root->left);
    freeTree(root->right);
    free(root);
}

void inOrder(Node* root) {
    if (!root) return;
    inOrder(root->left);
    printf("%d ", root->key);
    inOrder(root->right);
}

int main() {
    Node *root = NULL;

    root = insert(root, 10);
    root = insert(root, 20);
    root = insert(root, 30); // Forca rotação RR
    root = insert(root, 40);
    root = insert(root, 50); // Forca rotação RR
    root = insert(root, 25); // Forca rotação RL

    printf("Em-ordem da AVL: ");
    inOrder(root);
    printf("\nRaiz atual: %d\n", root->key);

    root = deleteNode(root, 30);
    printf("Em-ordem apos remover 30: ");
    inOrder(root);
    printf("\nNova raiz: %d\n", root->key);

    Node* found = search(root, 25);
    printf("Busca 25: %s\n", found ? "Encontrado" : "Nao encontrado");

    freeTree(root);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Acesso Direto à Altura em Ponteiros Nulos (`Segmentation Fault`):**  
   Fazer `node->left->height` sem verificar se `node->left` é `NULL`. **Solução:** Use sempre uma função auxiliar `int height(Node *n)` que retorna `0` quando `n == NULL`.

2. **Diferença de Checagem no Desbalanceamento: Inserção vs Remoção:**  
   Na inserção, decide-se o tipo de rotação comparando a chave inserida com a chave do filho (`key < node->left->key`). Na remoção, a chave original já foi removida! Deve-se usar o **Fator de Balanceamento do filho** (`getBalance(root->left) >= 0`) para escolher entre rotação simples ou dupla.

3. **Ordem Incorreta de Atualização de Alturas nas Rotações:**  
   Atualizar a altura do novo nó raiz antes de atualizar a altura do nó descendente causa valores corrompidos em cascata. **Regra:** Atualize sempre a altura do nó pivô antigo primeiro e, por último, a do nó que assumiu o topo da subárvore.

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função recursiva `int isAVL(Node* root)` que valide se uma árvore binária qualquer respeita a propriedade AVL (retorna `1` se for válida e `0` caso contrário).

**Gabarito:**

```c
int isAVL(Node* root) {
    if (!root) return 1;

    int balance = getBalance(root);
    
    // Verifica se o FB do nó atual está fora do intervalo [-1, 1]
    if (balance < -1 || balance > 1) 
        return 0;

    // Garante que as subárvores esquerda e direita também são AVL
    return isAVL(root->left) && isAVL(root->right);
}
```
*Explicação:* A função verifica de forma top-down se o fator de balanceamento do nó corrente está entre $-1$ e $1$. Se estiver correto, aplica recursivamente a verificação para as subárvores esquerda e direita. Se todas forem válidas, a árvore é uma AVL legítima.