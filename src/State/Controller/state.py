from math import sqrt, atan2, pi, cos, sin
from Model.model import Linha, Retangulo, Oval, Circulo, Rabisco, Poligono, PoligonoRegular


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

    def ao_clique_direito(self, event): pass


class SelecaoState(ControlState):
    def __init__(self, controller):
        super().__init__(controller)
        self.x_anterior = 0
        self.y_anterior = 0
        self.x_inicio = 0
        self.y_inicio = 0
        self.modo_selecionar_por_retangulo = False

    def ao_clicar(self, event):
        px, py = event.x, event.y
        tolerancia = 8

        figura_clicada = None

        ctrl = (event.state & 4) != 0

        for figura in reversed(self.model.figuras):
            if figura.foi_clicada(px, py, tolerancia):
                figura_clicada = figura
                break
        if figura_clicada:
            self.selecionar_por_retangulo = False
            if ctrl:
                if figura_clicada:
                    if figura_clicada in self.model.figuras_selecionadas:
                        figura_clicada.destacar(self.view.canvas, False)
                        self.model.figuras_selecionadas.remove(figura_clicada)
                    else:
                        figura_clicada.destacar(self.view.canvas, True)
                        self.model.figuras_selecionadas.append(figura_clicada)
            else:
                if figura_clicada:
                    if figura_clicada not in self.model.figuras_selecionadas:
                        for fig in self.model.figuras_selecionadas:
                            fig.destacar(self.view.canvas, False)
                        self.model.figuras_selecionadas = [figura_clicada]
                        figura_clicada.destacar(self.view.canvas, True)
                else:
                    for fig in self.model.figuras_selecionadas:
                        fig.destacar(self.view.canvas, False)
                    self.model.figuras_selecionadas.clear()
        else:
            # Se clicou no vazio, inicia a seleção por caixa
            self.modo_selecionar_por_retangulo = True
            self.x_inicio = px
            self.y_inicio = py
            
            # Se não estiver pressionando CTRL, limpa a seleção atual
            if not ctrl:
                for fig in self.model.figuras_selecionadas:
                    fig.destacar(self.view.canvas, False)
                self.model.figuras_selecionadas.clear()

        self.model.figura_selecionada = self.model.figuras_selecionadas[-1] if self.model.figuras_selecionadas else None
        self.x_anterior = px
        self.y_anterior = py

    def ao_arrastar(self, event):
        if self.modo_selecionar_por_retangulo:
            # Desenha o retângulo de seleção provisório 
            valores_retangulo = [self.x_inicio, self.y_inicio, event.x, event.y]
            self.model.desenhar_provisorio(
                self.view.canvas, 
                Retangulo, 
                valores_retangulo, 
                "",          # Fundo transparente 
                "blue"       # Cor da borda
            )
        elif self.model.figuras_selecionadas:
            # Arrastar figuras selecionadas
            dx = event.x - self.x_anterior
            dy = event.y - self.y_anterior

            for figura in self.model.figuras_selecionadas:
                figura.mover_no_canvas(self.view.canvas, dx, dy)
                figura.mover(dx, dy)

            self.x_anterior = event.x
            self.y_anterior = event.y
    def ao_soltar(self, event):
        if self.modo_selecionar_por_retangulo:
            # Remove o retângulo azul pontilhado provisório da tela
            self.model.deletar_provisorio(self.view.canvas)
            
            # Determina os limites da caixa de seleção final
            x_min, x_max = sorted([self.x_inicio, event.x])
            y_min, y_max = sorted([self.y_inicio, event.y])

            # Procura por figuras que estão inteiramente dentro do seu retângulo de seleção
            for figura in self.model.figuras:
                completamente_dentro = self.seEstadentro(figura)
                if completamente_dentro:
                    fig_x1, fig_y1, fig_x2, fig_y2 = completamente_dentro
                    # Confere se a figura está de fato dentro da área do arrasto
                    if (x_min <= fig_x1 and fig_x2 <= x_max and 
                        y_min <= fig_y1 and fig_y2 <= y_max):
                        if figura not in self.model.figuras_selecionadas:
                            self.model.figuras_selecionadas.append(figura)
                            figura.destacar(self.view.canvas, True)

            self.model.figura_selecionada = self.model.figuras_selecionadas[-1] if self.model.figuras_selecionadas else None
            self.modo_selecionar_por_retangulo = False
        else:
            pass

    def seEstadentro(self, figura):
        """Cria o retangulo delimitador"""
        # Se for um Círculo ou Oval, calculamos matematicamente os limites a partir dos valores armazenados
        if type(figura) in [Circulo, Oval] and len(figura.valores) >= 4:
            # Para círculos/ovais, valores geralmente são [x1, y1, x2, y2] 
            x1, y1, x2, y2 = figura.valores[:4]
            return min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)
            
        # Para Polígonos, Rabiscos e outras formas com múltiplos pontos
        if len(figura.valores) >= 2:
            xs = figura.valores[0::2]
            ys = figura.valores[1::2]
            return min(xs), min(ys), max(xs), max(ys)
        
        if figura.id:
            return self.view.canvas.completamente_dentro(figura.id)
            
        return None

