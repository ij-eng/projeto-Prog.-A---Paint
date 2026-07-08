from math import sqrt
from Model.model import Linha, Retangulo, Oval, Circulo, Rabisco, Poligono

class ControlState:
    def __init__(self, controller):
        self.controller = controller
        self.model = controller.model
        self.view = controller.view

    @property
    def cor_fill(self) -> str:
        return self.controller.cor_fill.get()

    @property
    def cor_out(self) -> str:
        return self.controller.cor_out.get()

    def ao_clicar(self, event): pass
    def ao_arrastar(self, event): pass
    def ao_soltar(self, event): pass
    def ao_mover(self, event): pass
    def ao_duplo_clique(self, event): pass


class SelecaoState(ControlState):
    def __init__(self, controller):
        super().__init__(controller)
        self.x_anterior = 0
        self.y_anterior = 0

    def ao_clicar(self, event):
        itens_clicados = self.view.canvas.find_withtag("current")

        if itens_clicados:
            id_clicado = itens_clicados[0]
            figura = self.model.obter_figura_por_id(id_clicado)

            if figura:
                if self.model.figura_selecionada and self.model.figura_selecionada != figura:
                    self.view.canvas.itemconfig(self.model.figura_selecionada.id_canvas, width=1)

                self.model.figura_selecionada = figura
                self.x_anterior = event.x
                self.y_anterior = event.y
                self.view.canvas.itemconfig(figura.id_canvas, width=3)
                return

        if self.model.figura_selecionada:
            self.view.canvas.itemconfig(self.model.figura_selecionada.id_canvas, width=1)
            self.model.figura_selecionada = None

    def ao_arrastar(self, event):
        if self.model.figura_selecionada:
            dx = event.x - self.x_anterior
            dy = event.y - self.y_anterior

            id_canvas = self.model.figura_selecionada.id_canvas
            self.view.canvas.move(id_canvas, dx, dy)

            for i in range(0, len(self.model.figura_selecionada.valores), 2):
                self.model.figura_selecionada.valores[i] += dx
                self.model.figura_selecionada.valores[i + 1] += dy

            self.x_anterior = event.x
            self.y_anterior = event.y

    def ao_soltar(self, event):
        pass

class FormaState(ControlState):
    def __init__(self, controller, classe_forma):
        super().__init__(controller)
        self.classe_forma = classe_forma

    def ao_clicar(self, event):
        self.model.deletar_provisorio(self.view.canvas)
        self.model.valores_atual = [event.x, event.y, event.x, event.y]

    def ao_arrastar(self, event):
        self.model.valores_atual.__setitem__(slice(2, 4), [event.x, event.y])
        self.model.desenhar_provisorio(self.view.canvas, self.classe_forma, self.model.valores_atual, self.cor_fill, self.cor_out)

    def ao_soltar(self, event):
        if not self.model.valores_atual: return
        self.model.deletar_provisorio(self.view.canvas)
        self.model.valores_atual[2:4] = [event.x, event.y]

        valores = self.model.valores_atual
        incompleta = len(valores) < 4 or (valores[0] == valores[2] and valores[1] == valores[3])

        if not incompleta:
            self.model.desenhar_definitivo(self.view.canvas, self.classe_forma, valores.copy(), self.cor_fill, self.cor_out)
        self.model.valores_atual = []


class LinhaState(FormaState):
    def __init__(self, controller):
        super().__init__(controller, Linha)


class RetanguloState(FormaState):
    def __init__(self, controller):
        super().__init__(controller, Retangulo)


class OvalState(FormaState):
    def __init__(self, controller):
        super().__init__(controller, Oval)


class CirculoState(FormaState):
    def __init__(self, controller):
        super().__init__(controller, Circulo)


class RabiscoState(ControlState):
    def ao_clicar(self, event):
        self.model.deletar_provisorio(self.view.canvas)
        self.model.valores_atual = [event.x, event.y]

    def ao_arrastar(self, event):
        if not self.model.valores_atual: return
        self.model.valores_atual.extend([event.x, event.y])
        self.model.desenhar_provisorio(self.view.canvas, Rabisco, self.model.valores_atual, self.cor_fill, self.cor_out)

    def ao_soltar(self, event):
        if not self.model.valores_atual: return
        self.model.deletar_provisorio(self.view.canvas)
        self.model.valores_atual.extend([event.x, event.y])

        valores = self.model.valores_atual

        if len(valores) > 2:
            self.model.desenhar_definitivo( self.view.canvas, Rabisco, valores.copy(), self.cor_fill, self.cor_out)
        self.model.valores_atual = []


class PoligonoState(ControlState):
    def ao_clicar(self, event):
        if not self.model.forma_em_andamento:
            self.model.valores_atual = [event.x, event.y]
            self.model.forma_em_andamento = True
        else:
            dist = sqrt((event.x - self.model.valores_atual[0]) ** 2 + (event.y - self.model.valores_atual[1]) ** 2)
            if dist < 10 and len(self.model.valores_atual) >= 6:
                self.finalizar_forma()
            else:
                self.model.valores_atual.extend([event.x, event.y])

    def ao_mover(self, event):
        if self.model.forma_em_andamento:
            valores_temp = self.model.valores_atual + [event.x, event.y]
            self.model.desenhar_provisorio(self.view.canvas, Poligono, valores_temp, self.cor_fill, self.cor_out)

    def ao_duplo_clique(self, event):
        if self.model.forma_em_andamento:
            if len(self.model.valores_atual) >= 8:
                self.model.valores_atual = self.model.valores_atual[:-2]
            self.finalizar_forma()

    def finalizar_forma(self):
        self.model.deletar_provisorio(self.view.canvas)
        if len(self.model.valores_atual) >= 6:
            self.model.desenhar_definitivo(self.view.canvas, Poligono, self.model.valores_atual.copy(), self.cor_fill, self.cor_out)
        self.model.valores_atual = []
        self.model.forma_em_andamento = False
