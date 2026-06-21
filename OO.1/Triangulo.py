from Figura import *

class Triangulo(Figura):
    def desenhar(self):
        topo = (self.valores[0]+self.valores[2])/2
        self.canvas.create_polygon(
            topo, self.valores[1],
            self.valores[2], self.valores[3],
            self.valores[0], self.valores[3],
            fill=self.cor_fill,
            outline=self.cor_out
        )


    def desenhar_provisorio(self):
        topo = (self.valores[0] + self.valores[2]) / 2
        return self.canvas.create_polygon(
            topo, self.valores[1],
            self.valores[2], self.valores[3],
            self.valores[0], self.valores[3],
            dash=(4,2),fill = self.cor_fill, outline= self.cor_out
        )