📊 Dashboard Financeiro - Análise de Dívidas

Este projeto consiste na construção de um dashboard interativo para análise de dívidas, utilizando Python e bibliotecas voltadas para manipulação e visualização de dados.

🚀 Tecnologias utilizadas
Python
Pandas
Plotly
Streamlit
OpenPyXL
📁 Estrutura dos dados

A base de dados (Excel) contém as seguintes colunas:

Devedores
Telefone (WhatsApp)
Data
Valor Dívida
Juros (%)
Correção
Valor Total da Dívida Corrigido
📊 Funcionalidades do dashboard
KPIs principais:
Total da dívida
Total de juros (calculado corretamente em R$)
Quantidade de devedores
Ticket médio
Filtros interativos:
Por devedor
Por período (data)
Visualizações:
📈 Evolução da dívida ao longo do tempo
🏆 Ranking de devedores
🧩 Composição da dívida (principal, juros e correção)
Insights automáticos:
Maior devedor e participação percentual
Crescimento da dívida no período
🧠 Regra importante aplicada

Os juros são armazenados como percentual (ex: 1%), e não como valor monetário.

Por isso, o cálculo correto é:

juros = Valor_Divida * (Juros / 100)
▶️ Como executar o projeto
Instale as dependências:
pip install pandas plotly streamlit openpyxl
Execute o dashboard:
streamlit run nome_do_arquivo.py
📌 Objetivo do projeto

Praticar análise de dados na prática, trabalhando desde o tratamento da base até a construção de dashboards interativos com foco em tomada de decisão.

🚀 Próximos passos
Integração com banco de dados
Automatização de cobranças
Deploy do dashboard online
Implementação de autenticação de usuários