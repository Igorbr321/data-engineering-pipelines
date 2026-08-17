import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.style import Style
from tkinter import messagebox
from web_scraping import extraction  # Importando a função de web scraping

def gerar_csv():
    url = entrada.get()
    table_name = entrada_2.get()
    if url and table_name:
        try:
            # Passe o nome da tabela para a função de extração
            arquivo_csv = extraction(url, table_name)
            messagebox.showinfo("Gerar CSV", f"Arquivo CSV '{arquivo_csv}' gerado com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao gerar o CSV: {e}")
    else:
        if not table_name:
            messagebox.showwarning("Gerar CSV", "Por favor, insira o nome da tabela.")
        else:
            messagebox.showwarning("Gerar CSV", "Por favor, insira a URL.")

app = ttk.Window('Data_Extraction')
app.geometry('500x250')
style = Style(theme='cyborg')

# Adicionar título
titulo = ttk.Label(app, text='Extração de Dados - Bombeiros', font=('Arial', 10, 'bold'))
titulo.pack(pady=10)

# Criar um frame para a linha de entrada e botão
linha = ttk.Frame(app)
linha.pack(pady=10, padx=10, fill='x')

# Adicionar label e entrada de texto no frame
ttk.Label(linha, text='URL').pack(side=LEFT, padx=5)
entrada = ttk.Entry(linha)
entrada.pack(side=LEFT, fill='x', expand=True, padx=5)

# Criar uma segunda linha para o nome da tabela e botão
linha_2 = ttk.Frame(app)
linha_2.pack(pady=10, padx=10, fill='x')

ttk.Label(linha_2, text='Table_name').pack(side=LEFT, padx=5)
entrada_2 = ttk.Entry(linha_2)
entrada_2.pack(side=LEFT, fill='x', expand=True, padx=5)

# Adicionar botão no segundo frame
botao = ttk.Button(linha_2, text='Gerar CSV', bootstyle=SUCCESS, command=gerar_csv)
botao.pack(side=RIGHT, padx=5)

app.mainloop()


