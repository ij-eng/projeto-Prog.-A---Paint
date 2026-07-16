from tkinter import colorchooser
from View.view import *
from Model.model import *
from tkinter import filedialog
from Controller.state import (LinhaState, RetanguloState, OvalState, CirculoState, RabiscoState, PoligonoState, SelecaoState, PoligonoRegularState)


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

        for figura in self.model.figuras_selecionadas:
            figura.destacar(self.view.canvas, False)
        self.model.figuras_selecionadas.clear()
        self.model.figura_selecionada = None

        estados = {
            "Linha": LinhaState(self),
            "Retangulo": RetanguloState(self),
            "Oval": OvalState(self),
            "Circulo": CirculoState(self),
            "Rabisco": RabiscoState(self),
            "Poligono": PoligonoState(self),
            "Poligono Regular": PoligonoRegularState(self),
            "Selecionar": SelecaoState(self)
        }

        self.estado_atual = estados[self.tipo_figura_var.get()]

    def deletar_figura(self, event=None):
        for figura in self.model.figuras_selecionadas:
            figura.deletar_do_canvas(self.view.canvas)
            if figura in self.model.figuras:
                self.model.figuras.remove(figura)
        self.model.figuras_selecionadas.clear()
        self.model.figura_selecionada = None

    def escolher_cor_out(self):
        cor = colorchooser.askcolor(title="Escolha a cor da borda")
        if cor[1]:
            self.cor_out.set(cor[1])

    def escolher_cor_in(self):
        cor = colorchooser.askcolor(title="Escolha a cor do preenchimento")
        if cor[1]:
            self.cor_fill.set(cor[1])

    def agrupar_figuras(self):
        if len(self.model.figuras_selecionadas) > 1:
            for fig in self.model.figuras_selecionadas:
                if fig in self.model.figuras:
                    self.model.figuras.remove(fig)
            grupo = FiguraComposta(list(self.model.figuras_selecionadas), self.cor_fill.get(), self.cor_out.get())
            self.model.figuras.append(grupo)
            self.model.figuras_selecionadas = [grupo]
            self.model.figura_selecionada = grupo
            grupo.destacar(self.view.canvas, True)

    def mover_posicao_frente(self, event=None):
        canvas = self.view.canvas
        for figura in self.model.figuras_selecionadas:
            idx = self.model.figuras.index(figura)
            if idx < len(self.model.figuras) - 1:
                figura_frente = self.model.figuras[idx + 1]
                self.model.figuras[idx], self.model.figuras[idx + 1] = self.model.figuras[idx + 1], self.model.figuras[idx]

                frente_ids = figura_frente.obter_ids_canvas()
                if frente_ids:
                    ultimo_id = frente_ids[-1]
                    for id_item in figura.obter_ids_canvas():
                        canvas.tag_raise(id_item, ultimo_id)
                        ultimo_id = id_item

    def mover_posicao_tras(self, event=None):
        canvas = self.view.canvas
        for figura in reversed(self.model.figuras_selecionadas):
            idx = self.model.figuras.index(figura)
            if idx > 0:
                figura_tras = self.model.figuras[idx - 1]
                self.model.figuras[idx], self.model.figuras[idx - 1] = self.model.figuras[idx - 1], self.model.figuras[idx]

                tras_ids = figura_tras.obter_ids_canvas()
                if tras_ids:
                    ultimo_id = tras_ids[0]
                    for id_item in reversed(figura.obter_ids_canvas()):
                        canvas.tag_lower(id_item, ultimo_id)
                        ultimo_id = id_item

    def mover_topo(self, event=None):
        canvas = self.view.canvas
        for figura in self.model.figuras_selecionadas:
            self.model.figuras.remove(figura)
            self.model.figuras.append(figura)
            for id_item in figura.obter_ids_canvas():
                canvas.tag_raise(id_item)

    def mover_fundo(self, event=None):
        canvas = self.view.canvas
        for figura in reversed(self.model.figuras_selecionadas):
            self.model.figuras.remove(figura)
            self.model.figuras.insert(0, figura)
            for id_item in reversed(figura.obter_ids_canvas()):
                canvas.tag_lower(id_item)

    def copiar_figura(self, event=None):
        self.model.copiar_figura()

    def colar_figura(self, event=None):
        if self.model.figura_copiada:
            self.model.colar_figura(self.view.canvas)

    def ao_mudar_cor_fill(self, *args):
        for figura in self.model.figuras_selecionadas:
            figura.mudar_cor_fill(self.view.canvas, self.cor_fill.get())

    def ao_mudar_cor_out(self, *args):
        for figura in self.model.figuras_selecionadas:
            figura.mudar_cor_out(self.view.canvas, self.cor_out.get())

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

    def ao_clique_direito(self, event):
        self.estado_atual.ao_clique_direito(event)