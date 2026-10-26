# Arvores AVL em C

## 1. Teoria e Complexidade
A Árvore AVL é uma Árvore Binária de Busca (BST) autobalanceada. Para cada nó, a diferença entre as alturas das subárvores esquerda e direita — chamada de **Fator de Balanceamento (FB)** — deve ser no máximo $\pm 1$ ($FB = h_{esq} - h_{dir} \in \{-1, 0, 1\}$).

Caso $|FB| > 1$, a árvore é considerada desbalanceada e passa por operações de **rotação** para restaurar a propriedade AVL:
- **Caso LL ($FB > 1$ e $FB_{filho\_esq} \ge 0$):** Rotação Simples à Direita.
- **Caso RR ($FB < -1$ e $FB_{filho\_dir} \le 0$):** Rotação Simples à Esquerda.
- **Caso LR ($FB > 1$ e $FB_{filho\_esq} < 0$):** Rotação Dupla Esquerda-Direita.
- **Caso RL ($FB < -1$ e $FB_{filho\_dir} > 0$):** Rotação Dupla Direita-Esquerda.

Esse balanceamento garante altura estritamente $h = O(\log n)$, eliminando o pior caso $O(n)$ das BSTs comuns.

| Operação | Caso Médio | Pior Caso | Espaço |
| :--- | :--- | :--- | :--- |
| Busca | $O(\log n)$ | $O(\log n)$ | $O(n)$ |
| Inserção | $O(\log n)$ | $O(\log n)$ | $O(n)$ |
| Remoção | $O(\log n)$ | $O(\log n)$ | $O(n)$ |

---

## 2. Implementacao Completa em C

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int chave;
    int altura;
    struct Node *esq;
    struct Node *dir;
} Node;

int altura(Node *n) {
    return (n == NULL) ? 0 : n->altura;
}

int max(int a, int b) {
    return (a > b) ? a : b;
}

int obterFB(Node *n) {
    return (n == NULL) ? 0 : altura(n->esq) - altura(n->dir);
}

Node* criarNo(int chave) {
    Node *no = (Node*)malloc(sizeof(Node));
    no->chave = chave;
    no->altura = 1;
    no->esq = NULL;
    no->dir = NULL;
    return no;
}

Node* rotacionarDireita(Node *y) {
    Node *x = y->esq;
    Node *T2 = x->dir;

    x->dir = y;
    y->esq = T2;

    y->altura = max(altura(y->esq), altura(y->dir)) + 1;
    x->altura = max(altura(x->esq), altura(x->dir)) + 1;

    return x;
}

Node* rotacionarEsquerda(Node *x) {
    Node *y = x->dir;
    Node *T2 = y->esq;

    y->esq = x;
    x->dir = T2;

    x->altura = max(altura(x->esq), altura(x->dir)) + 1;
    y->altura = max(altura(y->esq), altura(y->dir)) + 1;

    return y;
}

Node* inserir(Node *no, int chave) {
    if (no == NULL) return criarNo(chave);

    if (chave < no->chave)
        no->esq = inserir(no->esq, chave);
    else if (chave > no->chave)
        no->dir = inserir(no->dir, chave);
    else
        return no;

    no->altura = 1 + max(altura(no->esq), altura(no->dir));
    int fb = obterFB(no);

    // Caso LL
    if (fb > 1 && chave < no->esq->chave)
        return rotacionarDireita(no);

    // Caso RR
    if (fb < -1 && chave > no->dir->chave)
        return rotacionarEsquerda(no);

    // Caso LR
    if (fb > 1 && chave > no->esq->chave) {
        no->esq = rotacionarEsquerda(no->esq);
        return rotacionarDireita(no);
    }

    // Caso RL
    if (fb < -1 && chave < no->dir->chave) {
        no->dir = rotacionarDireita(no->dir);
        return rotacionarEsquerda(no);
    }

    return no;
}

Node* noMenorValor(Node *no) {
    Node *atual = no;
    while (atual->esq != NULL)
        atual = atual->esq;
    return atual;
}

