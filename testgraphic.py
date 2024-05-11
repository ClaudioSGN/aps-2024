import matplotlib.pyplot as plt  # Importa a biblioteca matplotlib.pyplot para a criação de gráficos
import json  # Importa o módulo json para trabalhar com dados JSON

# Bloco que carrega o arquivo JSON contendo os resultados
with open('results.json', 'r') as file:  # Abre o arquivo 'results.json' para leitura
    results = json.load(file)  # Carrega os dados JSON do arquivo

# Processa os dados carregados para criar o gráfico
labels = list(results.keys())  # Extrai as chaves do dicionário JSON para usar como rótulos no gráfico
sizes = [float(result[:-1]) for result in results.values()]  # Remove o símbolo de porcentagem dos valores e converte para float

# Cria e configura o gráfico de pizza
fig1, ax1 = plt.subplots()  # Cria uma figura e um conjunto de subplots (neste caso, apenas um)
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)  # Desenha um gráfico de pizza com os dados
ax1.axis('equal')  # Garante que o gráfico de pizza seja desenhado como um círculo (mantendo a proporção igual)

plt.show()  # Exibe o gráfico


#Este código nada mais faz do que puxar os dados resultantes do arquivo 'ai_analyzer.py" e transformá-los em um
#gráfico que apresenta em formato de pizza a porcentagem de notícias boas e notícias ruins.