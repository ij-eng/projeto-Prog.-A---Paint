from math import sqrt


class Model:
    def __init__(self):
        self.figuras = [] #salva as figuras desenhadas
        self.valores_atual = [] #guarda as coordenadas enquanto ta sendo arrastado o mouse para fazer a figura
        self.forma_em_andamento = False #serve para o poligono, para ver se ta sendo feito ainda
        self.id_provisorio = None #o tkinter da um id para cada figura que esta sendo desenhada, esse id_provisorio guarda isso
        self.figura_selecionada = None #guardar a figura que o usario clicou no modo selecionar
        self.figura_copiada = None #depois da figura selecionada o usuario clica no ctrl c e copia a figura

    def deletar_provisorio(self, canvas):
        if self.id_provisorio:
            canvas.delete(self.id_provisorio) #apaga a figura temporaria da tela usando o id
            self.id_provisorio = None #tira o id, pq n tem mais nenhuma figura provisoria la

    def desenhar_provisorio(self, canvas, classe_forma, valores, cor_fill, cor_out):
        self.deletar_provisorio(canvas)
        figura = classe_forma(valores, cor_fill, cor_out)
        self.id_provisorio = figura.desenhar_provisorio(canvas)

    def desenhar_definitivo(self, canvas, classe_forma, valores, cor_fill, cor_out):
        figura = classe_forma(valores, cor_fill, cor_out)
        figura.id_canvas = figura.desenhar(canvas) #desenha a forma real da figura e pega o id dela
        self.figuras.append(figura) #adiciona na lista de figuras, a bela figura feita pelo usuario

    #Procura na lista a figura selecionada
    def obter_figura_por_id(self, id_canvas):
        for figura in self.figuras:
            if figura.id_canvas == id_canvas:
                return figura
        return None

    #salva o seu desenho em forma de texto, salvando coordenadas das figuras desenhadas
    def salvar_para_txt(self, caminho):
        with open(caminho, 'w') as f:
            for figura in self.figuras:
                valores_str = ",".join(map(str, figura.valores))
                f.write(f"{type(figura).__name__}|{valores_str}|{figura.cor_fill}|{figura.cor_out}\n")

    def carregar_de_txt(self, caminho):
        self.figuras = [] #zera o desenho atual
        with open(caminho, 'r') as f: #abre o arquivo selecionado
            for linha in f:
                linha = linha.strip()
                if not linha: continue

                tipo, valores_str, cor_fill, cor_out = linha.split('|')
                valores = [float(x) if '.' in x else int(x) for x in valores_str.split(',')]

                classe_forma = globals().get(tipo) #vai pegando as formas pelo nome no txt

                if classe_forma and issubclass(classe_forma, FormasModelo):
                    figura = classe_forma(valores, cor_fill, cor_out)
                    self.figuras.append(figura) #adiciona tudo no canva

    def redesenhar_tudo(self, canvas):
        for figura in self.figuras:
            figura.id_canvas = figura.desenhar(canvas) #Pega as figuras desenhadas e manda elas irem para o canva

    def copiar_figura(self, figura):
        self.figura_copiada = type(figura)(figura.valores.copy(), figura.cor_fill, figura.cor_out) #copia a figura selecionada corretamente

    def colar_figura(self, canvas):
        if self.figura_copiada:
            self.figura_copiada.mover(10, 10) #deixa a copia em uma posição diferente do normal para ser selecionada melhor

            nova_figura = type(self.figura_copiada)(self.figura_copiada.valores.copy(),
                                                    self.figura_copiada.cor_fill,
                                                    self.figura_copiada.cor_out)

            nova_figura.id_canvas = nova_figura.desenhar(canvas)
            self.figuras.append(nova_figura) #coloca o clone na lista de figuras
            

class FormasModelo:
    def __init__(self, valores, cor_fill, cor_out):
        self.valores = valores  #as coordenadas x,y
        self.cor_fill = cor_fill  #cor de dentro
        self.cor_out = cor_out  #cor da borda
        self.id_canvas = None  #a identidade secreta da figura no canva

    def desenhar(self, canvas): pass

    def desenhar_provisorio(self, canvas): 
        return self.desenhar(canvas)

    #Procura na lista de valores as cordenadas e acrescenta o deslocamento
    def mover(self, dx, dy):
        for i in range(len(self.valores)):
            if i % 2 == 0:
                self.valores[i] += dx
            else:
                self.valores[i] += dy

    def mudar_cor_fill(self, canvas, cor):
        self.cor_fill = cor
        canvas.itemconfig(self.id_canvas, fill=cor) #pinta dentro da figura

    def mudar_cor_out(self, canvas, cor):
        self.cor_out = cor
        canvas.itemconfig(self.id_canvas, outline=cor) #pinta a linha da figura

    @staticmethod
    def distancia_ponto(x1, y1, x2, y2, px, py):
        dx = x2 - x1
        dy = y2 - y1
        ab_len_sq = dx ** 2 + dy ** 2

        if ab_len_sq == 0:
            return sqrt((px - x1) ** 2 + (py - y1) ** 2)

        ap_x = px - x1
        ap_y = py - y1
        t = (ap_x * dx + ap_y * dy) / ab_len_sq
        t = max(0.0, min(1.0, t))

        ponto_proximo_x = x1 + t * dx
        ponto_proximo_y = y1 + t * dy

        return sqrt((px - ponto_proximo_x) ** 2 + (py - ponto_proximo_y) ** 2)
    
    def distancia_figura(self, px, py): pass

    def esta_proximo(self, px, py, tolerancia):
        return self.distancia_figura(px, py) == 0.0

