class Poligono(FormasModelo):
    def desenhar(self, canvas):
        if len(self.valores) >= 4:
            return canvas.create_polygon(
                self.valores,
                fill=self.cor_fill, outline=self.cor_out
            )
    def desenhar_provisorio(self, canvas):
        if len(self.valores) >= 4:
            return canvas.create_line(self.valores, fill=self.cor_out)