# Arvores AVL em C

## 1. Teoria e Complexidade

Uma Árvore AVL é uma árvore binária de busca (BST) auto-balanceada. A propriedade fundamental da AVL é a **propriedade de balanceamento**: para qualquer nó, a diferença de altura entre suas subárvores esquerda e direita — chamada de **Fator de Balanceamento (FB)** — deve ser no máximo 1 em valor absoluto. 
$$\text{FB}(N) = \text{altura}(N \to \text{esquerda}) - \text{altura}(N \to \text{direita})$$

Se $\text{FB} \in \{-1, 0, 1\}$, o nó está balanceado. Se $|\text{FB}| > 1$, a árvore precisa de rebalanceamento imediato por meio de **rotações**:
- **Rotação Simples à Direita (LL):** Aplicada quando a desordem ocorre na subárvore esquerda do filho esquerdo ($\text{FB} > 1$ e $\text{FB}_{\text{filho\_esq}} \ge 0$).
- **Rotação Simples à Esquerda (RR):** Aplicada quando a desordem ocorre na subárvore direita do filho direito ($\text{FB} < -1$ e $\text{FB}_{\text{filho\_dir}} \le 0$).
- **Rotação Dupla Esquerda-Direita (LR):** Rotação simples à esquerda no filho esquerdo, seguida de rotação simples à direita no pai ($\text{FB} > 1$ e $\text{FB}_{\text{filho\_esq}} < 0$).
- **Rotação Dupla Direita-Esquerda (RL):** Rotação simples à direita no filho direito, seguida de rotação simples à esquerda no pai ($\text{FB} < -1$ e $\text{FB}_{\text{filho\_dir}} > 0$).

| Operação | Caso Médio | Pior Caso | Espaço |
| :--- | :--- | :--- | :--- |
| **Busca** | $O(\log n)$ | $O(\log n)$ | $O(1)$ |
| **Inserção** | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ (pilha de recursão) |
| **Remoção** | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ (pilha de recursão) |

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
    Node *node = (Node*)malloc(sizeof(Node));
    node->key = key;
    node->left = NULL;
    node->right = NULL;
    node->height = 1;
    return node;
}

int getBalance(Node *n) {
    return (n == NULL) ? 0 : height(n->left) - height(n->right);
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

Node* insert(Node *node, int key) {
    if (node == NULL) return createNode(key);

    if (key < node->key)
        node->left = insert(node->left, key);
    else if (key > node->key)
        node->right = insert(node->right, key);
    else
        return node; // Chaves duplicadas nao sao permitidas

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

Node* minValueNode(Node *node) {
    Node *current = node;
    while (current->left != NULL)
        current = current->left;
    return current;
}

Node* deleteNode(Node *root, int key) {
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
            Node *temp = minValueNode(root->right);
            root->key = temp->key;
            root->right = deleteNode(root->right, temp->key);
        }
    }

    if (root == NULL) return root;

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

Node* search(Node *root, int key) {
    if (root == NULL || root->key == key)
        return root;
    if (key < root->key)
        return search(root->left, key);
    return search(root->right, key);
}

void inOrder(Node *root) {
    if (root != NULL) {
        inOrder(root->left);
        printf("%d (FB: %d) ", root->key, getBalance(root));
        inOrder(root->right);
    }
}

void freeTree(Node *root) {
    if (root != NULL) {
        freeTree(root->left);
        freeTree(root->right);
        free(root);
    }
}

int main() {
    Node *root = NULL;

    // Insercoes testando casos de rebalanceamento
    int keys[] = {10, 20, 30, 40, 50, 25};
    for (int i = 0; i < 6; i++) {
        root = insert(root, keys[i]);
    }

    printf("Em-ordem apos insercoes (Valor e FB):\n");
    inOrder(root);
    printf("\n\nRaiz atual: %d\n", root->key);

    // Teste de busca
    int target = 25;
    Node *found = search(root, target);
    printf("Busca por %d: %s\n", target, found ? "Encontrado" : "Nao encontrado");

    // Teste de remocao
    printf("\nRemovendo 40...\n");
    root = deleteNode(root, 40);
    printf("Em-ordem apos remocao:\n");
    inOrder(root);
    printf("\n");

    freeTree(root);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Acessar ponteiros nulos ao calcular FB:** Tentar ler `node->left->height` diretamente sem tratar se `node->left` é `NULL`. Causa *Segmentation Fault*. A função auxiliar `height(n)` deve checar `if (n == NULL) return 0;`.
2. **Esquecer de atualizar a altura após rotações:** Rotações alteram a topologia da árvore. Se as alturas de $x$ e $y$ não forem recalculadas **na ordem correta** (primeiro o nó baixado, depois a nova raiz) durante a rotação, o Fator de Balanceamento calculado nos nós superiores estará incorreto.
3. **Condição de balanceamento na Remoção:** Na remoção, o teste do sinal do FB do filho é diferente da inserção:
   - Na inserção: compara-se a `key` inserida com a chave do filho.
   - Na remoção: compara-se o `getBalance(filho)` com `0` (ex: `getBalance(root->left) >= 0`). Tratar remoção com a lógica da inserção resulta em rotação incorreta ou falha de balanceamento.

---

## 4. Exercicio com Gabarito

**Enunciado:** Trace a inserção passo a passo da sequência de chaves `[30, 20, 10, 25, 28]` em uma árvore AVL inicialmente vazia. Indique quais rotações ocorrem e a chave que se torna a raiz principal ao final.

---

**Gabarito:**

1. **Inserir 30, 20, 10:**
   - Inserir 30: Raiz = 30.
   - Inserir 20: Filho esquerdo de 30.
   - Inserir 10: Filho esquerdo de 20.
   - **Desbalanceamento em 30** ($\text{FB} = +2$, filho esq $20$ tem $\text{FB} = +1$). Caso **LL**.
   - **Ação:** Rotação Simples à Direita em 30.
   - *Subárvore resultante:* Raiz = 20, Esquerda = 10, Direita = 30.

2. **Inserir 25:**
   - Vai para a esquerda de 30 (20->right = 30, 30->left = 25).
   - Árvore balanceada.

3. **Inserir 28:**
   - Vai para a direita de 25 (30->left = 25, 25->right = 28).
   - Verificação de balanceamento nos ancestrais:
     - Nó 30: $\text{FB} = +2$ (esquerda altura 2 [25, 28], direita altura 0).
     - Nó 25 (filho esquerdo de 30): $\text{FB} = -1$ (sua subárvore direita é maior).
   - Caso **LR (Dupla Esquerda-Direita)** no nó 30:
     - 1º: Rotação Simples à Esquerda no nó 25.
     - 2º: Rotação Simples à Direita no nó 30.
   - *Subárvore resultante:* Nó 28 sobe para o lugar do 30. 28 tem filho esquerdo 25 e filho direito 30.

**Resultado Final:**
- **Estrutura da Árvore:**
        20
       /  \
     10    28
          /  \
        25    30
- **Raiz Principal Final:** `20`
- **Rotações Realizadas:** 1 Rotação Simples à Direita (LL) e 1 Rotação Dupla Esquerda-Direita (LR).