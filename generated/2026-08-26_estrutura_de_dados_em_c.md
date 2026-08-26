# 📚 Licao de BSI: Estrutura de Dados em C: Criacao e Modularizacao de TADs (Tipos Abstratos de Dados em .h e .c)

**Disciplina:** Estrutura de Dados  
**Curso:** Bacharelado em Sistemas de Informacao (3º Período)  
**Professor:** Corpo Docente de Ciência da Computação e Estatística  

---

## 🎯 1. Fundamentacao Teorica e Intuicao

### 1.1 O que e um Tipo Abstrato de Dados (TAD)?
Na ciência da computação, um **Tipo Abstrato de Dados (TAD)** é um modelo matemático para tipos de dados onde o tipo é definido pelo seu **comportamento (operações)** do ponto de vista do *usuário/cliente* do código, e não pela sua *implementação*.

Diferente dos tipos primitivos da linguagem C (`int`, `float`, `char`), um TAD estabelece uma barreira clara entre:
1. **A Interface (O que a estrutura faz):** Declarada no arquivo de cabeçalho (`.h`).
2. **A Implementação (Como a estrutura faz):** Oculta no arquivo de código-fonte (`.c`).

```
 +-------------------------------------------------------+
 |                 CÓDIGO CLIENTE (main.c)                |
 +-------------------------------------------------------+
                            |
           Usa apenas funções públicas da API
                            v
 +-------------------------------------------------------+
 |                 INTERFACE (vetor.h)                   |
 |  - Declarações de Funções (Protótipos)                |
 |  - Ponteiro Opaco: typedef struct Vetor Vetor;        |
 +-------------------------------------------------------+
                            |
                 Implementado por
                            v
 +-------------------------------------------------------+
 |               IMPLEMENTAÇÃO (vetor.c)                 |
 |  - Definição da struct real (Campos ocultos)          |
 |  - Alocação de memória (malloc/realloc/free)          |
 +-------------------------------------------------------+
```

### 1.2 Por que o Encapsulamento via Ponteiro Opaco (Opaque Pointer) e Vital?
Em C, alcançamos o **encapsulamento estrito** através de *Ponteiros Opacos*. Declaramos apenas o `typedef struct Vetor Vetor;` no arquivo `.h`, sem definir os membros da `struct`. 

Isso impede que o código cliente faça acesso direto aos membros da estrutura (ex: `v->tamanho = -999;`), garantindo que **invariantes de representação** (regras de integridade dos dados) nunca sejam violadas.

### 1.3 Relevância Acadêmica e Industrial
* **Em Provas Universitárias:** Avalia-se a capacidade de gerenciar memória manualmente (`malloc`, `realloc`, `free`), modularizar código no compilador (`gcc`), evitar *dangling pointers* e manter o encapsulamento estrito.
* **Na Engenharia de Software e Banco de Dados:** O desenvolvimento de drivers, SGBDs (como a arquitetura interna do SQLite e PostgreSQL), kernels de sistemas operacionais e bibliotecas de alta performance (como a `GLib`) depende 100% da criação de TADs bem consolidados em C.

---

## 💻 2. Implementacao Pratica Completa

Vamos construir um TAD robusto de um **Vetor Dinâmico Redimensionável** (`VetorDinamico`), demonstrando a separação exata entre `.h`, `.c` e a aplicação principal `main.c`.

### 📄 Arquivo 1: `vetor.h` (Interface)

```c
#ifndef VETOR_H
#define VETOR_H

#include <stddef.h>

/* 
 * Declaração incompleta do tipo (Ponteiro Opaco).
 * O cliente do TAD sabe que 'Vetor' existe, mas não conhece seus campos internos.
 */
typedef struct Vetor Vetor;

/* 
 * Cria um vetor dinâmico com capacidade inicial especificada.
 * Retorna um ponteiro para a estrutura criada ou NULL em caso de falha de alocação.
 */
Vetor* vetor_criar(size_t capacidade_inicial);

/* 
 * Insere um elemento ao final do vetor. Se a capacidade for atingida,
 * o vetor será redimensionado automaticamente.
 * Retorna 1 em caso de sucesso e 0 em caso de erro.
 */
int vetor_inserir(Vetor *v, int elemento);

/* 
 * Obtém o elemento armazenado no índice especificado.
 * O valor retornado via ponteiro 'valor'.
 * Retorna 1 se o índice for válido e 0 caso contrário.
 */
int vetor_obter(const Vetor *v, size_t indice, int *valor);

/* 
 * Retorna o número atual de elementos armazenados no vetor.
 * Retorna 0 se o ponteiro do vetor for inválido (NULL).
 */
size_t vetor_tamanho(const Vetor *v);

/* 
 * Destrói o vetor, liberando toda a memória alocada dinamicamente.
 * O ponteiro para o vetor é ajustado para NULL para evitar 'dangling pointer'.
 */
void vetor_destruir(Vetor **v_ptr);

#endif /* VETOR_H */
```

