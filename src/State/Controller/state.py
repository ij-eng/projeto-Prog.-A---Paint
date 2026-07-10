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

    @staticmethod
    def distancia_ponto(x1, y1, x2, y2, px, py):
        dx = x2 - x1
        dy = y2 - y1
        ab_len_sq = dx ** 2 + dy ** 2

        if ab_len_sq == 0:
            return sqrt((px - x1) ** 2 + (py - y1) ** 2)

        ap_x = px - x1
        ap_y = py - y1
        t = (ap_x * dx + ap_y * dy) / ab_len_sq
        t = max(0.0, min(1.0, t))

        ponto_proximo_x = x1 + t * dx
        ponto_proximo_y = y1 + t * dy

        return sqrt((px - ponto_proximo_x) ** 2 + (py - ponto_proximo_y) ** 2)

    @staticmethod
    def contem(valores, px, py):
        pontos = [(valores[i], valores[i + 1]) for i in range(0, len(valores) - 1, 2)]
        n = len(pontos)

        if n < 3:
            return False

        dentro = False
        p1x, p1y = pontos[0]

        for i in range(n + 1):
            p2x, p2y = pontos[i % n]

            if py > min(p1y, p2y):
                if py <= max(p1y, p2y):
                    if px <= max(p1x, p2x):
                        x_interceptado = px
                        if p1y != p2y:
                            x_interceptado = (py - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or px <= x_interceptado:
                            dentro = not dentro

            p1x, p1y = p2x, p2y

        return dentro

    def distancia_figura(self, figura, px, py):
        valores = figura.valores

        if isinstance(figura, (Linha, Rabisco)):
            menor_dist = float('inf')
            for i in range(0, len(valores) - 2, 2):
                d = self.distancia_ponto(valores[i], valores[i + 1], valores[i + 2], valores[i + 3], px, py)
                if d < menor_dist:
                    menor_dist = d
            return menor_dist

        elif isinstance(figura, Poligono):
            if self.contem(valores, px, py):
                return 0.0

            menor_dist = float('inf')
            for i in range(0, len(valores) - 2, 2):
                d = self.distancia_ponto(valores[i], valores[i + 1], valores[i + 2], valores[i + 3], px, py)
                if d < menor_dist:
                    menor_dist = d
            if len(valores) >= 6:
                d = self.distancia_ponto(valores[-2], valores[-1], valores[0], valores[1], px, py)
                if d < menor_dist:
                    menor_dist = d
            return menor_dist

        elif isinstance(figura, (Retangulo, Oval)):
            if len(valores) >= 4:
                x_min, x_max = min(valores[0], valores[2]), max(valores[0], valores[2])
                y_min, y_max = min(valores[1], valores[3]), max(valores[1], valores[3])
                if x_min <= px <= x_max and y_min <= py <= y_max:
                    return 0.0

        elif isinstance(figura, Circulo):
            if len(valores) >= 4:
                x1, y1, x2, y2 = valores[:4]
                raio = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                dist_centro = sqrt((px - x1) ** 2 + (py - y1) ** 2)
                if dist_centro <= raio:
                    return 0.0

        return float('inf')

    def ao_clicar(self, event):
        px, py = event.x, event.y
        tolerancia = 8

        figura_clicada = None
        menor_distancia = float('inf')

        for figura in reversed(self.model.figuras):
            if isinstance(figura, (Linha, Rabisco)):
                dist = self.distancia_figura(figura, px, py)
                if dist < tolerancia and dist < menor_distancia:
                    menor_distancia = dist
                    figura_clicada = figura

        if not figura_clicada:
            for figura in reversed(self.model.figuras):
                if not isinstance(figura, (Linha, Rabisco)):
                    dist = self.distancia_figura(figura, px, py)
                    if dist == 0.0 or dist < tolerancia:
                        if dist < menor_distancia:
                            menor_distancia = dist
                            figura_clicada = figura
                        if dist == 0.0:
                            break

        if figura_clicada:
            if self.model.figura_selecionada and self.model.figura_selecionada != figura_clicada:
                self.view.canvas.itemconfig(self.model.figura_selecionada.id_canvas, width=1)

            self.model.figura_selecionada = figura_clicada
            self.x_anterior = px
            self.y_anterior = py
            self.view.canvas.itemconfig(figura_clicada.id_canvas, width=3)
        else:
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