from pydub import AudioSegment
import sys



audio_file = sys.argv[1]

# Cargar el archivo WAV
audio = AudioSegment.from_file(audio_file)

# Aumentar el volumen por 10 dB
audio_aumentado = audio + 100


# Guardar el archivo aumentado
audio_aumentado.export(audio_file.split(".")[0]+"_scaled100.mp3", format="mp3")

