# coding: utf-8
import datetime

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine


url = "https://www.bcb.gov.br/controleinflacao/historicotaxasjuros"
ativo = 'SELIC'


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

    return content.find_all("td")


def remove_multiple_spaces(string):
    """
    Se é String, então faz remoção de espaços em branco
    trans_string: remove os valores textuais por espaços em branco
    trans_n: / por espaço em branco AND (,) por (.) para facilitar a conversão de tipos
    """
    if type(string) == str:
        trans_string = string \
                            .replace('baixa', ' ') \
                            .replace('alta', ' ') \
                            .replace(' ex.', '') \
                            .replace('uso', ' ')

        divisao = ' '.join(trans_string.split())
        trans_n = divisao.replace('/', ' ').replace(',', '.')
        return trans_n
    return string


def generate_table(table: 'bs4.element.ResultSet'):
    """
    Contrução da tabela
    """
    df_selic = pd.DataFrame(columns=['Ano', 'Taxa SELIC'])

    print('\n')
    print(table)

    for row in table:
        text = row.text
        text = remove_multiple_spaces(text)

        # insere dados diferentes a cada linha
        text_dados = text.split(sep=" ")

        # convert list to String
        # quando é feito o slice do text_dados é retornado um list
        ano = np.asarray(text_dados[6:7])
        taxa = np.asarray(text_dados[13:])

        # DataFrame p organizar a inserção no dataframe
        dados = pd.DataFrame([[ano, taxa]], columns=['Ano', 'Taxa SELIC'])
        df_selic = df_selic.append(dados)

    print(df_selic)
    # drop rows with Strings
    df_selic = df_selic[3:]

    # select 10 years
    year = (datetime.date.today().year)
    data_inicial = (f'{year - 10}')
    df_selic = df_selic[df_selic.Ano >= data_inicial]

    # Conversão de tipos object
    df_selic.Ano = df_selic.Ano.astype('int16')
    df_selic['Taxa SELIC'] = df_selic['Taxa SELIC'].astype('float16')

    """ Granularidade anual: 
    - tanto a taxa selic quanto a PETR4 devem ser de mesma granularidade
    - nível do grão = ano
    """
    # dataframe somente com as taxas de fechamento de cada ano
    df_selic_clean = pd.DataFrame(columns=['Ano', 'Taxa SELIC'])

    # for serve para get fechamento do ano
    for ano in range(year - 9, year + 1):
        # print(ano)
        df_selic_year = df_selic[(df_selic['Ano'] == ano)]

        # get value
        taxa_ano = df_selic_year['Taxa SELIC'].iloc[0]
        # print(taxa_ano)

        # variável p organizar a inserção no dataframe
        dados = pd.DataFrame([[ano, taxa_ano]],
                             columns=['Ano', 'Taxa SELIC'])
        df_selic_clean = df_selic_clean.append(dados)

    return df_selic_year


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
