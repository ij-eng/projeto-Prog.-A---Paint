from tkinter import *
from tkinter.ttk import *
from model import FormasModelo, Linha, Rabisco, Retangulo, Oval, Circulo, Poligono


class View:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Padrão MVC (Money Vem Cedo)")

        self.cor_fill_var = StringVar(self.root, value="")
        self.cor_out_var = StringVar(self.root, value="black")
        self.tipo_figura_var = StringVar(self.root, value="Rabisco")

        self.id_provisorio = None

        self.interface()
        self.configurar_eventos()

    def interface(self):
        toolbar = Frame(self.root, padding=5)
        toolbar.pack(side=TOP, fill=X)

        Label(toolbar, text="Forma: ").pack(side=LEFT, padx=5)

        seletor = OptionMenu(toolbar, self.tipo_figura_var, "Rabisco", "Rabisco", "Linha", "Retangulo", "Oval", "Circulo", "Poligono")
        seletor.pack(side=LEFT, padx=5)

        btn_cor_out = Button(toolbar, text="Cor da Linha", command=self.controller.escolher_cor_out)
        btn_cor_out.pack(side=LEFT, padx=5)
        btn_cor_in = Button(toolbar, text="Cor do Preenchimento", command=self.controller.escolher_cor_in)
        btn_cor_in.pack(side=LEFT, padx=5)
        btn_transparente = Button(toolbar, text="Tornar Transparente", command=self.controller.definir_transparente)
        btn_transparente.pack(side=LEFT, padx=5)

        self.canvas = Canvas(self.root, bg="white", width=1440, height=800)
        self.canvas.pack(side=TOP, fill=BOTH, expand=True)

    def configurar_eventos(self):
        self.canvas.bind("<Button-1>", self.controller.ao_clicar)
        self.canvas.bind("<B1-Motion>", self.controller.ao_arrastar)
        self.canvas.bind("<ButtonRelease-1>", self.controller.ao_soltar)
        self.canvas.bind("<Motion>", self.controller.ao_mover)
        self.tipo_figura_var.trace_add("write", self.atualizar_binding_duplo_clique)
        self.atualizar_binding_duplo_clique()

    def atualizar_binding_duplo_clique(self, *args):
        tipo = self.tipo_figura_var.get()
        if tipo == "Poligono":
            self.canvas.bind("<Double-Button-1>", self.controller.ao_duplo_clique)
        else:
            self.canvas.unbind("<Double-Button-1>")

    def deletar_provisorio(self):
        if self.id_provisorio:
            self.canvas.delete(self.id_provisorio)
            self.id_provisorio = None

    def obter_figura_classe(self):
        tipo = self.tipo_figura_var.get()
        classes = {
            "Linha": Linha,
            "Rabisco": Rabisco,
            "Retangulo": Retangulo,
            "Oval": Oval,
            "Circulo": Circulo,
            "Poligono": Poligono
        }
        return classes[tipo]

    def desenhar_definitivo(self, valores, cor_fill, cor_out):
        classe = self.obter_figura_classe()
        figura = classe(valores, cor_fill, cor_out)
        figura.desenhar(self.canvas)

    def desenhar_provisorio(self, valores, cor_fill, cor_out):
        self.deletar_provisorio()
        classe = self.obter_figura_classe()
        figura = classe(valores, cor_fill, cor_out)
        self.id_provisorio = figura.desenhar_provisorio(self.canvas)
