from math import sqrt
from tkinter import colorchooser
from view import *
from model import *

class Controller:
    def __init__(self, root):
        self.model = AppModelo()
        self.view = View(root, self)
        self.tipo_figura_var = self.view.tipo_figura_var
        self.cor_fill = self.view.cor_fill_var
        self.cor_out = self.view.cor_out_var
        self.canvas = self.view.canvas

    @property
    def figuras(self):
        return self.model.figuras

    @figuras.setter
    def figuras(self, val):
        self.model.figuras = val

    @property
    def valores_atual(self):
        return self.model.valores_atual

    @valores_atual.setter
    def valores_atual(self, val):
        self.model.valores_atual = val

    @property
    def forma_em_andamento(self):
        return self.model.forma_em_andamento

    @forma_em_andamento.setter
    def forma_em_andamento(self, val):
        self.model.forma_em_andamento = val

    @property
    def id_provisorio(self):
        return self.view.id_provisorio

    @id_provisorio.setter
    def id_provisorio(self, val):
        self.view.id_provisorio = val

    def incompleta(self):
        self.model.tipo_atual = self.tipo_figura_var.get()
        return self.model.incompleta()

    def escolher_cor_out(self):
        cor_in = colorchooser.askcolor(title="Escolha uma cor")
        if cor_in[1]:
            self.cor_fill.set(cor_in[1])

    def escolher_cor_in(self):
        cor_outl = colorchooser.askcolor(title="Escolha uma cor")
        if cor_outl[1]:
            self.cor_out.set(cor_outl[1])

    def ao_clicar(self, event):
        if self.tipo_figura_var.get() == "Poligono":
            if not self.forma_em_andamento:
                self.valores_atual = [event.x, event.y]
                self.forma_em_andamento = True
            else:
                p_inicio_x, p_inicio_y = self.valores_atual[0], self.valores_atual[1]
                distancia_fechamento = sqrt((event.x - p_inicio_x) ** 2 + (event.y - p_inicio_y) ** 2)

                if distancia_fechamento < 10 and len(self.valores_atual) >= 6:
                    figura = Poligono(self.canvas, self.valores_atual.copy(), self.cor_fill.get(), self.cor_out.get())
                    figura.desenhar()
                    self.figuras.append(figura)

                    self.valores_atual = []
                    self.forma_em_andamento = False
                    if self.id_provisorio:
                        self.canvas.delete(self.id_provisorio)
                        self.id_provisorio = None
                else:
                    self.valores_atual.extend([event.x, event.y])
        else:
            if self.forma_em_andamento:
                self.forma_em_andamento = False
                if self.id_provisorio:
                    self.canvas.delete(self.id_provisorio)
                    self.id_provisorio = None
                self.valores_atual = []

            if self.tipo_figura_var.get() == "Rabisco":
                self.valores_atual = [event.x, event.y]
            else:
                self.valores_atual = [event.x, event.y, event.x, event.y]


    def ao_duplo_clique(self, event):
        if self.tipo_figura_var.get() == "Poligono" and self.forma_em_andamento:
            coordenadas = self.valores_atual.copy()
            if len(coordenadas) >= 8:
                coordenadas = coordenadas[:-2]
            if len(coordenadas) >= 6:
                figura = Poligono(self.canvas, coordenadas, self.cor_fill.get(), self.cor_out.get())
                figura.desenhar()
                self.figuras.append(figura)
            self.valores_atual = []
            self.forma_em_andamento = False
            if self.id_provisorio:
                self.canvas.delete(self.id_provisorio)
                self.id_provisorio = None


    def ao_mover(self, event):
        if self.tipo_figura_var.get() == "Poligono" and self.forma_em_andamento:
            valores_temp = self.valores_atual + [event.x, event.y]
            figura = Poligono(self.canvas, valores_temp, self.cor_fill.get(), self.cor_out.get())

            if self.id_provisorio:
                self.canvas.delete(self.id_provisorio)

            self.id_provisorio = figura.desenhar_provisorio()


    def ao_arrastar(self, event):
        if self.tipo_figura_var.get() == "Poligono":
            return

        if self.id_provisorio:
            self.canvas.delete(self.id_provisorio)

        classe = self.view.obter_figura_classe()

        if self.tipo_figura_var.get() == "Rabisco":
            self.valores_atual.append(event.x)
            self.valores_atual.append(event.y)
        else:
            self.valores_atual[2] = event.x
            self.valores_atual[3] = event.y

        figura = classe(self.canvas, self.valores_atual, self.cor_fill.get(), self.cor_out.get())
        self.id_provisorio = figura.desenhar_provisorio()


    def ao_soltar(self, event):
        if self.tipo_figura_var.get() == "Poligono":
            return

        if self.id_provisorio:
            self.canvas.delete(self.id_provisorio)
            self.id_provisorio = None

        classe = self.view.obter_figura_classe()

        if self.tipo_figura_var.get() == "Rabisco":
            self.valores_atual.append(event.x)
            self.valores_atual.append(event.y)
        else:
            self.valores_atual[2] = event.x
            self.valores_atual[3] = event.y

        if not self.incompleta():
            figura = classe(self.canvas, self.valores_atual, self.cor_fill.get(), self.cor_out.get())
            figura.desenhar()
            self.figuras.append(figura)
        self.valores_atual = []