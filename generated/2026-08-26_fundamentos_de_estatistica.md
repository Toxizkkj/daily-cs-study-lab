# 📚 Licao de BSI: Fundamentos de Estatistica: Estatistica Descritiva: Medidas de Posicao (Media, Mediana, Moda) e Sensibilidade a Outliers

---

## 🎯 1. Fundamentacao Teorica & Intuicao

Olá, alunos. Sejam bem-vindos a mais uma aula de Estatística Computacional do nosso curso de Bacharelado em Sistemas de Informação. 

Na aula de hoje, vamos construir a base de toda a análise exploratória de dados (**EDA - Exploratory Data Analysis**): as **Medidas de Posição** (ou de Tendência Central). Como futuros bacharéis em Sistemas de Informação, vocês não usarão esses conceitos apenas para passar na disciplina; vocês os utilizarão para resumir a latência de microserviços, monitorar utilização de CPU em clusters, avaliar a acurácia de modelos de *Machine Learning* e interpretar logs de dados massivos.

### 1.1 As Três Medidas Clássicas de Posição

Imagine que temos um conjunto de dados unidimensional $X = \{x_1, x_2, \dots, x_n\}$, representando $n$ observações numéricas (ex: tempo de resposta de requisições em milissegundos).

1. **Média Aritmética ($\bar{x}$):** É o centro de gravidade (ponto de equilíbrio) dos dados. Numericamente, é a soma de todos os valores dividida pela quantidade total de observações. 
2. **Mediana ($Md$ ou $Q_2$):** É o valor central que divide o conjunto de dados ordenado em duas partes com exatamente a mesma quantidade de elementos (50% abaixo, 50% acima). Corresponde ao 2º Quartil ou 50º Percentil.
3. **Moda ($Mo$):** É o valor (ou valores) de maior frequência absoluta no conjunto de dados. Diferente da média e da mediana, a moda pode ser aplicada a variáveis qualitativas/categóricas (ex: o método HTTP mais requisitado: `GET` ou `POST`).

---

### 1.2 O Fenômeno dos Outliers e a Sensibilidade das Métricas

Um **Outlier** (ou valor discrepante) é uma observação que se afasta significativamente do padrão das demais observações do conjunto. Em computação, outliers ocorrem o tempo todo: *garbage collection pauses*, gargalos de rede temporários, picos de tráfego (DDoS) ou falhas de hardware.

* **A Média é altamente SENSÍVEL a Outliers.** Matematicamente, como a média soma todos os termos ($x_i$), um único valor $x_k \to \infty$ fará com que $\bar{x} \to \infty$. A média "é puxada" na direção do outlier.
* **A Mediana é ROBUSTA a Outliers.** Como a mediana depende apenas da **ordem** dos dados e não do valor absoluto das extremidades, alterar um valor extremo não altera a posição do elemento central (desde que a ordem relativa da metade inferior/superior não seja destruída).
* **A Moda** é insensível a outliers, a menos que o outlier se repita tantas vezes a ponto de alterar a frequência máxima (o que o tornaria um padrão, e não um outlier).

#### Exemplo Intuitivo no Contexto de T.I.:
Considere o tempo de resposta (em ms) de 5 requisições de um banco de dados:
* Servidor A: `[10ms, 12ms, 11ms, 13ms, 10ms]`
* Servidor B (com gargalo de I/O): `[10ms, 12ms, 11ms, 13ms, 5000ms]`

| Servidor | Média | Mediana | Moda |
| :--- | :--- | :--- | :--- |
| **A** | 11.2 ms | 11.0 ms | 10.0 ms |
| **B** | **1009.2 ms** | **11.0 ms** | 10.0 ms |

Se você apresentar a **Média** para o Diretor de Tecnologia no Servidor B, dirá que o sistema leva **1 segundo** por requisição. Na realidade, 80% dos usuários experimentaram 11ms de latência! A média mascarou a realidade do sistema, enquanto a mediana preservou o comportamento da maioria das requisições.

---

### 1.3 Onde este conceito é cobrado em provas e entrevistas?

* **Provas Acadêmicas (POSCOMP, ENADE, Concursos Públicos):**
  * Cálculo direto sob restrições de tempo.
  * Questões teóricas sobre a assimetria da distribuição baseada na relação entre Média, Mediana e Moda:
    * **Simétrica:** $\bar{x} = Md = Mo$
    * **Assimétrica Positiva (à direita):** $\bar{x} > Md > Mo$ (cauda longa à direita, atração por outliers altos).
    * **Assimétrica Negativa (à esquerda):** $\bar{x} < Md < Mo$ (cauda longa à esquerda, atração por outliers baixos).
