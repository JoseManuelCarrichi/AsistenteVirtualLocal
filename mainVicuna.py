import json
from llama_cpp import Llama
from textwrap import indent
import time



# Cargar el mododelo
print("Cargado el modelo...")


#NEWS
#Vicuna 13b ggml v3
#vicuna = Llama(model_path="/home/mcim/Descargas/Vicuna/NewCuantization/ggml-vic13b-q5_1.bin")
#Wizard x Vicuna 7B
vicuna = Llama(model_path="/home/mcim/Descargas/Vicuna/NewCuantization/Wizard-Vicuna-7B-Uncensored.ggmlv3.q4_0.bin")
#Samantha 7B
#vicuna = Llama(model_path="/home/mcim/Descargas/Vicuna/NewCuantization/Samantha-7B.ggmlv3.q4_0.bin")
#WizardLM-7B
#vicuna = Llama(model_path="/home/mcim/Descargas/Vicuna/NewCuantization/WizardLM-7B-uncensored.ggmlv3.q4_0.bin")
#guanaco-7B
#vicuna = Llama(model_path="/home/mcim/Descargas/Vicuna/NewCuantization/guanaco-7B.ggmlv3.q4_0.bin")
#Wizard vicunaFineTunning
#vicuna = Llama(model_path="/home/mcim/Descargas/Vicuna/NewCuantization/Wizard-Vicuna-7B-Uncensored.ggmlv3.q4_0.bin")

print("Modelo cargado...")


def VicunaInference(userQuestion):
    #promt = "Answer the next in spanish. Question: " + userQuestion + " Answer:"
    promt = "Question: " + userQuestion + " Answer:"
    output = vicuna(promt, max_tokens = 180, temperature = 0.9, stop = ["Question:", "Q:"], echo = True)
    #print(json.dumps(output, indent = 2))
    resp = output["choices"][0]["text"]
    #print(resp)
    resp = resp.split('Answer: ')[1]
    return resp

while(True):
    userQuestion = input("Escribe una pregunta: ")
    try:
        inicio = time.time() # tiempo al iniciar la funcion 
        answer = VicunaInference(userQuestion)
        print(answer)
        fin = time.time()
        print("Tiempo total: ", fin-inicio) #Mostrar el tiempo total de procesamiento
    except:
        print("No entendi tu pregunta")
    