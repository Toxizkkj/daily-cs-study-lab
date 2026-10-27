# Arvores B em C

## 1. Teoria e Complexidade

Uma Árvore B é uma estrutura de dados auto-balanceada de busca multi-caminho projetada para otimizar operações de leitura e escrita em blocos de memória secundária (como discos e SSDs). Diferente de árvores binárias, cada nó de uma Árvore B de ordem $m$ pode conter até $m-1$ chaves e ter até $m$ filhos.

**Regras Fundamentais de uma Árvore B de ordem $m$ (com grau mínimo $t = \lceil m/2 \rceil$):**
1. **Chaves por Nó:** Todo nó (exceto a raiz) possui no mínimo $t - 1$ chaves e no máximo $2t - 1$ chaves (onde $m = 2t$).
2. **Filhos por Nó:** Um nó não-folha com $k$ chaves possui exatamente $k + 1$ filhos.
3. **Ordenação:** As chaves de cada nó estão sempre ordenadas de forma crescente.
4. **Folhas:** Todas as folhas estão exatamente no mesmo nível (balanceamento perfeito em altura).
5. **Split:** Quando um nó atinge o limite máximo de chaves ($2t-1$), ele é dividido (*split*): a chave mediana sobe para o nó pai e as chaves restantes são divididas igualmente em dois novos nós.

### Tabela de Complexidade Big-O

| Operação | Caso Médio | Pior Caso | Espaço |
| :--- | :--- | :--- | :--- |
| **Busca** | $O(\log_t n)$ | $O(\log_t n)$ | $O(n)$ |
| **Inserção** | $O(\log_t n)$ | $O(\log_t n)$ | $O(n)$ |
| **Remoção** | $O(\log_t n)$ | $O(\log_t n)$ | $O(n)$ |

---

## 2. Implementacao Completa em C

O código abaixo implementa uma Árvore B de grau mínimo $t=2$ (Capacidade: 1 a 3 chaves por nó, até 4 filhos).

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define T 2
#define MAX_KEYS (2 * T - 1)
#define MAX_CHILDREN (2 * T)

typedef struct BTreeNode {
    int keys[MAX_KEYS];
    struct BTreeNode *children[MAX_CHILDREN];
    int num_keys;
    bool leaf;
} BTreeNode;

typedef struct {
    BTreeNode *root;
} BTree;

BTreeNode* criar_no(bool leaf) {
    BTreeNode *no = (BTreeNode*)malloc(sizeof(BTreeNode));
    no->leaf = leaf;
    no->num_keys = 0;
    for (int i = 0; i < MAX_CHILDREN; i++) {
        no->children[i] = NULL;
    }
    return no;
}

BTree* criar_arvore() {
    BTree *tree = (BTree*)malloc(sizeof(BTree));
    tree->root = criar_no(true);
    return tree;
}

BTreeNode* buscar(BTreeNode *no, int chave) {
    int i = 0;
    while (i < no->num_keys && chave > no->keys[i]) {
        i++;
    }
    if (i < no->num_keys && no->keys[i] == chave) {
        return no;
    }
    if (no->leaf) {
        return NULL;
    }
    return buscar(no->children[i], chave);
}

void split_child(BTreeNode *pai, int i, BTreeNode *filho) {
    BTreeNode *novo = criar_no(filho->leaf);
    novo->num_keys = T - 1;

    for (int j = 0; j < T - 1; j++) {
        novo->keys[j] = filho->keys[j + T];
    }

    if (!filho->leaf) {
        for (int j = 0; j < T; j++) {
            novo->children[j] = filho->children[j + T];
        }
    }

    filho->num_keys = T - 1;

    for (int j = pai->num_keys; j >= i + 1; j--) {
        pai->children[j + 1] = pai->children[j];
    }
    pai->children[i + 1] = novo;

    for (int j = pai->num_keys - 1; j >= i; j--) {
        pai->keys[j + 1] = pai->keys[j];
    }
    pai->keys[i] = filho->keys[T - 1];
    pai->num_keys++;
}