* **Entrevistas Técnicas (Data Science, Backend, SRE):**
  * *"Por que não devemos usar a média para definir SLAs/SLOs de latência de um microserviço?"* (Resposta esperada: P95, P99 e Mediana são robustos a picos; a média oculta falhas isoladas mas graves).
  * Questões de código: "Implemente uma função para calcular a mediana de um *stream* de dados sem carregar tudo em memória" (uso de Heaps).

---

## 💻 2. Implementacao Pratica Completa

### 2.1 Fórmulas Matemáticas Passo a Passo

Dado o conjunto $X = \{x_1, x_2, \dots, x_n\}$:

#### 1. Média Aritmética ($\bar{x}$)
$$\bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i$$

#### 2. Mediana ($Md$)
Primeiro, ordena-se o conjunto $X$ gerando o conjunto ordenado $X_{( order )} = \{x_{(1)}, x_{(2)}, \dots, x_{(n)}\}$, onde $x_{(1)} \le x_{(2)} \le \dots \le x_{(n)}$.

$$Md = \begin{cases} 
x_{\left(\frac{n+1}{2}\right)}, & \text{se } n \text{ for ímpar} \\
\frac{x_{\left(\frac{n}{2}\right)} + x_{\left(\frac{n}{2} + 1\right)}}{2}, & \text{se } n \text{ for par} 
\end{cases}$$

#### 3. Moda ($Mo$)
$$Mo = \text{arg max}_{v} \left( \sum_{i=1}^{n} \mathbb{I}(x_i = v) \right)$$
Onde $\mathbb{I}$ é a função indicadora que vale 1 se $x_i = v$ e 0 caso contrário. Se nenhum valor se repetir, o conjunto é **Amodal**. Se houver múltiplos valores com a mesma frequência máxima, o conjunto é **Bimodal**, **Trimodal** ou **Multimodal**.

---

### 2.2 Script Executável em Python

O código abaixo simula um ambiente de telemetria de um microserviço, calculando as métricas estatísticas "na mão" (para entender a lógica algorítmica) e via bibliotecas otimizadas (`numpy`, `scipy`).

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Disciplina: Estatistica Computacional - BSI 3º Periodo
AULA: Medidas de Posicao e Sensibilidade a Outliers
"""

import numpy as np
from scipy import stats
import math

def calcular_media_manual(dados):
    """Soma todos os elementos e divide pelo total. Complexiade: O(n)"""
    if len(dados) == 0:
        return 0.0
    soma = 0.0
    for elemento in dados:
        soma += elemento
    return soma / len(dados)

def calcular_mediana_manual(dados):
    """
    Ordena o array e encontra o elemento central.
    Complexidade de Tempo: O(n log n) devido ao algoritmo de ordenacao.
    Complexidade de Espaco: O(n) para a copia ordenada.
    """
    if len(dados) == 0:
        return 0.0
    
    dados_ordenados = sorted(dados)  # Requisito OBRIGATORIO
    n = len(dados_ordenados)
    meio = n // 2
    
    if n % 2 != 0:
        # Impar: Elemento central exato
        return float(dados_ordenados[meio])
    else:
        # Par: Media dos dois elementos centrais
        return (dados_ordenados[meio - 1] + dados_ordenados[meio]) / 2.0

def calcular_moda_manual(dados):
    """
    Mapeia frequencias utilizando uma Tabela Hash (dict).
    Complexidade de Tempo: O(n)
    Complexidade de Espaco: O(n)
    """
    if len(dados) == 0:
        return []
    
    frequencias = {}
    for elem in dados:
        frequencias[elem] = frequencias.get(elem, 0) + 1
        
    max_frequencia = max(frequencias.values())
    
    # Se todos aparecem apenas 1 vez, e amodal
    if max_frequencia == 1 and len(dados) > 1:
        return [] # Amodal
        
    modas = [chave for chave, freq in frequencias.items() if freq == max_frequencia]
    return modas

# --- DEMONSTRACAO E COMPARACAO ---
if __name__ == "__main__":
    print("=" * 70)
    print(" SIMULACAO DE TELEMETRIA: LATENCIA DE SERVIDORES (em ms)")
    print("=" * 70)

    # Dados Normais de Requisicoes HTTP (ms)
    latencias_normais = [45, 50, 52, 48, 45, 51, 49, 45, 53, 50]
    
    # Simulando um Outlier Extremo (ex: Timeout de BD / Garbage Collection)
    latencias_com_outlier = latencias_normais + [3500]

    print(f"Dados Sem Outlier (n={len(latencias_normais)}): {latencias_normais}")
    print(f"Dados Com Outlier (n={len(latencias_com_outlier)}): {latencias_com_outlier}\n")

    # 1. Analise sem Outlier (Funcoes Manuais vs Numpy/SciPy)
    media_norm = calcular_media_manual(latencias_normais)
    mediana_norm = calcular_mediana_manual(latencias_normais)
    moda_norm = calcular_moda_manual(latencias_normais)

    print("--- 1. CENARIO NOMINAL (SEM OUTLIERS) ---")
    print