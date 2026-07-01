from math import sqrt
from tkinter import *
from tkinter import colorchooser
from tkinter.ttk import *
from model import *

class Linha(FormasModelo):
    def desenhar(self):
        self.canvas.create_line(
            self.valores[0], self.valores[1],
            self.valores[2], self.valores[3],
            fill=self.cor_out
        )

    def desenhar_provisorio(self):
        return self.canvas.create_line(
            self.valores[0], self.valores[1],
            self.valores[2], self.valores[3],
            fill=self.cor_out
        )


class Rabisco(FormasModelo):
    def desenhar(self):
        if len(self.valores) > 1:
            self.canvas.create_line(self.valores, fill=self.cor_out)

    def desenhar_provisorio(self):
        if len(self.valores) > 1:
            return self.canvas.create_line(self.valores, fill=self.cor_out)


class Retangulo(FormasModelo):
    def desenhar(self):
        self.canvas.create_rectangle(
            self.valores[0], self.valores[1],
            self.valores[2], self.valores[3],
            fill=self.cor_fill,
            outline=self.cor_out
        )

    def desenhar_provisorio(self):
        return self.canvas.create_rectangle(
            self.valores[0], self.valores[1],
            self.valores[2], self.valores[3],
            fill=self.cor_fill, outline=self.cor_out
        )


class Oval(FormasModelo):
    def desenhar(self):
        self.canvas.create_oval(
            self.valores[0], self.valores[1],
            self.valores[2], self.valores[3],
            fill=self.cor_fill,
            outline=self.cor_out
        )

    def desenhar_provisorio(self):
        return self.canvas.create_oval(
            self.valores[0], self.valores[1],
            self.valores[2], self.valores[3],
            fill=self.cor_fill,
            outline=self.cor_out
        )


class Circulo(FormasModelo):
    def desenhar(self):
        x1, y1 = self.valores[0], self.valores[1]
        x2, y2 = self.valores[2], self.valores[3]
        raio = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        self.canvas.create_oval(
            x1 - raio, y1 - raio,
            x1 + raio, y1 + raio,
            fill=self.cor_fill,
            outline=self.cor_out
        )

    def desenhar_provisorio(self):
        x1, y1 = self.valores[0], self.valores[1]
        x2, y2 = self.valores[2], self.valores[3]
        raio = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        return self.canvas.create_oval(
            x1 - raio, y1 - raio,
            x1 + raio, y1 + raio,
            fill=self.cor_fill,
            outline=self.cor_out
        )


class Poligono(FormasModelo):
    def desenhar(self):
        if len(self.valores) >= 6:
            self.canvas.create_polygon(
                self.valores, fill=self.cor_fill, outline=self.cor_out
            )

    def desenhar_provisorio(self):
        return self.canvas.create_line(self.valores, fill=self.cor_out)

class View:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("OO.1 - Padrão MVC")

        self.cor_fill_var = StringVar(self.root, value="")
        self.cor_out_var = StringVar(self.root, value="black")
        self.tipo_figura_var = StringVar(self.root, value="Rabisco")

        self.id_provisorio = None
        self.tag_temporaria = "temp_forma"

        self.interface()
        self.configurar_eventos()

    def interface(self):
        toolbar = Frame(self.root, padding=5)
        toolbar.pack(side=TOP, fill=X)

        Label(toolbar, text="Forma: ").pack(side=LEFT, padx=5)

        seletor = OptionMenu(toolbar, self.tipo_figura_var, "Rabisco", "Rabisco", "Linha", "Retangulo", "Oval",
                             "Circulo", "Poligono")
        seletor.pack(side=LEFT, padx=5)

        btn_cor_out = Button(toolbar, text="Cor da Linha", command=self.controller.escolher_cor_in)
        btn_cor_out.pack(side=LEFT, padx=5)

        btn_cor_in = Button(toolbar, text="Cor do Preenchimento", command=self.controller.escolher_cor_out)
        btn_cor_in.pack(side=LEFT, padx=5)

        self.canvas = Canvas(self.root, bg="white", width=1440, height=800)
        self.canvas.pack(side=TOP, fill=BOTH, expand=True)

    def configurar_eventos(self):
        self.canvas.bind("<Button-1>", self.controller.ao_clicar)
        self.canvas.bind("<B1-Motion>", self.controller.ao_arrastar)
        self.canvas.bind("<ButtonRelease-1>", self.controller.ao_soltar)
        self.canvas.bind("<Motion>", self.controller.ao_mover)
        self.canvas.bind("<Double-Button-1>", self.controller.ao_duplo_clique)

    def obter_figura_classe(self):
        classes = {
            "Linha": Linha,
            "Rabisco": Rabisco,
            "Retangulo": Retangulo,
            "Oval": Oval,
            "Circulo": Circulo,
            "Poligono": Poligono
        }
        return classes[self.tipo_figura_var.get()]