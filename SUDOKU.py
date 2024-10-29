import tkinter as tk
from tkinter import messagebox, simpledialog
import numpy as np
import random

# Crear el tablero de Sudoku (9x9) con valores iniciales usando numpy
def crear_tablero():
    tablero = np.zeros((9, 9), dtype=int)
    llenar_casillas_aleatorias(tablero)
    return tablero

# Llenar algunas casillas aleatoriamente con números del 1 al 9
def llenar_casillas_aleatorias(tablero, cantidad=30):
    for _ in range(cantidad):
        fila, columna = random.randint(0, 8), random.randint(0, 8)
        while tablero[fila, columna] != 0:
            fila, columna = random.randint(0, 8), random.randint(0, 8)
        num = random.randint(1, 9)
        if es_valido(tablero, fila, columna, num):
            tablero[fila, columna] = num

# Verificar si un número puede ser colocado en una casilla específica
def es_valido(tablero, fila, columna, num):
    # Verificar la fila, columna y subcuadrícula 3x3 usando numpy
    if num in tablero[fila, :]: 
        return False
    if num in tablero[:, columna]:  
        return False
    # Validar subcuadrícula 3x3
    fila_inicio, columna_inicio = 3 * (fila // 3), 3 * (columna // 3)
    if num in tablero[fila_inicio:fila_inicio + 3, columna_inicio:columna_inicio + 3]:
        return False
    return True

# Comprobar si el tablero está completo y cumple con las reglas
def es_completo(tablero):
    for fila in range(9):
        for columna in range(9):
            if tablero[fila, columna] == 0 or not es_valido(tablero, fila, columna, tablero[fila, columna]):
                return False
    return True

# Insertar número en la casilla seleccionada
def insertar_numero(event, fila, columna):
    if tablero[fila, columna] == 0:
        num = simpledialog.askinteger("Entrada", f"Inserta un número (1-9) para la posición ({fila + 1}, {columna + 1})")
        if num and 1 <= num <= 9:
            if es_valido(tablero, fila, columna, num):
                tablero[fila, columna] = num
                celdas[fila][columna].config(state='normal')
                celdas[fila][columna].delete(0, tk.END)
                celdas[fila][columna].insert(0, str(num))
                celdas[fila][columna].config(state='disabled')
                if es_completo(tablero):
                    messagebox.showinfo("¡Felicidades!", "¡Has completado el Sudoku!")
            else:
                messagebox.showerror("Error", "Número no válido para esta posición.")
        else:
            messagebox.showerror("Error", "Por favor, inserta un número entre 1 y 9.")


def crear_interfaz():
    ventana = tk.Tk()
    ventana.title("Sudoku")

    global celdas, tablero
    celdas = [[None] * 9 for _ in range(9)]
    tablero = crear_tablero()
    for fila_subgrid in range(3):
            for columna_subgrid in range(3):
                subgrid_frame = tk.Frame(
                    ventana,
                    bg="black", 
                    highlightbackground="black",
                    highlightthickness=2 
                )
                subgrid_frame.grid(row=fila_subgrid * 3, column=columna_subgrid * 3, 
                                rowspan=3, columnspan=3, padx=1, pady=1)
                for i in range(3):
                    for j in range(3):
                        fila = fila_subgrid * 3 + i
                        columna = columna_subgrid * 3 + j
                        celda = tk.Entry(
                            subgrid_frame,
                            width=3,
                            font=('Arial', 18),
                            justify='center',
                            relief="solid",
                            bd=1
                        )
                        celda.grid(row=i, column=j)
                        if tablero[fila, columna] != 0:
                            celda.insert(0, str(tablero[fila, columna]))
                            celda.config(state='disabled', disabledforeground='black')
                        else:
                            celda.config(state='disabled')
                            celda.bind("<Button-1>", lambda event, r=fila, c=columna: insertar_numero(event, r, c))
                        celdas[fila][columna] = celda

    ventana.mainloop()

    


crear_interfaz()
