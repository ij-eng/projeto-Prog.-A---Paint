from math import sqrt, atan2, pi, cos, sin


class Model:
    def __init__(self):
        self.figuras = [] #salva as figuras desenhadas
        self.valores_atual = [] #guarda as coordenadas de enquanto o mouse ta sendo arrastado
        self.forma_em_andamento = False #serve principalmente para os poligonos, para checar se ainda esta sendo feito
        self.id_provisorio = None #guarda o id que o tkinter da para cada figura
        self.figura_selecionada = None
        self.figura_copiada = [] #guarda a figura que foi copiada
        self.figuras_selecionadas = [] #guarda as figuras que foram selecionadas
        self.undo_pilha = [] #guarda tudo do canvas para conseguir voltar
        self.redo_pilha = [] #guarda tudo do canvas para conseguir ir para o estado mais avançado

    def salvar_estado(self):
        self.redo_pilha.clear()
        #clona cada figura individualmente para guardar as coordenadas antigas exatas
        figuras_clonadas = [fig.clonar() for fig in self.figuras]
        
        #mapeia as selecionadas para as novas instâncias clonadas
        selecionadas_clonadas = []
        for fig in self.figuras_selecionadas:
            if fig in self.figuras:
                idx = self.figuras.index(fig)
                selecionadas_clonadas.append(figuras_clonadas[idx])

        estado_atual = {
            'figuras': figuras_clonadas,
            'selecionadas': selecionadas_clonadas
        }
        self.undo_pilha.append(estado_atual)

    def undo(self):
        if not self.undo_pilha:
            return False

        #guarda o estado atual no Redo antes de voltar (também clonando)
        figuras_clonadas = [fig.clonar() for fig in self.figuras]
        selecionadas_clonadas = []
        for fig in self.figuras_selecionadas:
            if fig in self.figuras:
                idx = self.figuras.index(fig)
                selecionadas_clonadas.append(figuras_clonadas[idx])

        estado_atual = {
            'figuras': figuras_clonadas,
            'selecionadas': selecionadas_clonadas
        }
        self.redo_pilha.append(estado_atual)

        #restaura o estado anterior
        ultimo_estado = self.undo_pilha.pop()
        self.figuras = ultimo_estado['figuras']
        self.figuras_selecionadas = ultimo_estado['selecionadas']
        return True
    
    def redo(self):
        if not self.redo_pilha:
            return False
            
        #guarda o estado atual no Undo (também clonando)
        figuras_clonadas = [fig.clonar() for fig in self.figuras]
        selecionadas_clonadas = []
        for fig in self.figuras_selecionadas:
            if fig in self.figuras:
                idx = self.figuras.index(fig)
                selecionadas_clonadas.append(figuras_clonadas[idx])

        estado_atual = {
            'figuras': figuras_clonadas,
            'selecionadas': selecionadas_clonadas
        }
        self.undo_pilha.append(estado_atual)

        #restaura o próximo estado tirando da redo_pilha
        proximo_estado = self.redo_pilha.pop()
        self.figuras = proximo_estado['figuras']
        self.figuras_selecionadas = proximo_estado['selecionadas']
        return True
    
    def deletar_provisorio(self, canvas):
        if self.id_provisorio:
            canvas.delete(self.id_provisorio) #usa o id para apagar a figura temporaria da tela
            self.id_provisorio = None

    def desenhar_provisorio(self, canvas, classe_forma, valores, cor_fill, cor_out):
        self.deletar_provisorio(canvas)
        figura = classe_forma(valores, cor_fill, cor_out)
        self.id_provisorio = figura.desenhar_provisorio(canvas) 

    def desenhar_definitivo(self, canvas, classe_forma, valores, cor_fill, cor_out):
        self.salvar_estado()
        figura = classe_forma(valores, cor_fill, cor_out)
        figura.id_canvas = figura.desenhar(canvas)
        self.figuras.append(figura)  #desenha a forma real da figura e pega o id dela e adiciona ela na lista de figuras

    def obter_figura_por_id(self, id_canvas):
        for figura in self.figuras: #procura na lista a figura selecionada e se for uma figura composta ela vai ter o id procura dos componentes
            if id_canvas in figura.obter_ids_canvas():
                return figura
        return None

    def salvar_para_txt(self, caminho): #salva o desenho em formato de texto com o nome e coordenadas das figuras desenhadas
        with open(caminho, 'w') as f:
            for figura in self.figuras:
                self.salvar_recursivo(f, figura)

    def salvar_recursivo(self, f, figura): #vai passar pela lista e entender qual tipo de figura é aquilo, se é uma figura normal ou uma composta
        if isinstance(figura, FiguraComposta):
            f.write(f"InicioGrupo|{figura.cor_fill}|{figura.cor_out}\n")
            for sub_fig in figura.figuras_componentes:
                self.salvar_recursivo(f, sub_fig)
            f.write("FimGrupo\n")
        else:
            valores_str = ",".join(map(str, figura.valores))
            f.write(f"{type(figura).__name__}|{valores_str}|{figura.cor_fill}|{figura.cor_out}\n")

    def carregar_de_txt(self, caminho): #apaga as coisas do canvas e bota as registradas no arquivo txt de escolha do usuario
        self.figuras = []
        self.undo_pilha.clear()
        self.redo_pilha.clear()
        with open(caminho, 'r') as f:
            linhas = [linha.strip() for i in f if (linha := i.strip())]
        self.figuras = self.carregar_linhas_recursivo(linhas)

    def carregar_linhas_recursivo(self, linhas): #ele checa se a figura desenhada é composta ou não, atravas do InicioGrupo e FimGrupo
        figuras_carregadas = []
        while linhas:
            linha = linhas.pop(0)
            if linha == "FimGrupo":
                break

            partes = linha.split('|')
            tipo = partes[0]

            if tipo == "InicioGrupo":
                cor_fill = partes[1]
                cor_out = partes[2]
                componentes = self.carregar_linhas_recursivo(linhas)
                grupo = FiguraComposta(componentes, cor_fill, cor_out)
                figuras_carregadas.append(grupo)
            else:
                tipo, valores_str, cor_fill, cor_out = partes
                valores = [float(x) if '.' in x else int(x) for x in valores_str.split(',')]
                classe_forma = globals().get(tipo)
                if classe_forma and issubclass(classe_forma, FormasModelo):
                    figura = classe_forma(valores, cor_fill, cor_out)
                    figuras_carregadas.append(figura)
        return figuras_carregadas

    def redesenhar_tudo(self, canvas): #serve para o carregar_de_txt
        for figura in self.figuras:
            figura.id_canvas = figura.desenhar(canvas)

    def copiar_figura(self): #adiciona a figura na lista de copiadas e tbm usa o metodo clonar nela
        self.figura_copiada = []
        for figura in self.figuras_selecionadas:
            self.figura_copiada.append(figura.clonar())

    def colar_figura(self, canvas): 
        if not self.figura_copiada:
            return

        self.salvar_estado()
        for fig in self.figuras_selecionadas:
            fig.destacar(canvas, False)
        self.figuras_selecionadas.clear()

        novas_copias = []

        for figura in self.figura_copiada:
            nova_figura = figura.clonar()
            nova_figura.mover(canvas, 20, 20)
            nova_figura.id_canvas = nova_figura.desenhar(canvas)
            self.figuras.append(nova_figura)
            self.figuras_selecionadas.append(nova_figura)
            nova_figura.destacar(canvas, True)
            novas_copias.append(nova_figura)

        self.figura_selecionada = self.figuras_selecionadas[-1] if self.figuras_selecionadas else None
        self.figura_copiada = []
        for fig in novas_copias:
            self.figura_copiada.append(fig.clonar())