Node* remover(Node *raiz, int chave) {
    if (raiz == NULL) return raiz;

    if (chave < raiz->chave)
        raiz->esq = remover(raiz->esq, chave);
    else if (chave > raiz->chave)
        raiz->dir = remover(raiz->dir, chave);
    else {
        if ((raiz->esq == NULL) || (raiz->dir == NULL)) {
            Node *temp = raiz->esq ? raiz->esq : raiz->dir;
            if (temp == NULL) {
                temp = raiz;
                raiz = NULL;
            } else {
                *raiz = *temp;
            }
            free(temp);
        } else {
            Node *temp = noMenorValor(raiz->dir);
            raiz->chave = temp->chave;
            raiz->dir = remover(raiz->dir, temp->chave);
        }
    }

    if (raiz == NULL) return raiz;

    raiz->altura = 1 + max(altura(raiz->esq), altura(raiz->dir));
    int fb = obterFB(raiz);

    // Ajustes de balanceamento na remoção
    if (fb > 1 && obterFB(raiz->esq) >= 0)
        return rotacionarDireita(raiz);

    if (fb > 1 && obterFB(raiz->esq) < 0) {
        raiz->esq = rotacionarEsquerda(raiz->esq);
        return rotacionarDireita(raiz);
    }

    if (fb < -1 && obterFB(raiz->dir) <= 0)
        return rotacionarEsquerda(raiz);

    if (fb < -1 && obterFB(raiz->dir) > 0) {
        raiz->dir = rotacionarDireita(raiz->dir);
        return rotacionarEsquerda(raiz);
    }

    return raiz;
}

Node* buscar(Node *raiz, int chave) {
    if (raiz == NULL || raiz->chave == chave)
        return raiz;
    if (chave < raiz->chave)
        return buscar(raiz->esq, chave);
    return buscar(raiz->dir, chave);
}

void liberarArvore(Node *raiz) {
    if (raiz != NULL) {
        liberarArvore(raiz->esq);
        liberarArvore(raiz->dir);
        free(raiz);
    }
}

void emOrdem(Node *raiz) {
    if (raiz != NULL) {
        emOrdem(raiz->esq);
        printf("%d (FB: %d) ", raiz->chave, obterFB(raiz));
        emOrdem(raiz->dir);
    }
}

int main() {
    Node *raiz = NULL;

    // Teste de inserção com rotações
    raiz = inserir(raiz, 10);
    raiz = inserir(raiz, 20);
    raiz = inserir(raiz, 30); // Causa Rotação RR (Esquerda)
    raiz = inserir(raiz, 40);
    raiz = inserir(raiz, 50); // Causa Rotação RR (Esquerda)
    raiz = inserir(raiz, 25); // Causa Rotação RL (Direita-Esquerda)

    printf("Em-ordem apos insercoes:\n");
    emOrdem(raiz);
    printf("\n\n");

    // Teste de busca
    int valorBusca = 25;
    Node *encontrado = buscar(raiz, valorBusca);
    if (encontrado)
        printf("Valor %d encontrado na arvore.\n", valorBusca);
    else
        printf("Valor %d nao encontrado.\n", valorBusca);

    // Teste de remoção
    raiz = remover(raiz, 30);
    printf("\nEm-ordem apos remover 30:\n");
    emOrdem(raiz);
    printf("\n");

    liberarArvore(raiz);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Acesso Direto ao Campo Altura de Nó Nulo (`Segmentation Fault`)**:
   - *Erro*: Fazer `no->esq->altura` sem verificar se `no->esq == NULL`.
   - *Solução*: Sempre utilizar uma função auxiliar `altura(Node *n)` que retorna `0` caso `n == NULL`.

2. **Esquecer de Atualizar a Altura Após Rotações**:
   - *Erro*: Atualizar apenas os ponteiros dos nós durante as rotações simples/duplas e esquecer de recalcular `no->altura`.
   - *Consequência*: O cálculo de $FB$ nas chamadas superiores será corrompido, destruindo o balanceamento AVL.

3. **Verificação Incorreta do FB na Remoção**:
   - *Erro*: Na remoção, tentar validar os casos de rotação checando a chave inserida (como na inserção) em vez de checar o $FB$ do filho (`obterFB(raiz->esq) >= 0`).

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função em C `int ehAVL(Node *raiz)` que retorna `1` se a árvore binária dada for uma árvore AVL válida (em termos de balanceamento) e `0` caso contrário.

**Gabarito:**

```c
#include <stdlib.h>

int ehAVL(Node *raiz) {
    if (raiz == NULL) return 1;

    int fb = obterFB(raiz);
    if (fb < -1 || fb > 1) return 0;

    return ehAVL(raiz->esq) && ehAVL(raiz->dir);
}
```
*Nota: A solução acoplada à função `obterFB` percorre a árvore validando se todo subnó respeita a restrição $|FB| \le 1$.*