from Figura import *

class Rabisco(Figura):
    def desenhar(self):
        if len(self.valores) > 1:
            self.canvas.create_line(self.valores, fill=self.cor_out)

    def desenhar_provisorio(self):
        if len(self.valores) > 1:
            return self.canvas.create_line(self.valores, dash=(4, 2), fill=self.cor_out)