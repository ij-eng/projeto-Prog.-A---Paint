from tkinter import *
from tkinter import ttk
import math


def iniciar_figura_nova(event):
    global figura_nova

    tipo = tipo_figura_var.get()

    cor = cor_colocada.get()
    if cor == 'transparent':
        cor = ''

    if tipo == 'linha':
        figura_nova = ("linha", (event.x, event.y, event.x, event.y), cor)

    elif tipo == 'rabisco':
        figura_nova = ("rabisco", [(event.x, event.y)], cor)

    elif tipo == 'retangulo':
        figura_nova = ('retangulo', (event.x, event.y, event.x, event.y), cor)

    elif tipo == 'oval':
        figura_nova = ('oval', (event.x, event.y, event.x, event.y), cor)

    elif tipo == 'circulo':
        figura_nova = ('circulo',
                       (event.x, event.y,
                        event.x, event.y,
                        event.x, event.y), cor)


def atualizar_figura_nova(event):
    global figura_nova

    if figura_nova is None:
        return

    fig, values, cor = figura_nova

    if fig == "rabisco":
        values.append((event.x, event.y))

    elif fig == "linha":
        figura_nova = (
            "linha",
            (values[0], values[1], event.x, event.y),
            cor  # Repassamos a cor guardada
        )

    elif fig == "retangulo":
        figura_nova = (
            "retangulo",
            (values[0], values[1], event.x, event.y),
            cor
        )

    elif fig == "oval":
        figura_nova = (
            "oval",
            (values[0], values[1], event.x, event.y),
            cor
        )

    elif fig == 'circulo':
        x1, y1 = values[4], values[5]

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
            ),
            cor
        )

    desenhar_figuras()


def incluir_figura_nova(event):
    global figura_nova

    if figura_nova and not incompleta(figura_nova):
        figuras.append(figura_nova)

    figura_nova = None
    desenhar_figuras()


def desenhar_figuras():
    canvas.delete("all")

    for fig, values, cor_salva in figuras:

        if fig == "linha":
            canvas.create_line(
                values[0], values[1],
                values[2], values[3],
                fill=cor_salva if cor_salva else 'black'
            )

        elif fig == "rabisco":
            canvas.create_line(
                values,
                fill=cor_salva if cor_salva else 'black'
            )

        elif fig == "retangulo":
            canvas.create_rectangle(
                values[0], values[1],
                values[2], values[3],
                fill=cor_salva
            )

        elif fig == "oval":
            canvas.create_oval(
                values[0], values[1],
                values[2], values[3],
                fill=cor_salva
            )

        elif fig == "circulo":
            canvas.create_oval(
                values[0], values[1],
                values[2], values[3],
                fill=cor_salva
            )

    desenhar_figura_nova()


def desenhar_figura_nova():
    if figura_nova is None:
        return

    fig, values, cor = figura_nova

    if fig == "linha":
        canvas.create_line(
            values[0], values[1],
            values[2], values[3],
            dash=(4, 2), fill=cor if cor else "black"
        )

    elif fig == "rabisco":
        canvas.create_line(values, dash=(4, 2), fill=cor if cor else "black")

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
            dash=(4, 2), fill=cor
        )

    elif fig == "circulo":
        canvas.create_oval(
            values[0], values[1],
            values[2], values[3],
            dash=(4, 2), fill=cor
        )


def incompleta(figura):
    fig, values, cor = figura

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
root.title("Paint Simples")

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
    'transparent',
    'transparent',
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