class FormasModelo:
    def __init__(self, valores, cor_fill, cor_out):
        self.valores = valores #as coordenadas x,y
        self.cor_fill = cor_fill
        self.cor_out = cor_out
        self.id_canvas = None #a identidade secreta da figura no canvas

    def clonar(self): #faz o deep copy da forma
        return self.__class__(list(self.valores), self.cor_fill, self.cor_out)

    def obter_ids_canvas(self): #retorna uma lista com todos os ids do canvas associados com a figura
        return [self.id_canvas] if self.id_canvas else []

    def desenhar(self, canvas): pass

    def desenhar_provisorio(self, canvas):
        return self.desenhar(canvas)

    def mover(self, canvas, dx, dy): #procura na lista de coordenadas os valores e vai acrescentando ou diminuindo eles conforme o usuario vai movendo
        for i in range(len(self.valores)):
            if i % 2 == 0:
                self.valores[i] += dx
            else:
                self.valores[i] += dy
        if self.id_canvas:
            canvas.move(self.id_canvas, dx, dy)

    def destacar(self, canvas, ativo=True): #serve para destacar a figura quando selecionada
        if self.id_canvas:
            largura = 3 if ativo else 1
            canvas.itemconfig(self.id_canvas, width=largura)

    def deletar_do_canvas(self, canvas): #serve para deletar uma figura do canvas e da lista
        if self.id_canvas:
            canvas.delete(self.id_canvas)

    def mudar_cor_fill(self, canvas, cor):
        self.cor_fill = cor
        if self.id_canvas:
            canvas.itemconfig(self.id_canvas, fill=cor)

    def mudar_cor_out(self, canvas, cor):
        self.cor_out = cor
        if self.id_canvas:
            canvas.itemconfig(self.id_canvas, outline=cor)

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

    def dentro(self, px, py): pass

    def foi_clicada(self, px, py, tolerancia):  #serve para checar se a figura foi ou não clicada, se o clique for dentro ou proximo da figura (linha e rabisco) essa função verifica isso.
        return self.dentro(px, py) < tolerancia
    
    def obter_limites(self): 
        if not self.valores:
            return None
    
        xs = self.valores[0::2]
        ys = self.valores[1::2]
        return min(xs), min(ys), max(xs), max(ys)

