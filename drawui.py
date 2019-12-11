from IPython.display import display
import ipywidgets as widgets
import drawSvg as draw
from drawSvg.widgets import DrawingWidget
import time
import os
import math


def setup(levers, exp=True):
    start_time = time.time()
    global path
    path = "markovchain/%.0f/" % (start_time)

    drawbutton = widgets.Button(description="Draw")
    submit = widgets.Button(description="Submit")
    full_dwg = draw.Drawing(800, 600)
    dwg = draw.Group()
    full_dwg.append(dwg)
    animal = DrawingWidget(full_dwg)
    
    
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
    
    
    def draw_img(change):
        dwg.children.clear()
        width = 173*(levers["face_aspect_ratio"].value)**0.5
        height = 173/(levers["face_aspect_ratio"].value)**0.5
        cx = 800/2
        cy = 600/2
        
        #Ears
        ear_angle = levers["ear_angle"].value
        ear_tip_angle = levers["ear_tip_angle"].value
        ear_length = levers["ear_length"].value
        ear_orientation = levers["ear_orientation"].value
        ear_point = levers["ear_point"].value
        eye_height = levers["eye_height"].value
        eye_width = eye_height*levers["eye_aspect_ratio"].value
        eye_distance = levers["eye_distance"].value
        nose_size = levers["nose_size"].value
        fur_color = "hsl(%i, %i%%, %i%%)" % (45,levers["fur_saturation"].value,levers["fur_lightness"].value)
        
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
        whisker_length = levers["whisker_length"].value
        whiskers = [((cx-34,cy-nose_size-10),195), ((cx-40,cy-nose_size-4),185), ((cx-34,cy-nose_size+2),175),
                    ((cx+34,cy-nose_size-10),345), ((cx+40,cy-nose_size-4),355), ((cx+34,cy-nose_size+2),5) ]
        for whisker in whiskers:
            dwg.draw(draw.Line(*whisker[0],*dir_point(whisker[0],whisker_length,whisker[1]),stroke_width = 1, stroke='black', fill = "black"))
        
        animal.refresh()
    
    draw_img(None)
    
    levers_text = []
    for lever in levers:
        levers[lever].style = {'description_width': '200px'}
        levers[lever].layout.width = '800px'
        levers[lever].continuous_update = True
        levers[lever].readout=True
        levers[lever].readout_format='.2f'
        levers[lever].observe(draw_img, names = "value")
        levers_text.append(levers[lever])

    item_layout = widgets.Layout(margin='50px',
                                 justify_content='space-around',
                                 justify_items='center',
                                 align_content='space-evenly',
                                 align_items='center')
    

    def on_draw(b):
        draw_img(None)
    drawbutton.on_click(on_draw)
    
    
    def on_submit(b):
        point_time = time.time()
        if exp:
            filename = path + "%.0f.svg" % point_time
            if not os.path.isdir(path):
                os.makedirs(path)
            full_dwg.saveSvg(filename)
    submit.on_click(on_submit)
    
    
    if exp:
        subj_name = widgets.Text(description='Subject ID')
        subj_enter = widgets.Button(description="Submit Subject ID")
        subj = widgets.HBox([subj_name,subj_enter])
        def subj_dir(b):
            global path
            path = "markovchain/%.0f (ID %s)/" % (start_time, subj_name.value)
            os.makedirs(path)
            subj_name.layout.visibility = 'hidden'
            subj_enter.layout.visibility = 'hidden'
        subj_enter.on_click(subj_dir)
        return widgets.HBox([widgets.VBox(levers_text), widgets.VBox([subj, animal, submit], layout=item_layout)], layout=item_layout)

    return widgets.HBox([widgets.VBox(levers_text), widgets.VBox([animal, widgets.HBox([drawbutton, submit], layout=item_layout)], layout=item_layout)], layout=item_layout)
