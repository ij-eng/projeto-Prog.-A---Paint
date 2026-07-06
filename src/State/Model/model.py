from math import sqrt

class Model:
    def __init__(self):
        self.figuras = []
        self.valores_atual = []
        self.forma_em_andamento = False
        self.id_provisorio = None

    def deletar_provisorio(self, canvas):
        if self.id_provisorio:
            canvas.delete(self.id_provisorio)
            self.id_provisorio = None

    def desenhar_definitivo(self, canvas, classe_forma, valores, cor_fill, cor_out):
        figura = classe_forma(valores, cor_fill, cor_out)
        figura.desenhar(canvas)
        self.figuras.append(figura)

    def desenhar_provisorio(self, canvas, classe_forma, valores, cor_fill, cor_out):
        self.deletar_provisorio(canvas)
        figura = classe_forma(valores, cor_fill, cor_out)
        self.id_provisorio = figura.desenhar_provisorio(canvas)

    def salvar_para_txt(self, caminho):
        with open(caminho, 'w') as f:
            for figura in self.figuras:
                valores_str = ",".join(map(str, figura.valores))
                f.write(f"{type(figura).__name__}|{valores_str}|{figura.cor_fill}|{figura.cor_out}\n")

    def carregar_de_txt(self, caminho):
        self.figuras = []
        with open(caminho, 'r') as f:
            for linha in f:
                linha = linha.strip()
                if not linha: continue

                tipo, valores_str, cor_fill, cor_out = linha.split('|')
                valores = [float(x) if '.' in x else int(x) for x in valores_str.split(',')]

                classe_forma = globals().get(tipo)

                if classe_forma and issubclass(classe_forma, FormasModelo):
                    figura = classe_forma(valores, cor_fill, cor_out)
                    self.figuras.append(figura)

    def redesenhar_tudo(self, canvas):
        for figura in self.figuras:
            figura.desenhar(canvas)

class FormasModelo:
    def __init__(self, valores, cor_fill, cor_out):
        self.valores = valores
        self.cor_fill = cor_fill
        self.cor_out = cor_out

    def desenhar(self, canvas): pass

    def desenhar_provisorio(self, canvas):
        return self.desenhar(canvas)


class Linha(FormasModelo):
    def desenhar(self, canvas):
        if len(self.valores) >= 4:
            return canvas.create_line(self.valores[0], self.valores[1], self.valores[2], self.valores[3],
                                      fill=self.cor_out)

class Rabisco(FormasModelo):
    def desenhar(self, canvas):
        if len(self.valores) > 1:
            return canvas.create_line(self.valores, fill=self.cor_out)

class Retangulo(FormasModelo):
    def desenhar(self, canvas):
        if len(self.valores) >= 4:
            return canvas.create_rectangle(self.valores[0], self.valores[1], self.valores[2], self.valores[3],
                                           fill=self.cor_fill, outline=self.cor_out)

class Oval(FormasModelo):
    def desenhar(self, canvas):
        if len(self.valores) >= 4:
            return canvas.create_oval(self.valores[0], self.valores[1], self.valores[2], self.valores[3],
                                      fill=self.cor_fill, outline=self.cor_out)

class Circulo(FormasModelo):
    def desenhar(self, canvas):
        if len(self.valores) >= 4:
            x1, y1, x2, y2 = self.valores[:4]
            raio = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            return canvas.create_oval(x1 - raio, y1 - raio, x1 + raio, y1 + raio, fill=self.cor_fill,
                                      outline=self.cor_out)

class Poligono(FormasModelo):
    def desenhar(self, canvas):
        if len(self.valores) >= 6:
            return canvas.create_polygon(self.valores, fill=self.cor_fill, outline=self.cor_out)

    def desenhar_provisorio(self, canvas):
        if len(self.valores) >= 4:
            return canvas.create_line(self.valores, fill=self.cor_out)
