import drawSvg as draw
import pandas as pd
import random
import math
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM


image_folder = "./images/"
variables = ["fur_lightness",
             "fur_saturation",
             #"fur_pattern", # "plain", "eye_spot", "stripes", "v", "mask", "snout"
             "eye_distance", 
             "eye_height", 
             "eye_aspect_ratio", 
             #"whiskers", # boolean
             "whisker_length",
             #"whisker_weight",
             "face_aspect_ratio",
             "nose_size",
             #"cheek_tufts",
             #"chin_tufts",
             #"head_tufts",
             "ear_angle", #up/down
             "ear_tip_angle",
             "ear_point",
             "ear_orientation",
             "ear_length"]


def ellipse(cx, cy, rx, ry, stroke_width, stroke, fill):
        ell_path = draw.Path(stroke_width = stroke_width, stroke=stroke, fill = fill)
        ell_path.M(cx-rx, cy)
        ell_path.A(rx, ry, 0, False, False, cx+rx, cy)
        ell_path.A(rx, ry, 0, False, False, cx-rx, cy)
        return ell_path


def dir_point(start, distance, angle):
    return (start[0] + distance*math.cos(math.radians(angle)), 
            start[1] + distance*math.sin(math.radians(angle)))


def mirror(points, cx):
    return [(2*cx-point[0],point[1]) for point in points]


def r_ellipse(angle, rx, ry):
    return ((math.cos(math.radians(angle))/rx)**2+(math.sin(math.radians(angle))/ry)**2)**(-.5)


def draw_catdog(name, param):
    """
    Draws a cat/dog and saves it as an svg
    
    Parameters
    ----------
    name : string
        Filename to save catdog as
    param : dictionary (keys: variables list)
        Variable values for the structure of the face
    """
    full_dwg = draw.Drawing(800, 600)
    dwg = draw.Group()
    full_dwg.append(dwg)
    width = 173*(param["face_aspect_ratio"])**0.5
    height = 173/(param["face_aspect_ratio"])**0.5
    cx = 800/2
    cy = 600/2

    #Ears
    ear_angle = param["ear_angle"]
    ear_tip_angle = param["ear_tip_angle"]
    ear_length = param["ear_length"]
    ear_orientation = param["ear_orientation"]
    ear_point = param["ear_point"]
    eye_height = param["eye_height"]
    eye_width = eye_height*param["eye_aspect_ratio"]
    eye_distance = param["eye_distance"]
    nose_size = param["nose_size"]
    fur_color = "hsl(%i, %i%%, %i%%)" % (45,param["fur_saturation"],param["fur_lightness"])

    dist_to_tip = r_ellipse(ear_angle,width,height)+ear_length
    right_tip = dir_point((cx,cy),dist_to_tip,ear_angle)
    bottom_right = dir_point(right_tip,ear_length*2.2,180+ear_angle+ear_tip_angle*ear_orientation)
    bottom_right_ctrl = dir_point(bottom_right,ear_length*2.2-ear_point,ear_angle+ear_tip_angle*ear_orientation)
    top_right = dir_point(right_tip,ear_length*2.2,180+ear_angle-ear_tip_angle*(1-ear_orientation))
    top_right_ctrl = dir_point(top_right,ear_length*2.2-ear_point,ear_angle-ear_tip_angle*(1-ear_orientation))
    top_left, top_left_ctrl, left_tip, bottom_left_ctrl, bottom_left = mirror([top_right, top_right_ctrl, right_tip, bottom_right_ctrl, bottom_right],cx)
    
    left_ear = draw.Path(stroke_width = 1, stroke='black', fill = fur_color)
    left_ear.M(*bottom_left)
    left_ear.L(*bottom_left_ctrl)
    left_ear.A(ear_point*.8, ear_point*.8, 0, False, True, *top_left_ctrl)
    left_ear.L(*top_left)
    
    right_ear = draw.Path(stroke_width = 1, stroke='black', fill = fur_color)
    right_ear.M(*bottom_right)
    right_ear.L(*bottom_right_ctrl)
    right_ear.A(ear_point*.8, ear_point*.8, 0, False, False, *top_right_ctrl)
    right_ear.L(*top_right)
    
    dwg.draw(left_ear)
    dwg.draw(right_ear)
    
    #Face
    face = ellipse(cx, cy, width, height, stroke_width = 1, stroke='black', fill = fur_color)
    dwg.draw(face)

    #Eyes
    left_eye = ellipse(cx-eye_distance, cy+height/4, eye_width, eye_height, stroke_width = 1, stroke='black', fill = "black")
    right_eye = ellipse(cx+eye_distance, cy+height/4, eye_width, eye_height, stroke_width = 1, stroke='black', fill = "black")
    dwg.draw(left_eye)
    dwg.draw(right_eye)

    #Nose
    dwg.draw(draw.Lines(cx-nose_size, cy+nose_size/3, 
                          cx+nose_size, cy+nose_size/3, 
                          cx,cy-nose_size,
                          close=True, 
                          stroke_width = 1, stroke='black', fill = "black"))

    #Snout
    dwg.draw(draw.Line(cx,cy-nose_size,cx,cy-nose_size*2.5,
                         stroke_width = 2, stroke='black', fill = "black"))

    #Mouth
    mouth = draw.Path(fill = "none", stroke_width = 2, stroke = 'black')
    mouth.M(cx-nose_size*2,cy-nose_size*2.5-4)
    mouth.A(nose_size*2, nose_size*2, 30, False, False, cx, cy-nose_size*2.5)
    mouth.A(nose_size*2, nose_size*2, 150, False, False,  cx+nose_size*2, cy-nose_size*2.5-4)
    dwg.draw(mouth)

    #Whiskers
    whisker_length = param["whisker_length"]
    whiskers = [((cx-34,cy-nose_size-10),195), ((cx-40,cy-nose_size-4),185), ((cx-34,cy-nose_size+2),175),
                ((cx+34,cy-nose_size-10),345), ((cx+40,cy-nose_size-4),355), ((cx+34,cy-nose_size+2),5) ]
    for whisker in whiskers:
        dwg.draw(draw.Line(*whisker[0],*dir_point(whisker[0],whisker_length,whisker[1]), stroke_width = 1, stroke='black', fill = "black"))
    full_dwg.saveSvg(name)


