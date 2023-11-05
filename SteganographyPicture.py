from PIL import Image

"""
SteganographyPicture est une fonction prenant en entré deux images et en sortie il sauvegarde l'image encodé
L'objectif de cette fonction est encodé la deuxième image2 dans la première image image1
"""
def SteganographyPicture(image1, image2):
    img1 = Image.open(image1)#Ouvrir la prémière image
    img2 = Image.open(image2)#Ouvrir la deuxième image
    imageLoad1 = img1.load()#Charger les données de la première image
    imageLoad2 = img2.load()#charger les données de la deuxième image
    newImageRename = image1.split(".")
    newImage = newImageRename[0] + "inPictureEncode.PNG"
    if(VerifyPicture(img1.size, img2.size) == False):#Verifier que la taille de la première image est superieur à la deuxième image via la fonction VerifyPicture
        return "L'image " + image2 + " est plus grande que l'image " + image1 + ", on ne peut encoder l'image "+ image2 +" sur l'image " + image1
    [height, width] = img2.size
    imageLoad1 = endSignal(imageLoad1, img2.size)#Defenir le signal (zinzolin) pour pouvoir avoir la taille de l'image lors du decodage
    for x in range(height):
        for y in range(width):#Double for permettant d'itérer sur les deux images
            [R1,G1,B1] = TransformToBin(imageLoad1[x, y])#Recuperer le RGB de chaque pixel de l'image1 et transformer la valeur en binaire via la fonction TransformToBin
            [R2,G2,B2] = TransformToBin(imageLoad2[x, y])#Recuperer le RGB de chaque pixel de l'image2 et transformer la valeur en binaire via la fonction TransformToBin
            NewR = R1[:4]+R2[:4]#Garder les quatres premier bit de l'image1 et ajouter les quatres premier bit de l'image2 sur le R du pixel concerné
            NewG = G1[:4]+G2[:4]#Garder les quatres premier bit de l'image1 et ajouter les quatres premier bit de l'image2 sur le G du pixel concerné
            NewB = B1[:4]+B2[:4]#Garder les quatres premier bit de l'image1 et ajouter les quatres premier bit de l'image2 sur le B du pixel concerné
            imageLoad1[x,y] = (int(NewR, 2), int(NewG, 2), int(NewB, 2))#Attribuer les nouvelles valeur (RGB) du pixel de l'image sous format integer
    img1.save(newImage)#Sauvegarder la nouvelle image
    return image2 + " est bien inséré dans "+ image1 +", le nom du fichier encodé est " + newImage 

"""
decodeSteganographyImage prend en entrée une image à décodé 
"""            
def decodeSteganographyImage(image):
    img = Image.open(image)#Ouvrir l'image
    [heightImage, widthImage] = img.size #Recuperer la taille de l'image à décodé
    imageLoad = img.load() #Sauvegarder les donnée de l'image à décodé
    [height, width] = decodeSignal(imageLoad, img.size)#Recuperer la taille de l'image encodé dans l'image donnée en paramètre via la fonction decodeSignal
    newImageRename = image.split(".")
    newImage = newImageRename[0] + "inPictureDecode.PNG"
    for x in range(heightImage):
        for y in range(widthImage):#double for permettant d'itérer sur l'image à décodé
            if(x < height and y < width):#si x et y est inférieur à la taille de l'image encodé
                [R1,G1,B1] = TransformToBin(imageLoad[x, y])#Recuperer le RGB de l'image à décodé, transformé en binaire via la fonction TransformToBin 
                NewR = R1[-4:]+"0000" #Recuperer les quatres derniers bits de la valeur R du pixel et les placer sur les quatres prémier bits puis completer par quatres 0 pour que cela fasse un octet 
                NewG = G1[-4:]+"0000" #Recuperer les quatres derniers bits de la valeur G du pixel et les placer sur les quatres prémier bits puis completer par quatres 0 pour que cela fasse un octet 
                NewB = B1[-4:]+"0000" #Recuperer les quatres derniers bits de la valeur B du pixel et les placer sur les quatres prémier bits puis completer par quatres 0  pour que cela fasse un octet 
                imageLoad[x,y] = (int(NewR, 2), int(NewG, 2), int(NewB, 2)) #Nouvelle valeur RGB du pixel de l'image transformé en integer
            else:
                imageLoad[x,y] = (255, 255, 255) #attribuer la valeur (255, 255, 255) au pixel différents à la taille de l'image encodé afin d'avoir un visuel seulement sur l'image décodé
    img.save(newImage) #sauvegarder l'image décodé
    return "Image bien décodé, le nom du fichier décodé est " + newImage 

