# 📚 Lição do Dia: Regressão Linear Simples: Coeficiente de Determinação (R²) e Resíduos

## 🎯 1. Conceito Central

Os **Resíduos** ($e_i = y_i - \hat{y}_i$) representam o erro do nosso modelo: a diferença entre o valor real observado ($y_i$) e o valor previsto pela reta ($\hat{y}_i$). Em um bom modelo estatístico, os resíduos devem se comportar como ruído branco — ter média zero, variação constante (homoscedasticidade) e distribuição aleatória, sem padrões visíveis.

O **Coeficiente de Determinação ($R^2$)** mede a proporção da variância total da variável resposta ($Y$) que é explicada pela variável preditora ($X$). Variando entre 0 e 1 (ou 0% a 100%), o $R^2$ é calculado como $R^2 = 1 - \frac{SQ_{res}}{SQ_{tot}}$, onde $SQ_{res}$ é a soma dos quadrados dos resíduos e $SQ_{tot}$ é a soma dos quadrados totais. Em suma: quanto mais próximo de 1, maior é o poder explicativo da reta.

## 💻 2. Código Exemplo

Abaixo, um script enxuto em Python utilizando `numpy` e `scipy` para