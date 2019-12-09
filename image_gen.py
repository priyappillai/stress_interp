import svgwrite
import pandas as pd
import numpy as np
import random
import math

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


def style(fill_color=(0,0,0), fill_color_type="rgb", stroke_width=0, stroke_color=(0,0,0), stroke_color_type="rgb"):
    style_str = "fill:%s" %fill_color_type
    if fill_color_type == "hsl":
        style_str = style_str+("(%i, %i%%, %i%%)" %fill_color)
    elif fill_color_type != "none":
        style_str = style_str+("(%i, %i, %i)" %fill_color)
    style_str = style_str+(";stroke-width:%.2f;stroke:%s" %(stroke_width, stroke_color_type))
    if stroke_color_type == "hsl":
        style_str = style_str+("(%i, %i%%, %i%%)" %stroke_color)
    else:
        style_str = style_str+("(%i, %i, %i)" %stroke_color)
    return style_str


def dir_point(start, distance, angle):
    return (start[0] + distance*math.cos(math.radians(angle)), 
            start[1] - distance*math.sin(math.radians(angle)))


def mirror(points, cx):
    return [(2*cx-point[0],point[1]) for point in points]


def r_ellipse(angle, rx, ry):
    return ((math.cos(math.radians(angle))/rx)**2+(math.sin(math.radians(angle))/ry)**2)**(-.5)


def draw_catdog(name, param, dimensions):
    """
    Draws a cat/dog and saves it as an svg
    
    Parameters
    ----------
    name : string
        Filename to save catdog as
    param : dictionary (keys: variables list)
        Variable values for the structure of the face
    """
    dwg = svgwrite.Drawing(filename=name, debug=True)
    width = 173*(param["face_aspect_ratio"])**0.5
    height = 173/(param["face_aspect_ratio"])**0.5
    cx = dimensions[0]/2
    cy = dimensions[1]/2
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
    fur_color = (45,param["fur_saturation"],param["fur_lightness"])
    dist_to_tip = r_ellipse(ear_angle,width,height)+ear_length
    right_tip = dir_point((cx,cy),dist_to_tip,ear_angle)
    bottom_right = dir_point(right_tip,ear_length*2.2,180+ear_angle+ear_tip_angle*ear_orientation)
    bottom_right_ctrl = dir_point(bottom_right,ear_length*2.2-ear_point,ear_angle+ear_tip_angle*ear_orientation)
    top_right = dir_point(right_tip,ear_length*2.2,180+ear_angle-ear_tip_angle*(1-ear_orientation))
    top_right_ctrl = dir_point(top_right,ear_length*2.2-ear_point,ear_angle-ear_tip_angle*(1-ear_orientation))
    top_left, top_left_ctrl, left_tip, bottom_left_ctrl, bottom_left = mirror([top_right, top_right_ctrl, right_tip, bottom_right_ctrl, bottom_right],cx)
    #dwg.add(svgwrite.shapes.Polygon([top_left,left_tip,bottom_left],style=style((45,40,fur_lightness),"hsl",1)))
    #dwg.add(svgwrite.shapes.Polygon([top_right,right_tip,bottom_right],style=style((45,40,fur_lightness),"hsl",1)))
    left_ear = svgwrite.path.Path(d="M %.2f %.2f" %bottom_left, style=style(fur_color,"hsl",1))
    left_ear.push("L %.2f %.2f" %bottom_left_ctrl)
    left_ear.push_arc(top_left_ctrl, 0, (ear_point*.8, ear_point*.8), large_arc = False, absolute = True)
    left_ear.push("L %.2f %.2f" %top_left)
    right_ear = svgwrite.path.Path(d="M %.2f %.2f" %bottom_right, style=style(fur_color,"hsl",1))
    right_ear.push("L %.2f %.2f" %bottom_right_ctrl)
    right_ear.push_arc(top_right_ctrl, 0, (ear_point*.8, ear_point*.8), large_arc = False, angle_dir = "-", absolute = True)
    right_ear.push("L %.2f %.2f" %top_right)
    dwg.add(left_ear)
    dwg.add(right_ear)
    #Face
    dwg.add(dwg.ellipse(center=(cx,cy),r=(width,height),style=style(fur_color,"hsl",1)))
    #Eyes
    dwg.add(dwg.ellipse(center=(cx-eye_distance,cy-height/4),r=(eye_width,eye_height),style=style((0,0,0),"hsl",1)))
    dwg.add(dwg.ellipse(center=(cx+eye_distance,cy-height/4),r=(eye_width,eye_height),style=style((0,0,0),"hsl",1)))
    #Nose
    dwg.add(svgwrite.shapes.Polygon([(cx-nose_size,cy-nose_size/3), (cx+nose_size,cy-nose_size/3), (cx,cy+nose_size)],style=style((0,0,0),"hsl",1)))
    #Snout
    dwg.add(svgwrite.shapes.Line((cx,cy+nose_size),(cx,cy+nose_size*2.5),style=style((0,0,0),"hsl",2)))
    '''
    mouth = svgwrite.path.Path(d=("M %i %i" %(cx-30,cy+nose_size+24)), style=style(fill_color_type = "none",stroke_width=2))
    mouth.push_arc((cx,cy+nose_size+20), 30, (20,14), large_arc=False, angle_dir='-', absolute=True)
    mouth.push_arc((cx+30,cy+nose_size+24), 150, (20,14), large_arc=False, angle_dir='-', absolute=True)
    '''
    mouth = svgwrite.path.Path(d=("M %i %i" %(cx-nose_size*2,cy+nose_size*2.5+4)), style=style(fill_color_type = "none",stroke_width=2))
    mouth.push_arc((cx,cy+nose_size*2.5), 30, (nose_size*2,nose_size*2), large_arc=False, angle_dir='-', absolute=True)
    mouth.push_arc((cx+nose_size*2,cy+nose_size*2.5+4), 150, (nose_size*2,nose_size*2), large_arc=False, angle_dir='-', absolute=True)
    dwg.add(mouth)
    #Whiskers
    whisker_length = param["whisker_length"]
    whiskers = [((cx-34,cy+nose_size+10),195), ((cx-40,cy+nose_size+4),185), ((cx-34,cy+nose_size-2),175),
                ((cx+34,cy+nose_size+10),345), ((cx+40,cy+nose_size+4),355), ((cx+34,cy+nose_size-2),5) ]
    for whisker in whiskers:
        dwg.add(svgwrite.shapes.Line(whisker[0],dir_point(whisker[0],whisker_length,whisker[1]),style=style((0,0,0),"hsl",1)))
    dwg.save()


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
            param[var] = random.sample(var_dists[var], 1)
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
    #TODO
    params = []
    n = np.prod([len(var) for var in var_settings])
    for i in range(n):
        param = {}
        for var in var_settings:
            param[var] = random.sample(var_dists[var], 1)
        params.append(param)
    return pd.DataFrame(params)

    pass


def get_params(filename):
    return pd.read_excel(filename,dtype=float,index_col=0)


if __name__ == "__main__":
    save_params = False

    params = get_params('params.xlsx')
    dimensions = (800,600)
    for i, param in params.iterrows():
        name = "catdog_%i.svg" % i
        draw_catdog(name, param, dimensions)
    if save_params == True:
        with pd.ExcelWriter("saved_params.xlsx") as writer:
            params.to_excel(writer)

