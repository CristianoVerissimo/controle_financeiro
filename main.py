#By: Cristiano Verissimo
#Year: 2023
#GitHub: https://github.com/CristianoVerissimo

#pip install auto-py-to-exe --> python3 -m auto_py_to_exe

import tkinter as tk
from tkinter import ttk
import sqlite3
import locale
from tkcalendar import DateEntry

class ControleRecursos:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle de Recursos")

        # Configurar locale para o formato da moeda Real
        locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')

        # Conectar ao banco de dados
        self.conexao = sqlite3.connect("controle_recursos.db")
        self.criar_tabela()

        # Variáveis de controle
        self.descricao_var = tk.StringVar()
        self.tipo_var = tk.StringVar(value="Entrada")
        self.valor_var = tk.DoubleVar()
        self.data_var = tk.StringVar()

        # Interface gráfica
        ttk.Style().theme_use("clam")
        self.criar_interface()

    def criar_tabela(self):
        cursor = self.conexao.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT,
                tipo TEXT,
                valor REAL,
                data TEXT
            )
        ''')
        self.conexao.commit()

    def adicionar_transacao(self):
        descricao = self.descricao_var.get()
        tipo = self.tipo_var.get()
        valor = self.valor_var.get()
        data = self.data_var.get()

        if descricao and tipo and valor and data:
            if tipo == "Saída":
                valor *= -1

            cursor = self.conexao.cursor()
            cursor.execute("INSERT INTO transacoes (descricao, tipo, valor, data) VALUES (?, ?, ?, ?)",
                           (descricao, tipo, valor, data))
            self.conexao.commit()
            self.atualizar_lista_transacoes()
            self.atualizar_total_recursos()
            self.limpar_campos()

    def criar_interface(self):
        # Frames
        frame_entrada = ttk.Frame(self.root, padding="10")
        frame_entrada.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        frame_lista = ttk.Frame(self.root, padding="10")
        frame_lista.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Labels e Entradas
        ttk.Label(frame_entrada, text="Descrição:").grid(row=0, column=0, sticky=tk.W)
        entrada_descricao = ttk.Entry(frame_entrada, textvariable=self.descricao_var)
        entrada_descricao.grid(row=0, column=1, sticky=(tk.W, tk.E))

        ttk.Label(frame_entrada, text="Tipo:").grid(row=1, column=0, sticky=tk.W)
        combo_tipo = ttk.Combobox(frame_entrada, textvariable=self.tipo_var, values=["Entrada", "Saída"])
        combo_tipo.grid(row=1, column=1, sticky=(tk.W, tk.E))

        ttk.Label(frame_entrada, text="Valor (R$):").grid(row=2, column=0, sticky=tk.W)
        entrada_valor = ttk.Entry(frame_entrada, textvariable=self.valor_var)
        entrada_valor.grid(row=2, column=1, sticky=(tk.W, tk.E))

        ttk.Label(frame_entrada, text="Data:").grid(row=3, column=0, sticky=tk.W)
        self.calendario = DateEntry(frame_entrada, textvariable=self.data_var, date_pattern="dd/MM/yyyy", locale="pt_BR")
        self.calendario.grid(row=3, column=1, sticky=(tk.W, tk.E))

        # Botão de Adicionar
        btn_adicionar = ttk.Button(frame_entrada, text="Adicionar", command=self.adicionar_transacao)
        btn_adicionar.grid(row=4, column=1, sticky=tk.W)

        # Lista de Transações
        self.lista_transacoes = ttk.Treeview(frame_lista, columns=("Descrição", "Tipo", "Valor", "Data"), show="headings")
        self.lista_transacoes.heading("Descrição", text="Descrição")
        self.lista_transacoes.heading("Tipo", text="Tipo")
        self.lista_transacoes.heading("Valor", text="Valor")
        self.lista_transacoes.heading("Data", text="Data")
        self.lista_transacoes.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Adicionar tags para colorir os valores
        self.lista_transacoes.tag_configure("entrada", foreground="green")
        self.lista_transacoes.tag_configure("saida", foreground="red")

        # Atualizar a lista de transações
        self.atualizar_lista_transacoes()

        # Label para exibir o total de recursos
        ttk.Label(frame_lista, text="Total de Recursos:").grid(row=1, column=0, sticky=tk.W)
        self.label_total_recursos = ttk.Label(frame_lista, text="")
        self.label_total_recursos.grid(row=1, column=1, sticky=tk.W)

        # Atualizar o total de recursos
        self.atualizar_total_recursos()

    def atualizar_lista_transacoes(self):
        # Limpar a lista atual
        for item in self.lista_transacoes.get_children():
            self.lista_transacoes.delete(item)

        # Preencher a lista com os dados do banco de dados
        cursor = self.conexao.cursor()
        cursor.execute("SELECT descricao, tipo, valor, data FROM transacoes")
        transacoes = cursor.fetchall()

        for transacao in transacoes:
            # Formatar o valor como moeda Real
            valor_formatado = locale.currency(transacao[2], grouping=True)
            transacao_formatada = (transacao[0], transacao[1], valor_formatado, transacao[3])

            # Adicionar a tag correspondente
            if transacao[1] == "Entrada":
                self.lista_transacoes.insert("", "end", values=transacao_formatada, tags=("entrada",))
            else:
                self.lista_transacoes.insert("", "end", values=transacao_formatada, tags=("saida",))

    def atualizar_total_recursos(self):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT SUM(valor) FROM transacoes")
        total_recursos = cursor.fetchone()[0] or 0
        self.label_total_recursos.config(text=locale.currency(total_recursos, grouping=True))

    def limpar_campos(self):
        self.descricao_var.set("")
        self.tipo_var.set("Entrada")
        self.valor_var.set("")
        self.data_var.set("")


if __name__ == "__main__":
    root = tk.Tk()
    app = ControleRecursos(root)
    root.mainloop()
