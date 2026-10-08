# Tabelas Hash em Memoria em C

## 1. Teoria e Complexidade

Uma Tabela Hash (ou Tabela de Dispersao) e uma estrutura de dados que mapeia chaves a valores para permitir buscas, insercoes e remocoes em tempo medio constante $O(1)$. Ela utiliza uma **funcao de dispersao modular** ($h(k) = k \bmod M$, onde $M$ e o tamanho da tabela) para converter uma chave em um indice do vetor subjacente. Para otimizar a distribuicao e reduzir colisoes, o tamanho $M$ e tipicamente um numero primo.

Colisoes ocorrem quando chaves diferentes geram o mesmo indice. As duas abordagens principais para tratamento de colisoes sao:
- **Encadeamento Separado (Separate Chaining):** Cada posicao do vetor aponta para uma lista encadeada dinâmica. Colisoes sao tratadas adicionando nos a lista do balde correspondente.
- **Enderecamento Aberto (Open Addressing):** Todos os elementos sao armazenados no proprio vetor. Quando ocorre uma colisao, a estrutura procura a proxima posicao livre via sondagem (ex: **Sondagem Linear**: $(h(k) + i) \bmod M$).

| Operacao | Caso Medio | Pior Caso | Espaco |
| :--- | :--- | :--- | :--- |
| Busca | $O(1)$ | $O(N)$ | $O(N + M)$ |
| Insercao | $O(1)$ | $O(N)$ | $O(N + M)$ |
| Remocao | $O(1)$ | $O(N)$ | $O(N + M)$ |

*Nota: O pior caso $O(N)$ ocorre quando todas as chaves colidem no mesmo indice devido a uma funcao hash ruim ou alto fator de carga ($\alpha = N/M$).*

---

## 2. Implementacao Completa em C

Implementacao de Tabela Hash com **Encadeamento Separado** em um unico bloco compilavel:

```c
#include <stdio.h>
#include <stdlib.h>

#define TAMANHO_TABELA 7

typedef struct Node {
    int chave;
    int valor;
    struct Node *proximo;
} Node;

typedef struct {
    Node **baldes;
    int tamanho;
} TabelaHash;

int funcao_hash(int chave, int tamanho) {
    int hash = chave % tamanho;
    return (hash < 0) ? hash + tamanho : hash;
}

TabelaHash* criar_tabela(int tamanho) {
    TabelaHash *tabela = (TabelaHash*) malloc(sizeof(TabelaHash));
    tabela->tamanho = tamanho;
    tabela->baldes = (Node**) calloc(tamanho, sizeof(Node*));
    return tabela;
}

void inserir(TabelaHash *tabela, int chave, int valor) {
    int indice = funcao_hash(chave, tabela->tamanho);
    Node *atual = tabela->baldes[indice];
    
    while (atual != NULL) {
        if (atual->chave == chave) {
            atual->valor = valor;
            return;
        }
        atual = atual->proximo;
    }

    Node *novo = (Node*) malloc(sizeof(Node));
    novo->chave = chave;
    novo->valor = valor;
    novo->proximo = tabela->baldes[indice];
    tabela->baldes[indice] = novo;
}

int* buscar(TabelaHash *tabela, int chave) {
    int indice = funcao_hash(chave, tabela->tamanho);
    Node *atual = tabela->baldes[indice];
    
    while (atual != NULL) {
        if (atual->chave == chave) {
            return &(atual->valor);
        }
        atual = atual->proximo;
    }
    return NULL;
}

int remover(TabelaHash *tabela, int chave) {
    int indice = funcao_hash(chave, tabela->tamanho);
    Node *atual = tabela->baldes[indice];
    Node *anterior = NULL;

    while (atual != NULL) {
        if (atual->chave == chave) {
            if (anterior == NULL) {
                tabela->baldes[indice] = atual->proximo;
            } else {
                anterior->proximo = atual->proximo;
            }
            free(atual);
            return 1;
        }
        anterior = atual;
        atual = atual->proximo;
    }
    return 0;
}

void liberar_tabela(TabelaHash *tabela) {
    for (int i = 0; i < tabela->tamanho; i++) {
        Node *atual = tabela->baldes[i];
        while (atual != NULL) {
            Node *temp = atual;
            atual = atual->proximo;
            free(temp);
        }
    }
    free(tabela->baldes);
    free(tabela);
}

int main() {
    TabelaHash *ht = criar_tabela(TAMANHO_TABELA);

    inserir(ht, 10, 100);
    inserir(ht, 17, 200); // Colisao com 10 (10 % 7 == 3, 17 % 7 == 3)
    inserir(ht, 24, 300); // Outra colisao no mesmo balde

    int *val = buscar(ht, 17);
    if (val) printf("Chave 17 encontrada: %d\n", *val);

    remover(ht, 17);
    val = buscar(ht, 17);
    printf("Chave 17 apos remocao: %s\n", val ? "Encontrada" : "Nao encontrada");

    val = buscar(ht, 24);
    if (val) printf("Chave 24 preservada: %d\n", *val);

    liberar_tabela(ht);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Restos Negativos em C:** O operador `%` em C retoma o sinal do dividendo. Se a chave for negativa (ex: `-5 % 7`), o resultado e `-5`, gerando um acesso fora dos limites da memoria (*Segmentation Fault*). Sempre corrija o indice: `(chave % M + M) % M`.
2. **Memory Leak no Encadeamento:** Liberar apenas o ponteiro do vetor principal (`free(tabela->baldes)`) deixa todos os nos das listas encadeadas orfaos na memoria. E obrigatorio percorrer lista por lista e dar `free` em cada no antes de desalocar o vetor de ponteiros.
3. **Remocao em Enderecamento Aberto:** Em tabelas com sondagem linear, remover um elemento simplesmente definindo a celula como "VAZIA" quebra a cadeia de busca de chaves inseridas apos ele. E necessario usar um marcador especial (ex: `DELETED` ou "LIXO") para indicar que a celula esta disponivel para insercao, mas nao para parar a busca.

---

## 4. Exercicio com Gabarito

**Enunciado:**
Considere uma Tabela Hash de **Enderecamento Aberto** com tamanho $M = 5$ utilizando **Sondagem Linear** com a funcao hash $h(k) = k \bmod 5$. Desenvolva a funcao de busca `int buscar_linear(int tabela[], int M, int chave)` considerando que posicoes vazias contêm `-1` e posicoes marcadas como removidas contêm `-2`. A funcao deve retornar o indice onde a chave se encontra ou `-1` caso nao exista.

**Gabarito:**

```c
int buscar_linear(int tabela[], int M, int chave) {
    int h = (chave % M + M) % M;
    
    for (int i = 0; i < M; i++) {
        int idx = (h + i) % M;
        
        if (tabela[idx] == chave) {
            return idx; // Encontrado
        }
        if (tabela[idx] == -1) {
            return -1;  // Posicao vazia interrompe a busca
        }
        // Se tabela[idx] == -2 (DELETED), continua a sondagem
    }
    
    return -1; // Tabela cheia e elemento nao encontrado
}
```