class Linha(FormasModelo):
    def desenhar(self, canvas):
        if len(self.valores) >= 4:
            return canvas.create_line(self.valores[0], self.valores[1], self.valores[2], self.valores[3],
                                      fill=self.cor_out)

    def mudar_cor_fill(self, canvas, cor): pass

    def mudar_cor_out(self, canvas, cor):
        self.cor_out = cor
        if self.id_canvas:
            canvas.itemconfig(self.id_canvas, fill=cor)

    def dentro(self, px, py):
        valores = self.valores
        menor_dist = float('inf')
        for i in range(0, len(valores) - 2, 2):
            d = self.distancia_ponto(valores[i], valores[i + 1], valores[i + 2], valores[i + 3], px, py)
            if d < menor_dist:
                menor_dist = d
        return menor_dist


class Rabisco(FormasModelo):
    def desenhar(self, canvas):
        if len(self.valores) > 1:
            return canvas.create_line(self.valores, fill=self.cor_out)

    def mudar_cor_fill(self, canvas, cor): pass

    def mudar_cor_out(self, canvas, cor):
        self.cor_out = cor
        if self.id_canvas:
            canvas.itemconfig(self.id_canvas, fill=cor)

    def dentro(self, px, py):
        valores = self.valores
        menor_dist = float('inf')
        for i in range(0, len(valores) - 2, 2):
            d = self.distancia_ponto(valores[i], valores[i + 1], valores[i + 2], valores[i + 3], px, py)
            if d < menor_dist:
                menor_dist = d
        return menor_dist


class Retangulo(FormasModelo):
    def desenhar(self, canvas):
        if len(self.valores) >= 4:
            return canvas.create_rectangle(self.valores[0], self.valores[1], self.valores[2], self.valores[3],
                                           fill=self.cor_fill, outline=self.cor_out)

    def dentro(self, px, py):
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
                                      fill=self.cor_fill, outline=self.cor_out)

    def dentro(self, px, py):
        valores = self.valores
        if len(valores) >= 4:
            x_min, x_max = min(valores[0], valores[2]), max(valores[0], valores[2])
            y_min, y_max = min(valores[1], valores[3]), max(valores[1], valores[3])
            if x_min <= px <= x_max and y_min <= py <= y_max:
                return 0.0
        return float("inf")
    
    def obter_limites(self):
        if len(self.valores) < 4:
            return None
            
        x1, y1, x2, y2 = self.valores[:4]
        
        x_min = min(x1, x2)
        y_min = min(y1, y2)
        x_max = max(x1, x2)
        y_max = max(y1, y2)
        
        return x_min, y_min, x_max, y_max


class Circulo(FormasModelo):
    def desenhar(self, canvas):
        if len(self.valores) >= 4:
            x1, y1, x2, y2 = self.valores[:4]
            raio = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            return canvas.create_oval(x1 - raio, y1 - raio, x1 + raio, y1 + raio, fill=self.cor_fill,
                                      outline=self.cor_out)

    def dentro(self, px, py):
        valores = self.valores
        if len(valores) >= 4:
            x1, y1, x2, y2 = valores[:4]
            raio = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            dist_centro = sqrt((px - x1) ** 2 + (py - y1) ** 2)
            if dist_centro <= raio:
                return 0.0
        return float("inf")
    
    def obter_limites(self):
        if len(self.valores) < 4:
            return None
            
        x1, y1, x2, y2 = self.valores[:4]
        
        raio = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
        x_min = x1 - raio
        y_min = y1 - raio
        x_max = x1 + raio
        y_max = y1 + raio
        
        return x_min, y_min, x_max, y_max

