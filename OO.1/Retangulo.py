from Figura import *

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
            fill = self.cor_fill, outline= self.cor_out
        )