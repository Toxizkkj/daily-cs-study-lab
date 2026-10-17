# Tabelas Hash em Disco e Indexacao em C

## 1. Teoria e Complexidade

Tabelas Hash em Disco mapeiam chaves diretamente para posições offset dentro de um arquivo binário. O principal objetivo dessa técnica é minimizar o custo de I/O (operações de leitura e escrita em disco), que é ordens de grandeza mais lento do que o acesso à memória RAM. Ao utilizar funções de espalhamento (*hashing*) combinadas com o posicionamento direto do ponteiro de arquivo (`fseek`), acessamos qualquer registro sem a necessidade de percorrer o arquivo sequencialmente.

Para lidar com colisões sem alocação dinâmica contínua no arquivo, técnicas de *Static Hashing* usam endereçamento aberto (como a sondagem linear) ou blocos fixos (*buckets*). As remoções utilizam marcadores de exclusão lógica (*tombstones* ou lápides) para manter a integridade da cadeia de busca sem a necessidade de reorganizar o arquivo em disco durante as operações de exclusão.

| Operação | Complexidade Temporal (RAM) | Acessos I/O (Disco - Médio) | Acessos I/O (Disco - Pior) | Espaço Extra |
| :--- | :--- | :--- | :--- | :--- |
| **Busca** | $O(1)$ | $O(1)$ | $O(N)$ | $O(1)$ |
| **Inserção** | $O(1)$ | $O(1)$ | $O(N)$ | $O(1)$ |
| **Remoção** | $O(1)$ | $O(1)$ | $O(N)$ | $O(1)$ |
| **Espaço** | $O(N)$ | $O(N)$ | $O(N)$ | $O(N)$ em Disco |

---

## 2. Implementacao Completa em C

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TABLE_SIZE 11
#define EMPTY 0
#define OCCUPIED 1
#define DELETED 2

typedef struct {
    int id;
    char name[30];
    int status;
} Record;

int hash_function(int id) {
    return id % TABLE_SIZE;
}

void init_db(const char *filename) {
    FILE *fp = fopen(filename, "wb");
    if (!fp) return;

    Record empty_rec = {0, "", EMPTY};
    for (int i = 0; i < TABLE_SIZE; i++) {
        fwrite(&empty_rec, sizeof(Record), 1, fp);
    }
    fclose(fp);
}

int insert_record(const char *filename, Record r) {
    FILE *fp = fopen(filename, "rb+");
    if (!fp) return 0;

    int index = hash_function(r.id);
    int start_index = index;
    Record current;

    do {
        fseek(fp, index * sizeof(Record), SEEK_SET);
        fread(&current, sizeof(Record), 1, fp);

        if (current.status == EMPTY || current.status == DELETED) {
            r.status = OCCUPIED;
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

int search_record(const char *filename, int id, Record *out) {
    FILE *fp = fopen(filename, "rb");
    if (!fp) return 0;

    int index = hash_function(id);
    int start_index = index;
    Record current;

    do {
        fseek(fp, index * sizeof(Record), SEEK_SET);
        if (fread(&current, sizeof(Record), 1, fp) != 1) break;

        if (current.status == EMPTY) break;
        if (current.status == OCCUPIED && current.id == id) {
            *out = current;
            fclose(fp);
            return 1;
        }
        index = (index + 1) % TABLE_SIZE;
    } while (index != start_index);

    fclose(fp);
    return 0;
}

int delete_record(const char *filename, int id) {
    FILE *fp = fopen(filename, "rb+");
    if (!fp) return 0;

    int index = hash_function(id);
    int start_index = index;
    Record current;

    do {
        fseek(fp, index * sizeof(Record), SEEK_SET);
        if (fread(&current, sizeof(Record), 1, fp) != 1) break;

        if (current.status == EMPTY) break;
        if (current.status == OCCUPIED && current.id == id) {
            current.status = DELETED;
            fseek(fp, index * sizeof(Record), SEEK_SET);
            fwrite(&current, sizeof(Record), 1, fp);
            fclose(fp);
            return 1;
        }
        index = (index + 1) % TABLE_SIZE;
    } while (index != start_index);

    fclose(fp);
    return 0;
}

int main() {
    const char *db = "hash_table.bin";
    init_db(db);

    Record r1 = {12, "Alice", OCCUPIED};
    Record r2 = {23, "Bob", OCCUPIED};

    insert_record(db, r1);
    insert_record(db, r2);

    Record found;
    if (search_record(db, 23, &found)) {
        printf("Busca (ID 23): %s | Slot Hash: %d\n", found.name, hash_function(23));
    }

    delete_record(db, 12);
    printf("Removido ID 12.\n");

    if (search_record(db, 23, &found)) {
        printf("Busca pos-remocao (ID 23): %s (Mantido via Lápide)\n", found.name);
    }

    if (!search_record(db, 12, &found)) {
        printf("ID 12 nao encontrado no arquivo.\n");
    }

    remove(db);
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Esquecer o Reposicionamento antes do `fwrite`**:
   Ao alternar entre `fread` e `fwrite` no mesmo arquivo em modo `"rb+"`, a leitura desloca o ponteiro para o próximo registro. Tentar escrever imediatamente sem executar um `fseek` explícito sobrescreverá a posição errada do arquivo ou causará comportamento indefinido segundo o padrão C.

2. **Tratamento Errado de Remocao Lógica (`DELETED`)**:
   Parar a busca ao encontrar um slot `DELETED` quebra a resolução de colisões por sondagem linear. A busca só deve parar quando encontrar um slot `EMPTY` ou a própria chave buscada.

3. **Incompatibilidade de Struct Padding / Alignment**:
   Gravar structs com tipos mistos diretamente via `fwrite` pode variar o layout em bytes dependendo da arquitetura ou do alinhamento do compilador. Em sistemas reais de banco de dados, exige-se empacotamento (`#pragma pack(1)`) ou serialização manual do buffer.

---

## 4. Exercicio com Gabarito

**Enunciado:** Escreva uma função em C chamada `calculate_load_factor` que abre o arquivo da tabela hash binária, lê os registros diretamente do disco e retorna o Fator de Carga ($F = \frac{\text{Registros Ocupados}}{\text{Total de Slots}}$) como um tipo `double`.

### Gabarito Explicado e Código:

```c
double calculate_load_factor(const char *filename) {
    FILE *fp = fopen(filename, "rb");
    if (!fp) return 0.0;

    Record r;
    int occupied_count = 0;
    int total_slots = 0;

    // Leitura sequencial do arquivo binario para medicao de ocupacao
    while (fread(&r, sizeof(Record), 1, fp) == 1) {
        total_slots++;
        if (r.status == OCCUPIED) {
            occupied_count++;
        }
    }

    fclose(fp);

    if (total_slots == 0) return 0.0;
    return (double)occupied_count / total_slots;
}
```