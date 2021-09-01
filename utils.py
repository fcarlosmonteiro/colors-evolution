from PIL import Image, ImageDraw
import extcolors
import colorsys
import math

'''
get an image and extract a set of colors
example: [((217, 59, 34), 983059), ((244, 243, 241), 58107)
'''
def get_colors(path):
    colors, pixel_count = extcolors.extract_from_path(path)
    #palette="extcolors "+ path +" --image 5"
    #os.system(palette)
    print("Number of colors: ",len(colors)-1)
    return colors

'''find a base from a group of colours
'''
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

def find_main_color(colors):
    frequency=[]
    #print("main--",colors[0][0])
    for color in colors:
        frequency.append(color[1])
    return color

'''
get a RGB colors and convert to RGB
'''
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

def convert_scale255(color):
    result=[]
    try:
        for x in color:
            r=x*255
            result.append(int(r))
    except:
        for x in color[0]:
            r=x*255
            result.append(int(r))
    return result

def convert_scale(color):
    result=[]
    for x in color:
        r=x/255.0
        result.append(round(r,2))
    return result

def image_result(colors, size, filename):
    columns = 5
    width = int(min(len(colors), columns) * size)
    height = int((math.floor(len(colors) / columns) + 1) * size)

    result = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    canvas = ImageDraw.Draw(result)
    for idx, color in enumerate(colors):
        x = int((idx % columns) * size)
        y = int(math.floor(idx / columns) * size)
        canvas.rectangle([(x, y), (x + size - 1, y + size - 1)],
                         fill=color)

    result.save(filename, "PNG")