from PIL import Image
"""
steganography est une fonction prenant en entré un message de type string et une image
Cette fonction permet de rentrer le message dans l'image donné grâce à la méthode de steganography LSB
"""
def encodeSteganography(message, image):
    img = Image.open(image)#ouvrir l'image
    imageLoad = img.load()#Recuperer l'ensemble des données de l'image
    messageToBin = message_toBin(message + "###")#transforme le message de type string en binaire via la fonction message_toBin, les ### permettront de detecter la fin du message lors du decodage
    newImageRename = image.split(".")#Transformer en un tableau de taille 2 (avant le point et après le point)
    newImage = newImageRename[0] + "copy.PNG"#Recuperer la chaine de caractere avant le point + coller la chaine de caractere "copy.PNG"
    [height, width] = img.size
    compteur = 0
    sizeMessageToBinDivideTwo = len(messageToBin)/2 #cette variable indiquera la limite du compteur(le changement de pixel(RGB) de l'image se fera deux par deux donc la longuer du message divisé par deux)
    for i in range(height):
        for x in range(width):
                R,G,B = imageLoad[i,x]#Recuperer le RGB de chaque pixel de l'image
                NewRTOBit = bin(R)[2:]#Transformer R en binaire
                NewGTOBit = bin(G)[2:]#Transformer G en binaire
                NewBTOBit = bin(B)[2:]#Transformer B en binaire
                if(compteur < sizeMessageToBinDivideTwo):
                     NewRTOBit = NewRTOBit[0:len(NewRTOBit)-2] + messageToBin[:2]#Nouvelle valeur de R du pixel de l'image (prendre les 6 prémier caractere de la variable RToBit et ajouter les deux premier caractere de la variable messageToBin)
                     messageToBin = messageToBin[2:len(messageToBin)]#Retirer les deux prémier caractere de la variable messageToBin
                     compteur = compteur + 1
                if(compteur < sizeMessageToBinDivideTwo):
                     NewGTOBit = NewGTOBit[0:len(NewGTOBit)-2] + messageToBin[:2]#Nouvelle valeur de G du pixel de l'image (prendre les 6 prémier caractere de la variable GToBit et ajouter les deux premier caractere de la variable messageToBin)
                     messageToBin = messageToBin[2:len(messageToBin)]#Retirer les deux prémier caractere de la variable messageToBin
                     compteur = compteur + 1
                if(compteur < sizeMessageToBinDivideTwo):
                     NewBTOBit = NewBTOBit[0:len(NewBTOBit)-2] + messageToBin[:2]#Nouvelle valeur de B du pixel de l'image (prendre les 6 prémier caractere de la variable BToBit et ajouter les deux premier caractere de la variable messageToBin)
                     messageToBin = messageToBin[2:len(messageToBin)]#Retirer les deux prémier caractere de la variable messageToBin
                     compteur = compteur + 1  
                if(compteur < sizeMessageToBinDivideTwo + 1):            
                    imageLoad[i,x] = (int(NewRTOBit, 2), int(NewGTOBit, 2), int(NewBTOBit, 2))#Ajoutez le nouveau RGB du pixel de l'image
                    if(compteur == sizeMessageToBinDivideTwo): 
                        compteur  = compteur + 1 
                        break
    img.save(newImage)#Sauvegarde de la nouvelle image (message caché à l'intérieur) avec le nom du fichier donnée par la variable newImage                                

