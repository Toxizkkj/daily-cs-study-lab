# Tabelas Hash em Disco e Indexacao em C

## 1. Teoria e Complexidade

Tabelas Hash em disco mapeiam chaves para localizações físicas em arquivos binários usando funções de dispersão (hashing). A principal diferença em relação às estruturas em RAM é que o gargalo crítico de desempenho é a quantidade de operações de entrada/saída (I/O). Para minimizar acessos ao disco, o arquivo é organizado em blocos de tamanho fixo ou *buckets*, permitindo calcular o *offset* direto de leitura via deslocamento binário: $\text{Offset} = \text{Índice} \times \text{sizeof(Registro)}$.

No Hashing Estático em disco, o tratamento de colisões (como endereçamento aberto com sondagem linear ou encadeamento em áreas de *overflow*) é feito manipulando ponteiros de arquivo via `fseek`. O objetivo principal da indexação é garantir que a busca e escrita ocorram no menor número possível de ciclos de I/O (idealmente 1 ou 2 leituras de bloco).

### Tabela de Complexidade (Operações de I/O)

| Operação | Caso Médio (I/O) | Pior Caso (I/O) | Espaço em Disco |
| :--- | :--- | :--- | :--- |
| **Busca** | $O(1)$ | $O(N)$ | $O(N)$ |
| **Inserção** | $O(1)$ | $O(N)$ | $O(N)$ |
| **Remoção** | $O(1)$ | $O(N)$ | $O(N)$ |

---

## 2. Implementacao Completa em C

O código a seguir demonstra o Hashing Estático com Sondagem Linear gravado diretamente em arquivo binário.

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TABLE_SIZE 7
#define FILE_NAME "hash_table.bin"

typedef struct {
    int id;
    char name[30];
    int status; // 0: Livre, 1: Ocupado, -1: Removido (Tombstone)
} Record;

int hash_fn(int id) {
    return id % TABLE_SIZE;
}

void init_hash_file() {
    FILE *fp = fopen(FILE_NAME, "wb");
    if (!fp) return;
    Record empty = {0, "", 0};
    for (int i = 0; i < TABLE_SIZE; i++) {
        fwrite(&empty, sizeof(Record), 1, fp);
    }
    fclose(fp);
}

int insert_record(int id, const char *name) {
    FILE *fp = fopen(FILE_NAME, "rb+");
    if (!fp) return 0;

    int idx = hash_fn(id);
    Record r;

    for (int i = 0; i < TABLE_SIZE; i++) {
        int pos = (idx + i) % TABLE_SIZE;
        fseek(fp, pos * sizeof(Record), SEEK_SET);
        fread(&r, sizeof(Record), 1, fp);

        if (r.status == 0 || r.status == -1) {
            r.id = id;
            strncpy(r.name, name, sizeof(r.name) - 1);
            r.name[sizeof(r.name) - 1] = '\0';
            r.status = 1;

            fseek(fp, pos * sizeof(Record), SEEK_SET);
            fwrite(&r, sizeof(Record), 1, fp);
            fclose(fp);
            return 1;
        }
    }
    fclose(fp);
    return 0;
}

int search_record(int id, Record *out) {
    FILE *fp = fopen(FILE_NAME, "rb");
    if (!fp) return 0;

    int idx = hash_fn(id);
    Record r;

    for (int i = 0; i < TABLE_SIZE; i++) {
        int pos = (idx + i) % TABLE_SIZE;
        fseek(fp, pos * sizeof(Record), SEEK_SET);
        fread(&r, sizeof(Record), 1, fp);

        if (r.status == 0) break;
        if (r.status == 1 && r.id == id) {
            *out = r;
            fclose(fp);
            return 1;
        }
    }
    fclose(fp);
    return 0;
}

int remove_record(int id) {
    FILE *fp = fopen(FILE_NAME, "rb+");
    if (!fp) return 0;

    int idx = hash_fn(id);
    Record r;

    for (int i = 0; i < TABLE_SIZE; i++) {
        int pos = (idx + i) % TABLE_SIZE;
        fseek(fp, pos * sizeof(Record), SEEK_SET);
        fread(&r, sizeof(Record), 1, fp);

        if (r.status == 0) break;
        if (r.status == 1 && r.id == id) {
            r.status = -1;
            fseek(fp, pos * sizeof(Record), SEEK_SET);
            fwrite(&r, sizeof(Record), 1, fp);
            fclose(fp);
            return 1;
        }
    }
    fclose(fp);
    return 0;
}

int main() {
    init_hash_file();

    insert_record(10, "Alice");
    insert_record(17, "Bob"); // Colisao com ID 10 (10 % 7 == 3 e 17 % 7 == 3)

    Record r;
    if (search_record(17, &r)) {
        printf("Busca ID 17: %s (Status: %d)\n", r.name, r.status);
    }

    remove_record(10);

    if (search_record(17, &r)) {
        printf("Busca ID 17 apos deletar ID 10: %s\n", r.name);
    }

    remove(FILE_NAME);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Alternar `fread` e `fwrite` sem repositionar o ponteiro**: No padrão C, alternar entre leitura e escrita em um arquivo aberto com `"rb+"` sem uma chamada intermediária de `fseek`, `fsetpos` ou `fflush` causa comportamento indefinido.
2. **Escrever ponteiros (`char*`) em arquivo binário**: Gravar ponteiros em disco salva apenas o endereço da memória RAM atual. Ao reabrir o programa, esses endereços se tornam inválidos (causando *Segmentation Fault*). Sempre use arrays de tamanho fixo em *structs* persistentes.
3. **Esquecer de repositionar com `fseek` antes do `fwrite`**: Após ler um registro com `fread`, o cursor de arquivo avança automaticamente. Para sobrescrever o registro recém-lido, é obrigatório recuar o cursor usando `fseek(fp, -sizeof(Record), SEEK_CUR)` ou recalcular a posição absoluta com `SEEK_SET`.

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função em C chamada `update_name_in_disk` que receba o nome do arquivo, um `id` e o `new_name`. A função deve localizar o registro no arquivo hash binário usando a função hash (`id % TABLE_SIZE`) e atualizar o campo `name` diretamente no disco, efetuando o mínimo de I/O possível e sem recriar o arquivo.

**Gabarito:**

```c
int update_name_in_disk(const char *file_path, int id, const char *new_name) {
    FILE *fp = fopen(file_path, "rb+");
    if (!fp) return 0;

    int idx = id % TABLE_SIZE;
    Record r;

    for (int i = 0; i < TABLE_SIZE; i++) {
        int pos = (idx + i) % TABLE_SIZE;
        fseek(fp, pos * sizeof(Record), SEEK_SET);
        if (fread(&r, sizeof(Record), 1, fp) != 1) break;

        if (r.status == 0) break; // Registro nao existe

        if (r.status == 1 && r.id == id) {
            strncpy(r.name, new_name, sizeof(r.name) - 1);
            r.name[sizeof(r.name) - 1] = '\0';

            // Reposiciona para sobrescrever o mesmo slot
            fseek(fp, pos * sizeof(Record), SEEK_SET);
            fwrite(&r, sizeof(Record), 1, fp);
            fclose(fp);
            return 1; // Sucesso
        }
    }

    fclose(fp);
    return 0; // Nao encontrado
}
```