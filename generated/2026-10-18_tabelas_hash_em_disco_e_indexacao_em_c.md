# Tabelas Hash em Disco e Indexacao em C

## 1. Teoria e Complexidade

Tabelas Hash em disco permitem acesso direto a registros em arquivos binários mapeando chaves diretamente para posições físicas (offsets) no arquivo via função de espalhamento (hash). Essa abordagem evita a varredura linear ($O(N)$) do arquivo. Em dispersão estática, o arquivo possui um número fixo de posições (buckets). Na dispersão extensível, a estrutura cresce dinamicamente utilizando um diretório de ponteiros para páginas em disco.

A otimização de I/O em disco é o fator crítico de desempenho em sistemas de banco de dados. Como o acesso ao disco é ordens de grandeza mais lento que a memória RAM, estruturas em disco utilizam o cálculo de offset `posicao = hash(chave) * sizeof(Bucket)` combinado com `fseek` para realizar saltos diretos. Isso reduz o número de operações de leitura/escrita (`fread`/`fwrite`) para um número constante por busca.

| Operação | Complexidade de Tempo (Médio) | Complexidade de Tempo (Pior) | Espaço | Leituras de Disco (I/O Médio) |
| :--- | :--- | :--- | :--- | :--- |
| Busca | $O(1)$ | $O(N)$ | $O(N)$ | $O(1)$ Seeks |
| Inserção | $O(1)$ | $O(N)$ | $O(N)$ | $O(1)$ Seeks + 1 Write |
| Remoção | $O(1)$ | $O(N)$ | $O(N)$ | $O(1)$ Seeks + 1 Write |

---

## 2. Implementacao Completa em C

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TABLE_SIZE 7
#define FILE_NAME "hash_table.dat"

typedef struct {
    int id;
    char name[30];
    int state; // 0 = Livre, 1 = Ocupado, 2 = Removido (Tombstone)
} Record;

int hash_func(int id) {
    return id % TABLE_SIZE;
}

void init_file() {
    FILE *fp = fopen(FILE_NAME, "wb");
    if (!fp) exit(1);
    Record empty = {0, "", 0};
    for (int i = 0; i < TABLE_SIZE; i++) {
        fwrite(&empty, sizeof(Record), 1, fp);
    }
    fclose(fp);
}

int insert_record(Record r) {
    FILE *fp = fopen(FILE_NAME, "rb+");
    if (!fp) return 0;

    int index = hash_func(r.id);
    int start_index = index;
    Record current;

    r.state = 1;

    do {
        fseek(fp, index * sizeof(Record), SEEK_SET);
        fread(&current, sizeof(Record), 1, fp);

        if (current.state == 0 || current.state == 2) {
            fseek(fp, index * sizeof(Record), SEEK_SET);
            fwrite(&r, sizeof(Record), 1, fp);
            fclose(fp);
            return 1;
        }
        index = (index + 1) % TABLE_SIZE;
    } while (index != start_index);

    fclose(fp);
    return 0; // Tabela cheia
}

int search_record(int id, Record *out) {
    FILE *fp = fopen(FILE_NAME, "rb");
    if (!fp) return 0;

    int index = hash_func(id);
    int start_index = index;

    do {
        fseek(fp, index * sizeof(Record), SEEK_SET);
        if (fread(out, sizeof(Record), 1, fp) != 1) break;

        if (out->state == 0) break;
        if (out->state == 1 && out->id == id) {
            fclose(fp);
            return 1;
        }
        index = (index + 1) % TABLE_SIZE;
    } while (index != start_index);

    fclose(fp);
    return 0;
}

