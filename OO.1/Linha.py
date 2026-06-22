from Figura import *

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
            fill= self.cor_out
        )
