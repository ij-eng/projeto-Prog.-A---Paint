from tkinter import colorchooser, messagebox
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

        self.view.canvas.bind("<Button-1>", lambda event: self.view.canvas.focus_set(), add="+")
        self.view.canvas.focus_set()

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
        if self.model.figuras_selecionadas:
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
            figuras_ordenadas = sorted(
                [fig for fig in self.model.figuras_selecionadas if fig in self.model.figuras],
                key=lambda f: self.model.figuras.index(f)
            )

            indices = [self.model.figuras.index(fig) for fig in figuras_ordenadas]
            max_idx = max(indices)
            proximo_elemento = self.model.figuras[max_idx + 1] if max_idx + 1 < len(self.model.figuras) else None

            for fig in figuras_ordenadas:
                self.model.figuras.remove(fig)

            grupo = FiguraComposta(figuras_ordenadas, self.cor_fill.get(), self.cor_out.get())
            
            if proximo_elemento in self.model.figuras:
                idx_insercao = self.model.figuras.index(proximo_elemento)
                self.model.figuras.insert(idx_insercao, grupo)
            else:
                self.model.figuras.append(grupo)

            self.model.figuras_selecionadas = [grupo]
            self.model.figura_selecionada = grupo
            grupo.destacar(self.view.canvas, True)
            
            self.sincronizar_idx(self.view.canvas)

    def mover_posicao_frente(self, event=None):
        canvas = self.view.canvas
        figuras_totais = self.model.figuras
        selecionadas = self.model.figuras_selecionadas

        if not selecionadas: return
        canvas.focus_set()
        indices_ordenados = sorted(
            [figuras_totais.index(f) for f in selecionadas], 
            reverse=True
        )
        for idx in indices_ordenados:
            if idx < len(figuras_totais) - 1:
                if figuras_totais[idx] in self.model.figuras_selecionadas and figuras_totais[idx+1] not in self.model.figuras_selecionadas:
                    figura = figuras_totais[idx]
                    figura_frente = figuras_totais[idx + 1]
                    figuras_totais[idx], figuras_totais[idx + 1] = figuras_totais[idx + 1], figuras_totais[idx]
                    frente_ids = figura_frente.obter_ids_canvas()
                    if frente_ids:
                        ultimo_id = frente_ids[-1]
                        for id_item in figura.obter_ids_canvas():
                            canvas.tag_raise(id_item, ultimo_id)
                            ultimo_id = id_item

    def mover_posicao_tras(self, event=None):
        canvas = self.view.canvas
        figuras_totais = self.model.figuras
        selecionadas = self.model.figuras_selecionadas
        if not selecionadas: return
        canvas.focus_set()
        indices_ordenados = sorted(
            [figuras_totais.index(f) for f in selecionadas]
        )

        for idx in indices_ordenados:
            if idx > 0:
                figura = figuras_totais[idx]
                figura_tras = figuras_totais[idx - 1]
                if figuras_totais[idx] in self.model.figuras_selecionadas and figuras_totais[idx-1] not in self.model.figuras_selecionadas:
                    figuras_totais[idx], figuras_totais[idx - 1] = figuras_totais[idx - 1], figuras_totais[idx]
                    tras_ids = figura_tras.obter_ids_canvas()
                    if tras_ids:
                        ultimo_id = tras_ids[0]
                        for id_item in reversed(figura.obter_ids_canvas()):
                            canvas.tag_lower(id_item, ultimo_id)
                            ultimo_id = id_item

    def mover_topo(self, event=None):
        canvas = self.view.canvas
        if not self.model.figuras_selecionadas:
            return
        canvas.focus_set()
        figuras_ordenadas = sorted(self.model.figuras_selecionadas, 
                                   key=lambda f: self.model.figuras.index(f))
        for figura in figuras_ordenadas:
            self.model.figuras.remove(figura)
            self.model.figuras.append(figura)
        self.model.figuras_selecionadas.sort(key=lambda f: self.model.figuras.index(f))
        self.sincronizar_idx(canvas)

    def mover_fundo(self, event=None):
        canvas = self.view.canvas
        if not self.model.figuras_selecionadas:
            return
        canvas.focus_set()
        figuras_ordenadas = sorted(self.model.figuras_selecionadas, 
                                   key=lambda f: self.model.figuras.index(f),
                                   reverse=True)

        for figura in figuras_ordenadas:
            self.model.figuras.remove(figura)
            self.model.figuras.insert(0, figura)
        self.model.figuras_selecionadas.sort(key=lambda f: self.model.figuras.index(f))
            
        self.sincronizar_idx(canvas)

    def sincronizar_idx(self, canvas):
        for fig in self.model.figuras:
            for id_item in fig.obter_ids_canvas():
                canvas.tag_raise(id_item)

    def copiar_figura(self, event=None):
        self.model.copiar_figura()

    def colar_figura(self, event=None):
        if self.model.figura_copiada:
            self.model.colar_figura(self.view.canvas)

    def ao_mudar_cor_fill(self, *args):
        if self.model.figuras_selecionadas:
            for figura in self.model.figuras_selecionadas:
                figura.mudar_cor_fill(self.view.canvas, self.cor_fill.get())

    def ao_mudar_cor_out(self, *args):
        if self.model.figuras_selecionadas:
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

    def mostrar_ajuda(self):
        texto_ajuda = (
            "GUIA DE ATALHOS E FUNCIONALIDADES\n\n"
            "SELEÇÃO E MOUSE:\n"
            "- Selecionar: Escolha 'Selecionar' e clique em uma figura.\n"
            "- Seleção Múltipla: Segure 'Ctrl' ao clicar em figuras ou clique e arraste para criar uma caixa de seleção.\n"
            "- Tirar seleção: Para tirar uma seleção especifica segure 'Ctrl' e clique na figura desejada, para tirar a seleção de todas as figuras clique fora do desenho.\n\n"
            "TECLADO:\n"
            "- Ctrl + C : Copiar figuras selecionadas\n"
            "- Ctrl + V : Colar figuras copiadas\n"
            "- Delete / Backspace : Apagar figuras selecionadas\n\n"
            "CAMADAS (Com figuras selecionadas):\n"
            "- Seta para Direita : Mover figura um nível para a frente\n"
            "- Seta para Esquerda : Mover figura um nível para trás\n"
            "- Seta para Cima : Trazer figura para o topo absoluto\n"
            "- Seta para Baixo : Enviar figura para o fundo absoluto\n\n"
            "FORMAS ESPECIAIS:\n"
            "- Polígono: Clique para ir adicionando vértices. Dê um Duplo-clique para fechar a forma ou coloque a linha muito perto do primeiro ponto.\n"
            "- Polígono Regular: Clique para definir o centro, mova para definir o tamanho. O botão direito do mouse diminui os lados. Duplo-clique finaliza."
        )
        messagebox.showinfo("Ajuda e Atalhos do Paint", texto_ajuda)
