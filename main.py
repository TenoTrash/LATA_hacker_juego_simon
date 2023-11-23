"""

Juego "SIMON" sobre Raspberry pi pico
Teno, para el taller PIXEL
23/11/2023

Entradas:

    - GP0: Botón 1
    - GP1: Botón 2
    - GP2: Botón 3
    - GP3: Botón 4
    - GP4: Botón 5
    - GP5: Botón 6
    - GP6: Botón 7
    - GP7: Botón 8
    - GP8: Botón 9
    - GP9: Botón 10
    - GP10: Botón 11
    - GP11: Botón 12
    
Salidas:
    
    - GP25: Led Onboard (futuro buzzer?)
    - GP13: Led 1
    - GP14: Led 2
    - GP16: Led 3
    - GP17: Led 4
    - GP18: Led 5
    - GP19: Led 6
    - GP28: Led 7
    - GP27: Led 8
    - GP26: Led 9
    - GP22: Led 10
    - GP21: Led 11
    - GP20: Led 12

"""

from machine import Pin, PWM
from random  import randint
from utime   import sleep

# Función que inicializa el juego y declara las variables
def start():
    global level
    global levels
    global user_input
    global random_sequence
    
    level = 0
    levels = 20
    user_input = 0
    random_sequence = []
    
    random_sequence = [randint(0, 11) for _ in range(levels)]
    
    for index in range(len(OUTPUTS)):
        generate_sequence(index, 0.05)
    
    sleep(0.1)


# Función que genera las secuencias
def generate_sequence(index, delay):
    led = OUTPUTS[index]
    
    speaker.freq((index + 3) * 100)
    speaker.duty_u16(32768)
    
    led.value(True)
    
    sleep(delay)
    
    speaker.duty_u16(0)
    speaker.deinit()
    
    led.value(False)
    sleep(delay)


# Función que genera las secuencias aleatorias
def generate_random_sequence(level):
    delay_random = 0.35
    
    for pin in range(level + 1):
        index = random_sequence[pin]
        generate_sequence(index, delay_random)


# Función que verifica las secuencias
def verify_sequences(index):
    return random_sequence[index] == user_input


# Función que se encaraga de ingresar la secuencia del usuario
def input_sequence():
    global user_input
    
    delay_user = 0.25
    
    for index, button in enumerate(INPUTS):
        if not button.value():
            user_input = index
            generate_sequence(index, delay_user)
            
            return True
    
    return False
        

# Declaración del buzzer que va el led onboard por ahora
speaker = PWM(Pin(25, Pin.OUT))

# Declaración de las entradas (pulsadores en configuración pull up)
INPUTS = [
    Pin(0, Pin.IN, Pin.PULL_UP),
    Pin(1, Pin.IN, Pin.PULL_UP),
    Pin(2, Pin.IN, Pin.PULL_UP),
    Pin(3, Pin.IN, Pin.PULL_UP),
    Pin(4, Pin.IN, Pin.PULL_UP),
    Pin(5, Pin.IN, Pin.PULL_UP),
    Pin(6, Pin.IN, Pin.PULL_UP),
    Pin(7, Pin.IN, Pin.PULL_UP),
    Pin(8, Pin.IN, Pin.PULL_UP),
    Pin(9, Pin.IN, Pin.PULL_UP),
    Pin(10, Pin.IN, Pin.PULL_UP),
    Pin(11, Pin.IN, Pin.PULL_UP)
]


# Declaración de las salidas (leds a cada lado de su respectivo botón)
OUTPUTS = [
    Pin(13, Pin.OUT),
    Pin(14, Pin.OUT),
    Pin(16, Pin.OUT),
    Pin(17, Pin.OUT),
    Pin(18, Pin.OUT),
    Pin(19, Pin.OUT),
    Pin(28, Pin.OUT),
    Pin(27, Pin.OUT),
    Pin(26, Pin.OUT),
    Pin(22, Pin.OUT),
    Pin(21, Pin.OUT),
    Pin(20, Pin.OUT)
]

# Inicialización del juego
start()

# Bucle de repetición del juego
while True:
    generate_random_sequence(level)
    level = level + 1
    
    for index in range(level):
        while True:
            if input_sequence():
                break
        
        if not verify_sequences(index):
            start()
            break
    
    if level == levels:
        start()
    
    sleep(0.3)
    
