import tkinter as tk
from tkinter import messagebox, simpledialog
import numpy as np
import random

# Crear el tablero de Sudoku completo y válido
def crear_tablero():
    tablero = np.zeros((9, 9), dtype=int)
    resolver_sudoku(tablero)
    return tablero

# Resolver el tablero de Sudoku usando backtracking para generar un tablero válido
def resolver_sudoku(tablero):
    for fila in range(9):
        for columna in range(9):
            if tablero[fila, columna] == 0:
                for num in random.sample(range(1, 10), 9):  # Orden aleatorio para variedad
                    if es_valido(tablero, fila, columna, num):
                        tablero[fila, columna] = num
                        if resolver_sudoku(tablero):
                            return True
                        tablero[fila, columna] = 0
                return False
    return True

# Llenar el tablero, luego ocultar algunas casillas para que el jugador pueda resolver el sudoku
def generar_juego(tablero, vacias=45):
    juego = tablero.copy()
    casillas = random.sample(range(81), vacias)
    for casilla in casillas:
        fila, columna = divmod(casilla, 9)
        juego[fila, columna] = 0
    return juego

# Verificar si un número puede ser colocado en una casilla específica
def es_valido(tablero, fila, columna, num):
    if num in tablero[fila, :]:  # Validar fila
        return False
    if num in tablero[:, columna]:  # Validar columna
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

# Insertar número en la casilla seleccionada, verificando con la solución
def insertar_numero(event, fila, columna):
    if juego[fila, columna] == 0:  # Solo permitir en casillas vacías
        num = simpledialog.askinteger("Entrada", f"Inserta un número (1-9) para la posición ({fila + 1}, {columna + 1})")
        if num and 1 <= num <= 9:
            if num == solucion[fila, columna]:  # Comprobar si el número coincide con la solución
                juego[fila, columna] = num
                celdas[fila][columna].config(state='normal')
                celdas[fila][columna].delete(0, tk.END)
                celdas[fila][columna].insert(0, str(num))
                celdas[fila][columna].config(state='disabled')
                if es_completo(juego):
                    messagebox.showinfo("¡Felicidades!", "¡Has completado el Sudoku!")
            else:
                messagebox.showerror("Error", "Número incorrecto. Esta casilla no contiene ese número en la solución.")
        else:
            messagebox.showerror("Error", "Por favor, inserta un número entre 1 y 9.")

# Mostrar el tablero completo de solución
def mostrar_solucion():
    solucion_ventana = tk.Toplevel()
    solucion_ventana.title("Solución Completa")

    for fila in range(9):
        for columna in range(9):
            celda = tk.Entry(
                solucion_ventana,
                width=3,
                font=('Arial', 18),
                justify='center',
                relief="solid",
                bd=1
            )
            celda.grid(row=fila, column=columna)
            celda.insert(0, str(solucion[fila, columna]))
            celda.config(state='disabled', disabledforeground='black')
    
# Crear la ventana principal del Sudoku
def crear_interfaz():
    ventana = tk.Tk()
    ventana.title("Sudoku")

    global celdas, juego, solucion
    celdas = [[None] * 9 for _ in range(9)]
    solucion = crear_tablero()  # Generar un tablero completo y válido
    juego = generar_juego(solucion, vacias=45)  # Dejar algunas celdas vacías para que el jugador las complete

    # Configuración de grid y bordes más gruesos para las subcuadrículas
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
                    if juego[fila, columna] != 0:  # Mostrar solo los números iniciales del juego
                        celda.insert(0, str(juego[fila, columna]))
                        celda.config(state='disabled', disabledforeground='black')
                    else:
                        celda.config(state='disabled')
                        celda.bind("<Button-1>", lambda event, r=fila, c=columna: insertar_numero(event, r, c))
                    celdas[fila][columna] = celda

    # Botón para mostrar la solución completa
    boton_solucion = tk.Button(ventana, text="Mostrar Solución Completa", command=mostrar_solucion)
    boton_solucion.grid(row=10, column=0, columnspan=9, pady=10)

    ventana.mainloop()

crear_interfaz()