int delete_record(int id) {
    FILE *fp = fopen(FILE_NAME, "rb+");
    if (!fp) return 0;

    int index = hash_func(id);
    int start_index = index;
    Record r;

    do {
        fseek(fp, index * sizeof(Record), SEEK_SET);
        if (fread(&r, sizeof(Record), 1, fp) != 1) break;

        if (r.state == 0) break;
        if (r.state == 1 && r.id == id) {
            r.state = 2; // Exclusão lógica (Tombstone)
            fseek(fp, index * sizeof(Record), SEEK_SET);
            fwrite(&r, sizeof(Record), 1, fp);
            fclose(fp);
            return 1;
        }
        index = (index + 1) % TABLE_SIZE;
    } while (index != start_index);

    fclose(fp);
    return 0;
}

int main() {
    init_file();

    Record r1 = {10, "Alice", 1};
    Record r2 = {17, "Bob", 1};   // Colisão com id 10 (17 % 7 = 3, 10 % 7 = 3)
    Record r3 = {24, "Charlie", 1};

    insert_record(r1);
    insert_record(r2);
    insert_record(r3);

    Record res;
    if (search_record(17, &res)) {
        printf("Encontrado: ID=%d, Nome=%s\n", res.id, res.name);
    } else {
        printf("ID 17 nao encontrado.\n");
    }

    delete_record(17);

    if (search_record(17, &res)) {
        printf("Encontrado: ID=%d, Nome=%s\n", res.id, res.name);
    } else {
        printf("ID 17 removido com sucesso.\n");
    }

    remove(FILE_NAME);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Intercalação de `fread` e `fwrite` sem `fseek`:** Segundo o padrão C (ISO C), alternar entre operações de leitura e escrita no mesmo fluxo (`rb+`) sem uma chamada intermediária a `fseek`, `fsetpos` ou `fflush` gera comportamento indefinido (ub) e corrupção do ponteiro interno do arquivo.
2. **Remoção Física vs. Lógica (Tombstone):** Limpar o registro com zeros ou marcar como livre (`state = 0`) durante uma exclusão interrompe a cadeia de busca do tratamento de colisões por sondagem linear. Deve-se obrigatoriamente usar uma marcação de excluído/tombstone (`state = 2`).
3. **Padding de Structs e Offset Incorreto:** Calcular offset com aritmética manual e hardcoded (`pos * 34`) gera desalinhamento de memória. É obrigatório utilizar `sizeof(Record)` para garantir que os *paddings* inseridos pelo compilador sejam respeitados no cálculo do `fseek`.

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função em C chamada `rehash_file` que leia o arquivo binário `"hash_table.dat"` atual e crie um novo arquivo `"hash_table_resized.dat"` com o dobro do tamanho (`TABLE_SIZE * 2`), re-inserindo apenas os registros ativos (`state == 1`).

**Gabarito:**

```c
#include <stdio.h>

#define OLD_SIZE 7
#define NEW_SIZE 14

typedef struct {
    int id;
    char name[30];
    int state;
} Record;

void rehash_file(const char *old_filename, const char *new_filename) {
    FILE *in = fopen(old_filename, "rb");
    FILE *out = fopen(new_filename, "wb+");
    if (!in || !out) return;

    // Inicializa o novo arquivo com registros vazios
    Record empty = {0, "", 0};
    for (int i = 0; i < NEW_SIZE; i++) {
        fwrite(&empty, sizeof(Record), 1, out);
    }

    Record r;
    for (int i = 0; i < OLD_SIZE; i++) {
        fseek(in, i * sizeof(Record), SEEK_SET);
        if (fread(&r, sizeof(Record), 1, in) == 1 && r.state == 1) {
            int new_idx = r.id % NEW_SIZE;
            int start_idx = new_idx;
            Record tmp;

            // Sondagem linear no novo arquivo
            do {
                fseek(out, new_idx * sizeof(Record), SEEK_SET);
                fread(&tmp, sizeof(Record), 1, out);

                if (tmp.state == 0) {
                    fseek(out, new_idx * sizeof(Record), SEEK_SET);
                    fwrite(&r, sizeof(Record), 1, out);
                    break;
                }
                new_idx = (new_idx + 1) % NEW_SIZE;
            } while (new_idx != start_idx);
        }
    }

    fclose(in);
    fclose(out);
}
```