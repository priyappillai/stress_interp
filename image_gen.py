import svgwrite
import pandas as pd
import random

image_folder = "./images/"
variables = ["fur_pattern", # "plain", "eye_spot", "stripes", "v", "mask", "snout"
             "fur_lightness",
             "fur_saturation",
             "eye_distance", 
             "eye_height", 
             "eye_aspect_ratio", 
             "whiskers", # boolean
             "whisker_length",
             "whisker_weight",
             "face_aspect_ratio",
             "nose_size",
             "ear_angle", #up/down
             "ear_point",
             "cheek_tufts",
             "chin_tufts",
             "head_tufts"]


def style(fill_color=(0,0,0), fill_color_type="rgb", stroke_width=0, stroke_color=(0,0,0), stroke_color_type="rgb"):
    style_str = "fill:%s" %fill_color_type
    if fill_color_type == "hsl":
        style_str = style_str+("(%i, %i%%, %i%%)" %fill_color)
    else:
        style_str = style_str+("(%i, %i, %i)" %fill_color)
    style_str = style_str+(";stroke-width:%f;stroke:%s" %(stroke_width, stroke_color_type))
    if stroke_color_type == "hsl":
        style_str = style_str+("(%i, %i%%, %i%%)" %stroke_color)
    else:
        style_str = style_str+("(%i, %i, %i)" %stroke_color)
    return style_str


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
    dwg = svgwrite.Drawing(filename=name, debug=True)
    width = param["face_width"]
    height = width*param["face_aspect_ratio"]
    cx = width*2
    cy = height*2
    dwg.add(dwg.ellipse(center=(cx,cy),r=(width,height),style=style((45,40,80),"hsl",1)))
    eye_height = param["eye_height"]
    eye_width = eye_height*param["eye_aspect_ratio"]
    eye_distance = param["eye_distance"]
    dwg.add(dwg.ellipse(center=(cx-eye_distance,cy-height/4),r=(eye_width,eye_height),style=style((0,0,0),"hsl",1)))
    dwg.add(dwg.ellipse(center=(cx+eye_distance,cy-height/4),r=(eye_width,eye_height),style=style((0,0,0),"hsl",1)))
    nose_size = param["nose_size"]
    dwg.add(svgwrite.shapes.Polygon([(cx-nose_size,cy-nose_size/3), (cx+nose_size,cy-nose_size/3), (cx,cy+nose_size)],style=style((0,0,0),"hsl",1)))
    dwg.add(svgwrite.shapes.Line((cx,cy+nose_size),(cx,cy+nose_size+10),style=style((0,0,0),"hsl",2)))
    mouth = svgwrite.path.Path(d=("M %i %i" %(cx-15,cy+nose_size+12)))
    mouth.push_arc((cx,cy+nose_size+10), 45, (10,7), large_arc=False, angle_dir='-', absolute=True)
    dwg.add(mouth)
    #TODO
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
    list of dictionaries (keys: variables list)
        The parameter settings
    """
    #TODO
    pass


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
    list of dictionaries (keys: variables list)
        The parameter settings
    """
    #TODO
    pass


if __name__ == "__main__":
    params = [{"face_width": 100, "face_aspect_ratio": .75, "eye_height": 6,
               "eye_aspect_ratio": 1, "eye_distance": 40, "nose_size": 8}]
    for i, param in enumerate(params):
        name = "catdog_%i.svg" % i
        draw_catdog(name, param)
    df = pd.DataFrame(params)
    with pd.ExcelWriter("params.xlsx") as writer:
        df.to_excel(writer)

