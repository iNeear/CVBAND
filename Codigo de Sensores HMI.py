import serial  # Importa la biblioteca para la comunicación serie
import time # Importa la biblioteca para la manipulación del tiempo
import collections # Importa la biblioteca para manejar colecciones de datos
import matplotlib.pyplot as plt # Importa la biblioteca para graficar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # Importa la biblioteca para integrar gráficos en interfaz gráfica de usuario (GUI)
import matplotlib.animation as animation # Importa la biblioteca para animar gráficos
from tkinter import * # Importa la biblioteca para crear interfaces gráficas de usuario
from threading import Thread # Importa la biblioteca para la creación de hilos de ejecución en paralelo
import cv2
from PIL import Image, ImageTk

# Función para obtener datos del puerto serie
def getData():
    time.sleep(1.0)  # Espera 1 segundo
    serialConnection.reset_input_buffer()  # Limpia el buffer de entrada del puerto serie

    while isRun:
        global isReceiving  # Indica si se están recibiendo datos
        global rpm_value  # Valor de RPM leído del puerto serie
        global sensor_value  # Valor del sensor FC51 leído del puerto serie

        data = serialConnection.readline().strip().decode()  # Lee una línea del puerto serie y la convierte a una cadena de caracteres
        rpm_value, sensor_value = data.split("_")  # Separa la cadena de caracteres en dos valores diferentes
        rpm_value = float(rpm_value)  # Convierte el valor de RPM a un número decimal
        sensor_value = int(sensor_value)  # Convierte el valor del sensor FC51 a un número entero
        isReceiving = True  # Marca que se están recibiendo datos

    isReceiving = False

# Función para solicitar el cierre de la aplicación
def askQuit():
    global isRun  # Indica si la aplicación está en ejecución
    isRun = False  # Marca que la aplicación no está en ejecución
    thread.join()  # Espera a que el hilo de recepción de datos termine su ejecución
    serialConnection.write(('0\n').encode())  # Envía un comando de parada al dispositivo conectado por el puerto serie
    serialConnection.close()  # Cierra la conexión del puerto serie
    # Detener la captura de la cámara y liberar los recursos
    camera.release()
    cv2.destroyAllWindows()

    root.quit()  # Cierra la ventana de la GUI
    root.destroy()  # Destruye la instancia de la ventana de la GUI

# Función para graficar los datos en tiempo real
def plotData(self, Samples, lines):
    global rpm_value  # Valor de RPM leído del puerto serie
    data.append(rpm_value)  # Agrega el valor a la colección de datos
    lines.set_data(range(Samples), data)  # Actualiza los datos en la gráfica
    rpm.set("RPM: " + str(rpm_value))  # Actualiza el valor de la etiqueta de RPM

# Funciones para enviar las diferentes posiciones al servomotor
def enviar_datos(pwm=None, servo=None):
    global ultimo_pwm, ultimo_servo

    if pwm is None:
        pwm = ultimo_pwm
    else:
        ultimo_pwm = pwm

    if servo is None:
        servo = ultimo_servo
    else:
        ultimo_servo = servo

    data = str(pwm) + '_' + str(servo)
    serialConnection.write(data.encode())  # Envía la tupla por el puerto serie
    print(data)

def estado_1():
    enviar_datos(None, 1)     #Envio un estado 1 que representa un angulo de 70°
def estado_2():
    enviar_datos(None, 2)     #Envio un estado 2 que representa un angulo de 45°
def estado_3():
    enviar_datos(None, 3)     #Envio un estado 3 que representa un angulo de 0°

# Función para controlar el motor pololu
def motorControl(value):
    pwmValue = str(value)  # Convierte el valor de PWM a una cadena de caracteres
    pwm.set("PWM: " + pwmValue)  # Actualiza el valor de la etiqueta de PWM
    enviar_datos(value, None)  # Envía el valor de PWM al dispositivo conectado por el puerto serie

# Función para actualizar el setpoint del motor
def actualizar_setpoint():
    setpoint = int(entry.get())  # Obtener el valor ingresado en el Entry widget
    s1.set(setpoint)  # Actualizar el valor del control s1 con el setpoint
    motorControl(setpoint)  # Actualizar el valor del PWM en el motor

# Función para actualizar el valor del sensor FC51 en la etiqueta de texto
def actualizar_sensor():
    global sensor_value  # Valor del sensor FC51 leído del puerto serie

    if sensor_value == 1:      # Se detecta un objeto cuando es 1
        label.config(text="Obstáculo detectado", bg="green")

    else:                      # No detecta un objeto cuando es 0
        label.config(text="Despejado", bg="gray")

    root.after(100, actualizar_sensor)

# Función para mostrar la imagen de la cámara en el recuadro
def show_frame():
    _, frame = camera.read()  # Capturar un frame de la cámara
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convertir el formato de color de BGR a RGB
    frame = cv2.resize(frame, (640, 480))  # Redimensionar el frame

    # Convertir el frame en una imagen de PIL para poder mostrarlo en el recuadro de la GUI
    image = Image.fromarray(frame)
    photo = ImageTk.PhotoImage(image)

    # Actualizar la imagen en el recuadro
    label_camera.configure(image=photo)
    label_camera.image = photo

    # Llamar a la función de manera recursiva para mostrar frames continuamente
    root.after(10, show_frame)

