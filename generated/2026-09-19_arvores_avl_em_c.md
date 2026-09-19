# Arvores AVL em C

## 1. Teoria e Complexidade

Uma Árvore AVL é uma árvore binária de busca (BST) auto-balanceada. A propriedade fundamental da AVL é que, para qualquer nó, a diferença entre a altura da subárvore esquerda e a altura da subárvore direita — chamada de **Fator de Balanceamento ($FB$)** — deve ser obrigatoriamente $-1$, $0$ ou $1$.

$$FB(\text{nó}) = \text{altura}(\text{esquerda}) - \text{altura}(\text{direita})$$

Se $|FB| > 1$, a árvore está desbalanceada e exige reestruturação via rotações:
- **LL (Simples à Direita):** Nó desbalanceado com $FB > 1$ e filho esquerdo com $FB \ge 0$.
- **RR (Simples à Esquerda):** Nó desbalanceado com $FB < -1$ e filho direito com $FB \le 0$.
- **LR (Dupla Esquerda-Direita):** Nó desbalanceado com $FB > 1$ e filho esquerdo com $FB < 0$ (Rotaciona filho à esquerda, depois nó à direita).
- **RL (Dupla Direita-Esquerda):** Nó desbalanceado com $FB < -1$ e filho direito com $FB > 0$ (Rotaciona filho à direita, depois nó à esquerda).

As rotações mantêm a altura da árvore limitada a $O(\log n)$, garantindo o desempenho no pior caso.

| Operação | Caso Médio | Pior Caso | Espaço |
| :--- | :--- | :--- | :--- |
| **Busca** | $O(\log n)$ | $O(\log n)$ | $O(1)$ |
| **Inserção** | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ (pilha) |
| **Remoção** | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ (pilha) |

---

## 2. Implementacao Completa em C

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct No {
    int chave;
    int altura;
    struct No *esq;
    struct No *dir;
} No;

int altura(No *n) {
    return (n == NULL) ? 0 : n->altura;
}

int max(int a, int b) {
    return (a > b) ? a : b;
}

int fatorBalanceamento(No *n) {
    return (n == NULL) ? 0 : altura(n->esq) - altura(n->dir);
}

No* novoNo(int chave) {
    No* no = (No*)malloc(sizeof(No));
    no->chave = chave;
    no->altura = 1;
    no->esq = NULL;
    no->dir = NULL;
    return no;
}

No* rotacaoDireita(No *y) {
    No *x = y->esq;
    No *T2 = x->dir;

    x->dir = y;
    y->esq = T2;

    y->altura = max(altura(y->esq), altura(y->dir)) + 1;
    x->altura = max(altura(x->esq), altura(x->dir)) + 1;

    return x;
}

No* rotacaoEsquerda(No *x) {
    No *y = x->dir;
    No *T2 = y->esq;

    y->esq = x;
    x->dir = T2;

    x->altura = max(altura(x->esq), altura(x->dir)) + 1;
    y->altura = max(altura(y->esq), altura(y->dir)) + 1;

    return y;
}

No* inserir(No* no, int chave) {
    if (no == NULL) return novoNo(chave);

    if (chave < no->chave)
        no->esq = inserir(no->esq, chave);
    else if (chave > no->chave)
        no->dir = inserir(no->dir, chave);
    else
        return no;

    no->altura = 1 + max(altura(no->esq), altura(no->dir));
    int fb = fatorBalanceamento(no);

    // Caso LL
    if (fb > 1 && chave < no->esq->chave)
        return rotacaoDireita(no);

    // Caso RR
    if (fb < -1 && chave > no->dir->chave)
        return rotacaoEsquerda(no);

    // Caso LR
    if (fb > 1 && chave > no->esq->chave) {
        no->esq = rotacaoEsquerda(no->esq);
        return rotacaoDireita(no);
    }

    // Caso RL
    if (fb < -1 && chave < no->dir->chave) {
        no->dir = rotacaoDireita(no->dir);
        return rotacaoEsquerda(no);
    }

    return no;
}

No* menorNo(No* no) {
    No* atual = no;
    while (atual->esq != NULL)
        atual = atual->esq;
    return atual;
}

