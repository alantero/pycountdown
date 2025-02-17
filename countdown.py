import pygame
import time
from datetime import datetime, timedelta
import pandas as pd


# Inicializar pygame
pygame.init()

# Configuraciones de la ventana
screen_width, screen_height = 800, 600

#info = pygame.display.Info()
#screen_width = info.current_w
#screen_height = info.current_h

screen = pygame.display.set_mode((screen_width, screen_height))#, pygame.FULLSCREEN)
pygame.display.set_caption("Cuenta Regresiva")

# Configuraciones del reloj y sonido
clock = pygame.time.Clock()
pygame.mixer.init()
#beep_sound = pygame.mixer.Sound("beep.wav")  # Asegúrate de tener un archivo beep.wav en el mismo directorio
beep_sound = pygame.mixer.Sound("Nuclear_Alarm_scaled.mp3")  # Asegúrate de tener un archivo beep.wav en el mismo directorio
BEEP_EVENT = pygame.USEREVENT + 1


COFFE_TIME = 40 #mins
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
        weekday = now.weekday()
        if weekday == 4:
            desplazamiento = timedelta(days=3, hours=TIME_RESET["h"], minutes=TIME_RESET["m"], seconds=TIME_RESET["s"], microseconds=TIME_RESET["ms"])
        elif weekday == 5:
            desplazamiento = timedelta(days=2, hours=TIME_RESET["h"], minutes=TIME_RESET["m"], seconds=TIME_RESET["s"], microseconds=TIME_RESET["ms"])
        #elif weekday ==6:
        #    desplazamiento = timedelta(days=1, hours=TIME_RESET["h"], minutes=TIME_RESET["m"], seconds=TIME_RESET["s"], microseconds=TIME_RESET["ms"])
        else:
            desplazamiento = timedelta(days=TIME_RESET["d"], hours=TIME_RESET["h"], minutes=TIME_RESET["m"], seconds=TIME_RESET["s"], microseconds=TIME_RESET["ms"])
        target += desplazamiento

    time_left = target - now
    return time_left, target



def holiday_countdown(df):


    # Current date
    current_date = datetime.now()

    # Convert 'Start Date' to datetime format
    df['Start Date'] = pd.to_datetime(df['Start Date'], format='%m/%d/%Y')

    # Filter rows where the 'Start Date' is in the future
    future_holidays = df[df['Start Date'] > current_date]

    # Find the nearest future holiday
    next_holiday = future_holidays['Start Date'].min()

    # Calculate the number of days until the next holiday
    days_until_next_holiday = (next_holiday - current_date).days

    # Extract the corresponding holiday name
    next_holiday_name = future_holidays[future_holidays['Start Date'] == next_holiday]['Subject'].iloc[0]

    #print(days_until_next_holiday, next_holiday_name)

    return days_until_next_holiday, next_holiday_name



def render_holiday_countdown(days_until_next_holiday, next_holiday_name):
    # Use a smaller font size for the holiday countdown
    holiday_font_size = 30
    holiday_font = pygame.font.Font(None, holiday_font_size)

    # Prepare the text
    holiday_text = f"{next_holiday_name}: Quedan {days_until_next_holiday} dias"
    holiday_surface = holiday_font.render(holiday_text, True, COLORS["green"])#(255, 255, 255))  # White color

    #print(holiday_text)
    # Position the text on the screen (adjust according to your layout)
    
    text_rect = (130, screen_height - 200)#holiday_surface.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(holiday_surface,text_rect)# (10, screen_height - 60))





#df = pd.read_csv("calendario_laboral_cantabria_updated.csv", on_bad_lines='skip', comment="#")
df = pd.read_csv("calendario_laboral_cantabria.csv", on_bad_lines='skip', comment="#")



### Execute code

# Obtén la hora actual
now = datetime.now()

# Calcula la hora a la que debe sonar la alarma, que es 10 segundos después de la hora actual
alarm_time = now + timedelta(seconds=10)

# Desglosa la hora en horas, minutos, segundos y milisegundos
h, m, s, ms = alarm_time.hour, alarm_time.minute, alarm_time.second, alarm_time.microsecond // 1000

h, m, s, ms = 11, 0, 0, 0


blink_start = datetime.now().replace(hour=h, minute=m, second=s, microsecond=ms)

# Si la hora actual ya ha pasado la hora del café, ajusta blink_start para el día siguiente
if now >= blink_start:
    desplazamiento = timedelta(days=TIME_RESET["d"], hours=TIME_RESET["h"], minutes=TIME_RESET["m"], seconds=TIME_RESET["s"], microseconds=TIME_RESET["ms"])
    blink_start += desplazamiento

#print(blink_start)


beeped = False

running = True

fullscreen = False

while running:


    time_left, target = get_time_left(h, minute=m, second=s, microsecond=ms)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key is pygame.K_ESCAPE):
            pygame.quit()
            running = False
            exit() 
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_9:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((screen_width, screen_height))
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
        #blink_start = datetime.now().replace(hour=h, minute=m, second=s, microsecond=ms)

        desplazamiento = timedelta(days=TIME_RESET["d"], hours=TIME_RESET["h"], minutes=TIME_RESET["m"], seconds=TIME_RESET["s"], microseconds=TIME_RESET["ms"])


        #now = datetime.now()
        #next_alarm = now + desplazamiento  # Calcula el momento exacto para la próxima alarma
        #blink_start = next_alarm.replace(hour=h, minute=m, second=s, microsecond=ms*1000)  # Ajustar para la hora específica del café
        
        blink_start += desplazamiento
        #print(blink_start)
        
        beeped = False
        reset = False



    days_until_next_holiday, next_holiday_name = holiday_countdown(df)
    render_holiday_countdown(days_until_next_holiday, next_holiday_name)
    pygame.display.update()  # Make sure this is after the call to render the holiday countdown

    clock.tick(1)

pygame.quit()

