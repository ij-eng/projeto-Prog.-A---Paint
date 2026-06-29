class Model:
    def __init__(self):
        self.figuras = []
        self.valores_atual = []
        self.forma_em_andamento = False
        self.tipo_atual = "Rabisco"

    def incompleta(self):
        if len(self.valores_atual) < 4:
            return True

        if self.tipo_atual == "Rabisco":
            if len(self.valores_atual) == 4:
                return self.valores_atual[0] == self.valores_atual[2] and self.valores_atual[1] == self.valores_atual[3]
            return False
        return self.valores_atual[0] == self.valores_atual[2] and self.valores_atual[1] == self.valores_atual[3]
