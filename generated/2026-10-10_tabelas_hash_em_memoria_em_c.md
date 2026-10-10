# Tabelas Hash em Memoria em C

## 1. Teoria e Complexidade
Uma Tabela Hash é uma estrutura de dados que mapeia chaves a valores utilizando uma **função de dispersão (hash)** para calcular o índice de acesso numérico em um vetor ($h(k) = k \pmod m$). Quando duas chaves resultam no mesmo índice, ocorre uma **colisão**. A resolução de colisões pode ser feita por **Encadeamento Separado** (cada posição do vetor aponta para uma lista encadeada dinâmica) ou **Endereçamento Aberto** (busca-se outra posição livre no próprio vetor, ex.: via sondagem linear $h(k, i) = (h(k) + i) \pmod m$).

O desempenho da tabela depende de um baixo fator de carga ($\alpha = N/M$) e de uma boa distribuição da função hash. Se houver excesso de colisões, a complexidade degrada de tempo constante para linear.

| Operação | Caso Médio | Pior Caso |
| :--- | :--- | :--- |
| **Busca** | $O(1)$ | $O(N)$ |
| **Inserção** | $O(1)$ | $O(N)$ |
| **Remoção** | $O(1)$ | $O(N)$ |
| **Espaço** | $O(M + N)$ | $O(M + N)$ |

---

## 2. Implementacao Completa em C

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define TABLE_SIZE 7

typedef struct Node {
    int key;
    int value;
    struct Node* next;
} Node;

typedef struct {
    Node** buckets;
    int size;
} HashTable;

int hash_function(int key, int size) {
    return (key % size + size) % size;
}

HashTable* create_table(int size) {
    HashTable* ht = (HashTable*)malloc(sizeof(HashTable));
    ht->size = size;
    ht->buckets = (Node**)calloc(size, sizeof(Node*));
    return ht;
}

void insert(HashTable* ht, int key, int value) {
    int idx = hash_function(key, ht->size);
    Node* curr = ht->buckets[idx];
    
    while (curr != NULL) {
        if (curr->key == key) {
            curr->value = value;
            return;
        }
        curr = curr->next;
    }

    Node* new_node = (Node*)malloc(sizeof(Node));
    new_node->key = key;
    new_node->value = value;
    new_node->next = ht->buckets[idx];
    ht->buckets[idx] = new_node;
}

bool search(HashTable* ht, int key, int* out_value) {
    int idx = hash_function(key, ht->size);
    Node* curr = ht->buckets[idx];

    while (curr != NULL) {
        if (curr->key == key) {
            if (out_value) *out_value = curr->value;
            return true;
        }
        curr = curr->next;
    }
    return false;
}

bool remove_key(HashTable* ht, int key) {
    int idx = hash_function(key, ht->size);
    Node* curr = ht->buckets[idx];
    Node* prev = NULL;

    while (curr != NULL) {
        if (curr->key == key) {
            if (prev == NULL) {
                ht->buckets[idx] = curr->next;
            } else {
                prev->next = curr->next;
            }
            free(curr);
            return true;
        }
        prev = curr;
        curr = curr->next;
    }
    return false;
}

void free_table(HashTable* ht) {
    for (int i = 0; i < ht->size; i++) {
        Node* curr = ht->buckets[i];
        while (curr != NULL) {
            Node* temp = curr;
            curr = curr->next;
            free(temp);
        }
    }
    free(ht->buckets);
    free(ht);
}

int main() {
    HashTable* ht = create_table(TABLE_SIZE);

    insert(ht, 10, 100);
    insert(ht, 17, 200); // Colisao com 10 (10 % 7 == 3 e 17 % 7 == 3)
    insert(ht, 24, 300); // Colisao adicional no indice 3

    int val;
    if (search(ht, 17, &val)) {
        printf("Chave 17 encontrada! Valor: %d\n", val);
    }

    remove_key(ht, 17);

    if (!search(ht, 17, NULL)) {
        printf("Chave 17 removida com sucesso.\n");
    }

    free_table(ht);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Resto de Divisão com Chaves Negativas:** Em C, o operador `%` com valores negativos retorna resultados negativos (ex: `-5 % 7 == -5`). Acessar um índice negativo causa **Segmentation Fault**.
   * *Correção:* Ajustar a função de dispersão para `(key % size + size) % size` ou trabalhar com `unsigned int`.

2. **Remoção em Endereçamento Aberto (Sem Tombstone):** Apagar fisicamente um elemento (`NULL` no vetor) interrompe a busca por elementos inseridos após colisão via sondagem linear.
   * *Correção:* Deve-se usar uma flag especial (ex: marcador `DELETED`/`TOMBSTONE`) em vez de simplesmente limpar a posição.

3. **Vazamento de Memória ao Liberar a Tabela:** Liberar apenas o ponteiro da tabela (`free(ht)`) ou o vetor principal sem iterar pelas listas encadeadas encadeia vazamento de memória (**Memory Leak**) de todos os nós alocados.

---

## 4. Exercicio com Gabarito

**Enunciado:** Implemente uma função para Endereçamento Aberto com Sondagem Linear que receba uma tabela (vetor de inteiros), seu tamanho, e uma chave a ser inserida. Retorne o índice onde ela foi inserida ou `-1` se a tabela estiver cheia. Considere `-1` nas posições do vetor como célula vazia.

### Gabarito:

```c
#include <stdio.h>

int insert_linear_probing(int* table, int size, int key) {
    int hash_idx = (key % size + size) % size;
    
    for (int i = 0; i < size; i++) {
        int candidate_idx = (hash_idx + i) % size;
        if (table[candidate_idx] == -1) {
            table[candidate_idx] = key;
            return candidate_idx; // Retorna o indice onde inseriu
        }
    }
    return -1; // Tabela cheia
}
```