from Figura import *


class Hexagono(Figura):
    def desenhar(self):
        x1, y1 = self.valores[0], self.valores[1]
        x2, y2 = self.valores[2], self.valores[3]
        largura = x2 - x1
        y_m = (y1 + y2) / 2
        x_um_quarto = x1 + largura * 0.25
        x_tres_quartos = x1 + largura * 0.75
        self.canvas.create_polygon(
            x_um_quarto, y1, x_tres_quartos, y1, x2, y_m, x_tres_quartos, y2, x_um_quarto, y2, x1, y_m,
            fill=self.cor_fill, outline=self.cor_out
        )

    def desenhar_provisorio(self):
        x1, y1 = self.valores[0], self.valores[1]
        x2, y2 = self.valores[2], self.valores[3]
        largura = x2 - x1
        y_mid = (y1 + y2) / 2
        x_um_quarto = x1 + largura * 0.25
        x_tres_quartos = x1 + largura * 0.75
        return self.canvas.create_polygon(
            x_um_quarto, y1, x_tres_quartos, y1, x2, y_mid, x_tres_quartos, y2, x_um_quarto, y2, x1, y_mid,
            fill=self.cor_fill, outline=self.cor_out
        )
