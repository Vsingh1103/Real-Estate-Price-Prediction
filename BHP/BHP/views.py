from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
import json
import os
import pickle
import numpy as np
def index(request):
	#if request.method == 'GET':
	columns_data = open('C:/Users/Administrator/Desktop/Banglore houses prediction/BHP/static/columns.json').read()
	columns_data = json.loads(columns_data)
	#columns = json.dumps(columns)
	columns_data = columns_data['data_columns']
	columns = columns_data[3:]

	if request.method == 'POST':
		location = request.POST['location']
		area = request.POST['area']
		bathrooms = request.POST['bathrooms']
		bedrooms = request.POST['bedrooms']
		if location is '':
			messages.info(request,'Location should not be empty.')
		if area is '':
			messages.info(request,'Please specify the area.')
		if bathrooms is '':
			messages.info(request,'Please specify the number of bathrooms.')
		if bedrooms is '':
			messages.info(request,'Please specify the number of bedrooms.')

		with open('C:/Users/Administrator/Desktop/Banglore houses prediction/BHP/static/bangalore_home_prices_model.pickle','rb') as f:
			model = pickle.load(f)

		if location is not '' and area is not '' and bathrooms is not '' and bedrooms is not '':
			loc_index = np.where(columns_data == location)[0]
			x = np.zeros(len(columns_data))
			x[0] = area
			x[1] = bathrooms
			x[2] = bedrooms
			if loc_index >= 0:
				x[loc_index] = 1
			predicted_price = model.predict([x])[0]
			print(predicted_price)
			return render(request,'index.html',{'columns':columns,'location':location,'area':area,'bathrooms':bathrooms,'bedrooms':bedrooms,'predicted_price':predicted_price})

	return render(request,'index.html',{'columns':columns})