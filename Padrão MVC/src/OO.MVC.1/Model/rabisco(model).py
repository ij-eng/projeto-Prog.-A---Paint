class Rabisco(FormasModelo):
    def desenhar(self, canvas):
        if len(self.valores) > 1:
            return canvas.create_line(self.valores, fill=self.cor_out)
    def desenhar_provisorio(self, canvas):
        return self.desenhar(canvas)