from PIL import Image

def message_toBin(message):
    message_toBin = ''.join(format(ord(i), '08b') for i in message)
    return str(message_toBin)

def steganography(message, image):
    img = Image.open(image)
    imageLoad = img.load()
    messageToBin = message_toBin(message + "###")
    sizeMessageToBin = len(messageToBin)
    newImage = NomImage.replace(".jpg", "copy.PNG")    
    [width, height] = img.size
    compteur = 0
    sizeMessageToBinDivideTwo = sizeMessageToBin/2
    for i in range(width):
        for x in range(height):
                R,G,B = imageLoad[i,x]
                NewRTOBit = bin(R)[2:]
                NewGTOBit = bin(G)[2:]
                NewBTOBit = bin(B)[2:]
                if(compteur < sizeMessageToBinDivideTwo):
                     RToBit = bin(R)[2:]
                     SizeRToBit = len(RToBit)
                     NewRTOBit = RToBit[0:SizeRToBit-2] + messageToBin[:2]
                     messageToBin = messageToBin[2:len(messageToBin)]
                     compteur = compteur + 1
                if(compteur < sizeMessageToBinDivideTwo):
                     GToBit = bin(G)[2:]
                     SizeGToBit = len(GToBit)
                     NewGTOBit = GToBit[0:SizeGToBit-2] + messageToBin[:2]
                     messageToBin = messageToBin[2:len(messageToBin)]
                     compteur = compteur + 1
                if(compteur < sizeMessageToBinDivideTwo):
                     BToBit = bin(B)[2:]
                     SizeBToBit = len(BToBit)
                     NewBTOBit = BToBit[0:SizeBToBit-2] + messageToBin[:2]
                     messageToBin = messageToBin[2:len(messageToBin)]
                     compteur = compteur + 1  
                if(compteur < sizeMessageToBinDivideTwo + 1):            
                    imageLoad[i,x] = (int(NewRTOBit, 2), int(NewGTOBit, 2), int(NewBTOBit, 2))
                    if(compteur == sizeMessageToBinDivideTwo): 
                        compteur  = compteur + 1 
                        break
    img.save(newImage)                                

def verificationFinMessage(mes):
     if(len(mes) % 8 == 0):
          if(len(mes) != 8):
               mes = mes[-8:]
          if(mes == "00100011"):
               return True
     return False
    
def decodeSteganography(image):
     image1 = Image.open(image)
     image1Load = image1.load()
     [width, height] = image1.size
     stop = False
     compteur = 0
     messageDechifre = bin(255)[10:]
     for i in range(width):
        for x in range(height):
            if(stop == False and compteur < 4):
                R,G,B = image1Load[i,x] 
                RToBit = bin(R)[2:]
                messageDechifre += RToBit[-2:]
                if(verificationFinMessage(messageDechifre) == True):
                     compteur = compteur + 1
                     if(compteur == 3):
                          stop = True
                GToBit = bin(G)[2:]
                messageDechifre += GToBit[-2:]
                if(verificationFinMessage(messageDechifre) == True):
                     compteur = compteur + 1
                     if(compteur == 3):
                          stop = True
                BToBit = bin(B)[2:]
                messageDechifre += BToBit[-2:]
                if(verificationFinMessage(messageDechifre) == True):
                     compteur = compteur + 1
                     if(compteur == 3):
                          stop = True
        return FinalEncodeMessage(messageDechifre)
                    
def FinalEncodeMessage(messageDechifre):
     MessageFinalDechifre = ""
     BitDechiffrePer8 = bin(255)[10:]
     for i in range(len(messageDechifre)):
          BitDechiffrePer8 += messageDechifre[i]
          if(len(BitDechiffrePer8) % 8 == 0):
               if(len(BitDechiffrePer8) == 8):
                    MessageFinalDechifre += chr(int(BitDechiffrePer8, 2))
               if(len(BitDechiffrePer8) != 8):
                    MessageFinalDechifre += chr(int(BitDechiffrePer8[-8:], 2))
     return MessageFinalDechifre[:-3]                     



stop = False
while(stop == False):
     print("encodage ou decodage : ")
     type = input()
     if(type == "stop"):
          stop = True
     if(type == "encodage"):
          print("Veuillez entre une l'image : ")
          NomImage = input()
          print("Veuillez entrez le message que vous voulez insérer à l'image : ")
          message = input()
          steganography(message, NomImage)
          print("Message bien inséré dans l'image")
     if(type == "decodage"): 
          print("Decodage du message")
          print("Nom de l'image à  décodé : ")
          NomImage2 = input()
          print("Le message décodé est le suivant : " + decodeSteganography(NomImage2))
