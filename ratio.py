import wcag_contrast_ratio as contrast
import utils

def ratio_test(main_color,n):
    c1=main_color
    c2=utils.convert_scale(n)
    
    ratio = contrast.rgb(c1,c2)
    return ratio