#include <Servo.h>

const int enconderPin = 2; // Pin A para el Encoder
const int AIN2 = 5; // Salida PWM del motor
const byte pinObstaculo = 7;  // Pin digital utilizado para el sensor de obstáculos
const int servoPin = 9; // Pin de señal del servo

int motorPwm = 0; // Valor del PWM del motor
unsigned int rpm = 0;       // Variable para almacenar las RPM
volatile byte pulses = 0;   // Contador de pulsos del Encoder
int estadoAnterior = 0; // Variable para almacenar el estado anterior del sensor
char servoCommand = '3'; // Valor del servo

unsigned long lastTime = 0; // Variable para almacenar el tiempo anterior
int sampleTime = 100;       // Intervalo de muestreo en milisegundos
int hayObstaculo = HIGH;  // Variable para almacenar el estado del sensor de obstáculos

int angle1 = 110;    // Ángulo del primer estado
int angle2 = 135;   // Ángulo del segundo estado
int angle3 = 180;   // Ángulo del tercer estado

Servo myservo;  // Creamos un objeto servo para controlar un servo

String inputString = ""; // Cadena de entrada
//boolean stringComplete = false; // Bandera de cadena completa

void setup() {
  // Inicializar el puerto serie a 9600 baudios
  Serial.begin(9600);

  // Configurar la salida del motor
  pinMode(AIN2, OUTPUT);
  analogWrite(AIN2, 0); // Inicializar el valor del PWM en 0

  // Configurar la entrada del encoder
  pinMode(enconderPin, INPUT); // Configurar el pin del Encoder como entrada
  attachInterrupt(0, counter, RISING); // Habilitar la interrupción en el pin 1 (INT1) para contar los pulsos del Encoder

  // Configurar el servo
  myservo.attach(servoPin);
}

void loop() {
 
  if (Serial.available() > 0) { // Si hay datos disponibles en el puerto serie
  String inputString = Serial.readStringUntil('\n'); // Lee los datos hasta encontrar el caracter de fin de línea

  // Separa los valores del motor y del servo
  String motorString = inputString.substring(0, inputString.indexOf('_'));
  String servoString = inputString.substring(inputString.indexOf('_') + 1);

  // Convierte los valores a enteros y caracteres, respectivamente
  motorPwm = motorString.toInt();
  servoCommand = servoString.charAt(0);
  
  // Escribir el valor del PWM en la salida
  analogWrite(AIN2, motorPwm);

  // Mover el servo según el valor recibido
  switch(servoCommand) {
    case '1':
      myservo.write(angle1);
      break;
    
    case '2':
      myservo.write(angle2);
      break;

    case '3':
      myservo.write(angle3);
      break;
  }

  }

  leerSensorObstaculo(); // Función para leer el estado del sensor
  readRPM(); // Función para calcular y imprimir las RPM del motor

  // Enviar los datos como una tupla

  String msg = String(rpm) + "_" + String(estadoAnterior);
  Serial.println(msg);

}

void readRPM() {
  unsigned long currentMillis = millis(); // Obtener el tiempo actual en milisegundos
  
  if ((currentMillis - lastTime) >= sampleTime){
    
    detachInterrupt(0); // Deshabilitar la interrupción para evitar problemas de concurrencia
    lastTime = currentMillis; // Actualizar el tiempo anterior
    
    // Cálculo de las RPM del motor
    rpm = 0.1*(10*pulses*(60.0/374.22))+0.9*rpm; // RPM del eje principal
    
    lastTime = millis(); // Actualizar el tiempo anterior
    pulses = 0; // Reiniciar el contador de pulsos
    
    attachInterrupt(0,counter,RISING); // Volver a habilitar la interrupción en el pin 1 (INT1) del Encoder

  }

  delay(50); // Pequeña pausa para evitar lecturas erróneas del Encoder
}

void leerSensorObstaculo() {
  static unsigned long lastReadTime = 0; // Variable para almacenar el tiempo de la última lectura del sensor de obstáculos
  unsigned long currentTime = millis(); // Obtener el tiempo actual en milisegundos
  
  if ((currentTime - lastReadTime) >= 150){ // Si ha pasado al menos 150 ms desde la última lectura del sensor
    lastReadTime = currentTime; // Actualizar el tiempo de la última lectura del sensor
    hayObstaculo = digitalRead(pinObstaculo); // Leer el estado del sensor de obstáculos

    if (hayObstaculo == LOW) {  // Si se detecta un obstáculo
    estadoAnterior = 1;
    
    } else {      // No se detecta un obstaculo
    estadoAnterior = 0;
    }
  }
}

void counter(){
  pulses++; // Incrementar el contador de pulsos del Encoder
}
