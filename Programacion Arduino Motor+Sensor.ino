const int AIN2 = 5;         // Pin para la salida PWM
const int enconderPin = 2; // Pin A para el Encoder

unsigned int rpm = 0;       // Variable para almacenar las RPM
volatile byte pulses = 0;   // Contador de pulsos del Encoder
int pwm;                    // Variable para almacenar el valor del PWM

unsigned long lastTime = 0; // Variable para almacenar el tiempo anterior
int sampleTime = 100;       // Intervalo de muestreo en milisegundos

String inputString = "";   // Variable para almacenar la cadena de entrada del puerto serie
bool stringComplete = false; // Bandera para indicar que se ha completado la lectura de la cadena

const byte pinObstaculo = 7;  // Pin digital utilizado para el sensor de obstáculos
int estadoAnterior = 0; // Variable para almacenar el estado anterior del sensor
int hayObstaculo = HIGH;  // Variable para almacenar el estado del sensor de obstáculos

void setup() {
  
  Serial.begin(9600);         // Inicializar la comunicación serial a 9600 bps
  pinMode(enconderPin, INPUT); // Configurar el pin del Encoder como entrada
  pinMode(AIN2, OUTPUT);       // Configurar el pin de salida PWM como salida
  attachInterrupt(0, counter, RISING); // Habilitar la interrupción en el pin 1 (INT1) para contar los pulsos del Encoder
  analogWrite(AIN2, 0); // Inicializar el valor del PWM en 0
  
}

void loop() {
 
  if (stringComplete){
    
    pwm = inputString.toInt(); // Convertir la cadena de entrada a un valor entero

    analogWrite(AIN2, pwm); // Escribir el valor del PWM en la salida
    inputString = ""; // Reiniciar la variable de la cadena de entrada
    stringComplete = false; // Reiniciar la bandera de cadena completa
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
    
    } else {
    estadoAnterior = 0;
    }
  }
}


void serialEvent(){
  while (Serial.available()){
    char inChar = (char)Serial.read(); // Leer el caracter del puerto serie
    inputString += inChar; // Agregar el caracter a la cadena de entrada

    if (inChar == '\n'){ // Si se ha leído el final de línea
      stringComplete = true; // Activar la bandera de cadena completa
    }
  }
  
}

void counter(){
  pulses++; // Incrementar el contador de pulsos del Encoder
}