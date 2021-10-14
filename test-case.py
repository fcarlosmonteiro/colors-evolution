import wcag_contrast_ratio as contrast
import utils


cor1=[217, 59, 34]
cor2=[253, 254, 243]
c1=utils.convert_scale(cor1)
print(c1)
c2=utils.convert_scale(cor2)
print(c2)

ratio = contrast.rgb(c1,c2)
print(ratio)