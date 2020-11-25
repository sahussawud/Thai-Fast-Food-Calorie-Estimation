import cv2
import numpy as np
from imageSegmentation import getAreaOfFood
import base64
import requests
	
#density - gram / cm^3  of rice rough gain = 1.327 to 1.375
# https://www.osti.gov/etdeweb/servlets/purl/20655574
density_of_rice = 1.375

#skin of photo to real multiplier
skin_multiplier = 5*2.3

def get_calories_from_keyword(keyword):
	url = "https://api.myfitnesspal.com/public/nutrition"
	
	payload = {
		'q': keyword,
		'page': 1,
		'per_page': 1
	}
	
	response = requests.get(url, params=payload)
	
	json_res = response.json()
	print(json_res)
	return json_res['items'][0]['item']['nutritional_contents']['energy']['value']

def get_label(path_image):
	#save image to base64
	b64file = open(path_image, 'rb').read()
	imgData = base64.b64encode(b64file)
	imgFile = open('food-ex.txt', 'wb+')
	imgFile.write(imgData)
	imgFile.flush()
	imgFile.close()
	
	url = "https://api.aiforthai.in.th/thaifood"
	
	data = {
	'file': open('food-ex.txt', 'r').read()
	}
	headers = {
		'Content-Type': 'application/json',
		'Apikey': "HionRmBsNL24ACd11j3dlxbz0HKbZhqp",
		}
	response = requests.post(url, headers=headers, json=data)
	
	json_res = response.json()
	print(json_res)
	get_calories_from_keyword(json_res['objects'][0]['result'])
	return { 'name': json_res['objects'][0]['result'], 'accurate': json_res['objects'][0]['score']}

def getCalorie(label, volume): #volume in cm^3
	calorie = get_calories_from_keyword(label)
	density = density_of_rice
	mass = volume*density*1.0
	calorie_tot = (calorie/100.0)*mass
	return mass, calorie_tot, calorie #calorie per 100 grams

def getVolume(area, skin_area, pix_to_cm_multiplier, rice_contour, radius):
	area_rice = (area*skin_multiplier)/skin_area #area in cm^2
	volume = 100
	height_approx = 10
	#assume thai fastfood, they serve with plate, and it's in spherical dome shape
	radius = radius*pix_to_cm_multiplier
	volume = (4/3)*np.pi*radius*radius*height_approx/2
	print('\narea_rice', area_rice,'\npix_to_cm_multiplier',pix_to_cm_multiplier, '\nradius', radius,'\nvolume', volume,'\nskin_area', skin_area)
	return volume

def calories(result,img):
	# 1 tablespoon of rice = approx. 15g or 1/2 oz 3 tablespoons of rice = approx. 45g or 1 1/2 oz
    img_path =img 
    rice_areas,final_f,areaod,skin_areas, rice_contours, pix_cm, radius = getAreaOfFood(img_path)
    volume = getVolume(rice_areas, skin_areas, pix_cm, rice_contours, radius)
    mass, cal, cal_100 = getCalorie(result, volume)
    rice_volumes=volume
    rice_calories=cal
    rice_calories_100grams=cal_100
    rice_mass=mass
    print("\nrice_volumes",rice_volumes,"\nrice_calories",rice_calories,"\nruit_calories_100grams",rice_calories_100grams,"\nrice_mass",rice_mass)
    return rice_mass, rice_calories

# if __name__ == '__main__':
    
#     a=r'C:\Users\M Sc-2\Desktop\data\sa\data1.jpg'
#     a=cv2.imread(a)
#     print(testing(1,a))
