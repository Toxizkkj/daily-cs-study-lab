# Tabelas Hash em Memoria em C

## 1. Teoria e Complexidade

Uma Tabela Hash é uma estrutura de dados que mapeia chaves a valores para busca eficiente. Ela utiliza uma **função de dispersão (hash)**, como o método do resto da divisão (modular: `h(k) = k % TAM`), para transformar uma chave em um índice do vetor. Quando duas chaves distintas geram o mesmo índice, ocorre uma **colisão**.

As colisões são tratadas principalmente por dois métodos:
1. **Encadeamento Separado (Separate Chaining):** Cada posição do vetor aponta para uma lista encadeada. Permite inserir mais elementos que o tamanho do vetor.
2. **Endereçamento Aberto (Open Addressing):** Todos os elementos residem no próprio vetor. Havendo colisão, procura-se outra posição livre (Sondagem Linear, Quadrática ou Duplo Hashing).

### Complexidade de Tempo e Espaço

| Operação | Caso Médio | Pior Caso | Espaço |
| :--- | :--- | :--- | :--- |
| Busca | $O(1)$ | $O(n)$ | $O(n + m)$ |
| Inserção | $O(1)$ | $O(n)$ | $O(n + m)$ |
| Remoção | $O(1)$ | $O(n)$ | $O(n + m)$ |

*(Onde $n$ é o número de elementos e $m$ é o tamanho do vetor Hash. O pior caso ocorre quando todas as chaves colidem no mesmo índice).*

---

## 2. Implementacao Completa em C

Implementação usando **Encadeamento Separado**:

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int key;
    int value;
    struct Node* next;
} Node;

typedef struct {
    Node** buckets;
    int capacity;
} HashTable;

HashTable* create_table(int capacity) {
    HashTable* table = (HashTable*) malloc(sizeof(HashTable));
    table->capacity = capacity;
    table->buckets = (Node**) calloc(capacity, sizeof(Node*));
    return table;
}

int hash_function(int key, int capacity) {
    int hash = key % capacity;
    return (hash < 0) ? hash + capacity : hash;
}

void insert(HashTable* table, int key, int value) {
    int index = hash_function(key, table->capacity);
    Node* curr = table->buckets[index];
    
    while (curr != NULL) {
        if (curr->key == key) {
            curr->value = value;
            return;
        }
        curr = curr->next;
    }
    
    Node* new_node = (Node*) malloc(sizeof(Node));
    new_node->key = key;
    new_node->value = value;
    new_node->next = table->buckets[index];
    table->buckets[index] = new_node;
}

int search(HashTable* table, int key, int* found) {
    int index = hash_function(key, table->capacity);
    Node* curr = table->buckets[index];
    
    while (curr != NULL) {
        if (curr->key == key) {
            *found = 1;
            return curr->value;
        }
        curr = curr->next;
    }
    
    *found = 0;
    return -1;
}

void remove_key(HashTable* table, int key) {
    int index = hash_function(key, table->capacity);
    Node* curr = table->buckets[index];
    Node* prev = NULL;
    
    while (curr != NULL) {
        if (curr->key == key) {
            if (prev == NULL) {
                table->buckets[index] = curr->next;
            } else {
                prev->next = curr->next;
            }
            free(curr);
            return;
        }
        prev = curr;
        curr = curr->next;
    }
}

void free_table(HashTable* table) {
    for (int i = 0; i < table->capacity; i++) {
        Node* curr = table->buckets[i];
        while (curr != NULL) {
            Node* temp = curr;
            curr = curr->next;
            free(temp);
        }
    }
    free(table->buckets);
    free(table);
}

int main() {
    HashTable* ht = create_table(7);
    int found = 0;

    insert(ht, 10, 100);
    insert(ht, 17, 200); // Colisao com 10 (17 % 7 == 3 e 10 % 7 == 3)
    insert(ht, 3, 300);  // Colisao no mesmo bucket

    printf("Busca 17: %d\n", search(ht, 17, &found));
    printf("Busca 10: %d\n", search(ht, 10, &found));

    remove_key(ht, 17);
    search(ht, 17, &found);
    printf("17 encontrado apos remocao? %s\n", found ? "Sim" : "Nao");

    free_table(ht);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Resto Negativo em C (`key % TAM`):** Se a chave for negativa (ex: `-5 % 7`), C retorna um resultado negativo (`-5`). Acessar um vetor com índice negativo causa **Segmentation Fault**. Sempre trate chaves negativas na função hash.
2. **Ponteiros Perdidos na Remoção em Encadeamento:** Ao remover um elemento do meio da lista encadeada, se esquecer de atualizar o ponteiro do elemento anterior (`prev->next = curr->next`), você quebra a lista e gera um **Memory Leak**.
3. **Parada Precoce no Endereçamento Aberto:** Na remoção com endereçamento aberto, marcar a posição simplesmente como `NULL` interrompe as buscas futuras por chaves inseridas após a colisão. É necessário usar um marcador especial (ex: `DELETED` ou `TOMBSTONE`).

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função em C que receba uma tabela hash com **Endereçamento Aberto (Sondagem Linear)** e busque se uma chave existe. A tabela armazena inteiros, onde `-1` indica slot vazio e `-2` indica slot deletado.

**Gabarito:**

```c
int busca_enderecamento_aberto(int* tabela, int tamanho, int chave) {
    int hash = chave % tamanho;
    if (hash < 0) hash += tamanho;
    
    int index = hash;
    int i = 0;
    
    while (tabela[index] != -1 && i < tamanho) {
        if (tabela[index] == chave) {
            return index; // Encontrado
        }
        index = (hash + ++i) % tamanho; // Sondagem linear
    }
    
    return -1; // Nao encontrado (parou no slot vazio -1)
}
```