No* remover(No* raiz, int chave) {
    if (raiz == NULL) return raiz;

    if (chave < raiz->chave)
        raiz->esq = remover(raiz->esq, chave);
    else if (chave > raiz->chave)
        raiz->dir = remover(raiz->dir, chave);
    else {
        if ((raiz->esq == NULL) || (raiz->dir == NULL)) {
            No *temp = raiz->esq ? raiz->esq : raiz->dir;
            if (temp == NULL) {
                temp = raiz;
                raiz = NULL;
            } else {
                *raiz = *temp;
            }
            free(temp);
        } else {
            No* temp = menorNo(raiz->dir);
            raiz->chave = temp->chave;
            raiz->dir = remover(raiz->dir, temp->chave);
        }
    }

    if (raiz == NULL) return raiz;

    raiz->altura = 1 + max(altura(raiz->esq), altura(raiz->dir));
    int fb = fatorBalanceamento(raiz);

    // Rebalanceamento apos remocao
    if (fb > 1 && fatorBalanceamento(raiz->esq) >= 0)
        return rotacaoDireita(raiz);

    if (fb > 1 && fatorBalanceamento(raiz->esq) < 0) {
        raiz->esq = rotacaoEsquerda(raiz->esq);
        return rotacaoDireita(raiz);
    }

    if (fb < -1 && fatorBalanceamento(raiz->dir) <= 0)
        return rotacaoEsquerda(raiz);

    if (fb < -1 && fatorBalanceamento(raiz->dir) > 0) {
        raiz->dir = rotacaoDireita(raiz->dir);
        return rotacaoEsquerda(raiz);
    }

    return raiz;
}

No* buscar(No* raiz, int chave) {
    if (raiz == NULL || raiz->chave == chave)
        return raiz;
    if (chave < raiz->chave)
        return buscar(raiz->esq, chave);
    return buscar(raiz->dir, chave);
}

void liberarArvore(No* raiz) {
    if (raiz != NULL) {
        liberarArvore(raiz->esq);
        liberarArvore(raiz->dir);
        free(raiz);
    }
}

void emOrdem(No *raiz) {
    if (raiz != NULL) {
        emOrdem(raiz->esq);
        printf("%d (FB: %d) ", raiz->chave, fatorBalanceamento(raiz));
        emOrdem(raiz->dir);
    }
}

int main() {
    No *raiz = NULL;

    // Insercoes que forcam rotacoes
    raiz = inserir(raiz, 10);
    raiz = inserir(raiz, 20);
    raiz = inserir(raiz, 30); // Rotacao RR
    raiz = inserir(raiz, 15); // Rotacao RL
    raiz = inserir(raiz, 25);

    printf("Em-Ordem apos insercoes: ");
    emOrdem(raiz);
    printf("\n");

    int buscaChave = 15;
    No* encontrado = buscar(raiz, buscaChave);
    printf("Busca por %d: %s\n", buscaChave, encontrado ? "Encontrado" : "Nao encontrado");

    raiz = remover(raiz, 10);
    printf("Em-Ordem apos remover 10: ");
    emOrdem(raiz);
    printf("\n");

    liberarArvore(raiz);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Acessar ponteiro `NULL` ao calcular a altura:**
   Tentar ler `no->esq->altura` diretamente sem verificar se `no->esq` é `NULL` resulta em *Segmentation Fault*. **Solução:** Use uma função auxiliar `altura(No *n)` que retorna `0` quando o ponteiro for nulo.

2. **Esquecer de atualizar a altura após a rotação:**
   Ao efetuar uma rotação simples ou dupla, as alturas dos nós modificados mudam. Se você não recalcular a altura do nó rotacionado e de sua nova raiz antes de retornar, os fatores de balanceamento futuros serão calculados errados, destruindo a propriedade da AVL.

3. **Confundir FB na remoção:**
   Diferente da inserção (onde verificamos o valor da chave inserida), na remoção a escolha da rotação depende estritamente do **sinal do FB do filho**. Exemplo: se $FB(\text{raiz}) > 1$, verifica-se se $FB(\text{filho esquerdo}) \ge 0$ para rotação simples à direita, ou $< 0$ para rotação dupla.

---

## 4. Exercicio com Gabarito

**Enunciado:**
Escreva uma função em C `int ehAVL(No* raiz)` que recebe o ponteiro para a raiz de uma árvore binária e retorna `1` se ela for uma AVL válida ou `0` caso contrário.

**Gabarito:**

```c
int ehAVL(No* raiz) {
    if (raiz == NULL) return 1;

    int fb = fatorBalanceamento(raiz);
    
    // Verifica se o FB do no atual esta fora dos limites [-1, 1]
    if (fb < -1 || fb > 1) return 0;

    // Verifica recursivamente as subarvores esquerda e direita
    return ehAVL(raiz->esq) && ehAVL(raiz->dir);
}
```