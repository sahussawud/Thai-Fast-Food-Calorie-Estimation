import cv2
import numpy as np
from imageSegmentation import getAreaOfFood
import base64
import requests
	
#density - gram / cm^3
density_dict = { 1:0.609, 2:0.94, 3:0.641, 4:0.641,5:0.513, 6:0.482, 7:0.481}
#kcal
calorie_dict = { 1:52, 2:89,  3:41,4:16,5:40,6:47,7:18 }
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
	return str(json_res['items'][0]['item']['nutritional_contents']['energy']['value']) +" "+json_res['items'][0]['item']['nutritional_contents']['energy']['unit']

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
	calorie = calorie_dict[int(label)]
	density = density_dict[int(label)]
	mass = volume*density*1.0
	calorie_tot = (calorie/100.0)*mass
	return mass, calorie_tot, calorie #calorie per 100 grams

def getVolume( area, skin_area, pix_to_cm_multiplier, fruit_contour):
	area_fruit = (area/skin_area)*skin_multiplier #area in cm^2
	volume = 100
	height_approx = 10
	#assume thai fastfood, they serve with plate, and it's in spherical dome shape

	radius = np.sqrt(area_fruit/np.pi)
	volume = ((4/3)*np.pi*radius*radius*(height_approx*pix_to_cm_multiplier))/2
	print(area_fruit, radius, volume, skin_area, (height_approx*pix_to_cm_multiplier))

	return volume

def calories(result,img):
	# 1 tablespoon of rice = approx. 15g or 1/2 oz 3 tablespoons of rice = approx. 45g or 1 1/2 oz
    img_path =img 
    fruit_areas,final_f,areaod,skin_areas, fruit_contours, pix_cm = getAreaOfFood(img_path)
    volume = getVolume(fruit_areas, skin_areas, pix_cm, fruit_contours)
    mass, cal, cal_100 = getCalorie(result, volume)
    fruit_volumes=volume
    fruit_calories=cal
    fruit_calories_100grams=cal_100
    fruit_mass=mass
    #print("\nfruit_volumes",fruit_volumes,"\nfruit_calories",fruit_calories,"\nruit_calories_100grams",fruit_calories_100grams,"\nfruit_mass",fruit_mass)
    return fruit_calories

# if __name__ == '__main__':
    
#     a=r'C:\Users\M Sc-2\Desktop\data\sa\data1.jpg'
#     a=cv2.imread(a)
#     print(testing(1,a))
