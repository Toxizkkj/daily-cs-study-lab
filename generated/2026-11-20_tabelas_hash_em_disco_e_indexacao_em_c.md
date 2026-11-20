# Tabelas Hash em Disco e Indexacao em C

## 1. Teoria e Complexidade

Tabelas Hash em Disco organizam dados em arquivos binários mapeando chaves diretamente para posições físicas (offsets) no disco através de uma função de espalhamento (hash). Diferente das estruturas em memória RAM, o custo dominante aqui é o **I/O de disco** (operações de leitura e escrita). O objetivo primário é minimizar chamadas a `fread` e `fwrite`, permitindo acesso direto ao registro sem percorrer o arquivo sequencialmente.

Em um esquema de Hashing Estático em disco com tratamento de colisões por Encadeamento Aberto (Sondagem Linear) ou Tombstones (marcadores de remoção), o espaço no arquivo é pré-alocado em slots fixos. O cálculo do offset no arquivo é obtido por: $\text{Offset} = \text{Índice Hash} \times \text{sizeof(Registro)}$.

| Operação | Tempo (Médio) | Tempo (Pior Caso) | Espaço (Disco) |
| :--- | :--- | :--- | :--- |
| Busca | $O(1)$ I/Os | $O(N)$ I/Os | $O(M)$ slots |
| Inserção | $O(1)$ I/Os | $O(N)$ I/Os | $O(M)$ slots |
| Remoção | $O(1)$ I/Os | $O(N)$ I/Os | $O(M)$ slots |

*Nota: $N$ é o número de elementos inseridos e $M$ é a capacidade total de slots no arquivo.*

## 2. Implementacao Completa em C

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TABLE_SIZE 7
#define FILE_NAME "hash_data.bin"

typedef struct {
    int id;
    char name[30];
    int status; // 1 = Ocupado, 0 = Vazio, -1 = Removido (Tombstone)
} Record;

int hash_func(int id) {
    return id % TABLE_SIZE;
}

void init_hash_file() {
    FILE *fp = fopen(FILE_NAME, "wb");
    if (!fp) exit(1);
    Record empty = {0, "", 0};
    for (int i = 0; i < TABLE_SIZE; i++) {
        fwrite(&empty, sizeof(Record), 1, fp);
    }
    fclose(fp);
}

int insert_record(int id, const char *name) {
    FILE *fp = fopen(FILE_NAME, "rb+");
    if (!fp) return 0;

    int idx = hash_func(id);
    int start_idx = idx;
    Record r;

    do {
        fseek(fp, idx * sizeof(Record), SEEK_SET);
        fread(&r, sizeof(Record), 1, fp);

        if (r.status == 0 || r.status == -1) {
            r.id = id;
            strncpy(r.name, name, sizeof(r.name) - 1);
            r.name[sizeof(r.name) - 1] = '\0';
            r.status = 1;

            fseek(fp, idx * sizeof(Record), SEEK_SET);
            fwrite(&r, sizeof(Record), 1, fp);
            fclose(fp);
            return 1;
        }
        idx = (idx + 1) % TABLE_SIZE;
    } while (idx != start_idx);

    fclose(fp);
    return 0; // Tabela cheia
}

int search_record(int id, Record *out) {
    FILE *fp = fopen(FILE_NAME, "rb");
    if (!fp) return 0;

    int idx = hash_func(id);
    int start_idx = idx;
    Record r;

    do {
        fseek(fp, idx * sizeof(Record), SEEK_SET);
        fread(&r, sizeof(Record), 1, fp);

        if (r.status == 0) break; // Slot vazio indica fim da busca

        if (r.status == 1 && r.id == id) {
            *out = r;
            fclose(fp);
            return 1;
        }
        idx = (idx + 1) % TABLE_SIZE;
    } while (idx != start_idx);

    fclose(fp);
    return 0;
}

int delete_record(int id) {
    FILE *fp = fopen(FILE_NAME, "rb+");
    if (!fp) return 0;

    int idx = hash_func(id);
    int start_idx = idx;
    Record r;

    do {
        fseek(fp, idx * sizeof(Record), SEEK_SET);
        fread(&r, sizeof(Record), 1, fp);

        if (r.status == 0) break;

        if (r.status == 1 && r.id == id) {
            r.status = -1; // Marca como removido (Tombstone)
            fseek(fp, idx * sizeof(Record), SEEK_SET);
            fwrite(&r, sizeof(Record), 1, fp);
            fclose(fp);
            return 1;
        }
        idx = (idx + 1) % TABLE_SIZE;
    } while (idx != start_idx);

    fclose(fp);
    return 0;
}

int main() {
    init_hash_file();

    insert_record(10, "Alice");
    insert_record(17, "Bob"); // Colisao com 10 (10 % 7 = 3, 17 % 7 = 3)
    insert_record(24, "Charlie");

    Record r;
    if (search_record(17, &r)) {
        printf("Encontrado: ID=%d, Nome=%s\n", r.id, r.name);
    } else {
        printf("ID 17 nao encontrado.\n");
    }

    delete_record(17);

    if (search_record(17, &r)) {
        printf("Encontrado: ID=%d, Nome=%s\n", r.id, r.name);
    } else {
        printf("ID 17 removido com sucesso.\n");
    }

    remove(FILE_NAME);
    return 0;
}
```

## 3. Pegadinhas de Prova

1. **Esquecer de multiplicar pelo `sizeof(Struct)` no `fseek`:** 
   O parâmetro de offset em `fseek(fp, pos, SEEK_SET)` espera a distância em **bytes**. Passar apenas o índice lógico (ex: `fseek(fp, idx, SEEK_SET)`) sobrescreve o início do arquivo e corrompe a estrutura de dados.

2. **Esquecer de reposicionar o ponteiro do arquivo antes de reescrever (`fwrite` após `fread`):**
   Ao ler um registro com `fread`, o ponteiro do arquivo avança automaticamente `sizeof(Struct)` bytes. Se você tentar atualizar o registro lido chamando `fwrite` imediatamente, escreverá no slot **seguinte**. É obrigatório executar um `fseek` de volta para a posição correta antes do `fwrite`.

3. **Interromper a busca ao encontrar um registro removido (Tombstone):**
   Ao usar sondagem linear, a remoção deve ser **lógica** (`status = -1`). Se a busca parar ao encontrar um slot com valor `-1`, elementos inseridos após colisão naquele slot se tornarão inacessíveis. A busca só deve parar em um slot estritamente **vazio** (`status = 0`).

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função em C chamada `count_occupied` que recebe o nome do arquivo binário de tabela hash e retorna a quantidade total de registros ativos (com `status == 1`) no disco, sem carregar todo o arquivo para a memória de uma única vez.

**Gabarito Explicado:**

```c
int count_occupied(const char *filename) {
    FILE *fp = fopen(filename, "rb");
    if (!fp) return -1;

    Record r;
    int count = 0;

    // Le registro por registro sequencialmente do disco reduzindo uso de RAM
    while (fread(&r, sizeof(Record), 1, fp) == 1) {
        if (r.status == 1) {
            count++;
        }
    }

    fclose(fp);
    return count;
}
```