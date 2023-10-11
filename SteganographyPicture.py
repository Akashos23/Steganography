from PIL import Image

def SteganographyPicture(image1, image2):
    img1 = Image.open(image1)
    img2 = Image.open(image2)
    WidthPicture = False
    HeightPicture = False
    imageLoad1 = img1.load()
    imageLoad2 = img2.load()
    newImageRename = image1.split(".")
    newImage = newImageRename[0] + "inPictureEncode.PNG"
    if(VerifyPicture(img1.size, img2.size) == False):
        return "L'image " + image2 + " est plus grande que l'image " + image1 + ", on ne peut encoder l'image "+ image2 +" sur l'image " + image1
    [width1, height1] = img1.size
    [width, height] = img2.size
    WidthPicture = DefineSizeTab(width1, width)
    HeightPicture = DefineSizeTab(height1, height)
    for x in range(width):
        for y in range(height):
            if(WidthPicture == False and HeightPicture == False):
                [R1,G1,B1] = TransformToBin(imageLoad1[x, y])
                [R2,G2,B2] = TransformToBin(imageLoad2[x, y])
                NewR = R1[:4]+R2[:4]
                NewG = G1[:4]+G2[:4]
                NewB = B1[:4]+B2[:4]
                imageLoad1[x,y] = (int(NewR, 2), int(NewG, 2), int(NewB, 2))
    img1.save(newImage) 
            
def decodeSteganographyImage(image, size):
    img = Image.open(image)
    [width, height] = size
    imageLoad = img.load()
    newImageRename = image1.split(".")
    newImage = newImageRename[0] + "inPictureDecode.PNG"
    for x in range(width):
        for y in range(height):
            [R1,G1,B1] = TransformToBin(imageLoad[x, y])
            NewR = R1[-4:]+"0000"
            NewG = G1[-4:]+"0000"
            NewB = B1[-4:]+"0000"
            imageLoad[x,y] = (int(NewR, 2), int(NewG, 2), int(NewB, 2))
    img.save(newImage) 

def TransformToBin(image):
    R,G,B = image
    tabRGBToBin = []
    NewRToBin = bin(R)[2:].zfill(8) 
    NewGToBin = bin(G)[2:].zfill(8)
    NewBToBin = bin(B)[2:].zfill(8)
    tabRGBToBin.append(NewRToBin)
    tabRGBToBin.append(NewGToBin)
    tabRGBToBin.append(NewBToBin)
    return tabRGBToBin

def DefineSizeTab(Size1, Size2):
    if(Size1 > Size2):
        return False
    else:
        return True

def VerifyPicture(image1Size, image2Size):
    [width1, height1] = image1Size
    [width2, height2] = image2Size
    if(width1 >= width2 and height1 >= height2):
        return True
    else:
        return False

print("Entrez l'image sur laquelle vous voulez mettre une nouvelle image : ")
image1 = input()
print("Entrez l'image que vous voulez cachez : ")
image2 = input()
SteganographyPicture(image1, image2)
img2 = Image.open(image2)
newImageRename = image1.split(".")
newImage = newImageRename[0] + "inPictureEncode.PNG"
decodeSteganographyImage(newImage, img2.size)