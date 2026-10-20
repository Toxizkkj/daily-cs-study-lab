# Arvores Binarias de Busca (BST) em C

## 1. Teoria e Complexidade

Uma Árvore Binária de Busca (BST) é uma estrutura de dados hierárquica onde cada nó possui no máximo dois filhos (esquerdo e direito). A **propriedade de ordenação** estabelece que, para qualquer nó $X$, todas as chaves na sua subárvore esquerda são estritamente menores que a chave de $X$, e todas as chaves na sua subárvore direita são estritamente maiores.

Todas as operações principais (busca, inserção e remoção) dependem diretamente da altura da árvore ($h$). Em árvores balanceadas, a altura é $h = O(\log n)$. No pior caso, se os elementos forem inseridos de forma ordenada, a árvore degenera em uma lista encadeada com altura $h = O(n)$.

| Operação | Caso Médio | Pior Caso | Espaço (Pilha Recursiva) |
| :--- | :--- | :--- | :--- |
| Busca | $O(\log n)$ | $O(n)$ | $O(h)$ |
| Inserção | $O(\log n)$ | $O(n)$ | $O(h)$ |
| Remoção | $O(\log n)$ | $O(n)$ | $O(h)$ |

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

Node* create_node(int key) {
    Node* new_node = (Node*)malloc(sizeof(Node));
    new_node->key = key;
    new_node->left = NULL;
    new_node->right = NULL;
    return new_node;
}

Node* insert(Node* root, int key) {
    if (root == NULL) return create_node(key);
    
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

Node* min_value_node(Node* node) {
    Node* current = node;
    while (current && current->left != NULL)
        current = current->left;
    return current;
}

Node* remove_node(Node* root, int key) {
    if (root == NULL) return root;

    if (key < root->key)
        root->left = remove_node(root->left, key);
    else if (key > root->key)
        root->right = remove_node(root->right, key);
    else {
        // Caso 1 e 2: Folha (0 filhos) ou 1 filho
        if (root->left == NULL) {
            Node* temp = root->right;
            free(root);
            return temp;
        } else if (root->right == NULL) {
            Node* temp = root->left;
            free(root);
            return temp;
        }

        // Caso 3: 2 filhos (obtem o menor da subarvore direita - sucessor)
        Node* temp = min_value_node(root->right);
        root->key = temp->key;
        root->right = remove_node(root->right, temp->key);
    }
    return root;
}

void free_tree(Node* root) {
    if (root != NULL) {
        free_tree(root->left);
        free_tree(root->right);
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

    // Insercao
    root = insert(root, 50);
    root = insert(root, 30);
    root = insert(root, 20);
    root = insert(root, 40);
    root = insert(root, 70);
    root = insert(root, 60);
    root = insert(root, 80);

    printf("Em-Ordem: ");
    inorder(root);
    printf("\n");

    // Busca
    int target = 40;
    Node* found = search(root, target);
    printf("Busca %d: %s\n", target, found ? "Encontrado" : "Nao encontrado");

    // Remocao Caso 1 (folha): 20
    root = remove_node(root, 20);
    // Remocao Caso 2 (1 filho): 30
    root = remove_node(root, 30);
    // Remocao Caso 3 (2 filhos): 50
    root = remove_node(root, 50);

    printf("Apos remocoes: ");
    inorder(root);
    printf("\n");

    free_tree(root);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Perda de ponteiros no retorno recursivo**: Esquecer de reatribuir os retornos das chamadas recursivas (`root->left = insert(root->left, val)`). Se fizer apenas `insert(root->left, val)`, a árvore pai perde a referência ao sub-nó modificado ou recém-criado.
2. **Uso incorreto da desalocação no Caso 3 de remoção**: Na remoção com 2 filhos, dar `free(root)` diretamente destrói a subárvore inteira. O correto é apenas **sobrescrever a chave** do nó pelo valor do sucessor em-ordem e depois fazer uma chamada recursiva para remover o nó do sucessor original.
3. **Segmentation Fault em bases nulas**: Tentar acessar `root->key` antes de validar se `root != NULL`. Toda função de BST deve ter como primeira checagem a parada para ponteiro nulo.

---

## 4. Exercicio com Gabarito

**Exercício:** Escreva uma função recursiva `int altura(Node* root)` que retorna a altura de uma BST. A altura de uma árvore vazia é -1, e a altura de um nó folha é 0.

**Gabarito:**

```c
int altura(Node* root) {
    if (root == NULL) {
        return -1; // Arvore vazia tem altura -1
    }
    
    int alt_esq = altura(root->left);
    int alt_dir = altura(root->right);
    
    if (alt_esq > alt_dir) {
        return alt_esq + 1;
    } else {
        return alt_dir + 1;
    }
}
```
**Explicação:** A função calcula recursivamente a altura das subárvores esquerda e direita. Em seguida, pega o maior valor entre as duas e adiciona `1` (referente ao nível do nó atual). O caso base para subárvores inexistentes devolve `-1`, fazendo com que um nó folha resulte em $0 + 1 - 1 = 0$.