class FormaState(ControlState):
    def __init__(self, controller, classe_forma):
        super().__init__(controller)
        self.classe_forma = classe_forma

    def ao_clicar(self, event):
        self.model.deletar_provisorio(self.view.canvas)
        self.model.valores_atual = [event.x, event.y, event.x, event.y]

    def ao_arrastar(self, event):
        self.model.valores_atual[2:4] = [event.x, event.y]
        self.model.desenhar_provisorio(self.view.canvas, self.classe_forma, self.model.valores_atual, self.cor_fill,
                                       self.cor_out)

    def ao_soltar(self, event):
        if not self.model.valores_atual: return
        self.model.deletar_provisorio(self.view.canvas)
        self.model.valores_atual[2:4] = [event.x, event.y]

        valores = self.model.valores_atual
        incompleta = len(valores) < 4 or (valores[0] == valores[2] and valores[1] == valores[3])

        if not incompleta:
            self.model.desenhar_definitivo(self.view.canvas, self.classe_forma, valores.copy(), self.cor_fill,
                                           self.cor_out)
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
            self.model.desenhar_definitivo(self.view.canvas, Rabisco, valores.copy(), self.cor_fill, self.cor_out)
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
            self.model.desenhar_definitivo(self.view.canvas, Poligono, self.model.valores_atual.copy(), self.cor_fill,
                                           self.cor_out)
        self.model.valores_atual = []
        self.model.forma_em_andamento = False


class PoligonoRegularState(ControlState):
    def __init__(self, controller):
        super().__init__(controller)
        self.centro = None
        self.num_lados = 3

    def ao_clicar(self, event):
        if self.centro is None:
            self.centro = (event.x, event.y)
            self.num_lados = 3
            self.model.forma_em_andamento = True
            self.atualizar_provisorio(event.x, event.y)
        else:
            self.num_lados += 1
            self.atualizar_provisorio(event.x, event.y)

    def ao_mover(self, event):
        if self.centro is not None:
            self.atualizar_provisorio(event.x, event.y)

    def ao_clique_direito(self, event):
        if self.centro is not None:
            self.num_lados = max(3, self.num_lados - 1)
            self.atualizar_provisorio(event.x, event.y)

    def ao_duplo_clique(self, event):
        if self.centro is not None:
            self.num_lados = max(3, self.num_lados - 1)

            cx, cy = self.centro
            mx, my = event.x, event.y
            dx = mx - cx
            dy = my - cy
            raio = sqrt(dx ** 2 + dy ** 2)

            angulo_inicial = atan2(dy, dx)
            pontos = []
            for i in range(self.num_lados):
                ang = angulo_inicial + i * (2 * pi / self.num_lados)
                px = cx + raio * cos(ang)
                py = cy + raio * sin(ang)
                pontos.extend([px, py])

            self.model.deletar_provisorio(self.view.canvas)

            if len(pontos) >= 6:
                self.model.desenhar_definitivo(
                    self.view.canvas,
                    PoligonoRegular,
                    pontos,
                    self.cor_fill,
                    self.cor_out
                )

            self.centro = None
            self.num_lados = 3
            self.model.valores_atual = []
            self.model.forma_em_andamento = False

    def atualizar_provisorio(self, mx, my):
        cx, cy = self.centro
        self.model.valores_atual = [cx, cy, mx, my, self.num_lados]
        self.model.desenhar_provisorio(
            self.view.canvas,
            PoligonoRegular,
            self.model.valores_atual,
            self.cor_fill,
            self.cor_out
        )