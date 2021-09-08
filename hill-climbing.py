from os import PRIO_USER
import random

from networkx.drawing.layout import rescale_layout
import utils
import wcag_contrast_ratio as contrast

global result
result=[]

'''calcula o contraste, caso a cor não passe o HC é iniciado
e executa enquanto nao encontrar uma cor.
'''
def test_constrat_ratio(main_color,colors):
    main_color=utils.convert_scale(main_color)
    for idx,c in enumerate(colors):
        current_color=c[0]
        ratio=contrast.rgb(main_color, utils.convert_scale(c[0]))
        valueWCAG=contrast.passes_AA(ratio)
        while valueWCAG==False:
            print("Hill Climbing is starting for color "+str(idx+1)+"...")
            valueWCAG=hill_climbing(current_color,main_color)
        else:
            print("=============Color "+str(idx+1)+" passed the AA test=============")
            result.append(current_color)
    return current_color

'''processo algoritmo subida da encosta
'''
def hill_climbing(current_color,main_color):
    fit_value=[]
    neighborhood=generate_neighborhood(current_color)
    print("Current",current_color)
    print("Neighborhood",neighborhood)
    current,valueWCG=objective_function(current_color,neighborhood,main_color)
    return valueWCG

'''gera as cores vizinhas, porém está fugindo da matiz original
'''    
def generate_neighborhood(current):
    neighborhood=[]
    c=list(current)
    neighbor1=c.copy()
    neighbor1[0]=random.randint(0,255)
    neighbor1[1]=random.randint(0,255)
    neighborhood.append(neighbor1)
    
    neighbor2=c.copy()    
    neighbor2[1]=random.randint(0,255)
    neighborhood.append(neighbor2)
    
    neighbor3=c.copy()    
    neighbor3[2]=random.randint(0,255)
    neighborhood.append(neighbor3)
    
    return neighborhood

'''calcula o constrast ratio da vizinhança e retorna a cor que passar
'''
def objective_function(current_color,neighborhood, main_color):
    #color=utils.convert_scale(color)
    for n in neighborhood:
        ratioNeighbor=contrast.rgb(utils.convert_scale(main_color), utils.convert_scale(n))
        valueWCAG=contrast.passes_AA(ratioNeighbor)
        if valueWCAG==True:
            n=current_color
            return n,valueWCAG
        else:
            #retornar vizinho que mais se aproxima de ser true
            pass    


def find_nearest_neighbor(a,b):
    reference=4.5
    a_list=[a,b]
    absolute_difference_function = lambda list_value : abs(list_value - reference)
    closest_value = min(a_list, key=absolute_difference_function)
    return closest_value


if __name__ == '__main__':
    path="./image-dataset/1.jpeg"
    colors=utils.get_colors(path)
    print("Initial Colors",colors)
    main_color,colors=utils.get_main_color(colors)
    test_constrat_ratio(main_color,colors)
    print("Results: ",result)