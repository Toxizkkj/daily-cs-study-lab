# Arvores AVL em C

## 1. Teoria e Complexidade

Uma Árvore AVL é uma Árvore Binária de Busca (ABB) auto-balanceada. A propriedade fundamental é que, para qualquer nó, a diferença entre as alturas de suas subárvores esquerda e direita (chamada de **Fator de Balanceamento - FB**) deve ser no máximo $\pm 1$. 

$$FB(nó) = altura(esquerda) - altura(direita)$$

Se $|FB| > 1$, a árvore está desbalanceada. O rebalanceamento é feito através de **rotações**:
- **Rotação Simples à Direita (LL):** Nó desbalanceado com $FB = +2$ e filho com $FB \ge 0$.
- **Rotação Simples à Esquerda (RR):** Nó desbalanceado com $FB = -2$ e filho com $FB \le 0$.
- **Rotação Dupla Esquerda-Direita (LR):** Nó com $FB = +2$ e filho com $FB < 0$ (Rotação à esquerda no filho, depois à direita no nó).
- **Rotação Dupla Direita-Esquerda (RL):** Nó com $FB = -2$ e filho com $FB > 0$ (Rotação à direita no filho, depois à esquerda no nó).

Ao manter a altura estritamente delimitada a $O(\log n)$, a AVL garante que o pior caso de busca, inserção e remoção não degrade para $O(n)$ como em ABBs comuns.

### Tabela de Complexidade

| Operação | Caso Médio | Pior Caso | Complexidade de Espaço |
| :--- | :--- | :--- | :--- |
| **Busca** | $O(\log n)$ | $O(\log n)$ | $O(1)$ auxiliar |
| **Inserção** | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ pilha de recursão |
| **Remoção** | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ pilha de recursão |
| **Espaço Total** | $O(n)$ | $O(n)$ | $O(n)$ |

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

int getHeight(Node *n) {
    return (n == NULL) ? 0 : n->height;
}

int getMax(int a, int b) {
    return (a > b) ? a : b;
}

int getBalance(Node *n) {
    return (n == NULL) ? 0 : getHeight(n->left) - getHeight(n->right);
}

Node* createNode(int key) {
    Node* node = (Node*)malloc(sizeof(Node));
    node->key = key;
    node->height = 1;
    node->left = NULL;
    node->right = NULL;
    return node;
}

Node* rotateRight(Node *y) {
    Node *x = y->left;
    Node *T2 = x->right;

    x->right = y;
    y->left = T2;

    y->height = getMax(getHeight(y->left), getHeight(y->right)) + 1;
    x->height = getMax(getHeight(x->left), getHeight(x->right)) + 1;

    return x;
}

Node* rotateLeft(Node *x) {
    Node *y = x->right;
    Node *T2 = y->left;

    y->left = x;
    x->right = T2;

    x->height = getMax(getHeight(x->left), getHeight(x->right)) + 1;
    y->height = getMax(getHeight(y->left), getHeight(y->right)) + 1;

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

    node->height = 1 + getMax(getHeight(node->left), getHeight(node->right));
    int balance = getBalance(node);

    // Casos de Rotação
    if (balance > 1 && key < node->left->key)
        return rotateRight(node); // LL
    if (balance < -1 && key > node->right->key)
        return rotateLeft(node); // RR
    if (balance > 1 && key > node->left->key) {
        node->left = rotateLeft(node->left);
        return rotateRight(node); // LR
    }
    if (balance < -1 && key < node->right->key) {
        node->right = rotateRight(node->right);
        return rotateLeft(node); // RL
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

    root->height = 1 + getMax(getHeight(root->left), getHeight(root->right));
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

void freeTree(Node* root) {
    if (root != NULL) {
        freeTree(root->left);
        freeTree(root->right);
        free(root);
    }
}

void printInOrder(Node* root) {
    if (root != NULL) {
        printInOrder(root->left);
        printf("%d (h:%d) ", root->key, root->height);
        printInOrder(root->right);
    }
}

int main() {
    Node *root = NULL;

    int values[] = {10, 20, 30, 40, 50, 25};
    for (int i = 0; i < 6; i++) {
        root = insert(root, values[i]);
    }

    printf("Em-ordem apos insercoes: ");
    printInOrder(root);
    printf("\nRaiz atual: %d\n", root->key);

    int searchKey = 30;
    Node* found = search(root, searchKey);
    printf("Busca (%d): %s\n", searchKey, found ? "Encontrado" : "Nao Encontrado");

    root = deleteNode(root, 30);
    printf("Em-ordem apos deletar 30: ");
    printInOrder(root);
    printf("\n");

    freeTree(root);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Acesso Direto à Altura Sem Validar `NULL` (Segmentation Fault):**
   - *Erro:* Fazer `node->left->height` diretamente. Se `node->left` for `NULL`, ocorre erro de segmentação.
   - *Solução:* Sempre usar uma função auxiliar (ex: `getHeight(node)`) que retorne `0` caso o ponteiro seja `NULL`.

2. **Esquecer de Atualizar Alturas Durante as Rotações:**
   - *Erro:* Ajustar os ponteiros de rotação (`left` e `right`) mas esquecer de recalcular a altura dos nós manipulados.
   - *Solução:* Recalcular as alturas dos dois nós alterados dentro da própria função de rotação, respeitando a ordem de baixo para cima.

3. **Verificação Incorreta de Condição para Rotações Duplas:**
   - *Erro:* Tratar um desbalanceamento em zig-zag (LR ou RL) usando rotação simples.
   - *Solução:* Na inserção, verificar o valor inserido com a chave do filho; na remoção, verificar o $FB$ do filho para determinar se é necessário transformar primeiro o filho (ex: $FB_{pai} = +2$ e $FB_{filho\_esq} < 0 \implies \text{LR}$).

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função em C que receba a raiz de uma árvore binária e retorne `1` se ela for uma árvore AVL válida (respeita a propriedade de BST e o fator de balanceamento em todos os nós) ou `0` caso contrário. Pode assumir a existência de `getHeight(Node* n)`.

### Gabarito

```c
#include <limits.h>

int isBSTUtil(Node* node, int min, int max) {
    if (node == NULL) return 1;
    if (node->key <= min || node->key >= max) return 0;
    return isBSTUtil(node->left, min, node->key) && 
           isBSTUtil(node->right, node->key, max);
}

int isBalancedAVL(Node* root) {
    if (root == NULL) return 1;

    int lh = getHeight(root->left);
    int rh = getHeight(root->right);
    int fb = lh - rh;

    if (fb < -1 || fb > 1) return 0;

    return isBalancedAVL(root->left) && isBalancedAVL(root->right);
}

int isAVL(Node* root) {
    return isBSTUtil(root, INT_MIN, INT_MAX) && isBalancedAVL(root);
}
```
*Explicação:* A solução valida duas condições separadas: 1) Se a estrutura é uma BST válida comparando os valores dentro de limites min/max; 2) Se o fator de balanceamento ($|lh - rh| \le 1$) é respeitado recursivamente em todos os nós.