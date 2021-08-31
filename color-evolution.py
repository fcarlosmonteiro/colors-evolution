import extcolors
import colorsys
import os
import random
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from networkx.classes.function import neighbors
import wcag_contrast_ratio as contrast

global result,suggested_colors 
result=[]
suggested_colors=[]

#get an image and extract a set of colors
def get_colors(path):
    colors, pixel_count = extcolors.extract_from_path(path)
    palette="extcolors "+ path +" --image 5"
    os.system(palette)
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
    
        #get normal hsv: range (0-360, 0-255, 0-255)
        color_h=round(360*color_hsv_percentage[0])
        color_s=round(255*color_hsv_percentage[1])
        color_v=round(255*color_hsv_percentage[2])
        color_hsv=(color_h, color_s, color_h)
        colors_hsv.append(color_hsv_percentage)
    return colors_hsv

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
    try:
        for x in color:
            r=x*255.0
            result.append(round(r,2))
    except:
        for x in color[0]:
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
    findcolor=False
    for idx,c in enumerate(colors):
        initial_color=convert_scale(c[0])
        ratio=contrast.rgb(corBase, initial_color)
        
        valueWCAG=contrast.passes_AA(ratio)
        #print("Cor 1:"+str(corBase)+" e Cor 2:"+str(initial_color)+" - contrast ratio = "+str(round(ratio,2))+ " contrast test: ",valueWCAG)
        if valueWCAG==False:
            #print("Cor 1:"+str(corBase)+" e Cor 2:"+str(initial_color)+" - contrast ratio = "+str(round(ratio,2))+ " contrast test: ",valueWCAG)
            print("Hill Climbing is starting for color "+str(idx+1)+"...")
            hill_climbing(initial_color,ratio,corBase,findcolor)
            #return initial_color,ratio
        else:
            print("=============Color "+str(idx+1)+" passed the AA test=============")
            result.append(initial_color)

def hill_climbing(initial_color,ratio,corBase,findcolor):
    for i in range(1,6):
        #print("...")
        neighborhood=generate_neighborhood(initial_color)
        initial_color, findcolor=objective_function(initial_color,ratio,corBase,neighborhood)
        if findcolor==False:
            pass
        else:
            break
    print("new color not found")

def generate_neighborhood(current):
    neighborhood=[]
    currentRGB=convert_scale255(current)
    
    neighbor1=currentRGB.copy()
    neighbor1[0]=random.randint(0,255)
    
    neighborhood.append(neighbor1)
    
    return neighborhood

def objective_function(initial_color,ratio,corBase,neighborhood):
    for n in neighborhood:
        n=convert_scale(n)
        ratioNeighbor=contrast.rgb(corBase, n)
        valueWCAG=contrast.passes_AA(ratioNeighbor)
        #print("**Base color:"+str(corBase)+" and neighbor:"+str(n)+" - contrast ratio = "+str(round(ratioNeighbor,2))+ " contrast test: ",valueWCAG)
        obj_value=ratioNeighbor
        if valueWCAG==True:
            #n=convert_scale255(n)
            initial_color=n,obj_value
            result.append(n)
            findcolor=True
            print("=============HC suggested a new color: "+str(convert_scale255(n))+ "and it passed the AA test=============")
            suggested_colors.append(n)
            return initial_color,findcolor
        else:
            findcolor=False
            new=find_nearest_neighbor(ratio,obj_value)
            if new == ratio: initial_color=initial_color
            else: initial_color=n
            return initial_color,findcolor

def find_nearest_neighbor(a,b):
    reference=4.5
    a_list=[a,b]
    absolute_difference_function = lambda list_value : abs(list_value - reference)
    closest_value = min(a_list, key=absolute_difference_function)
    return closest_value


def main():
    path="./image-dataset/5.jpeg"
    result.clear()
    suggested_colors.clear()
    colors=get_colors(path)
    #print("colors",colors)
    qnt_colors=len(colors)-1
    colors_hsv=rgb2hsv(colors)
    colorBase=find_base(colors_hsv)
    compute_contrast_ratio(colorBase, colors)
    print("Cores que passaram no teste: "+str(result))
    print("Cores recomendadas:" +str(suggested_colors))
    

if __name__ == "__main__":
    #global best_result
    best_result=[]
    for interation in range(1,4):
        print("------------------------------Repetition: "+str(interation)+"------------------------------")
        main()
        if len(result)>len(best_result):
            best_result=result
        else:
            pass
    print()
    print("The best found solution: ",best_result)
        