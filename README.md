# html-color-contrsast
Developed to iterate through html code within the source code of a project and determine if any background-text color combinations are not WCAG AA compliant. 

contrast.py:
This code iterates through the html files in a source code folder and extracts the background-text color pairings. With those pairings, it determines if the pairing is AA compliant by calculating the contrast ratio. In order to utilize this code, make sure to enter the correct path to your code (indicated in the comments).

website.html:
This is the example of html code format I used to extract the color pairings. Since there are many ways to format html color (not to mention css files), use the contrast.py as a sort of building block to analyzing your code's color compliance. 

The original purpose of this project was to address the compliance issue of JupyterLab, but I hope that this code can also be used in other projects.
