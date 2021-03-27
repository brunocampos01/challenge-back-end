# Challenge Developer Back-end
Desenvolver uma análise quantitativa e gráfica relacionando o aumento das ações da
Petrobrás (PETR4) com as variações da taxa SELIC para os últimos 10 anos.

### Goals
Fazer um programa em python para:
- Extrair as informações dos sites e e tratá-las: 
  - https://www.infomoney.com.br/petrobras-petr4/cotacoes
  - https://www.bcb.gov.br/pec/copom/port/taxaselic.asp
- Armazenar as informações tratadas no SQLite;
  - Utilizar, de preferência, ORM (object relational mapping)
- Ler as informações do banco e apresentar em formato gráfico.

### Restrictions
- Utilizar a biblioteca pandas do Python

## Quickstart
Para visualizar os códigos e análises, abra o arquivo [desafio_back-end.ipynb](notebooks/)

## Pre Requirements
- Python 3.7 ou superior
```
sudo apt-get install python3.7
```

- Git
```bash
sudo apt-get install git
```

- pip
```bash
sudo apt-get install python-pip
```

- Python Virtual Environment
```sh
pip3 install --user virtualenv==16.6.0
```

## Running
1. Abra o terminal e clone o repositório

```bash
git clone https://github.com/brunocampos01/challenge-back-end
cd challenge-back-end
```
2. Escolha em qual ambiente quer executa
 - [local](src/environment/README.md)
 - [virtual environment](src/environment/README.md)
 - [container](src/environment/README.md)

2. Execute Notebook

```bash
jupyter-notebook notebooks/challenge_back-end.ipynb
```
---

<p  align="left">
<br/>
<a href="mailto:brunocampos01@gmail.com" target="_blank"><img src="https://github.com/brunocampos01/devops/blob/master/images/email.png" alt="Gmail" width="30">
</a>
<a href="https://stackoverflow.com/users/8329698/bruno-campos" target="_blank"><img src="https://github.com/brunocampos01/devops/blob/master/images/stackoverflow.png" alt="GitHub" width="30">
</a>
<a href="https://www.linkedin.com/in/brunocampos01" target="_blank"><img src="https://github.com/brunocampos01/devops/blob/master/images/linkedin.png" alt="LinkedIn" width="30"></a>
<a href="https://github.com/brunocampos01" target="_blank"><img src="https://github.com/brunocampos01/devops/blob/master/images/github.png" alt="GitHub" width="30"></a>
<a href="https://brunocampos01.netlify.app/" target="_blank"><img src="https://github.com/brunocampos01/devops/blob/master/images/blog.png" alt="Website" width="30">
</a>
<a href="https://medium.com/@brunocampos01" target="_blank"><img src="https://github.com/brunocampos01/devops/blob/master/images/medium.png" alt="GitHub" width="30">
</a>
<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png",  align="right" /></a><br/>
</p>