class Linha(FormasModelo):
    def desenhar(self, canvas):
        if len(self.valores) >= 4:
            return canvas.create_line(self.valores[0], self.valores[1], self.valores[2], self.valores[3], fill=self.cor_out)

    def mudar_cor_fill(self, canvas, cor): pass #a linha nao tem o preenchimento ent n faz nada

    def mudar_cor_out(self, canvas, cor):
        self.cor_out = cor
        canvas.itemconfig(self.id_canvas, fill=cor)

    def distancia_figura(self, px, py):
        valores = self.valores
        menor_dist = float('inf')
        for i in range(0, len(valores) - 2, 2):
            d = self.distancia_ponto(valores[i], valores[i + 1], valores[i + 2], valores[i + 3], px, py)
            if d < menor_dist:
                menor_dist = d
        return menor_dist
    
    def esta_proximo(self, px, py, tolerancia):
        return self.distancia_figura(px, py) < tolerancia


class Rabisco(FormasModelo):
    def desenhar(self, canvas):
        if len(self.valores) > 1:
            return canvas.create_line(self.valores, fill=self.cor_out)

    def mudar_cor_fill(self, canvas, cor): pass #mesma coisa da linha, n tem preenchimento

    def mudar_cor_out(self, canvas, cor):
        self.cor_out = cor
        canvas.itemconfig(self.id_canvas, fill=cor)

    def distancia_figura(self, px, py):
        valores = self.valores
        menor_dist = float('inf')
        for i in range(0, len(valores) - 2, 2):
            d = self.distancia_ponto(valores[i], valores[i + 1], valores[i + 2], valores[i + 3], px, py)
            if d < menor_dist:
                menor_dist = d
        return menor_dist
    
    def esta_proximo(self, px, py, tolerancia):
        return self.distancia_figura(px, py) < tolerancia


class Retangulo(FormasModelo):
    def desenhar(self, canvas):
        if len(self.valores) >= 4:
            return canvas.create_rectangle(self.valores[0], self.valores[1], self.valores[2], self.valores[3],
                                           fill=self.cor_fill, outline=self.cor_out) #cria retangulo

    def distancia_figura(self, px, py):
        valores = self.valores
        if len(valores) >= 4:
            x_min, x_max = min(valores[0], valores[2]), max(valores[0], valores[2])
            y_min, y_max = min(valores[1], valores[3]), max(valores[1], valores[3])
            if x_min <= px <= x_max and y_min <= py <= y_max:
                return 0.0
        return float("inf")


class Oval(FormasModelo):
    def desenhar(self, canvas):
        if len(self.valores) >= 4:
            return canvas.create_oval(self.valores[0], self.valores[1], self.valores[2], self.valores[3],
                                      fill=self.cor_fill, outline=self.cor_out) #cria oval

    def distancia_figura(self, px, py):
        valores = self.valores
        if len(valores) >= 4:
            x_min, x_max = min(valores[0], valores[2]), max(valores[0], valores[2])
            y_min, y_max = min(valores[1], valores[3]), max(valores[1], valores[3])
            if x_min <= px <= x_max and y_min <= py <= y_max:
                return 0.0
        return float("inf")


class Circulo(FormasModelo):
    def desenhar(self, canvas):
        if len(self.valores) >= 4:
            x1, y1, x2, y2 = self.valores[:4]
            raio = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            return canvas.create_oval(x1 - raio, y1 - raio, x1 + raio, y1 + raio, fill=self.cor_fill,
                                      outline=self.cor_out) #cria o circulo, q é um oval com regras corretas

    def distancia_figura(self, px, py):
        valores = self.valores
        if len(valores) >= 4:
            x1, y1, x2, y2 = valores[:4]
            raio = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            dist_centro = sqrt((px - x1) ** 2 + (py - y1) ** 2)
            if dist_centro <= raio:
                return 0.0
        return float("inf")


class Poligono(FormasModelo):
    def desenhar(self, canvas):
        if len(self.valores) >= 6:
            return canvas.create_polygon(self.valores, fill=self.cor_fill, outline=self.cor_out)

    def desenhar_provisorio(self, canvas):
        if len(self.valores) >= 4:
            return canvas.create_line(self.valores, fill=self.cor_out) #o desenho provisorio são linhas

    def distancia_figura(self, px, py):
        valores = self.valores
        pontos = [(valores[i], valores[i + 1]) for i in range(0, len(valores) - 1, 2)]
        n = len(pontos)
        if n < 3:
            return False
        dentro = False
        p1x, p1y = pontos[0]
        for i in range(n + 1):
            p2x, p2y = pontos[i % n]
            if py > min(p1y, p2y):
                if py <= max(p1y, p2y):
                    if px <= max(p1x, p2x):
                        x_interceptado = px
                        if p1y != p2y:
                            x_interceptado = (py - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or px <= x_interceptado:
                            dentro = not dentro
            p1x, p1y = p2x, p2y
        if dentro:
            return 0.0
        return float("inf")