def random_dists(filename):
    """
    Given a Excel filename with a row for each variable and columns for the 
    minimum and maximum, create a dictionary of Uniform distributions for 
    each variable.
    
    Parameters
    ----------
    filename : string
        Number of parameter settings to generate
    
    Returns
    -------
    dictionary (keys = variables, values = Uniform distributions)
        Random distributions for each variable
    """
    df = pd.read_excel(filename,index_col=0)
    return {var[0]: (var[1]["minimum"], var[1]["maximum"], var[1]["step"]) \
            for var in df.iterrows()}


def random_params(n, var_dists):
    """
    Given a distribution for each variable, randomly draw n 
    parameter settings.
    
    Parameters
    ----------
    n : int
        Number of parameter settings to generate
    var_dists : dictionary of distributions
        Probability distributions for each variable
    
    Returns
    -------
    DataFrame of parameters
        The parameter settings
    """
    params = []
    for _ in range(n):
        param = {}
        for var in var_dists:
            steps = int((var_dists[var][1] - var_dists[var][0])/var_dists[var][2])
            param[var] = var_dists[var][0] + (random.randint(0, steps)*var_dists[var][2])
        params.append(param)
    return pd.DataFrame(params)


def all_params(var_settings):
    """
    Given a list of settings for each variable, produce parameter 
    settings for every combination of variable settings
    
    Parameters
    ----------
    var_settings : dictionary (keys: variables list, values: lists)
        All possible settings for each variable

    Returns
    -------
    DataFrame of parameters
        The parameter settings
    """
    params = []
    n = 1
    for i in [len(var) for var in var_settings]:
        n *= i

    for i in range(n):
        param = {}
        mod = 1
        div = 1
        for var in var_settings:
            mod *= len(var)
            param[var] = var_settings[var][int((i%mod)/div)]
            div *= len(var)
        params.append(param)
    return pd.DataFrame(params)


if __name__ == "__main__":
    save_params = True
    '''
    filename = "params.xlsx"
    params = pd.read_excel(filename,dtype=float,index_col=0)
    '''
    var_dists = random_dists("ranges.xlsx")
    params = random_params(50, var_dists)

    for i, param in params.iterrows():
        name = "images/catdog_%i.svg" % i
        draw_catdog(name, param)
    if save_params == True:
        with pd.ExcelWriter("images/saved_params.xlsx") as writer:
            params.to_excel(writer)
    '''
    for i in range(10):
        svgname = "images/random2/catdog_%i.svg" % i
        pngname = "images/random2/png/catdog_%i.png" % i
        drawing = svg2rlg(svgname)
        renderPM.drawToFile(drawing, pngname, fmt="PNG")
    '''

