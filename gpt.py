import random
import keyboard
import pyaudio
import wave
import openai
import pygame
import tempfile
import os
import pygame
import random
from gtts import gTTS

openai.api_key = "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"
chat_history = []
prompt_file = "prompt.txt"

# Cargar el prompt desde el archivo .txt
def cargar_prompt():
    with open(prompt_file, "r") as f:
        prompt = f.read()
        return prompt

# Grabar audio usando PyAudio
def grabar_audio(nombre_archivo):
    formato = pyaudio.paInt16
    canales = 2
    tasa_muestreo = 44100
    duracion = 0

    p = pyaudio.PyAudio()

    print("Presiona la barra espaciadora para iniciar la grabación...")
    keyboard.wait("space")

    stream = p.open(format=formato,
                    channels=canales,
                    rate=tasa_muestreo,
                    input=True,
                    frames_per_buffer=1024)

    frames = []

    print("Grabando audio. Presiona la barra espaciadora nuevamente para detener...")
    while True:
        data = stream.read(1024)
        frames.append(data)
        if keyboard.is_pressed("space"):
            break

    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Deteniendo la grabación. Pensando...")

    wf = wave.open(nombre_archivo, 'wb')
    wf.setnchannels(canales)
    wf.setsampwidth(p.get_sample_size(formato))
    wf.setframerate(tasa_muestreo)
    wf.writeframes(b''.join(frames))
    wf.close()

# Transcribe el audio usando la API de OpenAI
def transcribir(path): 
    try:
        audio_file = open(path, "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript['text']
    except Exception as e:
        print(f"Error al transcribir el audio: {str(e)}")
        return ""

# Genera un numero aleatorio de la longitud especificada
def generar_numero_aleatorio(longitud):
    if longitud <= 0:
        raise ValueError("La longitud debe ser un número positivo")
    
    numero = 0
    for _ in range(longitud):
        digito = random.randint(0, 9)
        numero = numero * 10 + digito
    
    return numero

# Reproduce el texto usando la API de Google
def reproducir(text):
    pygame.init()
    tts = gTTS(text, lang='es')
    archivo_temporal = os.path.join(tempfile.gettempdir(), "texto_convertido.wav")
    tts.save(archivo_temporal)
    sonido = pygame.mixer.Sound(archivo_temporal)
    sonido.play()
    pygame.time.wait(int(sonido.get_length() * 1000))
    pygame.quit()

# Usa la API de OpenAI para generar una respuesta
def preguntar_primero(prompt):
        chat_history.append({"role": "user", "content": prompt})

        response_iterator = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = chat_history,
            stream=True,
            max_tokens=150,
        )

        collected_messages = []

        for chunk in response_iterator:
            chunk_message = chunk['choices'][0]['delta']
            collected_messages.append(chunk_message)
            full_reply_content = ''.join([m.get('content', '') for m in collected_messages])

        chat_history.append({"role": "assistant", "content": full_reply_content})
        return full_reply_content

def preguntar(prompt):
        chat_history.append({"role": "user", "content": prompt})

        response_iterator = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = chat_history,
            stream=True,
            max_tokens=150,
        )

        collected_messages = []

        for chunk in response_iterator:
            chunk_message = chunk['choices'][0]['delta']
            collected_messages.append(chunk_message)
            full_reply_content = ''.join([m.get('content', '') for m in collected_messages])

        chat_history.append({"role": "assistant", "content": full_reply_content})
        print(f"\nPregunta: {prompt}\nRespuesta: {full_reply_content}\n")
        return full_reply_content