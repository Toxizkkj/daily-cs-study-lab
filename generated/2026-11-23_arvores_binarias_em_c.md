# Arvores Binarias em C

## 1. Teoria e Complexidade
Uma Árvore Binária é uma estrutura de dados não linear e hierárquica onde cada elemento (nó) possui no máximo dois filhos, referenciados como filho esquerdo e filho direito. A navegação e manipulação da árvore são essencialmente recursivas, sendo a estrutura base para Árvores Binárias de Busca (BST), Árvores AVL e Red-Black.

Os percursos definem a ordem de visita aos nós: **Pré-ordem** (Raiz, Esquerda, Direita) é usada para clonagem/serialização; **Em-ordem** (Esquerda, Raiz, Direita) visita nós de uma BST em ordem crescente; **Pós-ordem** (Esquerda, Direita, Raiz) é obrigatória para desalocação de memória, garantindo que os filhos sejam liberados antes do pai.

| Operação | Complexidade de Tempo (Médio) | Complexidade de Tempo (Pior Caso) | Espaço em Memória (Pilha de Recursão) |
| :--- | :--- | :--- | :--- |
| Busca / Inserção | $O(\log n)$ (em BST balanceada) | $O(n)$ (árvore degenerada/linha) | $O(h)$ onde $h$ é a altura da árvore |
| Percursos (Pré/Em/Pós) | $O(n)$ | $O(n)$ | $O(h)$ |
| Cálculo de Altura | $O(n)$ | $O(n)$ | $O(h)$ |
| Desalocação (free) | $O(n)$ | $O(n)$ | $O(h)$ |

---

## 2. Implementacao Completa em C

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node* left;
    struct Node* right;
} Node;

Node* createNode(int val) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    newNode->data = val;
    newNode->left = NULL;
    newNode->right = NULL;
    return newNode;
}

Node* insert(Node* root, int val) {
    if (root == NULL) return createNode(val);
    if (val < root->data) {
        root->left = insert(root->left, val);
    } else if (val > root->data) {
        root->right = insert(root->right, val);
    }
    return root;
}

void preOrder(Node* root) {
    if (root == NULL) return;
    printf("%d ", root->data);
    preOrder(root->left);
    preOrder(root->right);
}

void inOrder(Node* root) {
    if (root == NULL) return;
    inOrder(root->left);
    printf("%d ", root->data);
    inOrder(root->right);
}

void postOrder(Node* root) {
    if (root == NULL) return;
    postOrder(root->left);
    postOrder(root->right);
    printf("%d ", root->data);
}

int getHeight(Node* root) {
    if (root == NULL) return -1; // Altura baseada em arestas (-1 para arvore vazia)
    int leftH = getHeight(root->left);
    int rightH = getHeight(root->right);
    return 1 + (leftH > rightH ? leftH : rightH);
}

void freeTree(Node* root) {
    if (root == NULL) return;
    freeTree(root->left);  // 1. Libera subárvore esquerda
    freeTree(root->right); // 2. Libera subárvore direita
    free(root);            // 3. Libera o nó atual (Pós-ordem)
}

int main() {
    Node* root = NULL;

    // Construcao da arvore: 50, 30, 70, 20, 40
    root = insert(root, 50);
    insert(root, 30);
    insert(root, 70);
    insert(root, 20);
    insert(root, 40);

    printf("Pre-ordem:  "); preOrder(root);  printf("\n");
    printf("Em-ordem:   "); inOrder(root);   printf("\n");
    printf("Pos-ordem:  "); postOrder(root); printf("\n");

    printf("Altura da arvore: %d\n", getHeight(root));

    freeTree(root);
    root = NULL;

    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Desalocação em Pré-ordem ou Em-ordem (`Use-After-Free`)**:
   Fazer `free(root)` antes de chamar a recursão para os filhos (`free(root); freeTree(root->left);`) gera acesso inválido à memória (`Segmentation Fault`), pois o ponteiro `root->left` é lido após `root` ter sido liberado. A desalocação deve **obrigatoriamente** ser em pós-ordem.

2. **Esquecer o caso base (`root == NULL`) na recursão**:
   Acessar `root->left` sem testar se `root` é `NULL` resulta em falha de segmentação imediata ao atingir as folhas da árvore.

3. **Convenção de Altura (Arestas vs. Nós)**:
   Fique atento ao enunciado: a altura de uma árvore com apenas 1 nó pode ser `0` (contagem de arestas) ou `1` (contagem de nós). Se for por arestas, o caso base para `NULL` deve retornar `-1`.

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função recursiva `int countLeaves(Node* root)` que retorne o número total de nós folha (nós que não possuem filhos esquerdo e nem direito) em uma árvore binária.

**Gabarito:**

```c
int countLeaves(Node* root) {
    // Caso 1: Arvore ou subarvore vazia
    if (root == NULL) {
        return 0;
    }
    // Caso 2: O no atual e uma folha (nao tem filhos)
    if (root->left == NULL && root->right == NULL) {
        return 1;
    }
    // Caso 3: Soma das folhas da subarvore esquerda e direita
    return countLeaves(root->left) + countLeaves(root->right);
}
```