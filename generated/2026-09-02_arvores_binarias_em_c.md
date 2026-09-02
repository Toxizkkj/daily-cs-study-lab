# Arvores Binarias em C

## 1. Teoria e Complexidade

Uma árvore binária é uma estrutura de dados hierárquica e não linear na qual cada nó possui no máximo dois filhos, referenciados como "esquerdo" e "direito". O nó inicial é chamado de raiz. Quando um nó não possui filhos, é chamado de folha. Devido à sua natureza recursiva, subárvores à esquerda e à direita também são árvores binárias.

A navegação e a manipulação dos nós dependem do uso de ponteiros e alocação dinâmica de memória. As operações clássicas de percurso visitam todos os nós de forma estruturada: **Pré-ordem** (Raiz, Esquerda, Direita), **Em-ordem** (Esquerda, Raiz, Direita) e **Pós-ordem** (Esquerda, Direita, Raiz). A desalocação de memória exige rigorosamente o percurso em Pós-ordem para evitar a perda de ponteiros para os filhos.

| Operação | Tempo (Médio) | Tempo (Pior Caso) | Espaço Auxiliar (Pilha Recursiva) |
| :--- | :--- | :--- | :--- |
| Busca / Inserção (BST) | $O(\log n)$ | $O(n)$ | $O(h)$ |
| Percursos (Pré/Em/Pós) | $O(n)$ | $O(n)$ | $O(h)$ |
| Cálculo de Altura | $O(n)$ | $O(n)$ | $O(h)$ |
| Desalocação (`freeTree`) | $O(n)$ | $O(n)$ | $O(h)$ |

*Nota: $n$ é o número total de nós e $h$ é a altura da árvore.*

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
    Node* newNode = (Node*)malloc(sizeof(Node));
    if (!newNode) return NULL;
    newNode->data = value;
    newNode->left = NULL;
    newNode->right = NULL;
    return newNode;
}

Node* insert(Node* root, int value) {
    if (root == NULL) {
        return createNode(value);
    }
    if (value < root->data) {
        root->left = insert(root->left, value);
    } else if (value > root->data) {
        root->right = insert(root->right, value);
    }
    return root;
}

void preOrder(Node* root) {
    if (root != NULL) {
        printf("%d ", root->data);
        preOrder(root->left);
        preOrder(root->right);
    }
}

void inOrder(Node* root) {
    if (root != NULL) {
        inOrder(root->left);
        printf("%d ", root->data);
        inOrder(root->right);
    }
}

void postOrder(Node* root) {
    if (root != NULL) {
        postOrder(root->left);
        postOrder(root->right);
        printf("%d ", root->data);
    }
}

int getHeight(Node* root) {
    if (root == NULL) {
        return -1; // Altura de árvore vazia
    }
    int leftHeight = getHeight(root->left);
    int rightHeight = getHeight(root->right);
    
    return (leftHeight > rightHeight ? leftHeight : rightHeight) + 1;
}

void freeTree(Node* root) {
    if (root != NULL) {
        freeTree(root->left);
        freeTree(root->right);
        free(root);
    }
}

int main() {
    Node* root = NULL;

    // Construção de uma Árvore Binária de Busca (BST)
    root = insert(root, 50);
    insert(root, 30);
    insert(root, 70);
    insert(root, 20);
    insert(root, 40);

    printf("Pre-ordem: ");
    preOrder(root);
    printf("\n");

    printf("Em-ordem: ");
    inOrder(root);
    printf("\n");

    printf("Pos-ordem: ");
    postOrder(root);
    printf("\n");

    printf("Altura da arvore: %d\n", getHeight(root));

    // Desalocação da memória
    freeTree(root);
    root = NULL;

    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Dereferência de Ponteiro Nulo (`Segmentation Fault`)**: Esquecer a condição base `if (root == NULL)` no início de funções recursivas. Tentar acessar `root->left` ou `root->right` em um nó inexistente resulta em travamento imediato do programa.
2. **Ordem Incorreta na Desalocação (`Use-After-Free` / `Memory Leak`)**: Tentar dar `free(root)` antes de desalocar as subárvores esquerda e direita. Se você liberar o nó pai primeiro, perderá as referências para `root->left` e `root->right`, causando vazamento de memória ou acesso inválido. A liberação **deve ser obrigatoriamente em Pós-ordem**.
3. **Não atualizar ponteiro da Raiz**: Em funções de inserção, esquecer de atribuir o retorno da função à subárvore correspondente (`root->left = insert(...)`). Sem essa atribuição, as modificações feitas nas chamadas recursivas são perdidas na pilha de execução.

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função recursiva em C chamada `countNodes` que receba o ponteiro para a raiz de uma árvore binária e retorne a quantidade total de nós presentes nessa árvore.

**Gabarito:**

```c
int countNodes(Node* root) {
    // Caso base: árvore vazia tem 0 nós
    if (root == NULL) {
        return 0;
    }
    // O total de nós é 1 (nó atual) + subárvore esquerda + subárvore direita
    return 1 + countNodes(root->left) + countNodes(root->right);
}
```

*Explicação:* A função percorre recursivamente a árvore. Se a raiz for nula, retorna `0`. Caso contrário, soma `1` (relativo ao nó corrente) ao resultado da contagem da subárvore esquerda e da subárvore direita, resultando na complexidade de tempo $O(n)$.