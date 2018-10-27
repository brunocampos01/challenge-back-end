import numpy as np
import pandas as pd
import sqlite3
import IPython.terminal
import matplotlib.pyplot as plt
get_ipython().system(' python3 etl_PETR4.py')
get_ipython().system(' python3 etl_SELIC.py')

# ### Load

# Create connection
conn = sqlite3.connect('desafio_AAWZ.db')

#load data
df_selic = pd.read_sql_query("SELECT * FROM selic", conn)
df_petr4 = pd.read_sql_query("SELECT * FROM petr4", conn)

print(df_selic)
print(df_petr4)


# ### Gráficos
# #### Gráfico SELIC

# visualização do gráfico SELIC\n",
x_selic = df_selic['Ano']
y_selic = df_selic['Taxa SELIC']

fig, selic_grafico = plt.subplots()
plt.plot(x_selic, y_selic, color='green', label='Taxa SELIC')
plt.grid()
plt.xlabel('Tempo')
plt.ylabel('Taxa')
plt.title("Variação da taxa SELIC")
plt.legend(loc="upper right")
plt.legend()
plt.show()


# #### Gráfico PETR4

# visualização do gráfico PETR4\n",
x_petr4 = df_petr4['Ano']
y_petr4 = df_petr4['Fechamento']

fig, petr4_grafico = plt.subplots()
plt.plot(x_petr4, y_petr4, color='blue', label='PETR4')
plt.grid()
plt.xlabel('Tempo')
plt.ylabel('Valor')
plt.title("Variação do preço das ações PETR4")
plt.legend(loc="upper right")
plt.legend()
plt.show()

# #### Plotagem no mesmo gráfico
tr4_grafico = plt.plot(x_petr4, y_petr4, color='blue', label='PETR4')
selic_grafico = plt.plot(x_selic, y_selic, color='green', label='Taxa SELIC')

plt.plot(x_petr4, y_petr4, color='blue', label='PETR4')
plt.plot(x_selic, y_selic, color='green', label='Taxa SELIC')

plt.grid()
plt.xlabel('Tempo')
plt.ylabel('Valor')
plt.title("PETR4 e SELIC nos últimos 10 anos")
plt.legend(loc="upper right")
plt.legend()
plt.show()


# ## Predição do fechamento do preço PETR4 a partir da taxa SELIC
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

X = df_selic[['Taxa SELIC']]

# escolhendo a variável dependente\n",
y = df_petr4[['Fechamento']]

# Split the data
X_train, X_test, y_train, y_test = train_test_split(
                                    X,
                                    y,
                                    test_size=0.25)

model = LinearRegression()
model = model.fit(X_train, y_train)
y_pred_model = model.predict(X_test)

# prediction valor aleatório\n",
meta_selic = 10
predicao_petr4 = model.predict(meta_selic)

print(f'A predição do fechamento anual para PETR4, (se meta SELIC = {meta_selic}) baseado numa regressão linear é: R${predicao_petr4} reais.')

