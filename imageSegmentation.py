# ref https://github.com/meghanamreddy/Calorie-estimation-from-food-images-OpenCV
import cv2
import numpy as np
import sys
import matplotlib.pyplot as plt
import os

def getAreaOfFood(img1):
    data=os.path.join(os.getcwd(),"images")
    if os.path.exists(data):
        print('folder exist for images at ',data)
    else:
        os.mkdir(data)
        print('folder created for images at ',data)
    cv2.imwrite('{}\\1 original image.jpg'.format(data),img1)
    img = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('{}\\2 original image BGR2GRAY.jpg'.format(data),img)
    img_filt = cv2.medianBlur(img, 5)
    cv2.imwrite('{}\\3 img_filt.jpg'.format(data),img_filt)
    img_th = cv2.adaptiveThreshold(img_filt,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    cv2.imwrite('{}\\4 img_th.jpg'.format(data),img_th)
    contours, hierarchy = cv2.findContours(img_th, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    
    mask_child = np.zeros(img.shape, np.uint8)
    # Find the index of the largest contour, imply it's a plate index
    areas = [cv2.contourArea(c) for c in contours]
    max_index = np.argmax(areas)
    child_in_plate = [contours[index] for index, ele in enumerate(hierarchy[0])if ele[3] == max_index]
    for target_list in child_in_plate:
        cv2.drawContours(mask_child, [target_list], 0, (255,255,255,255), -1)
    cv2.imwrite('{}\\5.1 mask_rice.jpg'.format(data),mask_child)

    #   #erode before finding contours
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
    # erode_rice = cv2.dilate(mask_child,kernel,iterations = 1)
    # cv2.imwrite('{}\\5.2 erode_rice.jpg'.format(data),erode_rice)

    # # #find largest contour since that will be the rice
    # img_th = cv2.adaptiveThreshold(erode_rice,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    # cv2.imwrite('{}\\5.3 img_th_rice.jpg'.format(data),img_th)

    # contours, hierarchy = cv2.findContours(img_th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # mask_rice = np.zeros(mask_child.shape, np.uint8)
    # largest_areas = sorted(contours, key=cv2.contourArea)
    # cv2.drawContours(mask_rice, [largest_areas[-1]], 0, (255,255,255), -1)
    # cv2.imwrite('{}\\5.4 mask_rice.jpg'.format(data),mask_rice)

    # # #dilate rice now
    # kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(13,13))
    # mask_rice2 = cv2.dilate(mask_rice,kernel2,iterations = 1)
    # cv2.imwrite('{}\\5.5 mask_rice2.jpg'.format(data),mask_rice2)
    # res = cv2.bitwise_and(mask_child, mask_child,mask = mask_rice2)
    # rice_final = cv2.bitwise_and(img1,img1,mask = mask_rice2)
    # cv2.imwrite('{}\\5.6 rice_final.jpg'.format(data),rice_final)


    # find contours. sort. and find the biggest contour. the biggest contour corresponds to the plate and food
    mask = np.zeros(img.shape, np.uint8)

    largest_areas = sorted(contours, key=cv2.contourArea)
    cv2.drawContours(mask, [largest_areas[-1]], 0, (255,255,255,255), -1)
    cv2.imwrite('{}\\5 mask.jpg'.format(data),mask)
    img_bigcontour = cv2.bitwise_and(img1,img1,mask = mask)
    cv2.imwrite('{}\\6 img_bigcontour.jpg'.format(data),img_bigcontour)

    # convert to hsv. otsu threshold in s to remove plate
    hsv_img = cv2.cvtColor(img_bigcontour, cv2.COLOR_BGR2HSV)
    cv2.imwrite('{}\\7 hsv_img.jpg'.format(data),hsv_img)
    h,s,v = cv2.split(hsv_img)
    mask_plate = cv2.inRange(hsv_img, np.array([0,0,50]), np.array([200,90,250]))

    cv2.imwrite('{}\\8 mask_plate.jpg'.format(data),mask_plate)

    mask_not_plate = cv2.bitwise_not(mask_plate)
    # item except a viand(กับข้าว), example rice 
    cv2.imwrite('{}\\9 mask_not_plate.jpg'.format(data),mask_not_plate)

    rice_skin = cv2.bitwise_and(img_bigcontour,img_bigcontour,mask = mask_not_plate)
    cv2.imwrite('{}\\10 rice_skin.jpg'.format(data),rice_skin)


    #convert to hsv to detect and remove skin pixels
    hsv_img = cv2.cvtColor(rice_skin, cv2.COLOR_BGR2HSV)
    cv2.imwrite('{}\\11 hsv_img.jpg'.format(data),hsv_img)
    skin = cv2.inRange(hsv_img, np.array([0,10,60]), np.array([10,160,255])) #Scalar(0, 10, 60), Scalar(20, 150, 255)
    cv2.imwrite('{}\\12 skin.jpg'.format(data),skin)
    not_skin = cv2.bitwise_not(skin); #invert skin and black
    cv2.imwrite('{}\\13 not_skin.jpg'.format(data),not_skin)
    rice = cv2.bitwise_and(rice_skin,rice_skin,mask = not_skin) #get only rice pixels
    cv2.imwrite('{}\\14 rice.jpg'.format(data),rice)


    rice_bw = cv2.cvtColor(rice, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('{}\\15 rice_bw.jpg'.format(data),rice_bw)
    rice_bin = cv2.inRange(rice_bw, 10, 255) #binary of rice
    cv2.imwrite('{}\\16 rice_bw.jpg'.format(data),rice_bin)

    #erode before finding contours
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    erode_rice = cv2.erode(rice_bin,kernel,iterations = 1)
    cv2.imwrite('{}\\17 erode_rice.jpg'.format(data),erode_rice)

    #find largest contour since that will be the rice
    img_th = cv2.adaptiveThreshold(erode_rice,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    cv2.imwrite('{}\\18 img_th.jpg'.format(data),img_th)

    contours, hierarchy = cv2.findContours(img_th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    mask_rice = np.zeros(rice_bin.shape, np.uint8)
    largest_areas = sorted(contours, key=cv2.contourArea)
    cv2.drawContours(mask_rice, [largest_areas[-2]], 0, (255,255,255), -1)
    cv2.imwrite('{}\\19 mask_rice.jpg'.format(data),mask_rice)


    #dilate now
    kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    mask_rice2 = cv2.dilate(mask_rice,kernel2,iterations = 1)
    cv2.imwrite('{}\\20 mask_rice2.jpg'.format(data),mask_rice2)
    res = cv2.bitwise_and(rice_bin,rice_bin,mask = mask_rice2)
    rice_final = cv2.bitwise_and(img1,img1,mask = mask_rice2)
    # draw eclipce
    # ellipse = cv2.fitEllipse(largest_areas[-2])
    # rice_final = cv2.ellipse(rice_final,ellipse,(0,255,0),10)

    (x,y),radius = cv2.minEnclosingCircle(largest_areas[-2])
    center = (int(x),int(y))
    radius = int(radius)
    rice_final = cv2.circle(img1,center,radius,(0,255,0),2)
    cv2.imwrite('{}\\21 rice_final.jpg'.format(data),rice_final)
    #find area of rice
    img_th = cv2.adaptiveThreshold(mask_rice2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    cv2.imwrite('{}\\22 img_th.jpg'.format(data),img_th)
    contours, hierarchy = cv2.findContours(img_th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    largest_areas = sorted(contours, key=cv2.contourArea)
    rice_contour = largest_areas[-1]
    rice_area = cv2.contourArea(rice_contour)


    #finding the area of skin. find area of biggest contour
    skin2 = skin - mask_rice2
    cv2.imwrite('{}\\23 skin2.jpg'.format(data),skin2)
    #erode before finding contours
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    skin_e = cv2.erode(skin2,kernel,iterations = 1)
    cv2.imwrite('{}\\24 skin_e .jpg'.format(data),skin_e )
    img_th = cv2.adaptiveThreshold(skin_e,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    cv2.imwrite('{}\\25 img_th.jpg'.format(data),img_th)
    contours, hierarchy = cv2.findContours(img_th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    mask_skin = np.zeros(skin.shape, np.uint8)
    largest_areas = sorted(contours, key=cv2.contourArea)
    cv2.drawContours(mask_skin, [largest_areas[-2]], 0, (255,255,255), -1)
    cv2.imwrite('{}\\26 mask_skin.jpg'.format(data),mask_skin)



    skin_rect = cv2.minAreaRect(largest_areas[-2])
    box = cv2.boxPoints(skin_rect)
    box = np.int0(box)
    mask_skin2 = np.zeros(skin.shape, np.uint8)
    cv2.drawContours(mask_skin2,[box],0,(255,255,255), -1)
    cv2.imwrite('{}\\27 mask_skin2.jpg'.format(data),mask_skin2)

    pix_height = max(skin_rect[1])
    pix_to_cm_multiplier = 5.0/pix_height
    print('\n\n\n\n\n\npix_height :', pix_height)
    skin_area = cv2.contourArea(box)

    return rice_area, mask_rice2, rice_final, skin_area, rice_contour, pix_to_cm_multiplier, radius

if __name__ == '__main__':
    img1 = cv2.imread(sys.argv[1])
    area, bin_rice, img_food, skin_area, rice_contour, pix_to_cm_multiplier = getAreaOfFood(img1)

    origimg = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    segmentimg = cv2.cvtColor(img_food, cv2.COLOR_BGR2RGB)

    plt.title('area {}, pix_to_cm_multiplier {}'.format(area, pix_to_cm_multiplier))
    plt.axis('off')
    plt.show()

    cv2.waitKey()
    cv2.destroyAllWindows()
