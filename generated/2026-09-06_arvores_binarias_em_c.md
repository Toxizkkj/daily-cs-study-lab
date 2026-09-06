# Arvores Binarias em C

## 1. Teoria e Complexidade

Uma Árvore Binária é uma estrutura de dados hierárquica não linear onde cada nó possui no máximo dois filhos, denominados esquerdo e direito. Na variante de Árvore Binária de Busca (BST), os valores menores que o nó pai ficam à esquerda e os maiores à direita. A navegação na árvore é feita via ponteiros, e sua manipulação depende fortemente de recursão.

Os percursos determinam a ordem de visita aos nós: **Pré-ordem** (Raiz, Esquerda, Direita), **Em-ordem** (Esquerda, Raiz, Direita - resulta em dados ordenados numa BST) e **Pós-ordem** (Esquerda, Direita, Raiz). A altura da árvore representa a maior distância da raiz até uma folha. A desalocação da memória DEVE ser feita em **Pós-ordem** para garantir que os filhos sejam liberados antes do nó pai.

| Operação | Tempo (Médio) | Tempo (Pior Caso) | Espaço (Pior Caso) |
| :--- | :--- | :--- | :--- |
| Busca / Inserção | O(log N) | O(N) | O(N) |
| Percursos (Pré/Em/Pós) | O(N) | O(N) | O(N) |
| Cálculo de Altura | O(N) | O(N) | O(N) |
| Desalocação (`free`) | O(N) | O(N) | O(N) |

---

## 2. Implementacao Completa em C

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node *left;
    struct Node *right;
} Node;

Node* createNode(int value) {
    Node *newNode = (Node*) malloc(sizeof(Node));
    newNode->data = value;
    newNode->left = NULL;
    newNode->right = NULL;
    return newNode;
}

Node* insert(Node *root, int value) {
    if (root == NULL) return createNode(value);
    if (value < root->data) {
        root->left = insert(root->left, value);
    } else if (value > root->data) {
        root->right = insert(root->right, value);
    }
    return root;
}

Node* search(Node *root, int value) {
    if (root == NULL || root->data == value) return root;
    if (value < root->data) return search(root->left, value);
    return search(root->right, value);
}

void preOrder(Node *root) {
    if (root != NULL) {
        printf("%d ", root->data);
        preOrder(root->left);
        preOrder(root->right);
    }
}

void inOrder(Node *root) {
    if (root != NULL) {
        inOrder(root->left);
        printf("%d ", root->data);
        inOrder(root->right);
    }
}

void postOrder(Node *root) {
    if (root != NULL) {
        postOrder(root->left);
        postOrder(root->right);
        printf("%d ", root->data);
    }
}

int height(Node *root) {
    if (root == NULL) return -1;
    int leftHeight = height(root->left);
    int rightHeight = height(root->right);
    return (leftHeight > rightHeight ? leftHeight : rightHeight) + 1;
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

    root = insert(root, 50);
    insert(root, 30);
    insert(root, 70);
    insert(root, 20);
    insert(root, 40);

    printf("Pre-ordem:  "); preOrder(root);  printf("\n");
    printf("Em-ordem:   "); inOrder(root);   printf("\n");
    printf("Pos-ordem:  "); postOrder(root);  printf("\n");

    printf("Altura da arvore: %d\n", height(root));

    int val = 30;
    Node *found = search(root, val);
    printf("Busca (%d): %s\n", val, found ? "Encontrado" : "Nao encontrado");

    freeTree(root);
    root = NULL;

    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Acesso sem checagem de `NULL` (Segmentation Fault):** Tentar acessar `root->left` ou `root->right` sem verificar se `root == NULL` primeiro. Todo caso base de recursão em árvores deve tratar a raiz nula.
2. **Desalocação em Pré-ordem (Memory Leak / Dangling Pointer):** Executar `free(root)` antes de chamar a função para `root->left` e `root->right`. Isso faz com que os ponteiros para os filhos sejam perdidos na memória, tornando a liberação do restante da árvore impossível.
3. **Não reatribuir o retorno da Inserção:** Ao chamar `insert(root, val)`, esquecer de fazer `root = insert(root, val)`. Se a árvore estiver vazia (`NULL`), o ponteiro da `main` continuará apontando para `NULL`.

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função recursiva `int countNodes(Node *root)` que receba o ponteiro para a raiz de uma árvore binária e retorne a quantidade total de nós presentes nela.

**Gabarito:**

```c
int countNodes(Node *root) {
    if (root == NULL) {
        return 0; // Caso base: arvore/sub-arvore vazia possui 0 nos
    }
    // Soma o no atual (1) com a quantidade de nos das sub-arvores esquerda e direita
    return 1 + countNodes(root->left) + countNodes(root->right);
}
```

*Explicação:* Se a raiz é nula, a contagem é 0. Caso contrário, a função conta o nó corrente (`1`) e soma recursivamente o total de nós da sub-árvore esquerda e da sub-árvore direita.