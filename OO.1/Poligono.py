from Figura import *
from math import sqrt

class Poligono(Figura):
    def desenhar(self):
        if len(self.valores) >= 6:
            self.canvas.create_polygon(
                self.valores, fill=self.cor_fill, outline=self.cor_out
            )

    def desenhar_provisorio(self):
        tag_temporaria = "temp_forma"
        self.canvas.delete(tag_temporaria)

        coords_vertices = self.valores[:-2]
        cursor_x, cursor_y = self.valores[-2], self.valores[-1]

        if len(coords_vertices) >= 4:
            self.canvas.create_line(coords_vertices, fill=self.cor_out, tag=tag_temporaria)

        if len(coords_vertices) >= 2:
            ultimo_x, ultimo_y = coords_vertices[-2], coords_vertices[-1]
            self.canvas.create_line(
                ultimo_x, ultimo_y, cursor_x, cursor_y,
                fill=self.cor_out, tag=tag_temporaria
            )

            p_inicio_x, p_inicio_y = coords_vertices[0], coords_vertices[1]
            distancia_fechamento = sqrt((cursor_x - p_inicio_x) ** 2 + (cursor_y - p_inicio_y) ** 2)

            if distancia_fechamento < 10:
                self.canvas.create_oval(
                    p_inicio_x - 5, p_inicio_y - 5, p_inicio_x + 5, p_inicio_y + 5,
                    outline="red", fill="white", tag=tag_temporaria
                )

        return tag_temporaria
