class Circulo(FormasModelo):
    def desenhar(self, canvas):
        x1, y1, x2, y2 = self.valores[0], self.valores[1], self.valores[2], self.valores[3]
        raio = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return canvas.create_oval(
            x1 - raio, y1 - raio,
            x1 + raio, y1 + raio,
            fill=self.cor_fill, outline=self.cor_out
        )
    def desenhar_provisorio(self, canvas):
        return self.desenhar(canvas)


