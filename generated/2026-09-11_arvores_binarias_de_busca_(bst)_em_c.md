# Arvores Binarias de Busca (BST) em C

## 1. Teoria e Complexidade

Uma Árvore Binária de Busca (BST) é uma estrutura de dados hierárquica na qual cada nó possui no máximo dois filhos (esquerdo e direito). A propriedade fundamental de ordenação estabelece que, para qualquer nó $N$, todos os valores na subárvore esquerda são estritamente menores que a chave de $N$, e todos os valores na subárvore direita são estritamente maiores. Isso permite aplicar a lógica de busca binária diretamente em estruturas encadeadas.

 O desempenho de uma BST depende diretamente da sua altura $h$. Em árvores balanceadas, a altura é $h = \log n$. No pior caso (inserções ordenadas que geram uma árvore degenerada/similar a uma lista encadeada), a altura torna-se $h = n$. As operações de busca, inserção e remoção percorrem um único caminho da raiz até as folhas, resultando em complexidade $O(h)$.

| Operação | Caso Médio | Pior Caso | Espaço (Auxiliar) |
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
    if (root == NULL || root->key == key) return root;
    if (key < root->key) return search(root->left, key);
    return search(root->right, key);
}

Node* min_value_node(Node* node) {
    Node* current = node;
    while (current && current->left != NULL)
        current = current->left;
    return current;
}

Node* delete_node(Node* root, int key) {
    if (root == NULL) return root;

    if (key < root->key) {
        root->left = delete_node(root->left, key);
    } else if (key > root->key) {
        root->right = delete_node(root->right, key);
    } else {
        // Casos 1 e 2: Sem filhos ou apenas 1 filho
        if (root->left == NULL) {
            Node* temp = root->right;
            free(root);
            return temp;
        } else if (root->right == NULL) {
            Node* temp = root->left;
            free(root);
            return temp;
        }
        // Caso 3: 2 filhos -> Sucessor em-ordem (menor da subarvore direita)
        Node* temp = min_value_node(root->right);
        root->key = temp->key;
        root->right = delete_node(root->right, temp->key);
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

    // Insercoes
    root = insert(root, 50);
    root = insert(root, 30);
    root = insert(root, 20);
    root = insert(root, 40);
    root = insert(root, 70);
    root = insert(root, 60);
    root = insert(root, 80);

    printf("Em-ordem original: ");
    inorder(root);
    printf("\n");

    // Busca
    int busca = 40;
    Node* res = search(root, busca);
    printf("Busca por %d: %s\n", busca, res ? "Encontrado" : "Nao encontrado");

    // Remocao Caso 1: Folha (20)
    root = delete_node(root, 20);
    // Remocao Caso 2: 1 Filho (30 -> possui filho 40)
    root = delete_node(root, 30);
    // Remocao Caso 3: 2 Filhos (50 -> substitui pelo sucessor 60)
    root = delete_node(root, 50);

    printf("Em-ordem apos remocoes: ");
    inorder(root);
    printf("\n");

    free_tree(root);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Perda de Retorno da Raiz (Ponteiro Solto):**
   Funções de inserção e remoção recriam/alteram a estrutura de subárvores. Ignorar o retorno (ex: chamar apenas `insert(root, val);` sem fazer `root = insert(root, val);`) faz com que modificações na raiz original sejam perdidas, mantendo ponteiros para memória liberada ou ignorando novas alocações.

2. **Memory Leak na Remoção do Caso 3 (2 Filhos):**
   Um erro comum é tentar trocar os ponteiros do nó a ser removido com os ponteiros do sucessor diretamente. O correto e mais seguro é copiar **apenas o valor** do sucessor para o nó atual e chamar a remoção recursiva na subárvore direita para liberar o nó original do sucessor.

3. **Dereferenciação de `NULL` antes da verificação:**
   Tentar acessar `root->key` antes de verificar se `root == NULL` em funções de busca ou remoção causa *Segmentation Fault* imediato quando a chave procurada não existe na árvore.

---

## 4. Exercicio com Gabarito

**Enunciado:**
Escreva uma função recursiva em C com a assinatura `int altura(Node* root)` que calcule e retorne a altura de uma BST. Considere a altura de uma árvore vazia (`NULL`) como `-1` e de uma árvore com apenas um nó (raiz) como `0`.

**Gabarito:**

```c
int altura(Node* root) {
    if (root == NULL) {
        return -1;
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

*Explicação:* A função calcula recursivamente a altura das subárvores esquerda e direita. Retorna `1` somado ao maior valor encontrado entre as duas subárvores. Se a árvore for vazia, o caso base retorna `-1`, garantindo que uma árvore de nó único retorne `max(-1, -1) + 1 = 0`.