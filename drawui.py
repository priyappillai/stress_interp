from IPython.display import display
import ipywidgets as widgets
#from svgwidgets import svgwidgets
import drawSvg as draw
import time
import os


def setup(levers, param, exp=True):
    start_time = time.time()
    global path
    path = "/%.0f/" % (start_time)

    draw = widgets.Button(description="Draw")
    submit = widgets.Button(description="Submit")
    
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

    def draw_img():
        '''
        dwg = draw.Drawing(800, 600)
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
        left_ear = draw.path(stroke_width = 1, stroke='black', fill = fur_color)
        left_ear.M(*bottom_left)
        left_ear.l(*bottom_left_ctrl)
        left_ear.a()
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
        '''
        return widgets.Button(description="Insert fig here")

    animal = draw_img()
    
    def redraw(var_changes):
        pass
    
    def update_img(change):
        redraw({change["name"]: change["new"]})
    
    levers_text = []
    for i, lever in enumerate(levers):
        lever.style = {'description_width': '200px'}
        lever.layout.width = '800px'
        lever.continuous_update = True
        lever.readout=True
        lever.readout_format='.2f'
        lever.observe(update_img, names = "value")
        levers_text.append(lever)

    item_layout = widgets.Layout(margin='50px',
                                 justify_content='space-around',
                                 justify_items='center',
                                 align_content='space-evenly',
                                 align_items='center')
    

    def on_draw(b):
        pass
    draw.on_click(on_draw)
    
    def on_submit(b):
        pass
    submit.on_click(on_submit)
    
    if exp:
        subj_name = widgets.Text(description='Subject-ID')
        subj_enter = widgets.Button(description="Submit Subject ID")
        subj = widgets.HBox([subj_name,subj_enter])
        def subj_dir(b):
            global path
            path = "/%.0f (ID %s)/" % (start_time, subj_name.value)
            os.makedirs(path)
            subj_name.layout.visibility = 'hidden'
            subj_enter.layout.visibility = 'hidden'
        subj_enter.on_click(subj_dir)
        return widgets.HBox([widgets.VBox(levers_text), widgets.VBox([animal, widgets.HBox([draw, submit], layout=item_layout), subj], layout=item_layout)], layout=item_layout)

    return widgets.HBox([widgets.VBox(levers_text), widgets.VBox([animal, widgets.HBox([draw, submit], layout=item_layout)], layout=item_layout)], layout=item_layout)
