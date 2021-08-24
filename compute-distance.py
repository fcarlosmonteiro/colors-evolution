from colormath.color_objects import HSVColor, sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
import colorsys
from wcag_contrast_ratio.contrast import rgb

# black Color
color1_rgb = sRGBColor(0.0, 0.0, 0.0)
# white Color
color2_rgb = sRGBColor(1.0, 1.0, 1.0)

#--------------HSV to LabColor----------------------#
corHSV=HSVColor(240,100,100)
teste= convert_color(corHSV,LabColor)
print(teste)


#--------------COMPUTE THE DIFF----------------------#
# Convert from RGB to Lab Color Space
color1_lab = convert_color(color1_rgb, LabColor)
#print(color1_lab)
# Convert from RGB to Lab Color Space
color2_lab = convert_color(color2_rgb, LabColor)
# Find the color difference
delta_e = delta_e_cie2000(color1_lab, color2_lab)
#print ("The difference between the 2 color = ", delta_e)
#----------------------------------------------------#

def rgb2hsv(red,green,blue):
    #rgb normal: range (0-255, 0-255, 0.255)
      
    #get rgb percentage: range (0-1, 0-1, 0-1 )
    red_percentage= red / float(255)
    green_percentage= green/ float(255)
    blue_percentage=blue / float(255)
 
    #get hsv percentage: range (0-1, 0-1, 0-1)
    color_hsv_percentage=colorsys.rgb_to_hsv(red_percentage, green_percentage, blue_percentage) 
    print('color_hsv_percentage: ', color_hsv_percentage)
   
    #get normal hsv: range (0-360, 0-255, 0-255)
    color_h=round(360*color_hsv_percentage[0])
    color_s=round(255*color_hsv_percentage[1])
    color_v=round(255*color_hsv_percentage[2])
    color_hsv=(color_h, color_s, color_h)
    return(color_hsv_percentage)
    print('color_hsv: ', color_hsv)


#cores bases
def find_base(color):
    if color[2]<0.2:
        return "Black"
    elif color[2]>0.8:
        return "White"
    elif color[1]<0.25:
        return "Grey"
    else: return "not found"

#matiz
def check_hue(color):
    if color[0]<30:
        return "Red"
    elif color[0]<90:
        return "Yellow"
    elif color[0]<150:
        return "Green"
    elif color[0]<210:
        return "Cyan"
    elif color[0]<270:
        return "Blue"
    elif color[0]<330:
        return "Magenta"
    else:
        return "not found"

corHSV=rgb2hsv(red=128,green=128,blue=128)
print(find_base(corHSV))
