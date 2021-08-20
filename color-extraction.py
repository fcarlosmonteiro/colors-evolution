import numpy
import extcolors
import itertools
import wcag_contrast_ratio as contrast

from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

colors, pixel_count = extcolors.extract_from_path("logo.png")

def rgb2hex(color):
    return f"#{''.join(f'{hex(c)[2:].upper():0>2}' for c in color)}"

def convert_scale(color):
    result=[]
    for x in color:
        r=x/255.0
        result.append(round(r,2))
    return result

for x,y in itertools.combinations(colors, 2):
    c=convert_scale(x[0])
    c1=convert_scale(y[0])
    ratio=contrast.rgb(c, c1)
    print("Cor 1:"+str(x[0])+" e Cor 2:"+str(y[0])+" - contrast ratio = "+str(round(ratio,2)))
    print()