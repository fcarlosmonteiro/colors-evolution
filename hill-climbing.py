from os import PRIO_USER
import random

from networkx.drawing.layout import rescale_layout
import utils
import objective_function as of
import wcag_contrast_ratio as contrast


global result
global result_ratio
global hex_result
result=[]
result_ratio=[]
hex_result=[]

'''calcula o contraste, caso a cor não passe o HC é iniciado
e executa enquanto nao encontrar uma cor.
'''
def test_constrat_ratio(main_color,colors):
    result.append(main_color)
    result_ratio.append(0.0)
    print("\nBase Color:", main_color)
    main_color=utils.convert_scale(main_color)
    for idx,c in enumerate(colors):
        print("=============Starting testing for Color "+str(idx+1)+"=============")
        current_color=c[0]
        ratio=contrast.rgb(main_color, utils.convert_scale(current_color))
        valueWCAG=contrast.passes_AA(ratio)
        while valueWCAG==False:
            print("Hill Climbing is starting for color "+str(idx+1)+"...")
            current_color,valueWCAG,ratioNeighbor=hill_climbing(current_color,main_color)
        else:
            try:
                ratio=ratioNeighbor
            except:
                pass
            print("=============Color "+str(idx+1)+" passed the AA test=============")
            print(current_color, ratio)
            result.append(current_color)
            result_ratio.append(ratio)
            try: del ratioNeighbor
            except: pass
    return current_color

'''processo algoritmo subida da encosta
'''
def hill_climbing(current_color,main_color):
    ratioNeighbor=0
    fit_value=[]
    neighborhood=generate_neighborhood(current_color)
    print("Current",current_color)
    print("Neighborhood",neighborhood)
    current,valueWCG,ratioNeighbor=of.objective_function(current_color,neighborhood,main_color)
    return current,valueWCG,ratioNeighbor

'''gera as cores vizinhas, porém está fugindo da matiz original
'''    
def generate_neighborhood(current):
    neighborhood=[]
    c=list(current)
    neighbor1=c.copy()
    neighbor1[0]=random.randint(0,255)
    neighborhood.append(neighbor1)
    
    neighbor2=c.copy()    
    neighbor2[1]=random.randint(0,255)
    neighborhood.append(neighbor2)
    
    neighbor3=c.copy()
    neighbor3[0]=random.randint(0,255)    
    neighbor3[1]=random.randint(0,255)
    neighbor3[2]=random.randint(0,255)

    neighborhood.append(neighbor3)
    
    return neighborhood


if __name__ == '__main__':
    path="./image-dataset/4.jpeg"
    
    colors=utils.get_colors(path)
    print("Initial Colors",colors)
    initial_colors=utils.reshape_colors(colors)
    name="initial"
    utils.plot_palette(name,initial_colors)
    
    main_color,colors=utils.get_main_color(colors)
    print(main_color)
    test_constrat_ratio(main_color,colors)
    
    utils.save_xls(result,result_ratio)
    
    print("Results: ",result)    
    namer="results"
    utils.plot_palette(namer,result)