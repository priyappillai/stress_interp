import svgwrite
import pandas as pd
import random

image_folder = "./images/"
variables = []


def draw_catdog(name, param):
    """
    Draws a cat/dog and saves it as an svg
    
    Parameters
    ----------
    name : string
        Filename to save catdog as
    param : list of floats
        Variables to set the structure of the catdog face
    """
    dwg = svgwrite.Drawing(filename=name, debug=True)
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
    var_dists : list of distributions
        A list of probability distributions for each variable
    
    Returns
    -------
    list of lists of floats
        The parameter settings, variable set in same order as distributions 
    """
    #TODO
    pass


def all_params(var_settings):
    """
    Given a list of settings for each variable, produce parameter 
    settings for every combination of variable settings
    
    Parameters
    ----------
    var_settings : list of lists of floats
        All possible settings for each variable

    Returns
    -------
    list of lists of floats
        The parameter settings, variable set in same order as settings
    """
    #TODO
    pass


if __name__ == "__main__":
    params = random_params()
    for i, param in ennumerate(params):
        name = "catdog_%i" % i
        draw_catdog(name, param)
    df = pd.DataFrame(data=params, columns=variables)
    with pd.ExcelWriter("params.xlsx") as writer:
        df.to_excel(writer)

