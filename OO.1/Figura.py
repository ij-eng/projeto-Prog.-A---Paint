from abc import ABC, abstractmethod

class Figura(ABC):
    def __init__(self, canvas, valores, cor_fill, cor_out):
        self.canvas = canvas
        self.valores = valores
        self.cor_fill = cor_fill
        self.cor_out = cor_out

    @abstractmethod
    def desenhar(self):
        pass

    @abstractmethod
    def desenhar_provisorio(self):
        pass