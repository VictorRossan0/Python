import pandas as pd
import matplotlib.pyplot as plt

# Carregar dados de um arquivo CSV
data = pd.read_csv('dados.csv')

# Verificar as primeiras linhas do conjunto de dados
print(data.head())

# Realizar algumas operações de manipulação de dados
filtered_data = data[data['idade'] > 30]
sorted_data = filtered_data.sort_values('salario', ascending=False)
grouped_data = sorted_data.groupby('departamento')['salario'].mean()

# Visualizar os dados
plt.bar(grouped_data.index, grouped_data.values)
plt.xlabel('Departamento')
plt.ylabel('Salário Médio')
plt.title('Salário Médio por Departamento')
plt.show()