print("Press ENTER to start")

"""
def fillZeroes(string):
    if len(string) < 6:
        return string+("0"*(6-len(string)))
    else: return string

print("brailleDict = {\n", end="\t")
for i, e in enumerate("⠀⠁⠂⠃⠄⠅⠆⠇⠈⠉⠊⠋⠌⠍⠎⠏⠐⠑⠒⠓⠔⠕⠖⠗⠘⠙⠚⠛⠜⠝⠞⠟⠠⠡⠢⠣⠤⠥⠦⠧⠨⠩⠪⠫⠬⠭⠮⠯⠰⠱⠲⠳⠴⠵⠶⠷⠸⠹⠺⠻⠼⠽⠾⠿"):
    print('"'+fillZeroes(str(bin(i))[2:][::-1])+'":"'+e+'",', end="")
    if not (i+1)%8 : print("\n\t",end="")
print("}")
"""

from PIL import Image, ImageFilter, ImageOps, ImageEnhance
import PIL, os, io, requests
import numpy as np

def getPix(x, y, img):
    r,g,b = img.getpixel((x,y)) 
    return max([r,g,b])

def main():
    brailleDict = {
        "000000":"⠀","100000":"⠁","010000":"⠂","110000":"⠃","001000":"⠄","101000":"⠅","011000":"⠆","111000":"⠇",
        "000100":"⠈","100100":"⠉","010100":"⠊","110100":"⠋","001100":"⠌","101100":"⠍","011100":"⠎","111100":"⠏",
        "000010":"⠐","100010":"⠑","010010":"⠒","110010":"⠓","001010":"⠔","101010":"⠕","011010":"⠖","111010":"⠗",
        "000110":"⠘","100110":"⠙","010110":"⠚","110110":"⠛","001110":"⠜","101110":"⠝","011110":"⠞","111110":"⠟",
        "000001":"⠠","100001":"⠡","010001":"⠢","110001":"⠣","001001":"⠤","101001":"⠥","011001":"⠦","111001":"⠧",
        "000101":"⠨","100101":"⠩","010101":"⠪","110101":"⠫","001101":"⠬","101101":"⠭","011101":"⠮","111101":"⠯",
        "000011":"⠰","100011":"⠱","010011":"⠲","110011":"⠳","001011":"⠴","101011":"⠵","011011":"⠶","111011":"⠷",
        "000111":"⠸","100111":"⠹","010111":"⠺","110111":"⠻","001111":"⠼","101111":"⠽","011111":"⠾","111111":"⠿"
    }

    getImage = requests.get(input("Enter URL >> "), stream=True)
    if getImage.status_code == 200:

        s = float(input("Enter a detail scalar\n (Between 0.8 [Finer] and 1.2 [Rougher]) Default : 0.95 >> ") or "0.95")

        image = Image.open(io.BytesIO(getImage.content)).convert("RGBA")
        image = ImageEnhance.Contrast(ImageOps.grayscale(image.filter(
        ImageFilter.Kernel((3, 3),(
            1/16, 1/8, 1/16, 
            1/8, 1/4,  1/8, 
            1/16, 1/8, 1/16), 1, 0))).filter(
                ImageFilter.Kernel((3, 3),(
                    -1*s,-1*s,-1*s, 
                    -1*s,float(input("Enter a brightness level\n (Between 7.0 and 11.0) Default : 9.0 >> ") or "9.0"),-1*s, 
                    -1*s,-1*s,-1*s), 1, 0))).enhance(
                        float(input("Enter a contrast level\n (Between 0.0 and 2.0) Default : 1.05 >> ") or "1.05")).convert("RGB").filter(
                            ImageFilter.GaussianBlur(radius=float(input("Enter a blur radius | Default: 0.0 >> ")  or "0.0")))
                            
        width, height = image.size

        stretch = float(input("Enter a width scalar | (Discord: 1.33) >> ") or "1.33")

        if(((width//2)*stretch) * (height//3) > 1900): 
            print("Image too large, might not work on discord...")
            print("Width: "+str(width),"Height: "+str(height))
            print(((width//2)*stretch) * (height//3),"Characters Long!")
            print("Suggested Scale:",((10*np.sqrt(19))/(np.sqrt((width//2)*stretch * (height//3)))))

        unsatisfied = 1
        while unsatisfied:
            scale = float(input("Enter a scale | Default: 1.0 >> ") or "1.0")
            limit = [int(input("Enter left offset | Default: 0 >> ") or "0"), int(input("Enter right offset | Default: 0 >> ") or "0")]

            image = image.resize((int((width*stretch)*scale),int(height*scale)))
            stretch = 1
            width, height = image.size

            if(((width//2)*stretch) * (height//3) > 1900): 
                print("Image still too large, might not work on discord...")
                print("Width: "+str(width),"Height: "+str(height))
                print(((width//2)*stretch) * (height//3),"Characters Long!")
                print("Suggested Scale:",((10*np.sqrt(19))/(np.sqrt((width//2)*stretch) * np.sqrt(height//3))))

            print(((width//2)*stretch) * (height//3),"Characters Long!")
            unsatisfied = (input("Continue? [Y/n] >> ") or "y") in ["no","NO"]
        string = ""
        for y in range(0,height-3,3):
            for x in range(2*limit[0],width-2-(2*limit[1]),2):
                string += (brailleDict[(
                    str(int(getPix(x,    y,image)>125)) + str(int(getPix(x,  y+1,image)>125))+
                    str(int(getPix(x,  y+2,image)>125)) + str(int(getPix(x+1,y  ,image)>125))+
                    str(int(getPix(x+1,y+1,image)>125)) + str(int(getPix(x+2,y+2,image)>125))
                )])
            string += "\n"
        
        return string

if __name__ == '__main__':
    
    data = main()
    with open((input("Enter filename without extension | Default: output >> ") or "output").split(".")[0] + ".txt", "w", encoding='utf8') as f:
        f.write(data)
    input("Press ENTER to exit")

"""
⠿⠿⠿⠿⠿⠿⠿⠿⠿⠟⠛⠉⠉⠉⠉⠙⠛⠛⠻⠿⠿⠿⠿⠿⠿⠿⠿⠿
⠿⠿⠿⠿⠿⠿⠿⠟⠋⠀⠠⠴⠶⠶⠶⠶⠶⠤⠄⠀⠈⠹⠿⠿⠿⠿⠿⠿
⠿⠿⠿⠿⠿⠿⠟⠁⠠⠾⠿⠿⠿⠿⠿⠿⠿⠿⠿⠶⠄⠀⠨⠿⠿⠿⠿⠿
⠿⠿⠿⠿⠿⠟⠃⠠⠾⠿⠿⠿⠟⠛⠩⠭⠥⠤⠤⠤⠄⠀⠀⠈⠻⠿⠿⠿
⠿⠿⠿⠟⠛⠋⠀⠠⠿⠿⠿⠟⠠⠼⠿⠿⠿⠿⠿⠿⠿⠿⠷⠄⠀⠹⠿⠿
⠿⠟⠁⠠⠤⠄⠀⠸⠿⠿⠿⠇⠀⠻⠿⠿⠿⠿⠿⠿⠿⠿⠿⠟⠀⠠⠿⠿
⠿⠇⠠⠾⠿⠏⠀⠸⠿⠿⠿⠟⠀⠈⠙⠻⠿⠿⠿⠿⠟⠛⠋⠀⠀⠰⠿⠿
⠿⠇⠰⠿⠿⠇⠀⠸⠿⠿⠿⠿⠷⠤⠄⠀⠀⠀⠠⠤⠤⠴⠶⠦⠴⠿⠿⠿
⠿⠇⠸⠿⠿⠇⠀⠸⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠧⠿⠿⠿⠿
⠿⠇⠸⠿⠿⠇⠀⠸⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠇⠹⠿⠿⠿
⠿⠇⠨⠿⠿⠇⠀⠸⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠇⠸⠿⠿⠿
⠿⠇⠀⠻⠿⠇⠀⠸⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠟⠡⠿⠿⠿⠿
⠿⠿⠆⠀⠉⠁⠀⠸⠿⠿⠿⠿⠿⠟⠛⠛⠛⠛⠻⠿⠿⠿⠿⠼⠿⠿⠿⠿
⠿⠿⠿⠿⠶⠆⠀⠨⠿⠿⠿⠿⠿⠇⠐⠀⠀⠠⠿⠿⠿⠟⠣⠿⠿⠿⠿⠿
⠿⠿⠿⠿⠿⠿⠄⠠⠿⠿⠿⠿⠟⠣⠼⠆⠀⠘⠻⠿⠟⠋⠰⠿⠿⠿⠿⠿
⠿⠿⠿⠿⠿⠿⠷⠄⠈⠉⠉⠉⠠⠴⠿⠿⠶⠤⠤⠤⠤⠶⠿⠿⠿⠿⠿⠿
⠿⠿⠿⠿⠿⠿⠿⠿⠿⠷⠶⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿
"""
