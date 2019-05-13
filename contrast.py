from bs4 import BeautifulSoup
import matplotlib.colors as colors
import os
from numpy import random

"""
rgb: string of hexadecimal value with only 3 digits (#***)
Converts 3 digit hexadecimal value to 6 digit hexadecimal value
Returns string of 6 digit hexadecimal value
"""
def toSix(rgb):
    h = rgb[0]
    r = rgb[1]
    g = rgb[2]
    b = rgb[3]
    return h + r + r + g + g + b + b


"""
h: string of hexadecimal value
Converts hexadecimal color value to rgb color
If h is 3 digit, convert to 6 digit first.
Returns rgb color format(tuple)
"""
def hexToRGB(h):
    h = h.lower()
    if len(h) == 4:
        h = toSix(h)
    return colors.to_rgb(h)


"""
rgb: color in rgb color tuple form
Utilizing equation from https://www.w3.org/TR/2008/REC-WCAG20-20081211/#relativeluminancedef
Calculates relative luminance
Returns float for relative luminance
"""
def brightness(rgb):
    if rgb[0] <= 0.03928:
        r = rgb[0]/12.92
    else:
        r = ((rgb[0] + 0.055)/1.055)**2.4
    if rgb[1] <= 0.03928:
        g = rgb[1]/12.92
    else:
        g = ((rgb[1] + 0.055)/1.055)**2.4
    if rgb[2] <= 0.03928:
        b = rgb[2]/12.92
    else:
        b = ((rgb[2] + 0.055)/1.055)**2.4

    return 0.2126*r + 0.7152*g + 0.0722*b


"""
rgb_1, rgb_2: string of hexadecimal values for which the contrast is desired
Calculate relative luminance of each color
Utilizing equation from https://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef
Calculates contrast ration between two colors
Returns rounded float contrast ratio
"""
def contrast(rgb_1, rgb_2):
    text_light = brightness(hexToRGB(rgb_1))
    back_light = brightness(hexToRGB(rgb_2))
    if text_light > back_light:
        return round((text_light + 0.05)/(back_light + 0.05), 3)
    else:
        return round((back_light + 0.05)/(text_light + 0.05), 3)


"""
soup: BeautifulSoup object of parsed file
Creates a dict with each key representing each background-text color pairing in html file
Once file is parsed for all pairs, return dict
"""
def extractColors(soup):
    fcolors = dict()
    for t in soup.find_all():
        # print(t.name)
        # print(t.attrs)  # gives you the class of the div to pair with the style tag content
        # print(t)
        # print()
        
        tlst = t.prettify().split("\n") #turn unicode string into line by line iteratable
        if t.name=="style":
            recent = ""
            for line in tlst:
                if len(line)>0 and line[0]=='.':
                    i = line.find('{')
                    recent = line[1:i]
                    fcolors[recent] = []
                # need to include possibility of commented out color
                elif "color:" in line or "background:" in line or "background-color:" in line:
                    h = line.find('#')
                    c = line[h:]
                    s = c.find(";")
                    fcolors[recent].append(c[0:s])
        else:
            for k,v in t.attrs.items():
                if k == "style":
                    i = t.prettify().find('>')
                    # print(t.prettify()[0:i+1])
                elif k == "class":
                    j = t.prettify().find('>')
                    # print(t.prettify()[0:j+1])
    return fcolors


"""
ratio: upper contrast ratio requirement given by user (4.5 if not given)
c: color for which a color pairing is desired
Randomly generates a color to match with c that meets ratio requirements
Returns color that has been selected
"""
def rgb_rand(ratio, c):
    while True:
        r = random.uniform(0.0,1.0)
        g = random.uniform(0.0,1.0)
        b = random.uniform(0.0,1.0)
        rgb = (r, g, b)
        
        cont = contrast(c, colors.to_hex(rgb))
        if cont > 4.5:
            if ratio == 4.5 or (ratio != 4.5 and cont < ratio):
                return rgb


"""
c: color requested for pairing
rt: upper contrast ratio requirement
Called when an alternate color pairing is requested for c by user
Returns hexadecimal value of color selected
"""
def altColor(c, rt=4.5):
    #second param is maximum contrast ratio, else just compliant
    if rt < 4.5:
        print("REQUESTED BRIGHTNESS LESS THAN 4.5!")
        return ""

    rgb = rgb_rand(rt, c)
    return colors.to_hex(rgb)
    

def main():
    # iterates through all files in source code (replace "./jupyterlab/" with correct path to desired source code)
    for root, dirs, files in os.walk("./jupyterlab/"):
        for filename in files:
            if filename.endswith(".html"):
                # print(os.path.join(root, filename))
                f = open(os.path.join(root, filename), 'r')
                soup = BeautifulSoup(f, 'html.parser')
                f.close()
                c = extractColors(soup)
                # prints pairings that are not compliant
                for k, v in c.items():
                    if len(v) == 2 and contrast(v[0], v[1]) < 4.5:
                        print(k, v)
                    elif len(v) == 1 and contrast(v[0], "#000") < 4.5:  # default black
                        print(k, v)

    # user interaction via terminal
    alt = input(
        "Need options for accessible colors?\nEnter one of the values of the non-compliant colors to get alternate pairings for that color: ")
    ratio = input(
        "Want the pairing to be under a certain contrast ratio? Enter a value here. If not, just press enter (NEEDS TO BE OVER 4.5): ")
    if ratio.lower() == "":
        h = altColor(alt)
    else:
        r = float(ratio)
        h = altColor(alt, r)
    print(h)
    again = input("Need another option? (y/n): ")
    while again.lower() == "y":
        if ratio.lower() == "":
            h = altColor(alt)
        else:
            r = float(ratio)
            h = altColor(alt, r)
        print(h)
        again = input("Need another option? (y/n): ")


if __name__== "__main__":
    main()
