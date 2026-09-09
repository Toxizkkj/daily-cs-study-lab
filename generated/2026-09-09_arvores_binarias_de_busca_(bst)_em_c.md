# Arvores Binarias de Busca (BST) em C

## 1. Teoria e Complexidade

Uma **Árvore Binária de Busca (BST)** é uma estrutura de dados onde cada nó possui no máximo dois filhos. A **propriedade de ordenação** estabelece que, para qualquer nó $X$:
- Todos os elementos na subárvore **esquerda** possuem chaves **menores** que a chave de $X$.
- Todos os elementos na subárvore **direita** possuem chaves **maiores** que a chave de $X$.

O desempenho das operações em uma BST depende diretamente da altura da árvore ($h$). No melhor caso (árvore balanceada), $h = \log_2(n)$. No pior caso (árvore degenerada/lista encadeada), $h = n$.

| Operação | Caso Médio (Balanceada) | Pior Caso (Degenerada) | Espaço (Pilha Recursiva) |
| :--- | :--- | :--- | :--- |
| **Busca** | $O(\log n)$ | $O(n)$ | $O(h)$ |
| **Inserção** | $O(\log n)$ | $O(n)$ | $O(h)$ |
| **Remoção** | $O(\log n)$ | $O(n)$ | $O(h)$ |

---

## 2. Implementacao Completa em C

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int key;
    struct Node *left;
    struct Node *right;
} Node;

Node* createNode(int key) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    newNode->key = key;
    newNode->left = NULL;
    newNode->right = NULL;
    return newNode;
}

Node* insert(Node* root, int key) {
    if (root == NULL) return createNode(key);
    
    if (key < root->key)
        root->left = insert(root->left, key);
    else if (key > root->key)
        root->right = insert(root->right, key);
        
    return root;
}

Node* search(Node* root, int key) {
    if (root == NULL || root->key == key)
        return root;
        
    if (key < root->key)
        return search(root->left, key);
        
    return search(root->right, key);
}

Node* findMin(Node* root) {
    while (root && root->left != NULL)
        root = root->left;
    return root;
}

Node* removeNode(Node* root, int key) {
    if (root == NULL) return NULL;

    if (key < root->key) {
        root->left = removeNode(root->left, key);
    } else if (key > root->key) {
        root->right = removeNode(root->right, key);
    } else {
        // Caso 1: Sem filhos (folha) & Caso 2: 1 filho
        if (root->left == NULL) {
            Node* temp = root->right;
            free(root);
            return temp;
        } else if (root->right == NULL) {
            Node* temp = root->left;
            free(root);
            return temp;
        }

        // Caso 3: 2 filhos (Substitui pelo sucessor em-ordem: menor da subárvore direita)
        Node* temp = findMin(root->right);
        root->key = temp->key;
        root->right = removeNode(root->right, temp->key);
    }
    return root;
}

void freeTree(Node* root) {
    if (root == NULL) return;
    freeTree(root->left);
    freeTree(root->right);
    free(root);
}

void inorder(Node* root) {
    if (root != NULL) {
        inorder(root->left);
        printf("%d ", root->key);
        inorder(root->right);
    }
}

int main() {
    Node* root = NULL;

    // Insercao
    root = insert(root, 50);
    insert(root, 30);
    insert(root, 20);
    insert(root, 40);
    insert(root, 70);
    insert(root, 60);
    insert(root, 80);

    printf("Em-ordem inicial: ");
    inorder(root);
    printf("\n");

    // Busca
    Node* found = search(root, 40);
    printf("Busca (40): %s\n", found ? "Encontrado" : "Nao encontrado");

    // Remocao - Caso 1: Folha (20)
    root = removeNode(root, 20);
    // Remocao - Caso 2: 1 filho (30 possui filho 40)
    root = removeNode(root, 30);
    // Remocao - Caso 3: 2 filhos (raiz 50)
    root = removeNode(root, 50);

    printf("Em-ordem apos remocoes: ");
    inorder(root);
    printf("\n");

    freeTree(root);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Perda de ponteiro na atribuição de retorno:** Esquecer de reatribuir o retorno das funções recursivas de modificação (`root->left = insert(root->left, key)`). Se fizer apenas `insert(root->left, key)`, as alterações na subárvore não serão ligadas ao pai.
2. **Segmentation Fault em `search`:** Tentar acessar `root->key` antes de validar se `root == NULL`. Sempre verifique a nulidade primeiro.
3. **Memory Leak no Caso 3 de remoção:** Desalocar o nó sucessor diretamente em vez de sobrescrever a chave do nó alvo e chamar `removeNode` recursivamente para remover a chave duplicada na subárvore direita.

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função em C `int countLeaves(Node* root)` que receba o ponteiro para a raiz de uma BST e retorne a quantidade total de nós folha (nós sem filhos esquerdos e direitos).

**Gabarito:**

```c
int countLeaves(Node* root) {
    if (root == NULL) 
        return 0;
    
    if (root->left == NULL && root->right == NULL) 
        return 1;
        
    return countLeaves(root->left) + countLeaves(root->right);
}
```