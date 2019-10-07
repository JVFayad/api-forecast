# api-forecast

<h1>API de Previsão do Tempo e Análise</h1>

Esta API foi desenvolvida utilizando basicamente:
```
    - Python 3.7.4
    - Flask 1.1.1
    - SQLite
    - Dockerfile
```

Comandos importantes para inicialização (utilizando docker-compose):

- Inicia a API 
```
docker-compose up
```

A API tem um funcionamento simples, com dois endpoints, um para buscar e atualizar os dados de previsão do tempo no banco,e o outro para fazer uma análise destes dados já cadastrados, através dos dados de temperatura máxima e média de precipitação de chuva (por cidade).

Algumas observações:

- Nunca havia desenvolvido um projeto usando Flask, então tentei buscar a melhor estrutura para uma API simples, baseado na minha experiência e no conteúdo que encontrei sobre o framework;

- Utilizei o Pipfile para genrenciamento de dependências do projeto;

- Espero ter entendido corretamente a idéia e regras de negócio do teste. Caso tenham alguma dúvida sobre como executar o projeto ou qualquer outra coisa, podem entrar em contato comigo;

<h1>Endpoints:</h1>

<h2>Previsão do Tempo</h2>

- <h3>Cadastrar/Atualizar Dados</h3>
__GET__ /cidade?id=<ID_CIDADE>

- <h3>Retornar Análise dos Dados</h3>
__GET__ /analise?data_inicial=<DATA_INICIAL>&data_final=<DATA_FINAL>
