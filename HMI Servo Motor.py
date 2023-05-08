import serial
import tkinter as tk

# Configuración del puerto serial
ser = serial.Serial('COM3', 9600)

# Crear la ventana principal
root = tk.Tk()
root.title("Control de servo")

# Funciones para enviar los comandos al Arduino
def enviar_comando(comando):
    ser.write(str.encode(comando))

def estado_1():
    enviar_comando("a")

def estado_2():
    enviar_comando("b")

def estado_3():
    enviar_comando("c")

'''
def estado_4():
    enviar_comando("a")

def estado_5():
    enviar_comando("b")

def estado_6():
    enviar_comando("c")
'''

# Crear botones para cada estado color
btn_estado_1 = tk.Button(root, text="Estado 1 (Rojo)", command=estado_1)
btn_estado_2 = tk.Button(root, text="Estado 2 (Amarillo)", command=estado_2)
btn_estado_3 = tk.Button(root, text="Estado 3 (Verde)", command=estado_3)

# Crear botones para cada estado forma
btn_estado_4 = tk.Button(root, text="Estado 4 (Triangulo)", command=estado_1)
btn_estado_5 = tk.Button(root, text="Estado 5 (Circulo)", command=estado_2)
btn_estado_6 = tk.Button(root, text="Estado 6 (Cuadrado)", command=estado_3)

# Posicionar los botones en la ventana
btn_estado_1.pack()
btn_estado_2.pack()
btn_estado_3.pack()
btn_estado_4.pack()
btn_estado_5.pack()
btn_estado_6.pack()

# Ejecutar la aplicación
root.mainloop()





'''
import serial
import tkinter as tk

# Configuración del puerto serial
ser = serial.Serial('COM3', 9600)

# Crear la ventana principal
root = tk.Tk()
root.title("Control de servo")

# Funciones para enviar los comandos al Arduino
def enviar_comando(comando):
    ser.write(str.encode(comando))

def estado_1():
    enviar_comando("1")

def estado_2():
    enviar_comando("2")

def estado_3():
    enviar_comando("3")

# Crear botones para cada estado
btn_estado_1 = tk.Button(root, text="Estado 1 (Rojo, Triangulo, Pequeño)", command=estado_1)
btn_estado_2 = tk.Button(root, text="Estado 2 (Amarillo, Cuadrado, Mediano)", command=estado_2)
btn_estado_3 = tk.Button(root, text="Estado 3 (Verde, Circulo, Grande)", command=estado_3)

# Posicionar los botones en la ventana
btn_estado_1.pack()
btn_estado_2.pack()
btn_estado_3.pack()

# Ejecutar la aplicación
root.mainloop()


import tkinter as tk
import serial

# Configurar la comunicación serial
arduino_port = 'COM3'
arduino_baudrate = 9600
ser = serial.Serial(arduino_port, arduino_baudrate)

# Definir las funciones para cambiar el estado del servo
def set_state1():
    ser.write(b'1')  # Enviar "1" al Arduino
    print("Servo en el estado 1")

def set_state2():
    ser.write(b'2')  # Enviar "2" al Arduino
    print("Servo en el estado 2")

def set_state3():
    ser.write(b'3')  # Enviar "3" al Arduino
    print("Servo en el estado 3")

# Crear la GUI
root = tk.Tk()
root.title("Control de Servo")

# Crear botones para cambiar el estado del servo
state1_button = tk.Button(root, text="Estado 1", command=set_state1)
state1_button.pack(side="left")

state2_button = tk.Button(root, text="Estado 2", command=set_state2)
state2_button.pack(side="left")

state3_button = tk.Button(root, text="Estado 3", command=set_state3)
state3_button.pack(side="left")

# Ejecutar la GUI
root.mainloop()

# Cerrar la conexión serial al salir
ser.close()
'''