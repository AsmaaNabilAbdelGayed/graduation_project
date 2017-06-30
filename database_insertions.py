import os
from photos.models import Photo, ImageClass , LabelsClass
from django.core.files import File
import numpy as np


images_directory = '/home/asmaanabil/Desktop/gp/mini-dataset'
features_directory = '/home/asmaanabil/Desktop/gp/mini-dataset2'
read_m_r = np.load('/home/asmaanabil/Desktop/mapping_r.npy').item()


only_labels = []
with open("/home/asmaanabil/Desktop/list_attr_cloth.txt") as f:
    for i in xrange(2):
        f.next()

    for line in f :
        all_in_a_line = line.split()
        label = ""
        for i in range(0 , len(all_in_a_line)-1):
            if i == len(all_in_a_line)-2:
                label += (all_in_a_line[i])
            else:
                label += (all_in_a_line[i] + " ")
        only_labels.append(label)


images_and_labels = {}
with open("/home/asmaanabil/Desktop/list_attr_img.txt") as f:
    for i in xrange(2):
        f.next()

    for line in f :
        line_in_a_list = line.split()
        key = line_in_a_list[0]
        line_in_a_list.pop(0)

        list_of_index = []
        offset = 0
        while offset < 5:
            if "1" in line_in_a_list:
                index = line_in_a_list.index("1")
                list_of_index.append(only_labels[index+offset])
                offset += 1
                line_in_a_list.pop(index)
            else:
                break

        images_and_labels[key] = list_of_index


for label in only_labels:
    label_class = LabelsClass(label_name = label)
    label_class.save()


for root, dirs, files in os.walk(images_directory):
    for direcory in dirs:
        image_class = ImageClass()
        image_class.class_name=direcory.lower()
        images_dir= images_directory+'/'+direcory
        if os.listdir(images_dir):
            image_class.save()
            print 'class ' + direcory + ' is added to database'
            for filee in os.listdir(images_dir):
                if filee.endswith('.jpg'):
                    ph = Photo()
                    ph.name = filee
                    ph.class_name=image_class
                    ph.photo.save(filee, File(open(images_dir+'/' + filee, 'r')))
                    feature_file_dir= features_directory+'/'+direcory+'/'+filee+'.txt'
                    ph.features.save(filee[:-3]+'csv', File(open(feature_file_dir, 'r')))
                    ph.save()

                    old_name = read_m_r[filee]
                    photo_labels = images_and_labels[old_name]
                    for label in photo_labels:
                        l = LabelsClass.objects.get(label_name = label)
                        ph.label_name.add(l)



