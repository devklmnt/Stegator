# Stegator 

Steganography Tool for Python

## Install Python Dependencies
    pip install -r requirements.txt

## Stegator Help
    python stegator.py -h
    
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

## Encode message 
Run the following command in your bash 

    python stegator.py -e

Stegator will asks for a text to encode and the basic filename. in this case test.file

    Enter the text to encode: 
    Enter the filename: test.file

Stegator will generate two .png files in the directory, one image will be the key generated automatically and the other will be the steganography of that image.

    k.test.file.png
    s.test.file.png

by Default Stegator will generate a 64x64 pixel image.

![example](https://github.com/devklmnt/Stegator/blob/main/k.test.file.png?raw=true)

## Decode message 
Run the following command to decode message 

    python stegator.py -d test.file

It will show the message hidden in the images 
