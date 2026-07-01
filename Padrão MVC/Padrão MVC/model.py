from math import sqrt

class Model:
    def __init__(self):
        self.figuras = []
        self.valores_atual = []
        self.forma_em_andamento = False
        self.tipo_atual = "Rabisco"
        self.id_provisorio = None

    def incompleta(self):
        if len(self.valores_atual) < 4:
            return True

        if self.tipo_atual == "Rabisco":
            if len(self.valores_atual) == 4:
                return self.valores_atual[0] == self.valores_atual[2] and self.valores_atual[1] == self.valores_atual[3]
            return False
        return self.valores_atual[0] == self.valores_atual[2] and self.valores_atual[1] == self.valores_atual[3]

    def obter_figura_classe(self, tipo):
        classes = {
            "Linha": Linha,
            "Rabisco": Rabisco,
            "Retangulo": Retangulo,
            "Oval": Oval,
            "Circulo": Circulo,
            "Poligono": Poligono
        }
        return classes[tipo]

    def deletar_provisorio(self, canvas):
        if self.id_provisorio:
            canvas.delete(self.id_provisorio)
            self.id_provisorio = None

    def desenhar_definitivo(self, canvas, tipo, valores, cor_fill, cor_out):
        classe = self.obter_figura_classe(tipo)
        figura = classe(valores, cor_fill, cor_out)
        figura.desenhar(canvas)

    def desenhar_provisorio(self, canvas, tipo, valores, cor_fill, cor_out):
        self.deletar_provisorio(canvas)
        classe = self.obter_figura_classe(tipo)
        figura = classe(valores, cor_fill, cor_out)
        self.id_provisorio = figura.desenhar_provisorio(canvas)


class FormasModelo:
    def __init__(self, valores, cor_fill, cor_out):
        self.valores = valores
        self.cor_fill = cor_fill if cor_fill != "" else ""
        self.cor_out = cor_out

    def desenhar(self, canvas): pass

    def desenhar_provisorio(self, canvas): pass


class Linha(FormasModelo):
    def desenhar(self, canvas):
        return canvas.create_line(
            self.valores[0], self.valores[1],
            self.valores[2], self.valores[3],
            fill=self.cor_out
        )
    def desenhar_provisorio(self, canvas):
        return self.desenhar(canvas)


class Rabisco(FormasModelo):
    def desenhar(self, canvas):
        if len(self.valores) > 1:
            return canvas.create_line(self.valores, fill=self.cor_out)
    def desenhar_provisorio(self, canvas):
        return self.desenhar(canvas)


class Retangulo(FormasModelo):
    def desenhar(self, canvas):
        return canvas.create_rectangle(
            self.valores[0], self.valores[1],
            self.valores[2], self.valores[3],
            fill=self.cor_fill, outline=self.cor_out
        )
    def desenhar_provisorio(self, canvas):
        return self.desenhar(canvas)


class Oval(FormasModelo):
    def desenhar(self, canvas):
        return canvas.create_oval(
            self.valores[0], self.valores[1],
            self.valores[2], self.valores[3],
            fill=self.cor_fill, outline=self.cor_out
        )
    def desenhar_provisorio(self, canvas):
        return self.desenhar(canvas)


class Circulo(FormasModelo):
    def desenhar(self, canvas):
        x1, y1, x2, y2 = self.valores[0], self.valores[1], self.valores[2], self.valores[3]
        raio = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return canvas.create_oval(
            x1 - raio, y1 - raio,
            x1 + raio, y1 + raio,
            fill=self.cor_fill, outline=self.cor_out
        )
    def desenhar_provisorio(self, canvas):
        return self.desenhar(canvas)


class Poligono(FormasModelo):
    def desenhar(self, canvas):
        if len(self.valores) >= 4:
            return canvas.create_polygon(
                self.valores,
                fill=self.cor_fill, outline=self.cor_out
            )
    def desenhar_provisorio(self, canvas):
        if len(self.valores) >= 4:
            return canvas.create_line(self.valores, fill=self.cor_out)
