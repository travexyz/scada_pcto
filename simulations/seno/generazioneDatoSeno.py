import math
import random

def genera():
    random_number = random.uniform(0.9 , 1.9)
    print (f"Il numero è: {random_number}")
    random_number = math.sin(random_number)
    print(f"Il seno è: {random_number}")
    return random_number


def scrittura():
    try:
        file_uno = open("datiSeno.ini" , "x")
        file_uno.close()
    except FileExistsError:
        pass
    file_uno = open("datiSeno.ini" , "a")
    sine_wave_value = genera()
    file_uno.write(str(sine_wave_value))
    file_uno.write(" ")
    file_uno.close()