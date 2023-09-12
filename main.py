import gpt
import os

primer_prompt = gpt.cargar_prompt()
resultado_primer_prompt = gpt.preguntar_primero(primer_prompt)
if "Ok" in resultado_primer_prompt:
    print("Todo Ok!")
while True:
    code = gpt.generar_numero_aleatorio(10)
    gpt.grabar_audio(f"{code}.wav")
    transcript = gpt.transcribir(f"{code}.wav")
    gpt.reproducir(gpt.preguntar(transcript))
    os.remove(f"{code}.wav")