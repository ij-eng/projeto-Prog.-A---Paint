from tkinter import *
from tkinter import ttk
import math


def iniciar_figura_nova(event):
    global figura_nova

    tipo = tipo_figura_var.get()

    if tipo == 'linha':
        figura_nova = ("linha", (event.x, event.y, event.x, event.y))

    elif tipo == 'rabisco':
        figura_nova = ("rabisco", [(event.x, event.y)])

    elif tipo == 'retangulo':
        figura_nova = ('retangulo', (event.x, event.y, event.x, event.y))

    elif tipo == 'oval':
        figura_nova = ('oval', (event.x, event.y, event.x, event.y))

    elif tipo == 'circulo':
        figura_nova = ('circulo',
                       (event.x, event.y,
                        event.x, event.y,
                        event.x, event.y))


def atualizar_figura_nova(event):
    global figura_nova

    if figura_nova is None:
        return

    elif figura_nova[0] == "rabisco":
        figura_nova[1].append((event.x, event.y))

    elif figura_nova[0] == "linha":
        figura_nova = (
            "linha",
            (figura_nova[1][0], figura_nova[1][1], event.x, event.y)
        )

    elif figura_nova[0] == "retangulo":
        figura_nova = (
            "retangulo",
            (figura_nova[1][0], figura_nova[1][1], event.x, event.y)
        )

    elif figura_nova[0] == "oval":
        figura_nova = (
            "oval",
            (figura_nova[1][0], figura_nova[1][1], event.x, event.y)
        )

    elif figura_nova[0] == 'circulo':
        x1, y1 = figura_nova[1][4], figura_nova[1][5]

        raio = math.sqrt(
            (event.x - x1) ** 2 +
            (event.y - y1) ** 2
        )

        figura_nova = (
            'circulo',
            (
                x1 - raio, y1 - raio,
                x1 + raio, y1 + raio,
                x1, y1
            )
        )

    desenhar_figuras()
    desenhar_figura_nova()


def incluir_figura_nova(event):
    global figura_nova

    if figura_nova and not incompleta(figura_nova):
        figuras.append(figura_nova)

    figura_nova = None
    desenhar_figuras()


def desenhar_figuras():
    canvas.delete("all")

    cor = cor_colocada.get()

    for fig, values in figuras:

        if fig == "linha":
            canvas.create_line(
                values[0], values[1],
                values[2], values[3],
                fill=cor
            )

        elif fig == "rabisco":
            canvas.create_line(values)

        elif fig == "retangulo":
            canvas.create_rectangle(
                values[0], values[1],
                values[2], values[3],
                fill=cor
            )

        elif fig == "oval":
            canvas.create_oval(
                values[0], values[1],
                values[2], values[3],
                fill=cor
            )

        elif fig == "circulo":
            canvas.create_oval(
                values[0], values[1],
                values[2], values[3],
                fill=cor
            )

    desenhar_figura_nova()


def desenhar_figura_nova():

    if figura_nova is None:
        return

    fig, values = figura_nova

    if fig == "linha":
        canvas.create_line(
            values[0], values[1],
            values[2], values[3],
            dash=(4, 2)
        )

    elif fig == "rabisco":
        canvas.create_line(values, dash=(4, 2))

    elif fig == "retangulo":
        canvas.create_rectangle(
            values[0], values[1],
            values[2], values[3]
        )

    elif fig == "oval":
        canvas.create_oval(
            values[0], values[1],
            values[2], values[3],
            dash=(4, 2)
        )

    elif fig == "circulo":
        canvas.create_oval(
            values[0], values[1],
            values[2], values[3],
            dash=(4, 2)
        )


def incompleta(figura):

    fig, values = figura

    if fig in ("linha", "retangulo", "oval"):
        return (values[0], values[1]) == (values[2], values[3])

    elif fig == "rabisco":
        return len(values) <= 1

    elif fig == "circulo":
        return values[0] == values[2] and values[1] == values[3]

    return False


figuras = []
figura_nova = None

root = Tk()

frame = Frame(root)

paddings = {'padx': 5, 'pady': 5}

label = ttk.Label(frame, text='Paint')
label.grid(column=0, row=0, sticky=W, **paddings)

tipo_figura_var = StringVar(root)

option_menu = ttk.OptionMenu(
    frame,
    tipo_figura_var,
    'linha',
    'linha',
    'rabisco',
    'retangulo',
    'oval',
    'circulo'
)

option_menu.grid(column=1, row=0, sticky=W, **paddings)

cor_colocada = StringVar(root)

cor_menu = ttk.OptionMenu(
    frame,
    cor_colocada,
    
    'black',
    'white',
    'red',
    'blue',
    'green',
    'yellow'
)

cor_menu.grid(row=0, column=2)

canvas = Canvas(frame, bg='white', width=600, height=600)
canvas.grid(column=0, row=1, columnspan=3, sticky=W, **paddings)

frame.pack()

canvas.bind('<ButtonPress-1>', iniciar_figura_nova)
canvas.bind('<B1-Motion>', atualizar_figura_nova)
canvas.bind('<ButtonRelease-1>', incluir_figura_nova)

root.mainloop()
