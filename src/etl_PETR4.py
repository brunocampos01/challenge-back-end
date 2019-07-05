# coding: utf-8
import datetime

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine

# Global
year = datetime.date.today().year
month = datetime.date.today().month
day = datetime.date.today().day
data_inicial = (f'{day}/{month}/{year - 10}')
data_final = (f'{day}/{month}/{year}')
ativo = 'PETR4'
url = (f"https://www.infomoney.com.br/Pages/Download/Download.aspx?"
       f"dtIni={data_inicial}&dtFinish={data_final}"
       f"&Ativo={ativo}"
       f"&Semana=null"
       f"&Per=null"
       f"&type=2"
       f"&Stock={ativo}"
       f"&StockType=1")


def prepare_url(url: str):
    """
    Construção da URL
    :return: http response
    """
    response = requests.get(url, timeout=60)

    print("get page: ", response)
    return response


def create_parser(response: str):
    """
    Criação do parser para navegação na árvore DOM
    :return: bs4.element
    """
    content = BeautifulSoup(response.content, "html.parser")
    return content.find_all("tr")


def remove_multiple_spaces(string):
    """
    Se é String, então faz remoção de espaços em branco
    replace: / por espaço em branco
    replace: , por . para facilitar a conversão de tipos
    replace: todas as palavras que entraram na tabela
    """
    if type(string) == str:
        string_n = ' '.join(string.split()) \
            .replace('/', ' ') \
            .replace(',', '.')

        string = string_n \
            .replace('Fech.', '-1') \
            .replace('Var.Dia',
                     '-1')
        return string

    return string


def generate_table(table: 'bs4.element.ResultSet'):
    # neste dataframe vou armazenar a data e o fechamento diário
    df_petr4 = pd.DataFrame(columns=['Ano', 'Fechamento'])

    # percorre tabela
    for row in table:
        # .text vem do requests e garante o scrapping
        text = row.text
        text = remove_multiple_spaces(text)

        # insere dados diferentes a cada linha
        text_dados = text.split(sep=" ")

        # quando é feito o slice do text_dados é retornado um list
        ano = np.asarray(text_dados[2:3])
        fechamento = np.asarray(text_dados[3:4])

        # variável p organizar a inserção no dataframe
        dados = pd.DataFrame([[ano, fechamento]],
                             columns=['Ano', 'Fechamento'])
        df_petr4 = df_petr4.append(dados)

    # remove linhas com Strings
    df_petr4 = df_petr4[1:]

    # Conversão de tipos object
    df_petr4.Ano = df_petr4.Ano.astype(
        'int16')  # int8 não aceitou, pequeno demais
    df_petr4.Fechamento = df_petr4.Fechamento.astype('float16')

    """ Granularidade anual: 
    - tanto a taxa selic quanto a PETR4 devem ser de mesma granularidade
    - nível do grão = ano
    """
    # dataframe somente com os fechamentos do ano
    df_petr4_clean = pd.DataFrame(columns=['Ano', 'Fechamento'])

    # for serve para get fechamento do ano
    for ano in range(year - 9, year + 1):
        df_petr4_year = df_petr4[(df_petr4['Ano'] == ano)]
        fechamento_ano = df_petr4_year.Fechamento.iloc[0]

        # variável p organizar a inserção no dataframe
        dados = pd.DataFrame([[ano, fechamento_ano]],
                             columns=['Ano', 'Fechamento'])
        df_petr4_clean = df_petr4_clean.append(dados)

    print(df_petr4_clean.info())
    return df_petr4_clean


def dataframe_to_sqlite(ativo: str, dataframe: 'dataframe'):
    engine = create_engine('sqlite:///data/desafio_AAWZ.db')
    dataframe.to_sql(ativo, con=engine,
              if_exists='replace',
              index=False)
    print(f'\n{ativo} salvo!')


def main():
    response = prepare_url(url=url)
    parser_bs = create_parser(response)
    df = generate_table(parser_bs)
    dataframe_to_sqlite(ativo=ativo, dataframe=df)


if __name__ == '__main__':
    main()
