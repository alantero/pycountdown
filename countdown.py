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

    # Determinar el pitido y el mensaje
    if blink_start <= datetime.now() < blink_start + timedelta(minutes=1):
        if not beeped:
            beep_sound.play()
            pygame.time.set_timer(BEEP_EVENT, 10000)  # Detener el sonido después de 10 segundos
            beeped = True
        if int(time_left.total_seconds()) % 2 == 0:
            text = font.render("Coffee Time!", True, COLORS['green'])  # Mensaje "Coffee Time!" en verde
        else:
            text = font.render("", True, color)  # Mensaje "Coffee Time!" en el color correspondiente
    else:
        # Calcular horas, minutos y segundos para la cuenta regresiva
        hours_left = int(time_left.total_seconds()) // 3600
        minutes_left = (int(time_left.total_seconds()) % 3600) // 60
        seconds_left = int(time_left.total_seconds()) % 60
        text = font.render(f"{hours_left:02}:{minutes_left:02}:{seconds_left:02}", True, color)

    # Posicionar y mostrar el tiempo
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, text_rect)

    pygame.display.flip()
    return beeped



def get_time_left(target_hour,minute=0,second=0,microsecond=0):
    """Calcula el tiempo restante hasta una hora específica."""
    now = datetime.now()
    target = now.replace(hour=target_hour, minute=minute, second=second, microsecond=microsecond)

    # Si ya pasaron las 11, establecer el objetivo para el día siguiente
    if now >= target:
        target = target.replace(day=target.day + 1)

    time_left = target - now
    return time_left


### Execute code

h, m, s, ms = 11, 0, 0, 0


blink_start = datetime.now().replace(hour=h, minute=m, second=s, microsecond=ms)

beeped = False

running = True

while running:
    time_left = get_time_left(h, minute=m, second=s, microsecond=ms)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key is pygame.K_ESCAPE):
            running = False
        elif event.type == BEEP_EVENT:
            beep_sound.stop()
            pygame.time.set_timer(BEEP_EVENT, 0)  # Desactivar el temporizador

    beeped = render_time(time_left, blink_start, beeped)

    clock.tick(1)

pygame.quit()

