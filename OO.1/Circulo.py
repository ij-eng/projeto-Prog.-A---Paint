from Figura import *
from math import sqrt

class Circulo(Figura):
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
            fill = self.cor_fill,
            outline= self.cor_out
        )