---

### 📄 Arquivo 2: `vetor.c` (Implementação)

```c
#include <stdio.h>
#include <stdlib.h>
#include "vetor.h"

/* 
 * Definição concreta da estrutura interna.
 * Visível EXCLUSIVAMENTE dentro deste arquivo .c.
 */
struct Vetor {
    int *dados;          /* Ponteiro para o array dinâmico de elementos */
    size_t capacidade;  /* Capacidade máxima atual do array */
    size_t tamanho;     /* Quantidade atual de elementos armazenados */
};

Vetor* vetor_criar(size_t capacidade_inicial) {
    if (capacidade_inicial == 0) {
        capacidade_inicial = 4; /* Capacidade mínima padrão */
    }

    Vetor *v = (Vetor*) malloc(sizeof(Vetor));
    if (v == NULL) {
        return NULL; /* Falha de alocação da estrutura principal */
    }

    v->dados = (int*) malloc(capacidade_inicial * sizeof(int));
    if (v->dados == NULL) {
        free(v); /* Limpeza para evitar vazamento de memória parcial */
        return NULL;
    }

    v->capacidade = capacidade_inicial;
    v->tamanho = 0;

    return v;
}

int vetor_inserir(Vetor *v, int elemento) {
    if (v == NULL) {
        return 0;
    }

    /* Redimensionamento dinâmico (estratégia de duplicação) */
    if (v->tamanho == v->capacidade) {
        size_t nova_capacidade = v->capacidade * 2;
        
        /* 
         * Uso seguro de realloc utilizando variável temporária 
         * para evitar memory leak em caso de falha.
         */
        int *novos_dados = (int*) realloc(v->dados, nova_capacidade * sizeof(int));
        if (novos_dados == NULL) {
            return 0; /* Falha no redimensionamento; dados antigos continuam preservados */
        }

        v->dados = novos_dados;
        v->capacidade = nova_capacidade;
    }

    v->dados[v->tamanho] = elemento;
    v->tamanho++;

    return 1;
}

int vetor_obter(const Vetor *v, size_t indice, int *valor) {
    if (v == NULL || valor == NULL || indice >= v->tamanho) {
        return 0; /* Acesso inválido por fora dos limites ou parâmetros nulos */
    }

    *valor = v->dados[indice];
    return 1;
}

size_t vetor_tamanho(const Vetor *v) {
    if (v == NULL) {
        return 0;
    }
    return v->tamanho;
}

void vetor_destruir(Vetor **v_ptr) {
    if (v_ptr == NULL || *v_ptr == NULL) {
        return;
    }

    Vetor *v = *v_ptr;

    /* 1. Libera o buffer interno de dados */
    if (v->dados != NULL) {
        free(v->dados);
        v->dados = NULL;
    }

    /* 2. Libera o bloco da estrutura */
    free(v);

    /* 3. Aterra o ponteiro no código do cliente para evitar Dangling Pointer */
    *v_ptr = NULL;
}
```

---

### 📄 Arquivo 3: `main.c` (Código Cliente)

```c
#include <stdio.h>
#include <stdlib.h>
#include "vetor.h"

int main(void) {
    printf("=== Teste de TAD Vetor Dinamico ===\n\n");

    /* Instanciação do TAD usando a interface pública */
    Vetor *meu_vetor = vetor_criar(2);
    if (meu_vetor == NULL) {
        fprintf(stderr, "Erro crítico: Falha ao alocar memória para o vetor.\n");
        return EXIT_FAILURE;
    }

    /* Inserção de dados provocando redimensionamento automático */
    printf("Inserindo elementos...\n");
    for (int i = 10; i <= 50; i += 10) {
        if (vetor_inserir(meu