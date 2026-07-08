from tkinter import colorchooser
from View.view import *
from Model.model import *
from tkinter import filedialog
from .state import LinhaState, RetanguloState, OvalState, CirculoState, RabiscoState, PoligonoState

class Controller:
    def __init__(self, root):
        self.model = Model()
        self.view = View(root, self)

        self.tipo_figura_var = self.view.tipo_figura_var
        self.cor_fill = self.view.cor_fill_var
        self.cor_out = self.view.cor_out_var

        self.estado_atual = RabiscoState(self)
        self.tipo_figura_var.trace_add("write", self.mudar_estado)

        root.bind("<Up>", self.mover_para_frente) 
        root.bind("<Down>",self.mover_para_tras)

    def salvar_arquivo(self):
        caminho_arquivo = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Arquivos de Texto", "*.txt"),
                ("Todos os arquivos", "*.*"),
            ],
            title="Salvar Desenho",
        )
        if caminho_arquivo:
            self.model.salvar_para_txt(caminho_arquivo)

    def abrir_arquivo(self):
        caminho_arquivo = filedialog.askopenfilename(
            filetypes=[
                ("Arquivos de Texto", "*.txt"),
                ("Todos os arquivos", "*.*"),
            ],
            title="Abrir Desenho",
        )
        if caminho_arquivo:
            self.model.carregar_de_txt(caminho_arquivo)
            self.view.canvas.delete("all")
            self.model.redesenhar_tudo(self.view.canvas)

    def mudar_estado(self, *args):
        if self.model.forma_em_andamento:
            self.model.forma_em_andamento = False
            self.model.deletar_provisorio(self.view.canvas)
            self.model.valores_atual = []

        estados = {"Linha": LinhaState(self),
                   "Retangulo": RetanguloState(self),
                   "Oval": OvalState(self),
                   "Circulo": CirculoState(self),
                   "Rabisco": RabiscoState(self),
                   "Poligono": PoligonoState(self),
                   "Selecionar/Mover": SelecaoState(self)}
        
        self.estado_atual = estados[self.tipo_figura_var.get()]


    def escolher_cor_out(self):
        cor = colorchooser.askcolor(title="Escolha a cor da borda")
        if cor[1]:
            self.cor_out.set(cor[1])

    def escolher_cor_in(self):
        cor = colorchooser.askcolor(title="Escolha a cor do preenchimento")
        if cor[1]:
            self.cor_fill.set(cor[1])
            
    def mover_para_frente(self, event=None): # <--- Adicionado event=None aqui
        if self.model.figura_selecionada:
            id_canvas = self.model.figura_selecionada.id_canvas
            self.view.canvas.tag_raise(id_canvas)
           
            self.model.figuras.append(self.model.figura_selecionada)

    def mover_para_tras(self, event=None):
        if self.model.figura_selecionada:
            id_canvas = self.model.figura_selecionada.id_canvas
            self.view.canvas.tag_lower(id_canvas)
            self.model.figuras.remove(self.model.figura_selecionada)
            self.model.figuras.insert(0, self.model.figura_selecionada)

    def definir_transparente(self):
        self.cor_fill.set("")

    def ao_clicar(self, event):
        self.estado_atual.ao_clicar(event)

    def ao_arrastar(self, event):
        self.estado_atual.ao_arrastar(event)

    def ao_soltar(self, event):
        self.estado_atual.ao_soltar(event)

    def ao_mover(self, event):
        self.estado_atual.ao_mover(event)

    def ao_duplo_clique(self, event):
        self.estado_atual.ao_duplo_clique(event)
