# Tabelas Hash em Disco e Indexacao em C

## 1. Teoria e Complexidade

Indexação por Tabela Hash em disco mapeia chaves diretamente para posições físicas em arquivos binários. Em vez de percorrer o arquivo sequencialmente ($O(N)$), a função hash calcula o deslocamento em bytes (*byte offset*) via `offset = index * sizeof(Registro)`. Isso permite posicionar o ponteiro do arquivo diretamente no bloco correto com `fseek`, minimizando operações de E/S (I/O), que são o principal gargalo em sistemas de arquivos.

O tratamento de colisões em disco geralmente utiliza **Endereçamento Aberto (Sondagem Linear)** ou **Buckets de Overflow**. Na remoção, é indispensável o uso de marcas lógicas (*tombstones* ou estado `DELETED`) para não interromper a cadeia de busca de elementos colididos posteriormente.

| Operação | Caso Médio (I/O) | Pior Caso (I/O) | Espaço |
| :--- | :--- | :--- | :--- |
| Busca | $O(1)$ | $O(N)$ | $O(N)$ |
| Inserção | $O(1)$ | $O(N)$ | $O(N)$ |
| Remoção | $O(1)$ | $O(N)$ | $O(N)$ |

---

## 2. Implementacao Completa em C

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TABLE_SIZE 7
#define SLOTS_EMPTY 0
#define SLOTS_OCCUPIED 1
#define SLOTS_DELETED 2

typedef struct {
    int id;
    char name[30];
    int status;
} Record;

int hash_fn(int id) {
    return id % TABLE_SIZE;
}

void init_disk_table(const char *filename) {
    FILE *f = fopen(filename, "wb");
    if (!f) return;
    Record empty_rec = {0, "", SLOTS_EMPTY};
    for (int i = 0; i < TABLE_SIZE; i++) {
        fwrite(&empty_rec, sizeof(Record), 1, f);
    }
    fclose(f);
}

int insert_record(const char *filename, int id, const char *name) {
    FILE *f = fopen(filename, "rb+");
    if (!f) return 0;
    
    int idx = hash_fn(id);
    int start = idx;
    Record r;
    
    do {
        fseek(f, idx * sizeof(Record), SEEK_SET);
        fread(&r, sizeof(Record), 1, f);
        
        if (r.status == SLOTS_EMPTY || r.status == SLOTS_DELETED) {
            r.id = id;
            strncpy(r.name, name, sizeof(r.name) - 1);
            r.name[sizeof(r.name) - 1] = '\0';
            r.status = SLOTS_OCCUPIED;
            
            fseek(f, idx * sizeof(Record), SEEK_SET);
            fwrite(&r, sizeof(Record), 1, f);
            fclose(f);
            return 1;
        }
        idx = (idx + 1) % TABLE_SIZE;
    } while (idx != start);
    
    fclose(f);
    return 0;
}

int search_record(const char *filename, int id, Record *out) {
    FILE *f = fopen(filename, "rb");
    if (!f) return 0;
    
    int idx = hash_fn(id);
    int start = idx;
    Record r;
    
    do {
        fseek(f, idx * sizeof(Record), SEEK_SET);
        fread(&r, sizeof(Record), 1, f);
        
        if (r.status == SLOTS_EMPTY) break;
        
        if (r.status == SLOTS_OCCUPIED && r.id == id) {
            if (out) *out = r;
            fclose(f);
            return 1;
        }
        idx = (idx + 1) % TABLE_SIZE;
    } while (idx != start);
    
    fclose(f);
    return 0;
}

int delete_record(const char *filename, int id) {
    FILE *f = fopen(filename, "rb+");
    if (!f) return 0;
    
    int idx = hash_fn(id);
    int start = idx;
    Record r;
    
    do {
        fseek(f, idx * sizeof(Record), SEEK_SET);
        fread(&r, sizeof(Record), 1, f);
        
        if (r.status == SLOTS_EMPTY) break;
        
        if (r.status == SLOTS_OCCUPIED && r.id == id) {
            r.status = SLOTS_DELETED;
            fseek(f, idx * sizeof(Record), SEEK_SET);
            fwrite(&r, sizeof(Record), 1, f);
            fclose(f);
            return 1;
        }
        idx = (idx + 1) % TABLE_SIZE;
    } while (idx != start);
    
    fclose(f);
    return 0;
}

int main() {
    const char *db_file = "hashtable.bin";
    init_disk_table(db_file);
    
    insert_record(db_file, 10, "Servidor A");
    insert_record(db_file, 17, "Servidor B"); // Colisao com 10 (17 % 7 == 3 % 7)
    
    Record res;
    if (search_record(db_file, 17, &res)) {
        printf("Encontrado: ID=%d, Nome=%s\n", res.id, res.name);
    }
    
    delete_record(db_file, 10);
    
    if (search_record(db_file, 17, &res)) {
        printf("Pos-Remocao de 10: ID=%d ainda encontrado.\n", res.id);
    }
    
    remove(db_file);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Alternância Leitura/Escrita sem Reposicionamento:** No padrão C (ANSI C), alternar entre `fread` e `fwrite` no mesmo ponteiro `FILE*` (modo `rb+`) sem chamar uma função de reposicionamento (`fseek`, `fsetpos` ou `fflush`) gera **Comportamento Indefinido (Undefined Behavior)**. Sempre reposite o ponteiro antes de escrever um registro recém-lido.
2. **Ponteiros em Structs Salvas em Disco:** Gravar uma `struct` que contém ponteiros (ex: `char *nome`) em disco salva apenas o endereço de memória RAM. Ao reabrir o arquivo, esse ponteiro causará **Segfault** ao ser desreferenciado. Em disco, use buffers estáticos (ex: `char nome[30]`).
3. **Resetar com `SLOTS_EMPTY` na Remoção:** Limpar um slot removido definindo-o como `EMPTY` quebra a cadeia de busca de chaves que sofreram colisão e foram gravadas em slots posteriores. É obrigatório marcar como `DELETED` (*tombstone*).

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função em C chamada `contar_acessos_disco` que busca um `id` no arquivo hash e retorna o **número de operações de leitura (`fread`)** realizadas no disco até encontrar o elemento ou concluir que ele não existe.

**Gabarito:**

```c
int contar_acessos_disco(const char *filename, int id) {
    FILE *f = fopen(filename, "rb");
    if (!f) return -1;
    
    int idx = hash_fn(id);
    int start = idx;
    int leituras = 0;
    Record r;
    
    do {
        fseek(f, idx * sizeof(Record), SEEK_SET);
        if (fread(&r, sizeof(Record), 1, f) == 1) {
            leituras++;
        }
        
        if (r.status == SLOTS_EMPTY) break;
        if (r.status == SLOTS_OCCUPIED && r.id == id) break;
        
        idx = (idx + 1) % TABLE_SIZE;
    } while (idx != start);
    
    fclose(f);
    return leituras;
}
```