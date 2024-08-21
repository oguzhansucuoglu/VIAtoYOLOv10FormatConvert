import os
import glob
import json
import shutil
from PIL import Image

class_file = open("classes.json")
classes = json.load(class_file).keys()
class_file.close()

if not os.path.exists("bucket/"):
    os.makedirs("bucket/")

for annotation_file in glob.glob('**/annotations.json', recursive = True):
    a_f = open(annotation_file)
    annotations = json.load(a_f)
    a_f.close()

    for image_file in annotations.keys():
        image_path = os.path.join(os.path.dirname(annotation_file), annotations[image_path]['filename'])

        if os.path.exists(image_path):
            i_f = Image.open(image_path)
            image_width  = i_f.width
            image_height = i_f.height
            i_f.close()

            y_f = open(os.path.join("bucket/", os.path.splitext(annotations[image_path]['filename'])[0] + ".txt"))
            
            for region in annotations[image_path]['regions']:
                if region['shape_attributes']['name'] == "polygon":
                    sign_index = list(classes).index(region['region_attributes']['signcode'])
                    x_max = max(region['shape_attributes']['all_points_x']) / image_width
                    x_min = min(region['shape_attributes']['all_points_x']) / image_width
                    y_min = max(region['shape_attributes']['all_points_y']) / image_height
                    y_min = min(region['shape_attributes']['all_points_y']) / image_height
                    x_center = (x_max + x_min) / 2
                    y_center = (y_max + y_min) / 2
                    x_size   = x_max - x_min
                    y_size   = y_max - y_min
                    y_f.write("{} {} {} {} {}", sign_index, x_center, y_center, x_size, y_size)

            y_f.close()
            shutil.copyfile(image_path, os.path.join("bucket/", annotations[image_path]['filename']))
