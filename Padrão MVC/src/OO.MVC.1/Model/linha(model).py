class Linha(FormasModelo):
    def desenhar(self, canvas):
        return canvas.create_line(
            self.valores[0], self.valores[1],
            self.valores[2], self.valores[3],
            fill=self.cor_out
        )
    def desenhar_provisorio(self, canvas):
        return self.desenhar(canvas)


