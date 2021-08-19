from colormath.color_objects import sRGBColor, LabColor, HSVColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
import math

# Red Color
color1_rgb = sRGBColor(0.0, 0.0, 1.0)
# Blue Color
color2_rgb = sRGBColor(0.0, 0.0, 0.9)

#print(color1_rgb.get_rgb_hex())
#print(color2_rgb.get_rgb_hex())


#--------------COMPUTE THE DIFF----------------------#
# Convert from RGB to Lab Color Space
color1_lab = convert_color(color1_rgb, LabColor)
# Convert from RGB to Lab Color Space
color2_lab = convert_color(color2_rgb, LabColor)
# Find the color difference
delta_e = delta_e_cie2000(color1_lab, color2_lab)
print ("The difference between the 2 color = ", delta_e)
#----------------------------------------------------#

# Check Hue
color1_Hue = convert_color(color1_rgb, HSVColor)
color2_Hue = convert_color(color2_rgb, HSVColor)
print(color1_Hue.get_value_tuple()[0])

def check_hue(corB):
    #angles
    print(color1_Hue.get_value_tuple()[0])
    #gree 60 - 150
    #blue 180 - 270
    #red 30 - 300
    return
