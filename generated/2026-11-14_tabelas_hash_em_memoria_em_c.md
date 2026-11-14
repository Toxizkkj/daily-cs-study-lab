# Tabelas Hash em Memoria em C

## 1. Teoria e Complexidade

Uma Tabela Hash é uma estrutura de dados que mapeia chaves a valores utilizando uma função de dispersão (*hash function*). A função calcula um índice a partir da chave (geralmente via aritmética modular: $h(k) = k \bmod \text{TAM}$), permitindo acesso direto à memória. Quando duas chaves resultam no mesmo índice, ocorre uma **colisão**.

As duas estratégias principais para tratamento de colisões são:
1. **Encadeamento Separado (*Separate Chaining*):** Cada posição do vetor é um ponteiro para uma lista encadeada. Permite fator de carga maior que 1.
2. **Endereçamento Aberto (*Open Addressing*):** Todos os elementos são armazenados no próprio vetor. Em caso de colisão, busca-se outra posição livre (ex: Sondagem Linear: $h(k, i) = (h'(k) + i) \bmod \text{TAM}$).

| Operação | Caso Médio | Pior Caso | Espaço |
| :--- | :--- | :--- | :--- |
| **Busca** | $O(1)$ | $O(n)$ | $O(n + m)$ (Encadeamento) |
| **Inserção** | $O(1)$ | $O(n)$ | $O(m)$ (Endereçamento Aberto) |
| **Remoção** | $O(1)$ | $O(n)$ | *$n$ = elementos, $m$ = tamanho da tabela* |

---

## 2. Implementacao Completa em C

Implementação usando **Encadeamento Separado** com alocação dinâmica.

```c
#include <stdio.h>
#include <stdlib.h>

#define TAM 7

typedef struct Node {
    int chave;
    int valor;
    struct Node* prox;
} Node;

typedef struct {
    Node* baldes[TAM];
} TabelaHash;

int funcao_hash(int chave) {
    int idx = chave % TAM;
    return (idx < 0) ? idx + TAM : idx;
}

TabelaHash* criar_tabela() {
    TabelaHash* t = (TabelaHash*)malloc(sizeof(TabelaHash));
    for (int i = 0; i < TAM; i++) {
        t->baldes[i] = NULL;
    }
    return t;
}

void inserir(TabelaHash* t, int chave, int valor) {
    int idx = funcao_hash(chave);
    Node* atual = t->baldes[idx];
    
    while (atual != NULL) {
        if (atual->chave == chave) {
            atual->valor = valor;
            return;
        }
        atual = atual->prox;
    }

    Node* novo = (Node*)malloc(sizeof(Node));
    novo->chave = chave;
    novo->valor = valor;
    novo->prox = t->baldes[idx];
    t->baldes[idx] = novo;
}

int buscar(TabelaHash* t, int chave, int* valor_encontrado) {
    int idx = funcao_hash(chave);
    Node* atual = t->baldes[idx];
    
    while (atual != NULL) {
        if (atual->chave == chave) {
            *valor_encontrado = atual->valor;
            return 1;
        }
        atual = atual->prox;
    }
    return 0;
}

int remover(TabelaHash* t, int chave) {
    int idx = funcao_hash(chave);
    Node* atual = t->baldes[idx];
    Node* anterior = NULL;

    while (atual != NULL) {
        if (atual->chave == chave) {
            if (anterior == NULL) {
                t->baldes[idx] = atual->prox;
            } else {
                anterior->prox = atual->prox;
            }
            free(atual);
            return 1;
        }
        anterior = atual;
        atual = atual->prox;
    }
    return 0;
}

void liberar_tabela(TabelaHash* t) {
    for (int i = 0; i < TAM; i++) {
        Node* atual = t->baldes[i];
        while (atual != NULL) {
            Node* temp = atual;
            atual = atual->prox;
            free(temp);
        }
    }
    free(t);
}

int main() {
    TabelaHash* tabela = criar_tabela();

    inserir(tabela, 10, 100);
    inserir(tabela, 17, 200); // Colisão com 10 (10 % 7 = 3 e 17 % 7 = 3)
    inserir(tabela, 5, 500);

    int valor;
    if (buscar(tabela, 17, &valor)) {
        printf("Chave 17 encontrada! Valor: %d\n", valor);
    }

    remover(tabela, 17);

    if (!buscar(tabela, 17, &valor)) {
        printf("Chave 17 removida com sucesso.\n");
    }

    liberar_tabela(tabela);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Restos Negativos em C:** A operação `%` em C pode retornar valores negativos se a chave for negativa (ex: `-10 % 7 = -3`). Acessar `vetor[-3]` gera **Segmentation Fault**. Solução: ajustar o resto para ser sempre positivo (`(idx < 0) ? idx + TAM : idx`).
2. **Memory Leak no Encadeamento:** Liberar o vetor da tabela (`free(t)`) sem percorrer e desalocar cada nó de cada lista encadeada deixa todos os nós órfãos na memória.
3. **Buracos no Endereçamento Aberto:** Na remoção em tabelas com endereçamento aberto, não se deve simplesmente limpar a posição (`NULL` ou `-1`). É preciso colocar um marcador especial (`DELETED` ou `DUMMY`), caso contrário, buscas por chaves inseridas após colisões serão interrompidas precocemente.

---

## 4. Exercicio com Gabarito

**Enunciado:** Implemente uma função de inserção para uma tabela hash simples de **Endereçamento Aberto** usando **Sondagem Linear**. O vetor tem tamanho `TAM`, posições vazias contêm `-1`, e posições marcadas como removidas contêm `-2`. A função deve retornar `1` em sucesso e `0` se a tabela estiver cheia.

**Gabarito:**

```c
#define TAM 5
#define VAZIO -1
#define DELETED -2

int inserir_enderecamento_aberto(int tabela[], int chave) {
    int idx_base = chave % TAM;
    if (idx_base < 0) idx_base += TAM;

    for (int i = 0; i < TAM; i++) {
        int idx = (idx_base + i) % TAM;
        
        // Insere na primeira vaga disponível (vazia ou deletada)
        if (tabela[idx] == VAZIO || tabela[idx] == DELETED) {
            tabela[idx] = chave;
            return 1;
        }
    }
    return 0; // Tabela cheia
}
```