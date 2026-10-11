# Tabelas Hash em Memoria em C

## 1. Teoria e Complexidade

Uma **Tabela Hash** mapeia chaves a valores permitindo acesso de tempo constante em casos ideais. A **função de dispersão modular** $h(k) = |k| \pmod m$ calcula o índice do elemento onde $m$ é o tamanho do vetor. Como múltiplas chaves podem resultar no mesmo índice, ocorrem colisões.

As duas estratégias principais para tratar colisões são:
1. **Encadeamento Separado (Separate Chaining):** Cada posição da tabela aponta para uma lista encadeada dinâmica de nós colididos.
2. **Endereçamento Aberto (Open Addressing):** Todos os elementos são salvos no próprio vetor. Havendo colisão, busca-se outra posição livre via **sondagem linear** $h(k, i) = (h'(k) + i) \pmod m$.

| Operação | Caso Médio | Pior Caso (Alta Colisão) |
| :--- | :--- | :--- |
| Busca | $O(1)$ | $O(n)$ |
| Inserção | $O(1)$ | $O(n)$ |
| Remoção | $O(1)$ | $O(n)$ |
| Espaço | $O(m + n)$ | $O(m + n)$ |

---

## 2. Implementacao Completa em C

Abaixo está a implementação funcional da Tabela Hash com **Encadeamento Separado**.

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define TABLE_SIZE 7

typedef struct Node {
    int key;
    int value;
    struct Node *next;
} Node;

typedef struct {
    Node **buckets;
    int capacity;
} HashTable;

HashTable* create_table(int capacity) {
    HashTable *ht = malloc(sizeof(HashTable));
    ht->capacity = capacity;
    ht->buckets = calloc(capacity, sizeof(Node*));
    return ht;
}

int hash_func(HashTable *ht, int key) {
    return abs(key) % ht->capacity;
}

void insert(HashTable *ht, int key, int value) {
    int idx = hash_func(ht, key);
    Node *curr = ht->buckets[idx];
    
    while (curr) {
        if (curr->key == key) {
            curr->value = value;
            return;
        }
        curr = curr->next;
    }

    Node *new_node = malloc(sizeof(Node));
    new_node->key = key;
    new_node->value = value;
    new_node->next = ht->buckets[idx];
    ht->buckets[idx] = new_node;
}

bool search(HashTable *ht, int key, int *out_value) {
    int idx = hash_func(ht, key);
    Node *curr = ht->buckets[idx];

    while (curr) {
        if (curr->key == key) {
            if (out_value) *out_value = curr->value;
            return true;
        }
        curr = curr->next;
    }
    return false;
}

bool remove_key(HashTable *ht, int key) {
    int idx = hash_func(ht, key);
    Node *curr = ht->buckets[idx];
    Node *prev = NULL;

    while (curr) {
        if (curr->key == key) {
            if (prev) prev->next = curr->next;
            else ht->buckets[idx] = curr->next;
            free(curr);
            return true;
        }
        prev = curr;
        curr = curr->next;
    }
    return false;
}

void free_table(HashTable *ht) {
    for (int i = 0; i < ht->capacity; i++) {
        Node *curr = ht->buckets[i];
        while (curr) {
            Node *tmp = curr;
            curr = curr->next;
            free(tmp);
        }
    }
    free(ht->buckets);
    free(ht);
}

int main() {
    HashTable *ht = create_table(TABLE_SIZE);

    insert(ht, 10, 100);
    insert(ht, 17, 200); // Colide com 10 pois 10%7=3 e 17%7=3
    insert(ht, 24, 300); // Colide no mesmo bucket

    int val;
    if (search(ht, 17, &val)) {
        printf("Chave 17 encontrada: %d\n", val);
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

1. **Chaves Negativas em C:** O operador `%` em C mantém o sinal do dividendo (ex: `-10 % 7 = -3`). Acessar `buckets[-3]` gera **Segmentation Fault**. Solução: Use `abs(key) % capacity`.
2. **Vazamento na Liberação Total (Memory Leak):** Dar `free(ht->buckets)` sem percorrer cada lista liberando todos os nós (`free(node)`) de cada bucket.
3. **Deleção em Endereçamento Aberto (Tombstone):** Se remover um elemento em Sondagem Linear definindo a posição como `NULL`/vazia, você **quebra a cadeia de busca** de chaves inseridas posteriormente no mesmo bucket. É preciso usar um marcador especial (ex: `-1` ou `DELETED`).

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função em C `insert_linear_probing` que insira um elemento em uma tabela hash representada por um vetor estático/dinâmico de inteiros usando **Endereçamento Aberto com Sondagem Linear**. Considere `-1` como posição livre.

**Gabarito:**

```c
#include <stdio.h>
#include <stdbool.h>

#define CAPACITY 5
#define EMPTY -1

bool insert_linear_probing(int table[], int key) {
    int idx = key % CAPACITY;
    
    for (int i = 0; i < CAPACITY; i++) {
        int prob_idx = (idx + i) % CAPACITY;
        
        // Espaco livre ou atualização do mesmo elemento
        if (table[prob_idx] == EMPTY || table[prob_idx] == key) {
            table[prob_idx] = key;
            return true;
        }
    }
    return false; // Tabela cheia
}
```