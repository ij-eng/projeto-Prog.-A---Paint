from tkinter import *
from tkinter.ttk import *
import math
from tkinter import colorchooser

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
        c_fill = cor_fill.get()
        if c_fill == 'transparent':
            c_fill = ''
        figuras.append((figura_nova, c_fill, cor_out.get()))

    figura_nova = None
    desenhar_figuras()


def desenhar_figuras():
    canvas.delete("all")
    for item_figura, cor1, cor2 in figuras:
        fig, values = item_figura

        if fig == "linha":
            canvas.create_line(
                values[0], values[1],
                values[2], values[3],
                fill=cor2
            )

        elif fig == "rabisco":
            canvas.create_line(values, fill=cor2)

        elif fig == "retangulo":
            canvas.create_rectangle(
                values[0], values[1],
                values[2], values[3],
                fill=cor1,
                outline=cor2
            )

        elif fig == "oval":
            canvas.create_oval(
                values[0], values[1],
                values[2], values[3],
                fill=cor1,
                outline=cor2
            )

        elif fig == "circulo":
            canvas.create_oval(
                values[0], values[1],
                values[2], values[3],
                fill=cor1,
                outline=cor2
            )


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


def escolher_cor_in():
    cor_in = colorchooser.askcolor(title="Escolha uma cor")
    if cor_in[1]:
        cor_hex = cor_in[1]
        cor_fill.set(cor_hex)

def escolher_cor_out():
    cor_outl= colorchooser.askcolor(title="Escolha uma cor")
    if cor_outl[1]:
        cor_hex = cor_outl[1]
        cor_out.set(cor_hex)

figuras = []
figura_nova = None

root = Tk()

cor_fill = StringVar(root, value="transparent")
cor_out = StringVar(root, value="black")

frame = Frame(root)

paddings = {'padx': 5, 'pady': 5}

label = Label(frame, text='Paint')
label.grid(column=0, row=0, sticky=W, **paddings)

tipo_figura_var = StringVar(root)

option_menu = OptionMenu(
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

botao1= Button(frame, text="Cor do preenchimento", command=escolher_cor_in)
botao1.grid(column=2, row=0, sticky=W, **paddings)
botao2= Button(frame, text="Cor da linha", command=escolher_cor_out)
botao2.grid(column=3, row=0, sticky=W, **paddings)

canvas = Canvas(frame, bg='white', width=1440, height=800)
canvas.grid(column=0, row=1, columnspan=4, sticky=W, **paddings)

frame.pack()

canvas.bind('<ButtonPress-1>', iniciar_figura_nova)
canvas.bind('<B1-Motion>', atualizar_figura_nova)
canvas.bind('<ButtonRelease-1>', incluir_figura_nova)

root.mainloop()
