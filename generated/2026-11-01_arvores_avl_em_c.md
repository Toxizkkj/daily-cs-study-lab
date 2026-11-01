# Arvores AVL em C

## 1. Teoria e Complexidade

Uma Árvore AVL é uma Árvore Binária de Busca (BST) autobalanceada. Para cada nó, a diferença entre a altura da subárvore esquerda e a da subárvore direita — chamada de **Fator de Balanceamento ($FB$)** — deve ser $-1$, $0$ ou $1$ ($FB = h_{esq} - h_{dir}$). Quando o $|FB| > 1$, ocorrem rotações simples (LL, RR) ou duplas (LR, RL) para reestruturar os ponteiros e restaurar o equilíbrio da árvore em tempo $O(1)$.

O balanceamento contínuo garante que a altura da árvore seja estritamente limitada a $O(\log n)$, evitando a degradação para uma lista encadeada (pior caso da BST comum).

| Operação | Caso Médio | Pior Caso | Espaço |
| :--- | :--- | :--- | :--- |
| **Busca** | $O(\log n)$ | $O(\log n)$ | $O(1)$ |
| **Inserção** | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ (pilha) |
| **Remoção** | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ (pilha) |

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
    node->left = NULL;
    node->right = NULL;
    node->height = 1;
    return node;
}

int getBalance(Node *n) {
    return n ? height(n->left) - height(n->right) : 0;
}

Node* rotateRight(Node *y) {
    Node *x = y->left;
    Node *T2 = x->right;

    x->right = y;
    y->left = T2;

    y->height = max(height(y->left), height(y->right)) + 1;
    x->height = max(height(x->left), height(x->right)) + 1;

    return x;
}

Node* rotateLeft(Node *x) {
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

    // LL
    if (balance > 1 && key < node->left->key)
        return rotateRight(node);
    // RR
    if (balance < -1 && key > node->right->key)
        return rotateLeft(node);
    // LR
    if (balance > 1 && key > node->left->key) {
        node->left = rotateLeft(node->left);
        return rotateRight(node);
    }
    // RL
    if (balance < -1 && key < node->right->key) {
        node->right = rotateRight(node->right);
        return rotateLeft(node);
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

    // Rebalanceamento apos remocao
    if (balance > 1 && getBalance(root->left) >= 0)
        return rotateRight(root);
    if (balance > 1 && getBalance(root->left) < 0) {
        root->left = rotateLeft(root->left);
        return rotateRight(root);
    }
    if (balance < -1 && getBalance(root->right) <= 0)
        return rotateLeft(root);
    if (balance < -1 && getBalance(root->right) > 0) {
        root->right = rotateRight(root->right);
        return rotateLeft(root);
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

void inorder(Node* root) {
    if (root) {
        inorder(root->left);
        printf("[%d | h:%d] ", root->key, root->height);
        inorder(root->right);
    }
}

int main() {
    Node *root = NULL;

    // Teste de inserção com rotações
    int elements[] = {10, 20, 30, 40, 50, 25};
    for (int i = 0; i < 6; i++) {
        root = insert(root, elements[i]);
    }

    printf("Em-ordem [Valor | Altura]: ");
    inorder(root);
    printf("\n");

    // Teste de busca
    int target = 25;
    Node *found = search(root, target);
    printf("Busca por %d: %s\n", target, found ? "Encontrado" : "Nao Encontrado");

    // Teste de remoção
    root = deleteNode(root, 30);
    printf("Apos remover 30: ");
    inorder(root);
    printf("\n");

    freeTree(root);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Acesso Direto à Altura de Nó Nulo (`Segmentation Fault`):**  
   Tentar ler `node->height` sem verificar se `node == NULL`. A solução obrigatória é usar a função auxilar `height(n)` que trata ponteiros nulos retornando $0$.

2. **Ordem Incorreta da Atualização de Alturas nas Rotações:**  
   Ao girar os nós (ex: em `rotateRight`), a altura do nó filho que subiu deve ser calculada **depois** da altura do nó pai que desceu. Inverter essa ordem gera alturas desatualizadas nos nós superiores.

3. **Confusão entre Rotação Simples e Dupla:**  
   Decidir entre LL/LR (ou RR/RL) depende da chave inserida em relação ao filho, ou do sinal do $FB$ do filho durante a remoção. Ignorar o sinal do filho leva a aplicar uma rotação simples onde uma dupla era necessária, corrompendo a estrutura de busca.

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função recursiva `int isAVL(Node* root)` que retorna `1` se a árvore for uma AVL válida (respeita a propriedade de BST e $|FB| \le 1$ em todos os nós) ou `0` caso contrário.

**Gabarito:**

```c
int isAVL(Node* root) {
    if (!root) return 1;

    int balance = getBalance(root);
    if (balance < -1 || balance > 1) return 0;

    // Checa propriedade de BST local
    if (root->left && root->left->key >= root->key) return 0;
    if (root->right && root->right->key <= root->key) return 0;

    // Recursão para as subárvores
    return isAVL(root->left) && isAVL(root->right);
}
```