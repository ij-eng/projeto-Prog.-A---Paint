from tkinter import *
from tkinter.ttk import *
from tkinter import colorchooser
from Rabisco import *
from Linha import *
from Retangulo import *
from Oval import *
from Circulo import *
from Triangulo import *
from Losango import *
from Pentagono import *
from Hexagono import *
from Peixe import *

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Paint OO.1")
        self.figuras = []
        self.tipo_atual = None
        self.valores_atual = []
        self.id_provisorio = None
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
                             "Circulo", "Triangulo", "Losango","Pentagono","Hexagono","Peixe"
                             )
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
            "Triangulo": Triangulo,
            "Losango": Losango,
            "Pentagono": Pentagono,
            "Hexagono": Hexagono,
            "Peixe": Peixe
        }
        return classes[self.tipo_figura_var.get()]

    def ao_clicar(self, event):
        if self.tipo_figura_var.get() == "Rabisco":
            self.valores_atual = [event.x, event.y]
        else:
            self.valores_atual = [event.x, event.y, event.x, event.y]

    def ao_arrastar(self, event):
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