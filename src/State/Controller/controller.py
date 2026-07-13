from tkinter import colorchooser
from View.view import *
from Model.model import *
from tkinter import filedialog
from .state import LinhaState, RetanguloState, OvalState, CirculoState, RabiscoState, PoligonoState, SelecaoState


class Controller:
    def __init__(self, root):
        self.model = Model()
        self.view = View(root, self)

        self.tipo_figura_var = self.view.tipo_figura_var
        self.cor_fill = self.view.cor_fill_var
        self.cor_out = self.view.cor_out_var

        self.estado_atual = RabiscoState(self)
        self.tipo_figura_var.trace_add("write", self.mudar_estado)

        self.cor_fill.trace_add("write", self.ao_mudar_cor_fill)
        self.cor_out.trace_add("write", self.ao_mudar_cor_out)

        root.bind("<Right>", self.mover_posicao_frente)
        root.bind("<Left>", self.mover_posicao_tras)
        root.bind("<Up>", self.mover_topo)
        root.bind("<Down>", self.mover_fundo)

        root.bind("<Delete>", self.deletar_figura)
        root.bind("<BackSpace>", self.deletar_figura)

        root.bind("<Control-c>", self.copiar_figura)
        root.bind("<Control-v>", self.colar_figura)

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

        if self.model.figura_selecionada:
            self.view.canvas.itemconfig(self.model.figura_selecionada.id_canvas, width=1)
            self.model.figura_selecionada = None

        estados = {"Linha": LinhaState(self),
                   "Retangulo": RetanguloState(self),
                   "Oval": OvalState(self),
                   "Circulo": CirculoState(self),
                   "Rabisco": RabiscoState(self),
                   "Poligono": PoligonoState(self),
                   "Selecionar": SelecaoState(self)}

        self.estado_atual = estados[self.tipo_figura_var.get()]

    def deletar_figura(self, event=None):
        if self.model.figura_selecionada:
            id_canvas = self.model.figura_selecionada.id_canvas
            self.view.canvas.delete(id_canvas)
            if self.model.figura_selecionada in self.model.figuras:
                self.model.figuras.remove(self.model.figura_selecionada)
            self.model.figura_selecionada = None

    def escolher_cor_out(self):
        cor = colorchooser.askcolor(title="Escolha a cor da borda")
        if cor[1]:
            self.cor_out.set(cor[1])

    def escolher_cor_in(self):
        cor = colorchooser.askcolor(title="Escolha a cor do preenchimento")
        if cor[1]:
            self.cor_fill.set(cor[1])

     def mover_frente(self, figura, canvas):
        if figura in self.figuras:
            idx = self.figuras.index(figura)
            if idx < len(self.figuras) - 1:
                figura_frente = self.figuras[idx + 1]
                self.figuras[idx], self.figuras[idx + 1] = self.figuras[idx + 1], self.figuras[idx]
                canvas.tag_raise(figura.id_canvas, figura_frente.id_canvas)

    def mover_tras(self, figura, canvas):
        if figura in self.figuras:
            idx = self.figuras.index(figura)
            if idx > 0:
                figura_tras = self.figuras[idx - 1]
                self.figuras[idx], self.figuras[idx - 1] = self.figuras[idx - 1], self.figuras[idx]
                canvas.tag_lower(figura.id_canvas, figura_tras.id_canvas)


    def mover_topo(self, figura, canvas):
        if figura in self.figuras:
            canvas.tag_raise(figura.id_canvas)
            self.figuras.remove(figura)
            self.figuras.append(figura)

    def mover_fundo(self, figura, canvas):
        if figura in self.figuras:
            canvas.tag_lower(figura.id_canvas)
            self.figuras.remove(figura)
            self.figuras.insert(0, figura)

    def copiar_figura(self, event=None):
        if self.model.figura_selecionada:
            self.model.copiar_figura(self.model.figura_selecionada)

    def colar_figura(self, event=None):
        if self.model.figura_copiada:
            self.model.colar_figura(self.view.canvas)

    def ao_mudar_cor_fill(self, *args):
        if self.model.figura_selecionada:
            self.model.figura_selecionada.mudar_cor_fill(self.view.canvas, self.cor_fill.get())

    def ao_mudar_cor_out(self, *args):
        if self.model.figura_selecionada:
            self.model.figura_selecionada.mudar_cor_out(self.view.canvas, self.cor_out.get())

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