"""
decodeSignal est une fonction prenant en entré une image ainsi que la taille de cette image
Cette fonction permet de retourner la taille de l'image encodé dans cette image en reperant la couleur zinzolin
"""
def decodeSignal(imageLoad, sizeImage):
    [height, width] = sizeImage
    tab = []
    for i in range(height):
        if(imageLoad[i, 0] == (108,2,119)):#si il repere la couleur zinzorin sur l'image alors il ajoute au tableau l'indice i de la couleur zinzolin
           tab.append(i)
           break
    for y in range(width):
        if(imageLoad[0, y] == (108,2,119)):#si il repere la couleur zinzorin sur l'image alors il ajoute au tableau l'indice y de la couleur zinzolin
            tab.append(y)
            break
    return tab

"""
message_toBin est une fonction prenant en entré un message de type String pouvant contenir des lettres, des symboles ou des chiffres
Cette fonction convertit le message donné en binaire et le retourne
"""
def message_toBin(message):
    message_toBin = ''.join(format(ord(i), '08b') for i in message)
    return str(message_toBin)

"""
endSignal est une fonction prenant en entré une image ainsi que la taille de l'image, 
Cette fonction retourne une image avec sur la longuer et la largeur de la taille de l'image 2, la couleur zinzolin 
"""
def endSignal(imageLoad, sizeImage2):
    [height, width] = sizeImage2
    imageLoad[0, width] = (108, 2, 119)#placer la couleur zinzolin a cette indice du pixel de l'image
    imageLoad[height, 0] = (108, 2, 119)#placer la couleur zinzolin a cette indice du pixel de l'image
    return imageLoad

"""
Fonction TransformToBin prenant en entrée un pixel de l'image et retournant un tableau avec les RGB du pixel sous format binaire
"""
def TransformToBin(image):
    R,G,B = image #RGB de l'image
    tabRGBToBin = []
    NewRToBin = bin(R)[2:].zfill(8) #transformer la valeur R en binaire et completer la taille en un octect avec les 0
    NewGToBin = bin(G)[2:].zfill(8) #transformer la valeur G en binaire et completer la taille en un octect avec les 0
    NewBToBin = bin(B)[2:].zfill(8) #transformer la valeur B en binaire et completer la taille en un octect avec les 0
    tabRGBToBin.append(NewRToBin) #Ajouter la valeur R sours format binaire au tableau
    tabRGBToBin.append(NewGToBin) #Ajouter la valeur g sours format binaire au tableau
    tabRGBToBin.append(NewBToBin) #Ajouter la valeur B sours format binaire au tableau
    return tabRGBToBin #Retourner le tableau

"""
Fonction VerifyPicture prenant en entrée la taille d'une première image et d'une deuxième image, retournant true si la taille de l'image 1 est superieur à l'image 2 sinon false
"""
def VerifyPicture(image1Size, image2Size):
    [height1, width1] = image1Size #Recuperer la taille de l'image 1
    [height2, width2] = image2Size #Recuperer la taille de l'image 2
    if(width1 >= width2 and height1 >= height2):
        return True #Retourne true si l'image 1 est superieur à l'image 2
    else:
        print("ok")
        return False #Retourne false si l'image 1 est inferieur à l'image 2

stop = False
while(stop == False):
     print("encodage ou decodage : ")
     type = input()
     if(type == "stop"):
          stop = True
     if(type == "encodage"):
          print("Entrez l'image sur laquelle vous voulez mettre une nouvelle image : ")
          image1 = input()
          print("Entrez l'image que vous voulez cachez : ")
          image2 = input()
          print(SteganographyPicture(image1, image2))
     if(type == "decodage"): 
          print("Decodage de l'image")
          print("Nom de l'image à  décodé : ")
          NomImage2 = input()
          print(decodeSteganographyImage(NomImage2))
