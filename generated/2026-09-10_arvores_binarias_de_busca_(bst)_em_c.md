# Arvores Binarias de Busca (BST) em C

## 1. Teoria e Complexidade

Uma Árvore Binária de Busca (BST - *Binary Search Tree*) é uma estrutura de dados encadeada e não linear que mantém seus elementos ordenados. A **propriedade de ordenação em BST** dita que, para qualquer nó $N$: todos os nós em sua subárvore esquerda possuem chaves estritamente menores que a chave de $N$, e todos os nós em sua subárvore direita possuem chaves estritamente maiores.

O desempenho de operações de busca, inserção e remoção em uma BST depende diretamente da altura $h$ da árvore. Em uma árvore balanceada, a altura é $O(\log n)$. No pior caso (árvore degenerada em lista encadeada), a altura se torna $O(n)$.

| Operação | Caso Médio | Pior Caso | Espaço Auxiliar (Recursivo) |
| :--- | :--- | :--- | :--- |
| **Busca** | $O(\log n)$ | $O(n)$ | $O(h)$ |
| **Inserção** | $O(\log n)$ | $O(n)$ | $O(h)$ |
| **Remoção** | $O(\log n)$ | $O(n)$ | $O(h)$ |
| **Espaço Total**| $O(n)$ | $O(n)$ | $O(1)$ |

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
    if (root == NULL || root->key == key) return root;
    if (key < root->key) return search(root->left, key);
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
        // Caso 1: Sem filhos (folha) ou Caso 2: Apenas 1 filho
        if (root->left == NULL) {
            Node* temp = root->right;
            free(root);
            return temp;
        } else if (root->right == NULL) {
            Node* temp = root->left;
            free(root);
            return temp;
        }
        // Caso 3: 2 filhos (Substitui pelo sucessor em-ordem: menor da direita)
        Node* temp = findMin(root->right);
        root->key = temp->key;
        root->right = removeNode(root->right, temp->key);
    }
    return root;
}

void freeTree(Node* root) {
    if (root != NULL) {
        freeTree(root->left);
        freeTree(root->right);
        free(root);
    }
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

    // Inserções
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

    // Remoção Caso 1: Folha (20)
    root = removeNode(root, 20);
    
    // Remoção Caso 2: 1 filho (30 possui apenas o 40 agora)
    root = removeNode(root, 30);
    
    // Remoção Caso 3: 2 filhos (50 é a raiz)
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

1. **Perda de Retorno Recursivo (Perda de Encadeamento):**
   Esquecer de atribuir o retorno das chamadas de `insert` ou `removeNode` ao filho correspondente (ex: escrever apenas `insert(root->left, key);` em vez de `root->left = insert(root->left, key);`). Isso desconecta as modificações da árvore e causa dangling pointers ou vazamento de memória.

2. **Derefenciação de Ponteiro Nulo (Segmentation Fault):**
   Acessar `root->left->key` antes de verificar se `root` ou `root->left` é `NULL`. Sempre trate o caso base (`if (root == NULL)`) antes de acessar ponteiros internos.

3. **Vazamento de Memória na Remoção de Nó com 2 Filhos:**
   No Caso 3, tentar dar `free(root)` diretamente antes de substituir pelo sucessor em-ordem. O procedimento correto é copiar o **valor** do sucessor para o nó atual e depois chamar `removeNode` para liberar recursivamente a duplicata na subárvore direita.

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função em C `int height(Node* root)` que calcula a altura de uma BST. A altura de uma árvore vazia é -1, e a de uma árvore com apenas a raiz é 0.

### Gabarito

```c
int height(Node* root) {
    if (root == NULL) return -1;
    
    int leftHeight = height(root->left);
    int rightHeight = height(root->right);
    
    return 1 + (leftHeight > rightHeight ? leftHeight : rightHeight);
}
```

**Explicação:** A função usa recursão pós-ordem. Se o nó atual for `NULL`, retorna `-1` (caso base). Caso contrário, calcula recursivamente a altura das subárvores esquerda e direita, retornando `1` (a aresta atual) somado ao máximo entre a altura esquerda e direita.