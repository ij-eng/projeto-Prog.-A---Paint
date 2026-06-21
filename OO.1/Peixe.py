from Figura import *

class Peixe(Figura):
    def desenhar(self):
        x1, y1 = self.valores[0], self.valores[1]
        x2, y2 = self.valores[2], self.valores[3]
        x_mid = (x1 + x2) / 2
        largura = x2 - x1
        altura = y2 - y1
        x_base1 = x1 + largura * 0.15
        x_base2 = x1 + largura * 0.85
        y_alt = y1 + altura * 0.4
        self.canvas.create_polygon(
            x_mid, y1, x2, y_alt, x_base1, y2, x_base2, y2, x1, y_alt,
            fill=self.cor_fill, outline=self.cor_out
        )
    def desenhar_provisorio(self):
        x1, y1 = self.valores[0], self.valores[1]
        x2, y2 = self.valores[2], self.valores[3]
        x_mid = (x1 + x2) / 2
        largura = x2 - x1
        altura = y2 - y1
        x_base1 = x1 + largura * 0.15
        x_base2 = x1 + largura * 0.85
        y_alt = y1 + altura * 0.4
        return self.canvas.create_polygon(
            x_mid, y1, x2, y_alt, x_base1, y2, x_base2, y2, x1, y_alt,
            dash=(4, 2), fill=self.cor_fill, outline=self.cor_out
        )