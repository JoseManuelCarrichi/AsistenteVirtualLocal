from assistant import Asistente

def main():

    modelWhisper = "tiny"
    record_timeout = 3
    phrase_timeout = 3
    energy_threshold = 1000
    wake_word = "ATOM"

    assistant = Asistente(modelWhisper, record_timeout, phrase_timeout, energy_threshold, wake_word)
    assistant.listen()
    #assistant.write_transcript()

if __name__ == "__main__":
    main()