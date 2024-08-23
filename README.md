# Documentação

## Introdução

O código implementa uma aplicação de Controle de Recursos utilizando a biblioteca Tkinter para a interface gráfica, SQLite para o banco de dados e tkcalendar para a entrada de datas. A aplicação permite o registro de transações financeiras, distinguindo entre entradas e saídas de recursos, exibindo um resumo na forma de uma tabela e o total de recursos.

## Requisitos

- Python 3.x
- Tkinter
- SQLite3
- Tkcalendar

Instale as bibliotecas necessárias com o seguinte comando:

```bash
pip install tk tkcalendar matplotlib
sudo apt get install tkinter -y
```

## Funcionalidades

1. **Cadastro de Transações:**
   - Descrição: O usuário pode inserir uma descrição para a transação.
   - Tipo: O usuário pode selecionar entre "Entrada" e "Saída" para indicar o tipo da transação.
   - Valor: Valor da transação em moeda Real (R$).
   - Data: Data da transação no formato DD/MM/AAAA.

2. **Registro no Banco de Dados:**
   - As transações são armazenadas em um banco de dados SQLite. A tabela `transacoes` contém os campos `id`, `descricao`, `tipo`, `valor` e `data`.

3. **Exibição de Transações na Tabela:**
   - As transações são exibidas em uma tabela Tkinter, apresentando as colunas: Descrição, Tipo, Valor e Data.
   - As entradas são exibidas em verde e as saídas em vermelho.

4. **Atualização do Total de Recursos:**
   - A aplicação calcula e exibe o total de recursos com base nas transações registradas.

5. **Tema "Clam" do Tkinter:**
   - O tema "Clam" é aplicado aos elementos gráficos da interface Tkinter para melhorar a aparência.

## Utilização

1. **Execução:**
   - Execute o script Python (`controle_recursos.py`).
   - A interface gráfica será exibida.

2. **Cadastro de Transações:**
   - Preencha os campos de descrição, tipo, valor e data.
   - Clique no botão "Adicionar" para registrar a transação.

3. **Visualização de Transações:**
   - As transações serão exibidas na tabela, com as entradas em verde e as saídas em vermelho.

4. **Total de Recursos:**
   - O total de recursos é atualizado automaticamente na interface.

5. **Limpeza de Campos:**
   - Clique no botão "Adicionar" para registrar a transação.
   - Os campos serão limpos para facilitar a entrada de uma nova transação.
