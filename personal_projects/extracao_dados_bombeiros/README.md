### Projeto de Coleta e Registro de Dados sobre Manutenções do Corpo de Bombeiros 🚒


Este projeto é uma aplicação de ETL (Extract, Transform, Load) que utiliza Web Scraping com a biblioteca Requests para a extração de dados sobre manutenções realizadas por Bombeiros. Na etapa de transformação (Transform), é aplicado Data Wrangling para estruturar e tratar os dados extraídos. Por fim, na etapa de carregamento (Load), os dados tratados são armazenados em um arquivo CSV. O projeto também conta com uma interface gráfica desenvolvida com a biblioteca ttkbootstrap, permitindo ao usuário inserir a URL do site e o nome da tabela.


🔍 Visão Geral do Projeto <br>
O projeto é estruturado em três componentes principais, detalhados abaixo:

🖥️ Interface Gráfica <br>
Uma interface intuitiva, desenvolvida com ttkbootstrap, que permite ao usuário:

- Inserir a URL do site de manutenções.
- Informar o nome da tabela a ser processada.
- Iniciar o processo de extração de dados com apenas um clique.
  
⚙️ Módulo de Extração e Processamento de Dados

- Utiliza Web Scraping com a biblioteca Requests para acessar e extrair os dados.
- Aplica técnicas de Data Wrangling na etapa de transformação, garantindo que os dados estejam limpos e organizados.
- Armazena os dados tratados em um arquivo CSV pronto para análise ou integração com outros sistemas.

📦 Script de Empacotamento <br>
Utiliza cx_Freeze para gerar um executável da aplicação, facilitando a distribuição sem a necessidade de instalar dependências manualmente:

- Dependências:
  Define os pacotes necessários, como os, ttkbootstrap, tkinter, requests, bs4 e csv, no parâmetro build_exe_options.
- Base para Aplicação GUI:
  Configura a base Win32GUI para garantir que a aplicação gráfica não exiba o console durante a execução no Windows.
- Empacotamento do Executável:
  Define interface_grafica.py como ponto de entrada, gerando o executável ProjetoBombeiros.exe.
- Portabilidade:
  Gera um executável autossuficiente, permitindo a execução em diferentes sistemas sem a necessidade de instalar o Python ou bibliotecas adicionais.
