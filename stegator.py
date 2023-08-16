# Importamos las librerías 
from PIL import Image
import numpy as np
from numpy import array
from datetime import datetime
import sys 
import getpass
from AESCipher import AESCipher
import os
# Declaramos las variables donde almacenaremos la información
binary_image = [] # Lista Binaria de la imagen RGBA
plain_text=[] # Lista binaria del texto a ocultar
binary_result = [] # Lista donde almacenaremos el resultado de la esteganografía
image_result = [] #


#**********************************************************************
# FUNCIÓN: load_image()
#**********************************************************************
# Descripción: FUNCIÓN PARA CARGAR LA IMAGEN
# Retorna: Image
#**********************************************************************
def load_image():
    # Cargamos la Imagen
    img = Image.open(r"8x8.png")
    img = img.convert("RGBA")
    # Imprimimos la información general de la imagen 
    print("Image Mode =",img.mode)
    print("Image Size =" ,img.size)
    print("Image Format =",img.format)
    return img
#**********************************************************************
# FUNCIÓN: get_text()
#**********************************************************************
# Descripción: 
# Retorna: 
#**********************************************************************
def get_text(text):
    #print("Texto a Ocultar = ", text)
    text= text.encode("UTF-8")
    text=list(text)
    # Transformamos el mensaje a una Lista 
    for i in range(0,len(text)):
        text[i] = list(format(text[i], '08b'))

    for i in range(0,len(text)):
        for j in range(0,8):
            text[i][j] = int(text[i][j]) # Esto es una matriz
            plain_text.append(int(text[i][j])) # Esto es una lista

    # Mostramos el resultado de la transformaciòn en pantalla
    #print("Bytes del texto = ", len(text))
    #print("Bits del Texto =",len(plain_text))
    #print("Binario del Texto =",plain_text)

    # Retornamos una lista con los bits del mensaje 
    return plain_text
#**********************************************************************
# FUNCIÓN: process_image()
#**********************************************************************
# Descripción: 
# Retorna: 
#**********************************************************************
def process_image(img,plain_text,filename):
    pixel_info=[] #
    row=[] #
    final_image=[] #
    # Recorremos la imagen para transformar sus bytes a una lista 
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            binary_image.append(img.getpixel((y,x))[0])
            binary_image.append(img.getpixel((y,x))[1])
            binary_image.append(img.getpixel((y,x))[2])
            binary_image.append(img.getpixel((y,x))[3])
    # Mostramos el resultado de la transformación en pantalla
    #print("Bytes de la Imagen =",len(binary_image))
    #print("Binario de la Imagen =", binary_image)
    # Ejecutamos el proceso para modificar los bytes de la imagen 
    for i in range(0, len(binary_image)):
        binary_result.append( plain_text[i]^binary_image[i])
    # Mostramos el resultado de la modificación en pantalla 
    #print("Bytes del resultado =",len(binary_result))
    #print("Binario del resultado =", binary_result)
    # Ejecutamos la transformación para dar formato a la imagen (R,G,B,A)
    for i in range(0,len(binary_result)):
        pixel_info.append(binary_result[i])
        if i % 4 == 3:
            image_result.append(pixel_info)
            pixel_info=[]
    for i in range(0, len(image_result)):
        row.append(image_result[i])
        if i % 64 == 63:
            final_image.append(row)
            row=[]
    im=Image.fromarray(array(final_image,dtype=np.uint8),mode="RGBA")
    im.save(filename)
    return im
#**********************************************************************
# FUNCIÓN: generate_random(w,h)
#**********************************************************************
# Descripción: 
# Retorna: 
#**********************************************************************
def generate_random(w,h,filename):
    pixel_data=np.random.randint(low=0,high=255,size=(w,h,4),dtype=np.uint8)
    image=Image.fromarray(pixel_data)
    image.save(filename)
    return image
#**********************************************************************
# FUNCIÓN: fill_message(text)
#**********************************************************************
# Descripción: 
# Retorna: 
#**********************************************************************
def fill_message(text):
    message_size=len(text)
    if message_size<=2048:
        #filler_size=128-message_size
        text=("{: <2048}".format(text))
        #print(len(text))
        return text
#**********************************************************************
# FUNCIÓN: decode_image(img,key)
#**********************************************************************
# Descripción: 
# Retorna: 
#**********************************************************************
def decode_image(stg,key):
    stg_image=[]
    for x in range(stg.size[0]):
        for y in range(stg.size[1]):
            stg_image.append(stg.getpixel((y,x))[0])
            stg_image.append(stg.getpixel((y,x))[1])
            stg_image.append(stg.getpixel((y,x))[2])
            stg_image.append(stg.getpixel((y,x))[3])
    key_image=[]
    for x in range(key.size[0]):
        for y in range(key.size[1]):
            key_image.append(key.getpixel((y,x))[0])
            key_image.append(key.getpixel((y,x))[1])
            key_image.append(key.getpixel((y,x))[2])
            key_image.append(key.getpixel((y,x))[3])
    decoded_text=[]
    for i in range(0,len(key_image)):
        decoded_text.append(stg_image[i]^key_image[i])
    byte=[]
    words=[]
    for i in range(0,len(decoded_text)):
        byte.append(str(decoded_text[i]))
        if i % 8 == 7:
            words.append(chr(int(''.join(byte),2)))
            byte=[]
    result = ''.join(words)
    return result 
