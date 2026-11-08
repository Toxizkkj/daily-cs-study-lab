# Arvores Binarias em C

## 1. Teoria e Complexidade

Uma Árvore Binária é uma estrutura de dados hierárquica onde cada nó possui no máximo dois filhos, referenciados como ponteiro esquerdo (`left`) e ponteiro direito (`right`). O nó principal é a raiz. Quando organizada como Árvore Binária de Busca (BST), os valores menores que o nó pai ficam à esquerda e os maiores à direita.

Os percursos definem a ordem de visitação dos nós: **Pré-ordem** (Raiz, Esquerda, Direita) é ideal para clonar a árvore; **Em-ordem** (Esquerda, Raiz, Direita) visita os elementos em ordem crescente em BSTs; **Pós-ordem** (Esquerda, Direita, Raiz) é essencial para desalocação de memória e cálculo de métricas bottom-up.

| Operação | Caso Médio | Pior Caso | Espaço (Pilha de Rec.) |
| :--- | :--- | :--- | :--- |
| Busca / Inserção | $O(\log n)$ | $O(n)$ | $O(h)$ onde $h$ é a altura |
| Percursos (Todos) | $O(n)$ | $O(n)$ | $O(h)$ |
| Cálculo de Altura | $O(n)$ | $O(n)$ | $O(h)$ |

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

Node* create_node(int value) {
    Node *new_node = (Node*) malloc(sizeof(Node));
    if (!new_node) exit(1);
    new_node->data = value;
    new_node->left = NULL;
    new_node->right = NULL;
    return new_node;
}

Node* insert(Node *root, int value) {
    if (root == NULL) return create_node(value);
    if (value < root->data)
        root->left = insert(root->left, value);
    else if (value > root->data)
        root->right = insert(root->right, value);
    return root;
}

void pre_order(Node *root) {
    if (root != NULL) {
        printf("%d ", root->data);
        pre_order(root->left);
        pre_order(root->right);
    }
}

void in_order(Node *root) {
    if (root != NULL) {
        in_order(root->left);
        printf("%d ", root->data);
        in_order(root->right);
    }
}

void post_order(Node *root) {
    if (root != NULL) {
        post_order(root->left);
        post_order(root->right);
        printf("%d ", root->data);
    }
}

int calculate_height(Node *root) {
    if (root == NULL) return -1;
    int left_h = calculate_height(root->left);
    int right_h = calculate_height(root->right);
    return (left_h > right_h ? left_h : right_h) + 1;
}

void free_tree(Node *root) {
    if (root == NULL) return;
    free_tree(root->left);
    free_tree(root->right);
    free(root);
}

int main() {
    Node *root = NULL;

    root = insert(root, 50);
    insert(root, 30);
    insert(root, 70);
    insert(root, 20);
    insert(root, 40);

    printf("Pre-ordem:  "); pre_order(root);  printf("\n");
    printf("Em-ordem:   "); in_order(root);   printf("\n");
    printf("Pos-ordem:  "); post_order(root); printf("\n");

    printf("Altura da arvore: %d\n", calculate_height(root));

    free_tree(root);
    root = NULL;

    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Desalocação fora de Pós-ordem:** Liberar a memória da raiz (`free(root)`) em pré-ordem invabiliza o acesso aos ponteiros `root->left` e `root->right`, gerando *Segmentation Fault* ou *Undefined Behavior*. A liberação **deve** ser em pós-ordem.
2. **Esquecer a verificação de `NULL`:** Acessar `root->data` ou fazer a chamada recursiva sem testar `if (root == NULL)` como caso-base da recursão estoura a pilha de execução (*Stack Overflow*) ou causa desreferenciação de ponteiro nulo.
3. **Não atualizar o ponteiro retornado na inserção:** Escrever `insert(root->left, val)` sem atribuir de volta (`root->left = insert(...)`) faz com que as alterações nos nós descendentes sejam perdidas na pilha de execução.

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função recursiva em C chamada `count_leaves` que receba o ponteiro para a raiz de uma árvore binária e retorne a quantidade total de nós folha (nós que não possuem filho esquerdo e nem filho direito).

**Gabarito:**

```c
int count_leaves(Node *root) {
    if (root == NULL) 
        return 0;
    
    // Um nó é folha se ambos os ponteiros forem NULL
    if (root->left == NULL && root->right == NULL) 
        return 1;
    
    // Soma as folhas da subárvore esquerda e direita
    return count_leaves(root->left) + count_leaves(root->right);
}
```