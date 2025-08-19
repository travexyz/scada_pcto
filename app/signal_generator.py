import numpy as np
import time
import json
import random
from datetime import datetime

# Funzione per generare un'onda sinusoidale
def sine_wave(i, freq=1, amp=1):
    return amp * np.sin(2 * np.pi * freq * i / 100)

# Funzione per generare un segnale a rampa
def ramp(i, start=0, stop=1):
    return start + (stop - start) * ((i % 100) / 100)

# Funzione per generare un'onda a dente di sega
def sawtooth(i, cycles=5):
    x = (i % 100) / 100 * cycles
    return 2 * (x - np.floor(x + 0.5))

# Funzione per generare un valore casuale
def random_signal(i, low=0, high=1):
    return np.random.uniform(low, high)

i = 0
signal_list = ["sine", "ramp", "saw", "random"]  # Lista dei tipi di segnali disponibili
signal_type = random.choice(signal_list)  # Sceglie casualmente il tipo di segnale

# Ciclo infinito per generare segnali continuamente
while True:

    # Genera il valore del segnale in base al tipo scelto
    if signal_type == "sine":
        value = sine_wave(i)
    elif signal_type == "ramp":
        value = ramp(i)
    elif signal_type == "saw":
        value = sawtooth(i)
    elif signal_type == "random":
        value = random_signal(i)
    else:
        raise ValueError("Tipo segnale non supportato")

    # Crea un messaggio con timestamp, indice, tipo di segnale e valore
    msg = {
        "timestamp": datetime.utcnow().isoformat(),
        "index": i,
        "signal": signal_type,
        "value": float(value)
    }
    print(json.dumps(msg), flush=True)  # Stampa il messaggio in formato JSON
    time.sleep(0.1)  # Attende prima di generare il prossimo segnale
    i += 1  # Incrementa l'indice
