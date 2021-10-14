import wcag_contrast_ratio as contrast
import utils
import ratio

'''calcula o constrast ratio da vizinhança e retorna a cor que passar
'''
def objective_function(current_color,neighborhood, main_color):
    ratioNeighbor=0
    ratioNeighborList=[]
    for index,n in enumerate(neighborhood):
        ratioNeighbor=ratio.ratio_test(main_color,n)
        ratioNeighborList.append(ratioNeighbor)
        #print("-->",n,ratioNeighbor)
        valueWCAG=contrast.passes_AA(ratioNeighbor)
        if valueWCAG==True:
            print("a new solution has been found", n,ratioNeighbor)
            return n,valueWCAG,ratioNeighbor
        elif index+1==len(neighborhood):
            #retornar vizinho que mais se aproxima de ser true
            nx = find_nearest_neighbor(ratioNeighborList)
            n = neighborhood[ratioNeighborList.index(nx)]
            return n,valueWCAG,ratioNeighbor

'''calcula o ratio mais proximo de se tornar true
'''
def find_nearest_neighbor(list):
    reference=4.5
    absolute_difference_function = lambda list_value : abs(list_value - reference)
    closest_value = min(list, key=absolute_difference_function)
    return closest_value