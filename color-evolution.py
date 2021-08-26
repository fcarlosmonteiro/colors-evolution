import extcolors
import colorsys
import random
from colormath.color_objects import ColorBase, HSVColor, sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from networkx.classes.function import neighbors
import wcag_contrast_ratio as contrast

#get an image and extract a set of colors
def get_colors(path):
    colors, pixel_count = extcolors.extract_from_path(path)
    return colors

def rgb2hsv(colors):
    #rgb normal: range (0-255, 0-255, 0.255)
    colors_hsv=[]
    for color in colors: 
        #get rgb percentage: range (0-1, 0-1, 0-1 )
        red_percentage= color[0][0] / float(255)
        green_percentage= color[0][1] / float(255)
        blue_percentage=color[0][2] / float(255)
    
        #get hsv percentage: range (0-1, 0-1, 0-1)
        color_hsv_percentage=colorsys.rgb_to_hsv(red_percentage, green_percentage, blue_percentage) 
        #print('color_hsv_percentage: ', color_hsv_percentage)
    
        #get normal hsv: range (0-360, 0-255, 0-255)
        color_h=round(360*color_hsv_percentage[0])
        color_s=round(255*color_hsv_percentage[1])
        color_v=round(255*color_hsv_percentage[2])
        color_hsv=(color_h, color_s, color_h)
        colors_hsv.append(color_hsv_percentage)
    return colors_hsv
    #print('color_hsv: ', color_hsv)

def find_base(colors):
    for color in colors:
        if color[2]<0.2:
            #return "Black"
            return color
        elif color[2]>0.8:
            #return "White"
            return color
        elif color[1]<0.25:
            #return "Grey"
            return color
        else: 
            return "not found"

def convert_scale255(color):
    result=[]
    for x in color:
        r=x*255.0
        result.append(round(r,2))
    return result

def convert_scale(color):
    result=[]
    for x in color:
        r=x/255.0
        result.append(round(r,2))
    return result
    
#recebe a cor base e o vetor de cores
def compute_contrast_ratio(corBase, colors):
    for c in colors:
        initial_color=convert_scale(c[0])
        ratio=contrast.rgb(corBase, initial_color)
        #print("Cor 1:"+str(corBase)+" e Cor 2:"+str(initial_color)+" - contrast ratio = "+str(round(ratio,2)))
        valueWCAG=contrast.passes_AA(ratio)
        if valueWCAG==False:
            return initial_color,ratio
        else:
            pass

def generate_neighborhood(current):
    neighborhood=[]
    neighbor1=current.copy()
    neighbor1[0]=random.uniform(0,1)
    #neighbor[0]=random.randint(0,255)
    neighborhood.append(neighbor1)
    
    #neighbor2=current.copy()
    #neighbor2[1]=neighbor2[1]+(neighbor2[1]*0.5)
    #neighborhood.append(neighbor2)
    
    return neighborhood

def objective_function(current,colorBase,neighborhood):
    for n in neighborhood:
        ratio=contrast.rgb(colorBase, n)
        valueWCAG=contrast.passes_AA(ratio)
        print("Cor 1:"+str(colorBase)+" e Cor 2:"+str(n)+" - contrast ratio = "+str(round(ratio,2))+ " contrast test: ",valueWCAG)
        obj_value=ratio
        if current[1]<obj_value:
            print("#############mudou################")
            current=n,obj_value
    return current

def main():
    path="logo.png"
    colors=get_colors(path)
    colors_hsv=rgb2hsv(colors)
    #colorBase=find_base(colors_hsv)
    colorBase=(1,1,1)
    #initial solution have the color and ratio
    initial_sol=compute_contrast_ratio(colorBase, colors)
    current=initial_sol

    for i in range(1,5):
        #print("------------->",current)
        neighborhood=generate_neighborhood(current[0])
        neighborhood=[[0,0,0]]
        current=objective_function(current,colorBase,neighborhood)
       
    print()

if __name__ == "__main__":
    main()