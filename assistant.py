import whisper
from files import write_file as wf
import speech_recognition as sr
from queue import Queue
from datetime import datetime, timedelta
import io
import pyttsx3
from tempfile import NamedTemporaryFile
#import os

class Asistente:
    def __init__(self, modelWhisper, record_timeout, phrase_timeout, energy_threshold, wake_word):
        self.temp_file = NamedTemporaryFile().name
        self.transcription = ['']
        self.audio_model = whisper.load_model(modelWhisper)
        self.phrase_time = None
        self.last_sample = bytes()
        self.data_queue = Queue() 
        self.recorder = sr.Recognizer()
        self.recorder.energy_threshold = energy_threshold
        self.recorder.dynamic_energy_threshold = False
        self.record_timeout = record_timeout
        self.phrase_timeout = phrase_timeout
        self.wake_word = wake_word
        
    def listen(self):
        # Configura el micrófono con una tasa de muestreo de 16000 Hz
        self.source = sr.Microphone(sample_rate=16000)
        # Se ajusta el nivel de ruido ambiente para que no se tome como voz
        with self.source:
            self.recorder.adjust_for_ambient_noise(self.source)
            # Función que se ejecutará cada vez que se termine una grabación
            def record_callback(_, audio:sr.AudioData) -> None:
                """
                Función de callback en otro hilo para recibir datos de audio cuando se terminan las grabaciones.
                audio: Un objeto AudioData que contiene los bytes grabados.
                """
                # Se obtienen los bytes crudos del objeto AudioData y se agregan a la cola thread-safe.
                data = audio.get_raw_data()
                self.data_queue.put(data)
            
        #Se deja el microfono escuchando con ayuda de speech_recognition
        # Se establece un límite de tiempo para cada grabación en "phrase_time_limit"
        self.recorder.listen_in_background(self.source, record_callback, phrase_time_limit=self.record_timeout)
        start = datetime.utcnow()
        while True:
            try:
                now = datetime.utcnow()
                # Se escribe la transcripción cada 18 segundos
                if ((now - start).total_seconds()%18) == 0:
                    print("Entro a escribir el trasncrit")
                    self.write_transcript()
                    print("Salgo de imprimir")
                # Se verifica si hay nuevos datos de audio en la cola thread-safe
                if not self.data_queue.empty():
                    phrase_complete = False
                    # Se verifica si la grabación actual ha superado el tiempo límite
                    if self.phrase_time and now - self.phrase_time > timedelta(seconds=self.phrase_timeout):
                        self.last_sample = bytes()
                        phrase_complete = True
                    # Esta es la última vez que recibimos datos de audio nuevos de la cola.
                    self.phrase_time = now
                    while not self.data_queue.empty():
                        data = self.data_queue.get()
                        self.last_sample += data
                    # Se crea un objeto AudioData con los datos de audio recibidos
                    audio_data = sr.AudioData(self.last_sample, self.source.SAMPLE_RATE, self.source.SAMPLE_WIDTH)
                    # Se convierte el objeto AudioData a formato wav
                    wav_data = io.BytesIO(audio_data.get_wav_data())
                    # Se guarda el archivo temporalmente para poder transcribirlo 
                    with open(self.temp_file, 'w+b') as f:
                        f.write(wav_data.read())
                    # Se llama a whisper para transcribir el audio
                    print("voy a transcribir con whisper")
                    result = self.audio_model.transcribe(self.temp_file, fp16=False, language='es')
                    text = result['text'].strip()
                    print(text)
                    # Se agrega la transcripción a la lista de transcripciones.
                    if phrase_complete:
                        self.transcription.append(text)
                    else:
                        self.transcription[-1] = text
                    # Si la palabra clave ("wake word") se encuentra en la última transcripción, se activa el asistente virtual.
                    if self.wake_word in self.transcription[-1].lower():
                        # Se activó el asistente
                        # Se extrae el mensaje del usuario, eliminando la palabra clave
                        prompt = self.transcription[-1].lower().replace(self.wake_word, "")
                        # Se agrega un encabezado indicando que es un mensaje del usuario
                        prompt = "USUARIO: " + prompt
                        # Se llama a la función call_gpt para obtener la respuesta del asistente virtual
                        respuesta = self.call_gpt(prompt)
                        # Se imprime la respuesta obtenida
                        print(respuesta)
                        # Se utiliza la función speak para convertir la respuesta a audio
                        self.speak(respuesta)
                            
            except KeyboardInterrupt:
                break
    def call_gpt(self, prompt):
        # LLamada al modelo GPT4ALL
        print(prompt)
        #Acá se debe hacer la inferencia, por ahora dejo un mensaje procicional
        respuesta = "Hola, la respuesta será generada por el modelo de lenguaje atorregresivo"
        print("ATOM: ", respuesta)
        return respuesta
        
    def speak(self, respuesta):
        # se utiliza pyttsx3
        atom = pyttsx3.init()
        atom.say(respuesta)
        atom.runAndWait()
   
    def write_transcript(self):
        print("\n\nTranscripcion:")
        line = self.transcription
        print(line)
        #wf(line, "transcript", "txt")
