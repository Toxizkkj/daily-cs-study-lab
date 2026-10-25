# Tabelas Hash em Disco e Indexacao em C

## 1. Teoria e Complexidade

Tabelas Hash em disco mapeiam chaves para posições físicas em arquivos usando funções de dispersão (*hashing*). Ao contrário da memória RAM, o gargalo principal em estruturas persistentes é o custo de I/O (operações de leitura e escrita no disco). Para minimizar o I/O, os dados são organizados em arquivos binários com registros de tamanho fixo. O deslocamento do registro é calculado diretamente por $Offset = hash(chave) \times sizeof(Registro)$, permitindo acesso direto usando `fseek` sem percorrer o arquivo sequencialmente.

O tratamento de colisões em disco (como o endereçamento aberto por sondagem linear) reutiliza posições marcadas como removidas (*tombstones*) e requer controle rigoroso do ponteiro de leitura/escrita do arquivo. O Hashing Estático em arquivo oferece acessos extremamente rápidos ($O(1)$ I/O em média), sendo a base para sistemas de indexação de arquivos de dados.

| Operação | Tempo (Médio) | Tempo (Pior) | I/O Disco (Médio) | I/O Disco (Pior) | Espaço em Disco |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Busca** | $O(1)$ | $O(N)$ | $O(1)$ | $O(N)$ | $O(N)$ |
| **Inserção** | $O(1)$ | $O(N)$ | $O(1)$ | $O(N)$ | $O(N)$ |
| **Remoção** | $O(1)$ | $O(N)$ | $O(1)$ | $O(N)$ | $O(N)$ |

---

## 2. Implementacao Completa em C

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TABLE_SIZE 7
#define FILENAME "hash_disk.dat"

typedef struct {
    int id;
    char name[30];
    int active; // 0: Vazio, 1: Ocupado, -1: Removido (Tombstone)
} Record;

int hash_function(int id) {
    return id % TABLE_SIZE;
}

void init_hash_file(FILE *fp) {
    Record empty = {0, "", 0};
    fseek(fp, 0, SEEK_SET);
    for (int i = 0; i < TABLE_SIZE; i++) {
        fwrite(&empty, sizeof(Record), 1, fp);
    }
}

int insert_record(FILE *fp, int id, const char *name) {
    int index = hash_function(id);
    Record current;

    for (int i = 0; i < TABLE_SIZE; i++) {
        int pos = (index + i) % TABLE_SIZE;
        fseek(fp, pos * sizeof(Record), SEEK_SET);
        fread(&current, sizeof(Record), 1, fp);

        if (current.active == 0 || current.active == -1) {
            Record new_rec;
            new_rec.id = id;
            strncpy(new_rec.name, name, sizeof(new_rec.name) - 1);
            new_rec.name[sizeof(new_rec.name) - 1] = '\0';
            new_rec.active = 1;

            fseek(fp, pos * sizeof(Record), SEEK_SET);
            fwrite(&new_rec, sizeof(Record), 1, fp);
            return pos;
        }
    }
    return -1; // Tabela cheia
}

int search_record(FILE *fp, int id, Record *res) {
    int index = hash_function(id);
    Record current;

    for (int i = 0; i < TABLE_SIZE; i++) {
        int pos = (index + i) % TABLE_SIZE;
        fseek(fp, pos * sizeof(Record), SEEK_SET);
        fread(&current, sizeof(Record), 1, fp);

        if (current.active == 0) return -1; // Slot nunca usado: para a busca
        if (current.active == 1 && current.id == id) {
            if (res) *res = current;
            return pos;
        }
    }
    return -1; // Nao encontrado
}

int remove_record(FILE *fp, int id) {
    Record r;
    int pos = search_record(fp, id, &r);
    if (pos != -1) {
        r.active = -1; // Marcacao de tombstone
        fseek(fp, pos * sizeof(Record), SEEK_SET);
        fwrite(&r, sizeof(Record), 1, fp);
        return 1;
    }
    return 0;
}

int main() {
    FILE *fp = fopen(FILENAME, "wb+");
    if (!fp) {
        perror("Erro ao abrir arquivo");
        return 1;
    }

    init_hash_file(fp);

    // Insercoes (com colisao entre ID 10 e ID 17, pois 10 % 7 = 3 e 17 % 7 = 3)
    insert_record(fp, 10, "Alice");
    insert_record(fp, 17, "Bob");
    insert_record(fp, 24, "Charlie");

    Record target;
    printf("--- BUSCA --- \n");
    if (search_record(fp, 17, &target) != -1) {
        printf("Encontrado no disco: ID=%d, Nome=%s\n", target.id, target.name);
    } else {
        printf("ID 17 nao encontrado.\n");
    }

    printf("\n--- REMOCAO E REBUSCA ---\n");
    remove_record(fp, 17);
    if (search_record(fp, 17, &target) == -1) {
        printf("ID 17 removido com sucesso.\n");
    }

    if (search_record(fp, 24, &target) != -1) {
        printf("Cadeia preservada! Encontrado ID=%d, Nome=%s\n", target.id, target.name);
    }

    fclose(fp);
    remove(FILENAME); // Libera o arquivo do SO
    return 0;
}
```

---

## 3. Pegadinhas de Prova

1. **Avanço Automático do Ponteiro de Arquivo**: Chamar `fread` move o ponteiro do arquivo para a posição posterior. Se você tentar fazer um `fwrite` logo em seguida sem recalcular a posição com `fseek`, sobrescreverá o registro **seguinte**, corrompendo a tabela.
2. **Ignorar Marcadores de Remoção (*Tombstones*)**: Ao remover um elemento de uma tabela hash com sondagem linear em disco, zerar o registro (`active = 0`) interrompe buscas futuras de elementos inseridos após uma colisão. Deve-se usar um marcador exclusivo (`active = -1`).
3. **Escrita de Memória Lixo (Struct Padding)**: Fazer `fwrite(&struct, sizeof(struct), ...)` sem inicializar completamente a struct faz com que lixo de memória da RAM seja escrito no disco, dificultando depurações e invalidando testes binários determinísticos.

---

## 4. Exercicio com Gabarito

**Enunciado**: Escreva uma função em C `int ler_direto(FILE *fp, int hash_pos, Record *out)` que realize o cálculo do offset absoluto e execute apenas **1 operação de I/O de leitura** no arquivo. A função deve retornar `1` se o slot apontado por `hash_pos` contiver um registro ativo (`active == 1`), e `0` caso contrário ou se a operação de leitura falhar.

**Gabarito**:

```c
int ler_direto(FILE *fp, int hash_pos, Record *out) {
    if (!fp || !out || hash_pos < 0) return 0;

    // Posiciona o ponteiro diretamente no offset do slot desejado
    if (fseek(fp, hash_pos * sizeof(Record), SEEK_SET) != 0) {
        return 0;
    }

    // Executa exatamente 1 I/O
    if (fread(out, sizeof(Record), 1, fp) != 1) {
        return 0;
    }

    // Retorna se o registro lido esta ativo
    return (out->active == 1);
}
```