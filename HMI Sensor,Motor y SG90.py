import serial  # Importa la biblioteca para la comunicación serie
import time # Importa la biblioteca para la manipulación del tiempo
import collections # Importa la biblioteca para manejar colecciones de datos
import matplotlib.pyplot as plt # Importa la biblioteca para graficar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # Importa la biblioteca para integrar gráficos en interfaz gráfica de usuario (GUI)
import matplotlib.animation as animation # Importa la biblioteca para animar gráficos
from tkinter import * # Importa la biblioteca para crear interfaces gráficas de usuario
from threading import Thread # Importa la biblioteca para la creación de hilos de ejecución en paralelo

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
    global isRun # Indica si la aplicación está en ejecución
    isRun = False # Marca que la aplicación no está en ejecución
    thread.join() # Espera a que el hilo de recepción de datos termine su ejecución
    serialConnection.write(('0\n').encode()) # Envía un comando de parada al dispositivo conectado por el puerto serie
    serialConnection.close() # Cierra la conexión del puerto serie
    root.quit() # Cierra la ventana de la GUI
    root.destroy() # Destruye la instancia de la ventana de la GUI

# Función para graficar los datos en tiempo real
def plotData(self, Samples, lines):
    global rpm_value  # Valor de RPM leído del puerto serie
    data.append(rpm_value)  # Agrega el valor a la colección de datos
    lines.set_data(range(Samples), data)  # Actualiza los datos en la gráfica
    rpm.set("RPM: "+str(rpm_value))  # Actualiza el valor de la etiqueta de RPM


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
    serialConnection.write(data.encode()) # Envía la tupla por el puerto serie
    print(data)

def estado_1():
    enviar_datos(None, 1)

def estado_2():
    enviar_datos(None, 2)

def estado_3():
    enviar_datos(None, 3)

# Función para controlar el motor pololu
def motorControl(value):
    pwmValue = str(value) # Convierte el valor de PWM a una cadena de caracteres
    pwm.set("PWM: " + pwmValue) # Actualiza el valor de la etiqueta de PWM
    enviar_datos(value, None) # Envía el valor de PWM al dispositivo conectado por el puerto serie

# Función para actualizar el setpoint del motor
def actualizar_setpoint():
    setpoint = int(entry.get()) # Obtener el valor ingresado en el Entry widget
    s1.set(setpoint) # Actualizar el valor del control s1 con el setpoint
    motorControl(setpoint) # Actualizar el valor del PWM en el motor

# Función para actualizar el valor del sensor FC51 en la etiqueta de texto
def actualizar_sensor():
    global sensor_value  # Valor del sensor FC51 leído del puerto serie

    if sensor_value == 1:
        label.config(text="Obstáculo detectado")
        boton.config(bg="red")
    else:
        label.config(text="Despejado")
        boton.config(bg="green")

    root.after(100, actualizar_sensor)

serialPort = 'COM3' # Puerto serie a utilizar
baudRate = 9600
isReceiving = False
isRun = True
value = 0.0

# Funciones para enviar las diferentes posiciones al servomotor
ultimo_pwm = 0
ultimo_servo = 3

try:
    serialConnection = serial.Serial(serialPort, baudRate)
except:
    print('No se puede conectar al puerto')

thread = Thread (target=getData)
thread.start()

while isReceiving != True:
    print("Iniciando recepción de datos")
    time.sleep (0.1)

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

lines = ax.plot([], []) [0]

root = Tk()
root.title("CVBAND")

# Crear botones para cada estado color
btn_estado_1 = Button(root, text="Estado 1 (70°)", command=estado_1)
btn_estado_2 = Button(root, text="Estado 2 (45°)", command=estado_2)
btn_estado_3 = Button(root, text="Estado 3 (0°)", command=estado_3)

# Posicionar los botones en la ventana
btn_estado_1.place(x=850, y=30)
btn_estado_2.place(x=850, y=70)
btn_estado_3.place(x=850, y=110)

# Posicionar las otras widgets en la ventana
canvas = FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.place(x=50, y=30)

frame = Frame(root, width=200, height=150)
frame.place(x=850, y=300)

pwm = StringVar(root, "PWM: 0.00")
labelPwm = Label(frame, textvariable=pwm)
labelPwm.place(x=10, y=20)

rpm = StringVar(root, "RPM: 0.00")
labelRpm = Label(root, textvariable=rpm, font=("Arial", 14))
labelRpm.place(x=860, y=250)

s1 = Scale(frame, from_=0, to=255, orient=HORIZONTAL, command=motorControl, length=150)
s1.place(x=10, y=50)

entry = Entry(frame, width=10)
entry.place(x=10, y=100)

button = Button(frame, text="Actualizar", command=actualizar_setpoint)
button.place(x=110, y=100)

label = Label(root, text="Esperando datos del sensor...", font=("Arial", 20))
label.place(x=850, y=500)

boton = Button(root, text="Detener", bg="gray", command=askQuit)
boton.place(x=850, y=550)

root.after(100, actualizar_sensor)

anim = animation.FuncAnimation(fig, plotData, fargs=(samples, lines), interval=sampleTime, cache_frame_data=False)

root.protocol('WM_DELETE WINDOW', askQuit)
root.geometry('1280x720')
root.mainloop()
