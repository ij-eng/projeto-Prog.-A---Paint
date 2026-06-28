class Model:
    def __init__(self):
        self.figuras = []
        self.tipo_atual = "Rabisco"
        self.valores_atual = []
        self.cor_fill = ""
        self.cor_out = "black"
        self.forma_em_andamento = False

    def incompleta(self):
        if self.tipo_atual == "Rabisco":
            return len(self.valores_atual) <= 4 and self.valores_atual[0] == self.valores_atual[2] and \
                self.valores_atual[1] == self.valores_atual[3]
        return self.valores_atual[0] == self.valores_atual[2] and self.valores_atual[1] == self.valores_atual[3]