#Funcion para preguntas de clasificacion
def seleccionar_opcion(opcion):
    global opcion_actual

    if opcion == "color":
        opcion_actual = "color"
        print("Opción seleccionada: Color")

    if opcion == "forma":
        opcion_actual = "forma"
        print("Opción seleccionada: Forma")

    if opcion == "tamaño":
        opcion_actual = "tamaño"
        print("Opción seleccionada: Tamaño")

serialPort = 'COM5'  # Puerto serie a utilizar
baudRate = 9600
isReceiving = False
isRun = True

# Funciones para enviar las diferentes posiciones al servomotor
ultimo_pwm = 0
ultimo_servo = 3

try:
    serialConnection = serial.Serial(serialPort, baudRate)
    thread = Thread(target=getData)
    thread.start()
    while not isReceiving:
        print("Iniciando recepción de datos")
        time.sleep(0.1)
except:
    print('No se puede conectar al puerto')

samples = 100
data = collections.deque([0] * samples, maxlen=samples)
sampleTime = 100

xmin = 0
xmax = samples
ymin = 0
ymax = 400

fig = plt.figure(facecolor='0.94')
ax = plt.axes(xlim=(xmin, xmax), ylim=(ymin, ymax))
plt.title("Real-time RPM reading")
ax.set_xlabel("Samples")
ax.set_ylabel("RPM")

lines = ax.plot([], [])[0]


#  Ventana Principal
# Pantalla
root = Tk()
root.title("GUI | TKINTER | CVBAND")
root.geometry('1366x768')

# Fondo de la ventana
imagenF = PhotoImage(file="FondoGUI.png")
background = Label(image = imagenF, text = "Fondo")
background.place(x = 0, y = 0, relwidth = 1, relheight = 1)

# Cargar la imagen del logo y ajustar el tamaño
logo = PhotoImage(file="LOGO.png")
logo = logo.subsample(2, 2)

# Crear un Label y configurarlo para mostrar el logo
logo_label = Label(root, image=logo)
logo_label.place(x=915, y=10)

# Interfaz
texto1 = Label(root, text=" Video en tiempo real ", font=("Arial", 16), bd=1, relief="solid")
texto1.place(x=225, y=50)

# Crear el recuadro para mostrar la imagen de la cámara
label_camera = Label(root)
label_camera.place(x=30, y=100, width=600, height=450)

# Inicializar la cámara
camera = cv2.VideoCapture(0)

texto2 = Label(root, text=" Seleccione una opcion para la clasificacion: ", font=("Arial", 14), bd=1, relief="solid")
texto2.place(x=130, y=580)

# Crear los botones
boton_color = Button(root, text="Color",width=10, command=lambda: seleccionar_opcion("color"), font=("Arial", 12))
boton_color.place(x=130, y=630)

boton_forma = Button(root, text="Forma",width=10, command=lambda: seleccionar_opcion("forma"), font=("Arial", 12))
boton_forma.place(x=270, y=630)

boton_forma = Button(root, text="Tamaño",width=10, command=lambda: seleccionar_opcion("tamaño"), font=("Arial", 12))
boton_forma.place(x=410, y=630)

# Interfaz
texto3 = Label(root, text=" Control de velocidad y lectura del sensor infrarrojo ", font=("Arial", 16), bd=1, relief="solid")
texto3.place(x=770, y=450)

# Posicionar las otras widgets en la ventana
canvas = FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.place(x=727, y=200, width=570, height=220)

# Posicionar la etiqueta del control de motor
frame = Frame(root, width=180, height=150, bd=1, relief="solid")
frame.place(x=790, y=500)

rpm = StringVar(root, "RPM: 0.00")
labelRpm = Label(frame, textvariable=rpm, font=("Arial", 12))
labelRpm.place(x=10, y=0)

pwm = StringVar(root, "PWM: 0.00")
labelPwm = Label(frame, textvariable=pwm, font=("Arial", 12))
labelPwm.place(x=10, y=30)

s1 = Scale(frame, from_=0, to=255, orient=HORIZONTAL, command=motorControl, length=150)
s1.place(x=10, y=60)

entry = Entry(frame, width=11)
entry.place(x=13, y=120)

button = Button(frame, text="Actualizar", command=actualizar_setpoint)
button.place(x=100, y=117)

label = Label(root, text="Esperando datos del sensor...", bd=2, relief="solid", font=("Arial", 20),width=16)
label.place(x=1000, y=550)

salida = Button(text="Detener", bg="red", command=askQuit, font=("Arial", 15))  # Asociar la función askQuit al botón
salida.place(x=1260, y=650)


root.after(100, actualizar_sensor)

anim = animation.FuncAnimation(fig, plotData, fargs=(samples, lines), interval=sampleTime, cache_frame_data=False)

# Iniciar la visualización de la cámara
show_frame()

root.protocol('WM_DELETE WINDOW', askQuit)
root.mainloop()