"""
decodeSteganography est une fonction prenant en entré une image et retournant le texte que contient l'image
"""
def decodeSteganography(image):
     image1 = Image.open(image)#ouvrir l'image
     image1Load = image1.load()#recuperer les données de l'image
     [height, width] = image1.size#recuperer la taille de l'image(longueur, largeur)
     stop = False
     compteur = 0
     messageDechifre = bin(255)[10:]
     for i in range(height):
        for x in range(width):
            if(stop == False and compteur < 4):
                R,G,B = image1Load[i,x] #Recuperer le RGB de chaque pixel de l'image
                RToBit = bin(R)[2:]#Transformer R en binaire de chaque pixel
                messageDechifre += RToBit[-2:]#Ajouter a la variable messageDechiffre les deux dernier bits de R
                if(verificationFinMessage(messageDechifre) == True):#Verifier si messageDechifre est egal à un hashtag 
                     compteur = compteur + 1#si c'est le cas ajouter 1 au compteur
                     if(compteur == 3):#si 3 hastag on été détecté alors mettre stop à true et cela permettra de stoper le dechiffrement (message déja dechiffré)
                          stop = True
                elif(len(messageDechifre) % 8 == 0):
                     compteur = 0
                GToBit = bin(G)[2:]#Transformer G en binaire de chaque pixel
                messageDechifre += GToBit[-2:]#Ajouter a la variable messageDechiffre les deux dernier bits de G
                if(verificationFinMessage(messageDechifre) == True):#Verifier si messageDechifre est egal à un hashtag 
                     compteur = compteur + 1#si c'est le cas ajouter 1 au compteur
                     if(compteur == 3):#si 3 hastag on été détecté alors mettre stop à true et cela permettra de stoper le dechiffrement (message déja dechiffré)
                          stop = True
                elif(len(messageDechifre) % 8 == 0):
                     compteur = 0
                BToBit = bin(B)[2:]#Transformer B en binaire de chaque pixel
                messageDechifre += BToBit[-2:]#Ajouter a la variable messageDechiffre les deux dernier bits de B
                if(verificationFinMessage(messageDechifre) == True):#Verifier si messageDechifre est egal à un hashtag 
                     compteur = compteur + 1#si c'est le cas ajouter 1 au compteur
                     if(compteur == 3):#si 3 hastag on été détecté alors mettre stop à true et cela permettra de stoper le dechiffrement (message déja dechiffré)
                          stop = True
                elif(len(messageDechifre) % 8 == 0):
                     compteur = 0
        return FinalEncodeMessage(messageDechifre)#Retourner le message fourni par la fonction FinalEncodeMessage 
                    
"""
FinalEncodeMessage prend en entré un message en binaire et retourne ce message en chaine de caractere sans les 3 #
"""
def FinalEncodeMessage(messageDechifre):
     MessageFinalDechifre = ""
     BitDechiffrePer8 = bin(255)[10:]
     for i in range(len(messageDechifre)):#Parcourir les différents bits composant la variable messageDechifre
          BitDechiffrePer8 += messageDechifre[i]#Ajoutez les bits de la variable messageDechifre dans la variable BitDechiffrePer8
          if(len(BitDechiffrePer8) % 8 == 0):#verifier lorsque la variable est divisible par 8 (donc avec un reste à 0)
               if(len(BitDechiffrePer8) == 8):#si la variable à une longueur de 8 alors on le transforme au character qui le correspond
                    MessageFinalDechifre += chr(int(BitDechiffrePer8, 2))
               if(len(BitDechiffrePer8) != 8):#si la variable à une longuer différent de 8 alors on prend les 8 dernier character et on transforme en charactere, exemple : sur une chaine de caractere ayant 16 caractere, on prend les 8 derniers caractere
                    MessageFinalDechifre += chr(int(BitDechiffrePer8[-8:], 2))
     return MessageFinalDechifre[:-3]#Retourner le message final en chaine de caractere sans les 3 hashtag                     

"""
verificationFinMessage est une fonction prenant en entré un message, cette fonction permet de detecter ou non la fin de message 
Si fin de message il retourne le boolean true sinon false
"""
def verificationFinMessage(mes):
     if(len(mes) % 8 == 0):#verification que la longuer du message est divisible par 8 (reste à 0)
          if(len(mes) != 8):#si le longuer du message est différent de 8 alors on retire les prémier caractere (exemple : 16 -> 8)
               mes = mes[-8:]
          if(mes == "00100011"):#si le message est égale à "00100011" correspondant à un # alors on retourne true sinon false
               return True
     return False

"""
message_toBin est une fonction prenant en entré un message de type String pouvant contenir des lettres, des symboles ou des chiffres
Cette fonction convertit le message donné en binaire et le retourne
"""
def message_toBin(message):
    message_toBin = ''.join(format(ord(i), '08b') for i in message)
    return str(message_toBin)

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
          encodeSteganography(message, NomImage)
          print("Message bien inséré dans l'image")
     if(type == "decodage"): 
          print("Decodage du message")
          print("Nom de l'image à  décodé : ")
          NomImage2 = input()
          print("Le message décodé est le suivant : " + decodeSteganography(NomImage2) + " dans l'image " + NomImage2)
