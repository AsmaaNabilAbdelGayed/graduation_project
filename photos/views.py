from django.views import generic
from django.shortcuts import render , redirect
from django.views.generic.edit import CreateView , UpdateView , DeleteView
from models import Photo , ImageClass , LabelsClass
from django.http import HttpResponse
import numpy as np
import tensorflow as tf
import argparse
import glob
import os
import re
from tensorflow.python.platform import gfile
import csv
from django.contrib.auth import authenticate , login
from django.views.generic import View
from django.contrib.auth.models import User
from cart.forms import CartAddProductForm
from math import *
from django.db import models


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# imagePath = os.path.abspath(os.path.join(BASE_DIR, 'img/258890_img_00000002.jpg'))
path_class = os.path.abspath(os.path.join(BASE_DIR, 'media/features'))
modelFullPath = os.path.abspath(os.path.join(BASE_DIR, 'photos/inception_dec_2015/tensorflow_inception_graph.pb'))


def create_graph():
    with tf.gfile.FastGFile(modelFullPath, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

def run_on_image(imagePath):
    answer = None

    if not tf.gfile.Exists(imagePath):
        tf.logging.fatal('File does not exist %s', imagePath)
        return answer

    image_data = tf.gfile.FastGFile(imagePath, 'rb').read()

    create_graph()

    with tf.Session() as sess:
        next_to_last_tensor = sess.graph.get_tensor_by_name('pool_3:0')
        # output = open(indexpath, "w")
        image_data = gfile.FastGFile(imagePath, 'rb').read()
        predictions = sess.run(next_to_last_tensor, {'DecodeJpeg/contents:0': image_data})
        queryfeature = np.squeeze(predictions)

    return queryfeature

class Searcher:
    def __init__(self, path_class):

        self.path_class = path_class

    def square_rooted(self, x):
        return round(sqrt(sum([a * a for a in x])), 5)

    def cosine_similarity(self, x, y):
        numerator = sum(a * b for a, b in zip(x, y))
        denominator = self.square_rooted(x) * self.square_rooted(y)
        return round(numerator / float(denominator), 5)
        # tgroba we faslaet bst5dam el numpy

    def cos_sim(self, a, b):

        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        return dot_product / (norm_a * norm_b)

    def euclidean_distance(self, x, y):
        return sqrt(sum(pow(a - b, 2) for a, b in zip(x, y)))

    def manhattan_distance(self, x, y):

        return sum(abs(a - b) for a, b in zip(x, y))

    def jaccard_similarity(self, x, y):

        intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
        union_cardinality = len(set.union(*[set(x), set(y)]))
        return intersection_cardinality / float(union_cardinality)

    def search(self, queryFeatures, limit=4):

        results = {}
        results1 = {}

        for filename in os.listdir(path_class):
            with open(path_class + '/' + filename, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    features = [float(x) for x in row[0:]]
                    d = self.cosine_similarity(features, queryFeatures)

                    results[filename[:-4]+'.jpg'] = d

                f.close()
                results1.update(results)


        results1 = sorted(results1, key=results1.get,reverse=True)

        return results1[:limit]

def detail(request, image_id):
    det_photo = Photo.objects.get(id=image_id)
    all_photo=Photo.objects.all()
    path1='media/photos'
    path2=det_photo.name
    imagePath1 = os.path.abspath(os.path.join(BASE_DIR, os.path.join(path1,path2)))


    feature = run_on_image(imagePath1)
    searcher = Searcher(path_class)
    results = searcher.search(feature)
    list_images = results
    show = Photo.objects.filter(name__in=results)
    context = {
    'det_photo': det_photo,
    'image_id': image_id,
    'results': results,
    'show' :show,
    'all_photo' :all_photo}

    return render(request, 'photos/detail.html', context)








































def test(request):
    return render(request , 'photos/user_home_page.html' )


def Index(request):
	photos=Photo.objects.all()
	cart_product_form = CartAddProductForm()
	return render(request,'photos/index.html',{'photos':photos,'cart_product_form': cart_product_form})


all_classes_names = []
all_classes = ImageClass.objects.all()
for classX in all_classes:
	all_classes_names.append(classX.class_name)

all_labels_names = []
all_labels = LabelsClass.objects.all()
for label in all_labels:
	all_labels_names.append(label.label_name)


# def get_labels_for_classX(classX):
# 	related_labels = []
# 	for image_class in ImageClass.objects.all():
# 		if image_class.class_name == classX.lower():
# 			related_images = image_class.photo_set.all()
# 			for image in related_images:
# 				labels = list(image.label_name.all())
# 				for label in labels:
# 					related_labels.append(label)
#
# 	return 	list(set(related_labels))

def get_all_images(name , type):
	if type == 'class':
		related_images = []
		for image_class in ImageClass.objects.all():
			if image_class.class_name == name.lower():
				related_images = image_class.photo_set.all()
				break
	if type == 'label':
		related_images = []
		for image_label in LabelsClass.objects.all():
			if image_label.label_name == name.lower():
				related_images = image_label.photo_set.all()
				break

	return related_images

def search(request):
	# suggested_labels = []
	list_for_each_word = []
	related_images = []
	empty = 1
	if request.method == "POST":
		search_text = request.POST.get("input")
		search_words = search_text.split()

		for i in range(0 , len(search_words)):
			if search_words[i] in all_labels_names:
				empty = 0

				three_words_label = search_words[i]
				two_words_label = search_words[i]

				if len(search_words) > i+3:
					three_words_label= search_words[i]+' '+search_words[i+1]+' '+search_words[i+2]
				elif len(search_words) > i+2 :
					two_words_label = search_words[i]+' '+search_words[i+1]

				if three_words_label in all_labels_names:
					related_images = get_all_images(three_words_label , 'label')
					i += 3
				elif two_words_label in all_labels_names:
					related_images = get_all_images(two_words_label, 'label')
					i += 2
				else:
					related_images = get_all_images(search_words[i] , 'label')

				if len(related_images) != 0:
					list_for_each_word.append(related_images)

			elif search_words[i] in all_classes_names:
				empty = 0
				# suggested_labels = get_labels_for_classX(search_words[i])
				related_images = get_all_images(search_words[i] , 'class')
				if len(related_images) != 0:
					list_for_each_word.append(related_images)

		if len(list_for_each_word) != 0:
			related_images = set(list_for_each_word[0])
			for s in list_for_each_word[1:]:
				related_images.intersection_update(s)


	return render(request, 'photos/search.html' , {'related_images':related_images,
												   'empty':empty , 'all_classes': ImageClass.objects.all()})

def search_buttons(request , id):
	classX = ImageClass.objects.filter(id=id).first()
	images = get_all_images(classX.class_name , 'class')
	return render(request , 'photos/show_classX_images.html' , {'related_images':images})

# def suggested_labels_buttons(request , label_id , class_id):
# 	return

























