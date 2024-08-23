# By: Cristiano Verissimo
# Year: 2023
# GitHub: https://github.com/CristianoVerissimo

# pip install auto-py-to-exe --> python3 -m auto_py_to_exe

import tkinter as tk
from tkinter import ttk
import sqlite3
import locale
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
        self.tipo_var = tk.StringVar(value="Demais Despesas")
        self.valor_var = tk.DoubleVar()
        self.data_var = tk.StringVar(value=datetime.now().strftime("%d/%m/%Y"))

        # Interface gráfica
        ttk.Style().theme_use("clam")
        self.criar_interface()

    def criar_tabela(self):
        cursor = self.conexao.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT,
                valor REAL,
                data TEXT
            )
        ''')
        self.conexao.commit()

    def adicionar_transacao(self):
        tipo = self.tipo_var.get()
        valor = self.valor_var.get()
        data = self.data_var.get()

        if tipo and valor:
            if tipo == "Saída":
                valor *= -1

            cursor = self.conexao.cursor()
            cursor.execute("INSERT INTO transacoes (tipo, valor, data) VALUES (?, ?, ?)",
                           (tipo, valor, data))
            self.conexao.commit()
            self.atualizar_lista_transacoes()
            self.atualizar_total_recursos()
            self.limpar_campos()
            self.atualizar_grafico()

    def excluir_transacao(self):
        item_selecionado = self.lista_transacoes.selection()
        if item_selecionado:
            transacao_id = self.lista_transacoes.item(item_selecionado)["values"][0]

            cursor = self.conexao.cursor()
            cursor.execute("DELETE FROM transacoes WHERE id = ?", (transacao_id,))
            self.conexao.commit()

            self.atualizar_lista_transacoes()
            self.atualizar_total_recursos()
            self.atualizar_grafico()

    def criar_interface(self):
        # Frames
        frame_entrada = ttk.Frame(self.root, padding="10")
        frame_entrada.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        frame_lista = ttk.Frame(self.root, padding="10")
        frame_lista.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Labels e Entradas
        ttk.Label(frame_entrada, text="Tipo:").grid(row=0, column=0, sticky=tk.W)
        combo_tipo = ttk.Combobox(frame_entrada, textvariable=self.tipo_var, values=["Pensão", "Contas Mensais", "Cartão Ju", "Maquina Lavar", "Demais Despesas", "Poupança"])
        combo_tipo.grid(row=0, column=1, sticky=(tk.W, tk.E))

        ttk.Label(frame_entrada, text="Valor (R$):").grid(row=1, column=0, sticky=tk.W)
        entrada_valor = ttk.Entry(frame_entrada, textvariable=self.valor_var)
        entrada_valor.grid(row=1, column=1, sticky=(tk.W, tk.E))

        # Botão de Adicionar
        btn_adicionar = ttk.Button(frame_entrada, text="Adicionar", command=self.adicionar_transacao)
        btn_adicionar.grid(row=2, column=1, sticky=tk.W)

        # Botão de Pago
        btn_pago = ttk.Button(frame_entrada, text="Pago", command=self.excluir_transacao)
        btn_pago.grid(row=2, column=2, sticky=tk.W)

        # Lista de Transações
        self.lista_transacoes = ttk.Treeview(frame_lista, columns=("ID", "Tipo", "Valor", "Data"), show="headings")
        self.lista_transacoes.heading("ID", text="ID")
        self.lista_transacoes.heading("Tipo", text="Tipo")
        self.lista_transacoes.heading("Valor", text="Valor")
        self.lista_transacoes.heading("Data", text="Data")
        self.lista_transacoes.column("ID", width=30)  # Ajustar largura da coluna ID
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

        # Frame para o gráfico
        frame_grafico = ttk.Frame(self.root, padding="10")
        frame_grafico.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.figura = Figure(figsize=(5, 3), dpi=75)
        self.ax = self.figura.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figura, master=frame_grafico)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.atualizar_grafico()

    def atualizar_lista_transacoes(self):
        # Limpar a lista atual
        for item in self.lista_transacoes.get_children():
            self.lista_transacoes.delete(item)

        # Preencher a lista com os dados do banco de dados
        cursor = self.conexao.cursor()
        cursor.execute("SELECT id, tipo, valor, data FROM transacoes")
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
        self.tipo_var.set("Demais Despesas")
        self.valor_var.set("")

    def atualizar_grafico(self):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT tipo, SUM(valor) FROM transacoes GROUP BY tipo")
        dados = cursor.fetchall()

        tipos = [dado[0] for dado in dados]
        valores = [abs(dado[1]) for dado in dados]  # Utilizar valor absoluto para evitar valores negativos

        self.ax.clear()
        self.ax.pie(valores, labels=tipos, autopct='%1.1f%%', startangle=140)
        self.ax.set_title("Distribuição das Despesas")
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = ControleRecursos(root)
    root.mainloop()
