from tkinter import *
from tkinter.ttk import *


class View:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Top 10 melhores paints da atualidade") #O titulo do app

        self.cor_fill_var = StringVar(self.root, value="") #guarda a cor de preenchimento
        self.cor_out_var = StringVar(self.root, value="black") #guarda a cor da linha/borda
        self.tipo_figura_var = StringVar(self.root, value="Rabisco") #Guarda a figura selecionada OptionMenu

        self.interface()
        self.configurar_eventos()

    def interface(self):
        toolbar = Frame(self.root, padding=5)
        toolbar.pack(side=TOP, fill=X)

        Label(toolbar, text="Forma: ").pack(side=LEFT, padx=5) #Essas 3 primeiras parte da interface é para definir o lugar que fica os botões

        seletor = OptionMenu(toolbar, self.tipo_figura_var, "Rabisco", "Rabisco", "Linha", "Retangulo", "Oval",
                             "Circulo", "Poligono", "Poligono Regular", "Selecionar") #Menu de seleção de figuras e do modo selecionar
        seletor.pack(side=LEFT, padx=5)

        btn_cor_out = Button(toolbar, text="Cor da Linha/Borda", command=self.controller.escolher_cor_out) #escolher a cor da linha/borda
        btn_cor_out.pack(side=LEFT, padx=5)

        btn_cor_in = Button(toolbar, text="Cor Do Preenchimento", command=self.controller.escolher_cor_in) #escolher a cor de dentro da figura
        btn_cor_in.pack(side=LEFT, padx=5)

        btn_transparente = Button(toolbar, text="Tornar Transparente", command=self.controller.definir_transparente) #Mudar a cor de dentro para que seja transparente
        btn_transparente.pack(side=LEFT, padx=5)

        btn_salvar = Button(toolbar, text="Salvar", command=self.controller.salvar_arquivo) #salvar nos arquivos a sua bela pintura
        btn_salvar.pack(side=LEFT, padx=5)

        btn_abrir = Button(toolbar, text="Abrir", command=self.controller.abrir_arquivo) #Abrir dos arquivos a sua bela pintura selecionada
        btn_abrir.pack(side=LEFT, padx=5)

        self.canvas = Canvas(self.root, bg="white", width=1440, height=800) #tamanho do canva
        self.canvas.pack(side=TOP, fill=BOTH, expand=True)

    def configurar_eventos(self):
        self.canvas.bind("<Button-1>", self.controller.ao_clicar) #clique do mouse
        self.canvas.bind("<B1-Motion>", self.controller.ao_arrastar) #arrastar o mouse enquanto clicado
        self.canvas.bind("<ButtonRelease-1>", self.controller.ao_soltar) #quando solta o mose
        self.canvas.bind("<Motion>", self.controller.ao_mover) #mover sem o mouse clicado
        self.canvas.bind("<Double-Button-1>", self.controller.ao_duplo_clique) #clicar duas vezes para o poligono
        self.canvas.bind("<Button-3>", self.controller.ao_clique_direito) #clique direito do mouse para o poligono regular