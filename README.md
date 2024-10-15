# Trabalho-Faculdade-Python
Este é a primeira parte do trabalho a3 da faculdade, onde o objetivo do nosso grupo é criar uma aplicação flask com mysql-connector para o usuário conseguir criar uma conta e acessa-la pelo navegador.

Para poder rodar este projeto é necessario ter instalado os seguindes requesitos:
    Python, MySQL (Worckbench, Xammp ou outro que possua o mysql).

Outros requisitos:
    Bibliotecas python: pip, Flask, mysql-connector-python


## Manutenção Realizada
- **Tipo de Manutenção**: Correção de segurança
- **Descrição da Manuntenção**: Verificar conexão ao banco de dados antes de realizar operação. Foi criado uma função para testar a conexão para evitar falhas, mudança feita na linha  13 di app.py