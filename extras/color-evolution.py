import random
import utils
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from networkx.classes.function import neighbors
import wcag_contrast_ratio as contrast

global result,suggested_colors 
result=[]
suggested_colors=[]
    
#recebe a cor base e o vetor de cores
def compute_contrast_ratio(corBase, colors):
    findcolor=False
    for idx,c in enumerate(colors):
        initial_color=utils.convert_scale(c[0])
        ratio=contrast.rgb(corBase, initial_color)
        
        valueWCAG=contrast.passes_AA(ratio)
        #print("Cor 1:"+str(corBase)+" e Cor 2:"+str(initial_color)+" - contrast ratio = "+str(round(ratio,2))+ " contrast test: ",valueWCAG)
        if valueWCAG==False:
            #print("Cor 1:"+str(corBase)+" e Cor 2:"+str(initial_color)+" - contrast ratio = "+str(round(ratio,2))+ " contrast test: ",valueWCAG)
            print("Hill Climbing is starting for color "+str(idx+1)+"...")
            hill_climbing(initial_color,ratio,corBase,findcolor)
        else:
            print("=============Color "+str(idx+1)+" passed the AA test=============")
            result.append(tuple(utils.convert_scale255(initial_color)))

def hill_climbing(initial_color,ratio,corBase,findcolor):
    for i in range(1,101):
        neighborhood=generate_neighborhood(initial_color)
        initial_color, findcolor=objective_function(initial_color,ratio,corBase,neighborhood)
        if findcolor==False:
            pass
        else:
            break

def generate_neighborhood(current):
    neighborhood=[]
    currentRGB=utils.convert_scale255(current)
    
    neighbor1=currentRGB.copy()
    neighbor1[0]=random.randint(0,255)
    neighbor1[1]=random.randint(0,255)
    neighborhood.append(neighbor1)
    
    neighbor2=currentRGB.copy()    
    neighbor2[1]=random.randint(0,255)
    neighborhood.append(neighbor2)
    
    neighbor3=currentRGB.copy()    
    neighbor3[2]=random.randint(0,255)
    neighborhood.append(neighbor3)
    
    return neighborhood

def objective_function(initial_color,ratio,corBase,neighborhood):
    for n in neighborhood:
        n=utils.convert_scale(n)
        ratioNeighbor=contrast.rgb(corBase, n)
        valueWCAG=contrast.passes_AA(ratioNeighbor)
        #print("**Base color:"+str(corBase)+" and neighbor:"+str(n)+" - contrast ratio = "+str(round(ratioNeighbor,2))+ " contrast test: ",valueWCAG)
        obj_value=ratioNeighbor
        if valueWCAG==True:
            initial_color=n,obj_value
            result.append(tuple(utils.convert_scale255(n)))
            findcolor=True
            print("=============HC suggested a new color: "+str(utils.convert_scale255(n))+ " and it passed the AA test=============")
            suggested_colors.append(utils.convert_scale255(n))
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
    path="./image-dataset/4.jpeg"
    result.clear()
    suggested_colors.clear()
    colors=utils.get_colors(path)
    print("Initial colors",colors)
    qnt_colors=len(colors)-1
    colors_hsv=utils.rgb2hsv(colors)
    colorBase=utils.find_base(colors_hsv)
    compute_contrast_ratio(colorBase, colors)
    print("Cores que passaram no teste: "+str(result))
    print("Cores recomendadas:" +str(suggested_colors))        

if __name__ == "__main__":
    best_result=[]
    best_recommended_colors=[]
    for interation in range(1,2):
        print("------------------------------Repetition: "+str(interation)+"------------------------------")
        main()
        if len(result)>len(best_result):
            best_result=result
            best_recommended_colors=suggested_colors
        else:
            pass
    print()
    print("The best found solution: ",str(best_result))
    
    #print palett result
    a=tuple(best_result)
    utils.image_result(a,200,"result")
    #color,size,filename
