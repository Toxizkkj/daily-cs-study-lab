# Arvores AVL em C

## 1. Teoria e Complexidade

Uma Árvore AVL é uma árvore binária de busca (BST) auto-balanceada na qual a diferença entre as alturas das subárvores esquerda e direita (chamada de Fator de Balanceamento ou $FB$) de qualquer nó não pode exceder 1. O fator é calculado como $FB = \text{altura}(esq) - \text{altura}(dir)$. Quando $|FB| > 1$, a árvore é considerada desbalanceada e passa por operações de rotação (Simples: LL/RR ou Duplas: LR/RL) para restaurar o equilíbrio.

O rebalanceamento constante garante que a altura $h$ da árvore permaneça estritamente limitada a $O(\log n)$, evitando a degradação para uma lista encadeada (pior caso de BSTs comuns). Assim, todas as operações fundamentais mantêm tempo logarítmico no pior caso.

| Operação | Caso Médio | Pior Caso | Espaço (Memória) |
| :--- | :--- | :--- | :--- |
| Busca | $O(\log n)$ | $O(\log n)$ | $O(n)$ |
| Inserção | $O(\log n)$ | $O(\log n)$ | $O(n)$ |
| Remoção | $O(\log n)$ | $O(\log n)$ | $O(n)$ |

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
    return n ? n->altura : 0;
}

int max(int a, int b) {
    return (a > b) ? a : b;
}

int obterFB(No *n) {
    return n ? altura(n->esq) - altura(n->dir) : 0;
}

No* criarNo(int chave) {
    No *no = (No*)malloc(sizeof(No));
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

No* inserir(No *no, int chave) {
    if (!no) return criarNo(chave);

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

No* menorValorNo(No *no) {
    No *atual = no;
    while (atual->esq)
        atual = atual->esq;
    return atual;
}

No* remover(No *raiz, int chave) {
    if (!raiz) return raiz;

    if (chave < raiz->chave)
        raiz->esq = remover(raiz->esq, chave);
    else if (chave > raiz->chave)
        raiz->dir = remover(raiz->dir, chave);
    else {
        if (!raiz->esq || !raiz->dir) {
            No *temp = raiz->esq ? raiz->esq : raiz->dir;
            if (!temp) {
                temp = raiz;
                raiz = NULL;
            } else {
                *raiz = *temp;
            }
            free(temp);
        } else {
            No *temp = menorValorNo(raiz->dir);
            raiz->chave = temp->chave;
            raiz->dir = remover(raiz->dir, temp->chave);
        }
    }

    if (!raiz) return raiz;

    raiz->altura = 1 + max(altura(raiz->esq), altura(raiz->dir));
    int fb = obterFB(raiz);

    // Caso LL
    if (fb > 1 && obterFB(raiz->esq) >= 0)
        return rotacaoDireita(raiz);
    // Caso LR
    if (fb > 1 && obterFB(raiz->esq) < 0) {
        raiz->esq = rotacaoEsquerda(raiz->esq);
        return rotacaoDireita(raiz);
    }
    // Caso RR
    if (fb < -1 && obterFB(raiz->dir) <= 0)
        return rotacaoEsquerda(raiz);
    // Caso RL
    if (fb < -1 && obterFB(raiz->dir) > 0) {
        raiz->dir = rotacaoDireita(raiz->dir);
        return rotacaoEsquerda(raiz);
    }

    return raiz;
}

No* buscar(No *raiz, int chave) {
    if (!raiz || raiz->chave == chave) return raiz;
    if (chave < raiz->chave) return buscar(raiz->esq, chave);
    return buscar(raiz->dir, chave);
}

void emOrdem(No *raiz) {
    if (raiz) {
        emOrdem(raiz->esq);
        printf("%d (FB: %d) ", raiz->chave, obterFB(raiz));
        emOrdem(raiz->dir);
    }
}

void liberarArvore(No *raiz) {
    if (raiz) {
        liberarArvore(raiz->esq);
        liberarArvore(raiz->dir);
        free(raiz);
    }
}

int main() {
    No *raiz = NULL;

    raiz = inserir(raiz, 10);
    raiz = inserir(raiz, 20);
    raiz = inserir(raiz, 30); // Provoca Rotação RR em 10
    raiz = inserir(raiz, 40);
    raiz = inserir(raiz, 50); // Provoca Rotação RR em 30
    raiz = inserir(raiz, 25); // Provoca Rotação RL em 20

    printf("Em-Ordem com FB: ");
    emOrdem(raiz);
    printf("\n");

    printf("Busca 25: %s\n", buscar(raiz, 25) ? "Encontrado" : "Nao Encontrado");

    raiz = remover(raiz, 30);
    printf("Em-Ordem apos remover 30: ");
    emOrdem(raiz);
    printf("\n");

    liberarArvore(raiz);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Acesso Direto à Altura de Nó Nulo (`Segfault`)**: Tentar acessar `no->altura` diretamente sem checar se `no == NULL`.
   * *Correção*: Sempre use uma função auxiliar (ex: `altura(No *n)`) que retorna `0` caso o nó seja `NULL`.
2. **Ordem Incorreta na Atualização das Alturas Durante Rotações**: Atualizar a altura do nó pai antes dos nós filhos redirecionados.
   * *Correção*: Calcule primeiro a altura do nó que desceu na árvore e só depois a do novo nó raiz da subárvore.
3. **Confusão nos Casos de Rotação Dupla (LR e RL)**: Esquecer de reatribuir o ponteiro do filho antes de aplicar a rotação principal.
   * *Exemplo LR*: `raiz->esq = rotacaoEsquerda(raiz->esq);` **deve** preceder `return rotacaoDireita(raiz);`. Sem essa reatribuição, a subárvore intermediária é desconectada, gerando um ponteiro corrompido (*dangling pointer*).

---

## 4. Exercicio com Gabarito

**Enunciado:** Desenhe/determine a estrutura resultante da árvore AVL após a inserção sequencial dos valores: `15, 20, 10, 5, 12, 8`. Identifique qual rotação ocorre ao inserir o elemento `8`.

**Gabarito:**
1. Inserções `15, 20, 10, 5, 12`: A árvore se mantém balanceada com raiz `15`.
   * Subárvore esquerda de 15: `10` (raiz), `5` (esq), `12` (dir).
   * Subárvore direita de 15: `20`.
2. Ao inserir `8`:
   * `8` vai para a direita do nó `5`.
   * O nó `10` fica com $FB = +2$ ($h_{esq}=2, h_{dir}=1$).
   * O nó filho à esquerda (`5`) tem $FB = -1$ ($h_{esq}=0, h_{dir}=1$).
   * **Diagnóstico**: Caso LR (Desbalanceamento Esquerda-Direita) no nó `10`.
3. **Resolução do Rebalanceamento**:
   * Rotação Simples à Esquerda no nó `5` (transforma o caso em LL).
   * Rotação Simples à Direita no nó `10`.
4. **Estrutura Final (Em-Ordem: 5, 8, 10, 12, 15, 20)**:
   * Raiz Principal: `15`
   * Filho Esquerdo de 15: `8` (Filho Esq: `5`, Filho Dir: `10`, cujo filho Dir é `12`).
   * Filho Direito de 15: `20`.