void inserir_nao_cheio(BTreeNode *no, int chave) {
    int i = no->num_keys - 1;

    if (no->leaf) {
        while (i >= 0 && no->keys[i] > chave) {
            no->keys[i + 1] = no->keys[i];
            i--;
        }
        no->keys[i + 1] = chave;
        no->num_keys++;
    } else {
        while (i >= 0 && no->keys[i] > chave) {
            i--;
        }
        i++;
        if (no->children[i]->num_keys == MAX_KEYS) {
            split_child(no, i, no->children[i]);
            if (no->keys[i] < chave) {
                i++;
            }
        }
        inserir_nao_cheio(no->children[i], chave);
    }
}

void inserir(BTree *tree, int chave) {
    BTreeNode *r = tree->root;
    if (r->num_keys == MAX_KEYS) {
        BTreeNode *s = criar_no(false);
        tree->root = s;
        s->children[0] = r;
        split_child(s, 0, r);
        inserir_nao_cheio(s, chave);
    } else {
        inserir_nao_cheio(r, chave);
    }
}

void em_ordem(BTreeNode *no) {
    if (no != NULL) {
        int i;
        for (i = 0; i < no->num_keys; i++) {
            em_ordem(no->children[i]);
            printf("%d ", no->keys[i]);
        }
        em_ordem(no->children[i]);
    }
}

void liberar_no(BTreeNode *no) {
    if (no != NULL) {
        if (!no->leaf) {
            for (int i = 0; i <= no->num_keys; i++) {
                liberar_no(no->children[i]);
            }
        }
        free(no);
    }
}

void liberar_arvore(BTree *tree) {
    if (tree != NULL) {
        liberar_no(tree->root);
        free(tree);
    }
}

int main() {
    BTree *arvore = criar_arvore();

    int valores[] = {10, 20, 5, 6, 12, 30, 7, 17};
    int n = sizeof(valores) / sizeof(valores[0]);

    for (int i = 0; i < n; i++) {
        inserir(arvore, valores[i]);
    }

    printf("Impressao em-ordem: ");
    em_ordem(arvore->root);
    printf("\n");

    int busca_valor = 12;
    BTreeNode *res = buscar(arvore->root, busca_valor);
    if (res != NULL) {
        printf("Chave %d encontrada na arvore.\n", busca_valor);
    } else {
        printf("Chave %d nao encontrada.\n", busca_valor);
    }

    liberar_arvore(arvore);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Acesso Inválido no *Split* (Off-By-One):**
   Ao mover a chave mediana no *split*, o índice correto do elemento a subir é `T - 1`. Mover o elemento de índice `T` corrompe a ordenação das páginas resultantes.

2. **Perda de Ponteiros ao Desalocar (Memory Leak):**
   Liberar um nó não-folha sem antes desalocar recursivamente seus `num_keys + 1` filhos gera *dangling pointers* e vazamento de memória grave na Heap.

3. **Invasão do Limite de Filhos em Folhas:**
   Tentar acessar `children` em nós onde `leaf == true`. Nós folha contêm ponteiros nulos em seus vetores de filhos; navegar por eles resultará em **Segmentation Fault**.

---

## 4. Exercicio com Gabarito

**Enunciado:**
Considere uma Árvore B com grau mínimo $T = 2$.
Insira as chaves na seguinte sequência em uma árvore inicialmente vazia: `15, 30, 20, 40`.
Escreva qual será a chave contida no nó **raiz** e quais chaves estarão no seu **filho direito** após todas as inserções.

---

### Gabarito Explicado:

1. **Inserir 15, 30, 20:**
   O nó raiz inicial (folha) acumula as 3 chaves ordenadas: `[15, 20, 30]`. O nó atinge a capacidade máxima ($2T - 1 = 3$ chaves).

2. **Inserir 40 (Causa Split):**
   - Como a raiz está cheia, ocorre o *Split*.
   - A mediana `20` (índice $T-1$) sobe para criar a nova raiz.
   - O nó antigo se divide em dois:
     - Filho esquerdo: `[15]`
     - Filho direito: `[30]`
   - A chave `40` é então inserida no filho direito, resultando em: `[30, 40]`.

**Resposta Final:**
- **Nó Raiz:** `[20]`
- **Filho Direito:** `[30, 40]`