#**********************************************************************
# FUNCIÓN: encrypt_message(pwd, text)
#**********************************************************************
# Descripción: 
# Retorna: 
#**********************************************************************
def encrypt_message(pwd, text):
    crypto  =  AESCipher(pwd)
    message = crypto.encrypt(text)
    return(message)
#**********************************************************************
# FUNCIÓN: decrypt_message(pwd, text)
#**********************************************************************
# Descripción: 
# Retorna: 
#**********************************************************************
def decrypt_message(pwd, text):
    crypto  =  AESCipher(pwd)
    message = crypto.decrypt(text)
    return(message)
#**********************************************************************
# FUNCIÓN: banner()
#**********************************************************************
# Descripción: 
# Retorna: 
#**********************************************************************
def banner():
    print('''
            ███████╗████████╗███████╗ ██████╗  █████╗ ████████╗ ██████╗ ██████╗ 
            ██╔════╝╚══██╔══╝██╔════╝██╔════╝ ██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
            ███████╗   ██║   █████╗  ██║  ███╗███████║   ██║   ██║   ██║██████╔╝
            ╚════██║   ██║   ██╔══╝  ██║   ██║██╔══██║   ██║   ██║   ██║██╔══██╗
            ███████║   ██║   ███████╗╚██████╔╝██║  ██║   ██║   ╚██████╔╝██║  ██║
            ╚══════╝   ╚═╝   ╚══════╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
                                                                                
                                            v0.1
                                    Steganography Tool 
            
''')
#**********************************************************************
def run():
    #img = load_image()
    #random.show()
    #input_filename =  str(datetime.now().year) + str(datetime.now().month) + str(datetime.now().day) + str(datetime.now().hour) + str(datetime.now().minute)+ "_Key" + ".png"
    #output_filename = str(datetime.now().year) + str(datetime.now().month) + str(datetime.now().day) + str(datetime.now().hour) + str(datetime.now().minute)+ "_Stg" + ".png"
    os.system('cls' if os.name == 'nt' else 'clear')
    banner()
    if sys.argv[1] == "-e":
        text = input("Enter the text to encode: ")
        filename = input("Enter the filename: ")
        os.system('cls' if os.name == 'nt' else 'clear')
        banner()
        password = getpass.getpass("Password for encryption: ")
        confirm_password = getpass.getpass("Confirm password: ")
        if password == confirm_password:
            text = encrypt_message(password,text)
            text = fill_message(text)
            input_filename = "./k." + filename + ".png"
            output_filename = "./s." + filename + ".png"
            key = generate_random(64,64,input_filename)
            binary_text = get_text(text)
            stg_image = process_image(key, binary_text, output_filename)
        else:
            print("Error, password don't match")
            input("Press Enter to continue...")
            os.system('cls' if os.name == 'nt' else 'clear')
            run()
        
    if sys.argv[1] == "-d":
        password = getpass.getpass("Password for encryption: ")
        key = Image.open("./k." + sys.argv[2] + ".png")
        key = key.convert("RGBA")
        stg_image = Image.open("./s." + sys.argv[2] + ".png")
        stg_image = stg_image.convert("RGBA")
        decoded_text = decode_image(stg_image,key)
        decoded_text = decoded_text.strip()
        print("Decoded Text =", decrypt_message(password,decoded_text))

    if sys.argv[1] == "-h":
        os.system('cls' if os.name == 'nt' else 'clear')
        print('''
            ███████╗████████╗███████╗ ██████╗  █████╗ ████████╗ ██████╗ ██████╗ 
            ██╔════╝╚══██╔══╝██╔════╝██╔════╝ ██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
            ███████╗   ██║   █████╗  ██║  ███╗███████║   ██║   ██║   ██║██████╔╝
            ╚════██║   ██║   ██╔══╝  ██║   ██║██╔══██║   ██║   ██║   ██║██╔══██╗
            ███████║   ██║   ███████╗╚██████╔╝██║  ██║   ██║   ╚██████╔╝██║  ██║
            ╚══════╝   ╚═╝   ╚══════╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
                                                                                
                                            v0.1
                                    Steganography Tool 
            
    Encode Authomatic           python stegator.py -e 
    Decode Message              python stegator.py -d filename
    Open This Help              python stegator.py -h
            
            ''')


#**********************************************************************
if __name__ == "__main__":
    run()
#**********************************************************************