class Poligono(FormasModelo):
    def desenhar(self, canvas):
        if len(self.valores) >= 6:
            return canvas.create_polygon(self.valores, fill=self.cor_fill, outline=self.cor_out)

    def desenhar_provisorio(self, canvas):
        if len(self.valores) >= 4:
            return canvas.create_line(self.valores, fill=self.cor_out)

    def dentro(self, px, py):
        valores = self.valores
        pontos = [(valores[i], valores[i + 1]) for i in range(0, len(valores) - 1, 2)]
        n = len(pontos)
        if n < 3:
            return float("inf")
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


class PoligonoRegular(Poligono):
    def desenhar_provisorio(self, canvas):
        if len(self.valores) < 5:
            return None

        cx, cy, mx, my, num_lados = self.valores
        num_lados = int(num_lados)

        dx = mx - cx
        dy = my - cy
        raio = sqrt(dx ** 2 + dy ** 2)

        tag = "provisorio_poligono_regular"

        canvas.create_oval(cx - raio, cy - raio, cx + raio, cy + raio,
                           outline="black", dash=(4, 4), tags=tag)

        angulo_inicial = atan2(dy, dx)
        pontos = []
        for i in range(num_lados):
            ang = angulo_inicial + i * (2 * pi / num_lados)
            px = cx + raio * cos(ang)
            py = cy + raio * sin(ang)
            pontos.extend([px, py])

        canvas.create_polygon(pontos, fill=self.cor_fill, outline=self.cor_out, tags=tag)
        return tag


class FiguraComposta(FormasModelo):
    def __init__(self, figuras_componentes, cor_fill="", cor_out="black"):
        super().__init__([], cor_fill, cor_out)
        self.figuras_componentes = figuras_componentes
        self.atualizar_valores_compostos()

    def atualizar_valores_compostos(self):
        self.valores = []
        for fig in self.figuras_componentes:
            self.valores.extend(fig.valores)

    def clonar(self):
        componentes_clonados = [fig.clonar() for fig in self.figuras_componentes]
        return FiguraComposta(componentes_clonados, self.cor_fill, self.cor_out)

    def obter_ids_canvas(self):
        ids = []
        for fig in self.figuras_componentes:
            ids.extend(fig.obter_ids_canvas())
        return ids

    def desenhar(self, canvas):
        for figura in self.figuras_componentes:
            figura.id_canvas = figura.desenhar(canvas)
        return self.figuras_componentes[0].id_canvas if self.figuras_componentes else None

    def mover(self, canvas, dx, dy):
        for figura in self.figuras_componentes:
            figura.mover(canvas, dx, dy)
        self.atualizar_valores_compostos()

    def destacar(self, canvas, ativo=True):
        for figura in self.figuras_componentes:
            figura.destacar(canvas, ativo)

    def deletar_do_canvas(self, canvas):
        for figura in self.figuras_componentes:
            figura.deletar_do_canvas(canvas)

    def mudar_cor_fill(self, canvas, cor):
        self.cor_fill = cor
        for figura in self.figuras_componentes:
            figura.mudar_cor_fill(canvas, cor)

    def mudar_cor_out(self, canvas, cor):
        self.cor_out = cor
        for figura in self.figuras_componentes:
            figura.mudar_cor_out(canvas, cor)

    def dentro(self, px, py):
        menor_dist = float('inf')
        for figura in self.figuras_componentes:
            d = figura.dentro(px, py)
            if d < menor_dist:
                menor_dist = d
        return menor_dist
    
    def obter_limites(self):
        
        x_mins = []
        y_mins = []
        x_maxs = []
        y_maxs = []
        
        for fig in self.figuras_componentes:
            limites = fig.obter_limites()
            if limites:
                x_mins.append(limites[0])
                y_mins.append(limites[1])
                x_maxs.append(limites[2])
                y_maxs.append(limites[3])
        
            
        return min(x_mins), min(y_mins), max(x_maxs), max(y_maxs)
