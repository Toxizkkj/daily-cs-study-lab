# Tabelas Hash em Memoria em C

## 1. Teoria e Complexidade

Uma Tabela Hash (ou Tabela de Dispersão) é uma estrutura de dados que mapeia chaves a valores associando cada chave a um índice em um vetor através de uma **Função de Dispersão (Hash)**. O método modular mais comum é $h(k) = k \bmod M$, onde $M$ é o tamanho da tabela (de preferência um número primo para minimizar colissões).

Quando duas chaves geram o mesmo índice, ocorre uma **colisão**. As duas principais estratégias de resolução são:
1. **Encadeamento Separado (Separate Chaining):** Cada posição do vetor contém um ponteiro para uma lista encadeada dinâmica com todos os elementos que colidiram naquele índice.
2. **Endereçamento Aberto (Open Addressing):** Todos os elementos residem no próprio vetor. Na colisão, busca-se a próxima posição livre através de técnicas como Sondagem Linear ($h(k, i) = (h'(k) + i) \bmod M$).

### Complexidade Assintótica (Big-O)

| Operação | Encadeamento (Médio) | Encadeamento (Pior Caso) | Endereçamento Aberto (Médio) | Endereçamento Aberto (Pior Caso) |
| :--- | :--- | :--- | :--- | :--- |
| **Inserção** | $O(1)$ | $O(N)$ | $O(1)$ | $O(N)$ |
| **Busca** | $O(1)$ | $O(N)$ | $O(1)$ | $O(N)$ |
| **Remoção** | $O(1)$ | $O(N)$ | $O(1)$ | $O(N)$ |
| **Espaço** | $O(M + N)$ | $O(M + N)$ | $O(M)$ | $O(M)$ |

*Nota: O pior caso ocorre quando todas as chaves colidem no mesmo índice (gerando um fator de carga $\alpha = N/M$ alto).*

---

## 2. Implementacao Completa em C

Abaixo está a implementação funcional de uma Tabela Hash com **Encadeamento Separado**.

```c
#include <stdio.h>
#include <stdlib.h>

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

int hashFunction(int key, int size) {
    return (key % size + size) % size; // Tratamento para chaves negativas
}

HashTable* createTable(int size) {
    HashTable* table = (HashTable*)malloc(sizeof(HashTable));
    table->size = size;
    table->buckets = (Node**)calloc(size, sizeof(Node*));
    return table;
}

void insert(HashTable* table, int key, int value) {
    int index = hashFunction(key, table->size);
    Node* current = table->buckets[index];
    
    while (current != NULL) {
        if (current->key == key) {
            current->value = value; // Atualiza se a chave ja existe
            return;
        }
        current = current->next;
    }
    
    Node* newNode = (Node*)malloc(sizeof(Node));
    newNode->key = key;
    newNode->value = value;
    newNode->next = table->buckets[index];
    table->buckets[index] = newNode;
}

int search(HashTable* table, int key, int* found) {
    int index = hashFunction(key, table->size);
    Node* current = table->buckets[index];
    
    while (current != NULL) {
        if (current->key == key) {
            *found = 1;
            return current->value;
        }
        current = current->next;
    }
    *found = 0;
    return -1;
}

void removeKey(HashTable* table, int key) {
    int index = hashFunction(key, table->size);
    Node* current = table->buckets[index];
    Node* prev = NULL;
    
    while (current != NULL) {
        if (current->key == key) {
            if (prev == NULL) {
                table->buckets[index] = current->next;
            } else {
                prev->next = current->next;
            }
            free(current);
            return;
        }
        prev = current;
        current = current->next;
    }
}

void freeTable(HashTable* table) {
    for (int i = 0; i < table->size; i++) {
        Node* current = table->buckets[i];
        while (current != NULL) {
            Node* temp = current;
            current = current->next;
            free(temp);
        }
    }
    free(table->buckets);
    free(table);
}

int main() {
    HashTable* table = createTable(TABLE_SIZE);

    insert(table, 10, 100);
    insert(table, 17, 200); // Colisão com 10 (17 % 7 = 3)
    insert(table, 24, 300); // Colisão no mesmo bucket (24 % 7 = 3)

    int status;
    int val = search(table, 17, &status);
    if (status) printf("Chave 17 encontrada! Valor: %d\n", val);

    removeKey(table, 17);
    val = search(table, 17, &status);
    printf("Chave 17 apos remocao: %s\n", status ? "Encontrada" : "Nao encontrada");

    freeTable(table);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Valores Negativos no Operador Módulo (`%`):** Em C, o resultado do operador `%` para um dividendo negativo é negativo ou zero (ex: `-5 % 7 = -5`). Usar diretamente esse resultado gera estouro de memória (acesso invalido a vetor).
   * *Solução:* Use `(key % size + size) % size` ou `abs(key) % size`.

2. **Memory Leak ao Liberar a Tabela:** Liberar apenas o ponteiro do vetor (`free(table->buckets)`) causa vazamento de memória massivo, pois os nós encadeados continuam alocados no Heap.
   * *Solução:* Percorrer bucket por bucket com um ponteiro auxiliar limpando cada `Node` antes de dar `free` na tabela.

3. **Remoção Incorreta em Endereçamento Aberto:** Ao deletar um elemento em uma tabela com Sondagem Linear, simplesmente definir o slot como `EMPTY` quebra a cadeia de busca das chaves inseridas posteriormente.
   * *Solução:* É obrigatório utilizar uma constante ou flag especial tipo `DELETED` (*tombstone*).

---

## 4. Exercicio com Gabarito

**Enunciado:** Considere uma Tabela Hash de tamanho $M = 5$, inicialmente vazia, utilizando a função hash $h(k) = k \bmod 5$. Desenhe a estrutura final da tabela após a inserção das chaves na seguinte ordem: `12`, `7`, `22`, utilizando a estratégia de **Endereçamento Aberto por Sondagem Linear** ($h(k, i) = (h(k) + i) \bmod M$).

### Gabarito:

1. **Chave 12:**
   - $h(12) = 12 \bmod 5 = 2$.
   - Índice 2 está **livre**. Posição 2 recebe `12`.

2. **Chave 7:**
   - $h(7) = 7 \bmod 5 = 2$.
   - Colisão no índice 2! Tentativa $i=1$: $h(7, 1) = (2 + 1) \bmod 5 = 3$.
   - Índice 3 está **livre**. Posição 3 recebe `7`.

3. **Chave 22:**
   - $h(22) = 22 \bmod 5 = 2$.
   - Colisão no índice 2! Tentativa $i=1$: $(2 + 1) \bmod 5 = 3$ (ocupado por 7).
   - Tentativa $i=2$: $h(22, 2) = (2 + 2) \bmod 5 = 4$.
   - Índice 4 está **livre**. Posição 4 recebe `22`.

**Estado Final do Vetor:**
- `Vetor[0]` = VAZIO
- `Vetor[1]` = VAZIO
- `Vetor[2]` = **12**
- `Vetor[3]` = **7**
- `Vetor[4]` = **22**