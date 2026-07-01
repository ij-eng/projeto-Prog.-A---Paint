from math import sqrt
from tkinter import colorchooser
from view import *
from model import *


class Controller:
    def __init__(self, root):
        self.model = Model()
        self.view = View(root, self)

        self.tipo_figura_var = self.view.tipo_figura_var
        self.cor_fill = self.view.cor_fill_var
        self.cor_out = self.view.cor_out_var

    def escolher_cor_out(self):
        cor = colorchooser.askcolor(title="Escolha a cor da linha")
        if cor[1]:
            self.cor_out.set(cor[1])

    def escolher_cor_in(self):
        cor = colorchooser.askcolor(title="Escolha a cor do preenchimento")
        if cor[1]:
            self.cor_fill.set(cor[1])

    def definir_transparente(self):
        self.cor_fill.set("")

    def ao_clicar(self, event):
        tipo = self.tipo_figura_var.get()
        if tipo == "Poligono":
            if not self.model.forma_em_andamento:
                self.model.valores_atual = [event.x, event.y]
                self.model.forma_em_andamento = True
            else:
                p_inicio_x, p_inicio_y = self.model.valores_atual[0], self.model.valores_atual[1]
                distancia_fechamento = sqrt((event.x - p_inicio_x) ** 2 + (event.y - p_inicio_y) ** 2)

                if distancia_fechamento < 10 and len(self.model.valores_atual) >= 6:
                    dados_figura = {
                        "tipo": tipo,
                        "valores": self.model.valores_atual.copy(),
                        "cor_fill": self.cor_fill.get(),
                        "cor_out": self.cor_out.get()
                    }
                    self.model.figuras.append(dados_figura)
                    self.view.desenhar_definitivo(self.model.valores_atual, self.cor_fill.get(), self.cor_out.get())
                    self.view.deletar_provisorio()
                    self.model.valores_atual = []
                    self.model.forma_em_andamento = False
                else:
                    self.model.valores_atual.extend([event.x, event.y])
        else:
            if self.model.forma_em_andamento:
                self.model.forma_em_andamento = False
                self.view.deletar_provisorio()
                self.model.valores_atual = []
            if tipo == "Rabisco":
                self.model.valores_atual = [event.x, event.y]
            else:
                self.model.valores_atual = [event.x, event.y, event.x, event.y]

    def ao_arrastar(self, event):
        tipo = self.tipo_figura_var.get()
        if tipo == "Poligono" or not self.model.valores_atual:
            return

        if tipo == "Rabisco":
            self.model.valores_atual.extend([event.x, event.y])
        else:
            if len(self.model.valores_atual) >= 4:
                self.model.valores_atual[2:4] = [event.x, event.y]
            else:
                self.model.valores_atual = [self.model.valores_atual[0], self.model.valores_atual[1], event.x, event.y]
        self.view.desenhar_provisorio(self.model.valores_atual, self.cor_fill.get(), self.cor_out.get())

    def ao_soltar(self, event):
        tipo = self.tipo_figura_var.get()
        if tipo == "Poligono" or not self.model.valores_atual:
            return

        self.view.deletar_provisorio()
        if tipo == "Rabisco":
            self.model.valores_atual.extend([event.x, event.y])
        else:
            self.model.valores_atual[2:4] = [event.x, event.y]

        self.model.tipo_atual = tipo

        if not self.model.incompleta():
            self.view.desenhar_definitivo(self.model.valores_atual, self.cor_fill.get(), self.cor_out.get())
            dados_figura = {
                "tipo": tipo,
                "valores": self.model.valores_atual.copy(),
                "cor_fill": self.cor_fill.get(),
                "cor_out": self.cor_out.get()
            }
            self.model.figuras.append(dados_figura)
        self.model.valores_atual = []

    def ao_mover(self, event):
        if self.tipo_figura_var.get() == "Poligono" and self.model.forma_em_andamento:
            valores_temp = self.model.valores_atual + [event.x, event.y]
            self.view.desenhar_provisorio(valores_temp, self.cor_fill.get(), self.cor_out.get())

    def ao_duplo_clique(self, event):
        if self.model.forma_em_andamento:
            coordenadas = self.model.valores_atual.copy()
            if len(coordenadas) >= 6:
                self.view.desenhar_definitivo(coordenadas, self.cor_fill.get(), self.cor_out.get())
                self.model.figuras.append(
                    {
                        "tipo": "Poligono",
                        "valores": coordenadas,
                        "cor_fill": self.cor_fill.get(),
                        "cor_out": self.cor_out.get()
                    }
                )
            elif len(coordenadas) >= 8:
                coordenadas = coordenadas[:-2]
            self.model.valores_atual = []
            self.model.forma_em_andamento = False
            self.view.deletar_provisorio()
