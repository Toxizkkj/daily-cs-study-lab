# Arvores AVL em C

## 1. Teoria e Complexidade

Uma Árvore AVL é uma Árvore Binária de Busca (BST) auto-balanceada na qual a diferença entre as alturas das subárvores esquerda e direita de qualquer nó — chamada de **Fator de Balanceamento (FB)** — deve ser no máximo 1 em valor absoluto ($FB = h_{esq} - h_{dir} \in \{-1, 0, 1\}$). Quando uma inserção ou remoção faz o $|FB|$ de algum nó atingir 2, a árvore reestrutura seus ponteiros localmente através de **Rotações** (Simples: LL, RR; ou Duplas: LR, RL) para restabelecer o equilíbrio.

O rigor do fator de balanceamento garante que a altura $h$ da árvore seja sempre limitada superiormente por $O(\log n)$. Consequentemente, elimina-se o risco de degradação para o pior caso de uma BST padrão ($O(n)$ em dados ordenados), garantindo desempenho genérico e previsível para aplicações de tempo crítico.

| Operação | Caso Médio | Pior Caso | Complexidade de Espaço |
| :--- | :--- | :--- | :--- |
| **Busca** | $O(\log n)$ | $O(\log n)$ | $O(n)$ |
| **Inserção** | $O(\log n)$ | $O(\log n)$ | $O(n)$ |
| **Remoção** | $O(\log n)$ | $O(\log n)$ | $O(n)$ |

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
    return (n == NULL) ? 0 : n->height;
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
    return (n == NULL) ? 0 : height(n->left) - height(n->right);
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
    if (node == NULL) return createNode(key);

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
        return rotateRight(node);

    // Caso RR
    if (balance < -1 && key > node->right->key)
        return rotateLeft(node);

    // Caso LR
    if (balance > 1 && key > node->left->key) {
        node->left = rotateLeft(node->left);
        return rotateRight(node);
    }

    // Caso RL
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
    if (root == NULL) return root;

    if (key < root->key)
        root->left = deleteNode(root->left, key);
    else if (key > root->key)
        root->right = deleteNode(root->right, key);
    else {
        if ((root->left == NULL) || (root->right == NULL)) {
            Node *temp = root->left ? root->left : root->right;
            if (temp == NULL) {
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

    if (root == NULL) return root;

    root->height = 1 + max(height(root->left), height(root->right));
    int balance = getBalance(root);

    // Rebalanceamento pós-remoção
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
    if (root == NULL || root->key == key)
        return root;
    if (key < root->key)
        return search(root->left, key);
    return search(root->right, key);
}

void preOrder(Node *root) {
    if (root != NULL) {
        printf("%d ", root->key);
        preOrder(root->left);
        preOrder(root->right);
    }
}

void freeTree(Node* root) {
    if (root != NULL) {
        freeTree(root->left);
        freeTree(root->right);
        free(root);
    }
}

int main() {
    Node *root = NULL;

    // Inserções que forçam rotações (LL, RR, LR, RL)
    root = insert(root, 10);
    root = insert(root, 20);
    root = insert(root, 30); // Rotação Simples RR
    root = insert(root, 40);
    root = insert(root, 50); // Rotação Simples RR
    root = insert(root, 25); // Rotação Dupla RL

    printf("Pre-Ordem da AVL construida: ");
    preOrder(root);
    printf("\n");

    // Busca
    int target = 30;
    Node* found = search(root, target);
    printf("Busca (%d): %s\n", target, found ? "Encontrado" : "Nao encontrado");

    // Remoção
    root = deleteNode(root, 30);
    printf("Pre-Ordem apos remover 30: ");
    preOrder(root);
    printf("\n");

    freeTree(root);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Acesso Direto ao Ponteiro `NULL` (Segfault na Altura):**
   Acessar `node->height` sem tratar se `node` é `NULL` resulta em falha de segmentação. É indispensável utilizar uma função auxiliar (`height(node)`) que retorne `0` para ponteiros nulos antes de realizar cálculos de altura ou FB.

2. **Ordem Incorreta de Atualização de Alturas nas Rotações:**
   Na rotação, a altura do nó descendente promovido deve ser calculada **após** a atualização da altura do nó ancestral rebaixado. Inverter a ordem das atribuições gera alturas inconsistentes nos nós superiores da árvore.

3. **Confundir Casos de Rotação Dupla (LR / RL):**
   Tratar um desbalanceamento `LR` ($FB = +2$ e filho esquerdo com $FB = -1$) usando apenas uma rotação simples à direita produz uma árvore incorreta. É obrigatório aplicar primeiro a rotação à esquerda no filho e, em seguida, a rotação à direita na raiz da subárvore.

---

## 4. Exercicio com Gabarito

**Enunciado:**
Escreva uma função recursiva em C com a assinatura `int ehAVL(Node* root)` que retorne `1` se uma árvore binária atende estritamente às propriedades de balanceamento AVL ($FB \in \{-1, 0, 1\}$ em todos os nós) e `0` caso contrário. Assuma que a função `height(Node*)` já está disponível.

**Gabarito Explicado:**
Para ser AVL, cada nó deve ser nulo OU ter um Fator de Balanceamento entre -1 e 1 **e** ambas as suas subárvores também devem ser árvores AVL válidas.

```c
int ehAVL(Node* root) {
    if (root == NULL) 
        return 1;

    int fb = height(root->left) - height(root->right);

    if (fb < -1 || fb > 1) 
        return 0;

    return ehAVL(root->left) && ehAVL(root->right);
}
```