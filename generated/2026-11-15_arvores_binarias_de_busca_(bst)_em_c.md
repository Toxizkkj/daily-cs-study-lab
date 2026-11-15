# Arvores Binarias de Busca (BST) em C

## 1. Teoria e Complexidade

Uma Árvore Binária de Busca (BST) é uma estrutura de dados hierárquica baseada em nós. A **propriedade de ordenação** garante que, para qualquer nó $N$:
* Todos os nós na subárvore à **esquerda** possuem chaves **menores** que a chave de $N$.
* Todos os nós na subárvore à **direita** possuem chaves **maiores** que a chave de $N$.

O percurso em-ordem (in-order) em uma BST visita os elementos de forma estritamente crescente. As operações de busca, inserção e remoção dependem diretamente da altura $h$ da árvore. A remoção lida com 3 cenários: **(1) Nó folha** (basta remover), **(2) Nó com 1 filho** (o filho substitui o pai), e **(3) Nó com 2 filhos** (substitui-se a chave pelo menor nó da subárvore direita — o *sucessor em-ordem* — e remove-se o sucessor).

| Operação | Caso Médio | Pior Caso | Espaço (Auxiliar) |
| :--- | :--- | :--- | :--- |
| **Busca** | $O(\log n)$ | $O(n)$ | $O(h)$ recursivo |
| **Inserção** | $O(\log n)$ | $O(n)$ | $O(h)$ recursivo |
| **Remoção** | $O(\log n)$ | $O(n)$ | $O(h)$ recursivo |

*(Nota: O pior caso $O(n)$ ocorre quando a árvore se degenera em uma lista encadeada por conta de inserções ordenadas).*

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
    if (key < root->key) root->left = insert(root->left, key);
    else if (key > root->key) root->right = insert(root->right, key);
    return root;
}

Node* search(Node* root, int key) {
    if (root == NULL || root->key == key) return root;
    if (key < root->key) return search(root->left, key);
    return search(root->right, key);
}

Node* find_min(Node* root) {
    while (root && root->left != NULL) root = root->left;
    return root;
}

Node* remove_node(Node* root, int key) {
    if (root == NULL) return NULL;

    if (key < root->key) {
        root->left = remove_node(root->left, key);
    } else if (key > root->key) {
        root->right = remove_node(root->right, key);
    } else {
        // Caso 1: Sem filhos ou Caso 2: Apenas 1 filho (Direita)
        if (root->left == NULL) {
            Node* temp = root->right;
            free(root);
            return temp;
        }
        // Caso 2: Apenas 1 filho (Esquerda)
        else if (root->right == NULL) {
            Node* temp = root->left;
            free(root);
            return temp;
        }
        // Caso 3: 2 filhos -> Obter o menor da subárvore direita (sucessor)
        Node* temp = find_min(root->right);
        root->key = temp->key;
        root->right = remove_node(root->right, temp->key);
    }
    return root;
}

void inorder(Node* root) {
    if (root != NULL) {
        inorder(root->left);
        printf("%d ", root->key);
        inorder(root->right);
    }
}

void free_tree(Node* root) {
    if (root == NULL) return;
    free_tree(root->left);
    free_tree(root->right);
    free(root);
}

int main() {
    Node* root = NULL;

    // Inserções
    root = insert(root, 50);
    root = insert(root, 30);
    root = insert(root, 70);
    root = insert(root, 20);
    root = insert(root, 40);
    root = insert(root, 60);
    root = insert(root, 80);

    printf("Em-ordem inicial: ");
    inorder(root);
    printf("\n");

    // Busca
    int busca_key = 40;
    Node* res = search(root, busca_key);
    printf("Busca por %d: %s\n", busca_key, res ? "Encontrado" : "Nao encontrado");

    // Remoções (3 casos)
    root = remove_node(root, 20); // Caso 1: Folha
    root = remove_node(root, 30); // Caso 2: 1 filho (ficou com 40)
    root = remove_node(root, 50); // Caso 3: 2 filhos (raiz)

    printf("Em-ordem apos remocoes (20, 30, 50): ");
    inorder(root);
    printf("\n");

    free_tree(root);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Esquecer de atualizar o ponteiro pai na recursão**:
   Ao chamar `insert` ou `remove_node`, é obrigatório reatribuir o retorno (`root->left = insert(...)`). Caso contrário, modificações nos ponteiros descendentes se perdem e geram ponteiros soltos.
2. **Vazamento de memória na remoção de nó com 2 filhos**:
   No **Caso 3**, a forma correta é copiar a chave do sucessor para o nó atual e depois chamar a remoção recursiva para a subárvore direita. Se você tentar desalocar (`free`) o nó atual diretamente sem ajustar a estrutura, causará *Segmentation Fault* ou *Memory Leak*.
3. **Perda da raiz original**:
   Ao remover a raiz original da árvore, o ponteiro mantido na `main` precisa receber o retorno atualizado da função `remove_node`. Caso contrário, a `main` continuará apontando para uma área de memória liberada.

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função recursiva `int altura(Node* root)` em C que calcule e retorne a altura de uma árvore binária de busca. A altura de uma árvore vazia é -1 e a de uma árvore com apenas a raiz é 0.

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
*Explicação:* A função percorre pós-ordem cada subárvore, pega a maior altura entre os dois lados e adiciona 1. A condição base retorna -1 para garantir que a folha tenha altura $0$ ($-1 + 1 = 0$). Complexidade de Tempo: $O(n)$, Espaço: $O(h)$.