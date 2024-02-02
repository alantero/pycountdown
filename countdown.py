import pygame
import time
from datetime import datetime, timedelta

# Inicializar pygame
pygame.init()

# Configuraciones de la ventana
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Cuenta Regresiva")

# Configuraciones del reloj y sonido
clock = pygame.time.Clock()
pygame.mixer.init()
#beep_sound = pygame.mixer.Sound("beep.wav")  # Asegúrate de tener un archivo beep.wav en el mismo directorio
beep_sound = pygame.mixer.Sound("Nuclear_Alarm.mp3")  # Asegúrate de tener un archivo beep.wav en el mismo directorio
BEEP_EVENT = pygame.USEREVENT + 1


COFFE_TIME = 40#/60 #mins
ALARM_TIME = 20000 #ms

# Fuente para los números
font_size = 170
font = pygame.font.Font(None, font_size)



import pygame
import time
from datetime import datetime, timedelta

# Configuración de los umbrales de tiempo
TIME_THRESHOLDS = {
    'one_hour_left': timedelta(hours=1),
    'thirty_minutes_left': timedelta(minutes=30),
    'five_minutes_left': timedelta(minutes=5),
}


TIME_RESET = {
        "d": 1,   
        "h": 0,
        "m": 0,
        "s": 0,
        "ms": 0
}


# Configuración de los colores
COLORS = {
    'white': (255, 255, 255),
    'yellow': (255, 255, 0),
    'orange': (255, 165, 0),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
}


def render_time(time_left, blink_start, beeped):
    """Renderiza el tiempo en la pantalla."""
    screen.fill((0, 0, 0))  # Fondo negro

    # Determinar el color basado en los umbrales de tiempo
    if time_left <= TIME_THRESHOLDS['five_minutes_left']:
        color = COLORS['red']
    elif time_left <= TIME_THRESHOLDS['thirty_minutes_left']:
        color = COLORS['orange']
    elif time_left <= TIME_THRESHOLDS['one_hour_left']:
        color = COLORS['yellow']
    else:
        color = COLORS['white']

    reset = False
    # Determinar el pitido y el mensaje
    if blink_start <= datetime.now() < blink_start + timedelta(minutes=COFFE_TIME):
        if not beeped:
            beep_sound.play()
            pygame.time.set_timer(BEEP_EVENT, ALARM_TIME)  # Detener el sonido después de 10 segundos
            beeped = True
        if int(time_left.total_seconds()) % 2 == 0:
            text = font.render("Coffee Time!", True, COLORS['green'])  # Mensaje "Coffee Time!" en verde
        else:
            text = font.render("", True, color)  # Mensaje "Coffee Time!" en el color correspondiente
    else:
        if beeped:
            reset = True
            beeped = False
        # Calcular horas, minutos y segundos para la cuenta regresiva
        hours_left = int(time_left.total_seconds()) // 3600
        minutes_left = (int(time_left.total_seconds()) % 3600) // 60
        seconds_left = int(time_left.total_seconds()) % 60
        text = font.render(f"{hours_left:02}:{minutes_left:02}:{seconds_left:02}", True, color)
    
    # Posicionar y mostrar el tiempo
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, text_rect)

    pygame.display.flip()
    return beeped, reset



def get_time_left(target_hour,minute=0,second=0,microsecond=0):
    """Calcula el tiempo restante hasta una hora específica."""
    now = datetime.now()
    target = now.replace(hour=target_hour, minute=minute, second=second, microsecond=microsecond)

    # Si ya pasaron las 11, establecer el objetivo para el día siguiente
    if now >= target:
        #target = target.replace(day=target.day + 1)
        #target = target.replace(day=+ 1)

        desplazamiento = timedelta(days=TIME_RESET["d"], hours=TIME_RESET["h"], minutes=TIME_RESET["m"], seconds=TIME_RESET["s"], microseconds=TIME_RESET["ms"])
        target += desplazamiento

    time_left = target - now
    return time_left, target


### Execute code

# Obtén la hora actual
now = datetime.now()

# Calcula la hora a la que debe sonar la alarma, que es 10 segundos después de la hora actual
alarm_time = now + timedelta(seconds=10)

# Desglosa la hora en horas, minutos, segundos y milisegundos
h, m, s, ms = alarm_time.hour, alarm_time.minute, alarm_time.second, alarm_time.microsecond // 1000

h, m, s, ms = 11, 0, 0, 0


blink_start = datetime.now().replace(hour=h, minute=m, second=s, microsecond=ms)

#if blink_start - datetime.now() < 0:
#    blink_start +=  deltatime(days=1)



beeped = False

running = True




while running:

    #now = datetime.now()

    # Lógica para determinar si estamos en el periodo de "Coffee Time!"
    #if blink_start <= now < blink_start + timedelta(minutes=COFFE_TIME):
    #    if not beeped:
    #        # Activar alarma, mostrar mensaje, etc.
    #        continue
    #else:
    #    # Si no estamos en el periodo, y beeped es True, entonces lo reseteamos
    #    if beeped:
    #        beeped = False
    #        blink_start = datetime.now().replace(hour=h, minute=m, second=s, microsecond=ms)


    time_left, target = get_time_left(h, minute=m, second=s, microsecond=ms)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key is pygame.K_ESCAPE):
            running = False
        elif event.type == BEEP_EVENT:
            beep_sound.stop()
            pygame.time.set_timer(BEEP_EVENT, 0)  # Desactivar el temporizador

    beeped, reset = render_time(time_left, blink_start, beeped)

    if reset:
        #blink_start = target#datetime.now().replace(hour=h, minute=m, second=s, microsecond=ms)
        # Obtén la hora actual
        #now = datetime.now()
        # Calcula la hora a la que debe sonar la alarma, que es 10 segundos después de la hora actual
        #alarm_time = now + timedelta(seconds=10)
        # Desglosa la hora en horas, minutos, segundos y milisegundos
        #h, m, s, ms = alarm_time.hour, alarm_time.minute, alarm_time.second, alarm_time.microsecond // 1000
        h, m, s, ms = 11, 0, 0, 0
        blink_start = datetime.now().replace(hour=h, minute=m, second=s, microsecond=ms)
        beeped = False



    clock.tick(1)

pygame.quit()

