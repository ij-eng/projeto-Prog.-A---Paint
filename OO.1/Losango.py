from Figura import *

class Losango(Figura):
    def desenhar(self):
        x1, y1 = self.valores[0], self.valores[1]
        x2, y2 = self.valores[2], self.valores[3]
        x_m = (x1 + x2) / 2
        y_m = (y1 + y2) / 2
        self.canvas.create_polygon(
            x_m, y1, x2, y_m, x_m, y2, x1, y_m,
            fill=self.cor_fill, outline=self.cor_out
        )

    def desenhar_provisorio(self):
        x1, y1 = self.valores[0], self.valores[1]
        x2, y2 = self.valores[2], self.valores[3]
        x_m = (x1 + x2) / 2
        y_m = (y1 + y2) / 2
        return self.canvas.create_polygon(
            x_m, y1, x2, y_m, x_m, y2, x1, y_m,
            dash=(4, 2), fill = self.cor_fill, outline= self.cor_out
        )