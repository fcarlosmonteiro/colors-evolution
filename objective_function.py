import wcag_contrast_ratio as contrast
import utils

'''calcula o constrast ratio da vizinhança e retorna a cor que passar
'''
def objective_function(current_color,neighborhood, main_color):
    for n in neighborhood:
        ratioNeighbor=contrast.rgb(utils.convert_scale(main_color), utils.convert_scale(n))
        valueWCAG=contrast.passes_AA(ratioNeighbor)
        if valueWCAG==True:
            n=current_color
            return n,valueWCAG
        else:
            #retornar vizinho que mais se aproxima de ser true
            pass    

'''calcula o ratio mais proximo de se tornar true
'''
def find_nearest_neighbor(a,b):
    reference=4.5
    a_list=[a,b]
    absolute_difference_function = lambda list_value : abs(list_value - reference)
    closest_value = min(a_list, key=absolute_difference_function)
    return closest_value