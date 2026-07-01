class Retangulo(FormasModelo):
    def desenhar(self, canvas):
        return canvas.create_rectangle(
            self.valores[0], self.valores[1],
            self.valores[2], self.valores[3],
            fill=self.cor_fill, outline=self.cor_out
        )
    def desenhar_provisorio(self, canvas):
        return self.desenhar(canvas)