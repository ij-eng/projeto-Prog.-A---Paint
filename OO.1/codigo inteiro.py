from tkinter import *
from tkinter.ttk import *
import math
from tkinter import colorchooser
from abc import ABC, abstractmethod


class Figura(ABC):
    def __init__(self, canvas, valores, cor_fill, cor_out):
        self.canvas = canvas
        self.valores = valores
        self.cor_fill = cor_fill
        self.cor_out = cor_out

    @abstractmethod
    def desenhar(self):
        pass

    @abstractmethod
    def desenhar_provisorio(self):
        pass


class Linha(Figura):
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


class Rabisco(Figura):
    def desenhar(self):
        if len(self.valores) > 1:
            self.canvas.create_line(self.valores, fill=self.cor_out)

    def desenhar_provisorio(self):
        if len(self.valores) > 1:
            return self.canvas.create_line(self.valores, fill=self.cor_out)


class Retangulo(Figura):
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


class Oval(Figura):
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


class Circulo(Figura):
    def desenhar(self):
        x1, y1 = self.valores[0], self.valores[1]
        x2, y2 = self.valores[2], self.valores[3]
        raio = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        self.canvas.create_oval(
            x1 - raio, y1 - raio,
            x1 + raio, y1 + raio,
            fill=self.cor_fill,
            outline=self.cor_out
        )

    def desenhar_provisorio(self):
        x1, y1 = self.valores[0], self.valores[1]
        x2, y2 = self.valores[2], self.valores[3]
        raio = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return self.canvas.create_oval(
            x1 - raio, y1 - raio,
            x1 + raio, y1 + raio,
            fill=self.cor_fill,
            outline=self.cor_out
        )


class Poligono(Figura):
    def desenhar(self):
        if len(self.valores) >= 6:
            self.canvas.create_polygon(
                self.valores, fill=self.cor_fill, outline=self.cor_out
            )

    def desenhar_provisorio(self):
        tag_temporaria = "temp_forma"
        self.canvas.delete(tag_temporaria)

        coords_vertices = self.valores[:-2]
        cursor_x, cursor_y = self.valores[-2], self.valores[-1]

        if len(coords_vertices) >= 4:
            self.canvas.create_line(coords_vertices, fill=self.cor_out, tag=tag_temporaria)

        if len(coords_vertices) >= 2:
            ultimo_x, ultimo_y = coords_vertices[-2], coords_vertices[-1]
            self.canvas.create_line(
                ultimo_x, ultimo_y, cursor_x, cursor_y,
                fill=self.cor_out, tag=tag_temporaria
            )

            p_inicio_x, p_inicio_y = coords_vertices[0], coords_vertices[1]
            distancia_fechamento = math.sqrt((cursor_x - p_inicio_x) ** 2 + (cursor_y - p_inicio_y) ** 2)

            if distancia_fechamento < 10:
                self.canvas.create_rectangle(
                    p_inicio_x - 5, p_inicio_y - 5, p_inicio_x + 5, p_inicio_y + 5,
                    outline="red", fill="white", tag=tag_temporaria
                )

        return tag_temporaria


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Paint POO Avançado Megatron3000")
        self.figuras = []
        self.tipo_atual = None
        self.valores_atual = []
        self.id_provisorio = None
        self.forma_em_andamento = False

        self.cor_fill = StringVar(self.root, value="")
        self.cor_out = StringVar(self.root, value="black")
        self.tipo_figura_var = StringVar(self.root, value="Rabisco")
        self.configurar_interface()
        self.configurar_eventos()

    def configurar_interface(self):
        toolbar = Frame(self.root, padding=5)
        toolbar.pack(side=TOP, fill=X)

        Label(toolbar, text="Forma: ").pack(side=LEFT, padx=5)

        seletor = OptionMenu(toolbar, self.tipo_figura_var, "Rabisco", "Rabisco", "Linha", "Retangulo", "Oval",
                             "Circulo", "Poligono")
        seletor.pack(side=LEFT, padx=5)

        btn_cor_out = Button(toolbar, text="Cor da Linha", command=self.escolher_cor_in)
        btn_cor_out.pack(side=LEFT, padx=5)

        btn_cor_in = Button(toolbar, text="Cor do Preenchimento", command=self.escolher_cor_out)
        btn_cor_in.pack(side=LEFT, padx=5)

        self.canvas = Canvas(self.root, bg="white", width=1440, height=800)
        self.canvas.pack(side=TOP, fill=BOTH, expand=True)

    def configurar_eventos(self):
        self.canvas.bind("<Button-1>", self.ao_clicar)
        self.canvas.bind("<B1-Motion>", self.ao_arrastar)
        self.canvas.bind("<ButtonRelease-1>", self.ao_soltar)
        self.canvas.bind("<Motion>", self.ao_mover)

    def escolher_cor_out(self):
        cor_in = colorchooser.askcolor(title="Escolha uma cor")
        if cor_in[1]:
            self.cor_fill.set(cor_in[1])

    def escolher_cor_in(self):
        cor_outl = colorchooser.askcolor(title="Escolha uma cor")
        if cor_outl[1]:
            self.cor_out.set(cor_outl[1])

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

    def ao_clicar(self, event):
        if self.tipo_figura_var.get() == "Poligono":
            if not self.forma_em_andamento:
                self.valores_atual = [event.x, event.y]
                self.forma_em_andamento = True
            else:
                p_inicio_x, p_inicio_y = self.valores_atual[0], self.valores_atual[1]
                distancia_fechamento = math.sqrt((event.x - p_inicio_x) ** 2 + (event.y - p_inicio_y) ** 2)

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

        classe = self.obter_figura_classe()

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

        classe = self.obter_figura_classe()

        if self.tipo_figura_var.get() == "Rabisco":
            self.valores_atual.append(event.x)
            self.valores_atual.append(event.y)
        else:
            self.valores_atual[2] = event.x
            self.valores_atual[3] = event.y

        figura = classe(self.canvas, self.valores_atual, self.cor_fill.get(), self.cor_out.get())
        figura.desenhar()
        self.figuras.append(figura)
        self.valores_atual = []


root = Tk()
app = App(root)
root.mainloop()
