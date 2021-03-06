# import the necessary packages
from calories import get_label, get_calories_from_keyword, calories
from imageSegmentation import getAreaOfFood
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import cv2

from tkinter import Tk, Text, BOTH, W, N, E, S
from tkinter.ttk import Frame, Button, Label, Style, LabelFrame

zoom = 0.2
upload = cv2.imread("upload.png")
fontStyle = "Arial 20 bold italic"


class Example(Frame):
    area = None

    # pixels_x, pixels_y = tuple([int(zoom * x)  for x in upload.size])
    
    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        self.master.title("Thai Food Calories Estimate Program")
        self.pack(fill=BOTH, expand=True)

        self.columnconfigure(1, weight=3)
        # self.columnconfigure(3, pad=1)
        # self.rowconfigure(3, weight=1)
        # self.rowconfigure(5, pad=7)

        lbl = Label(self, text="เลือกภาพ")
        lbl.grid(sticky=W, pady=4, padx=4)

        upload_ar = cv2.resize(upload, (400, 400), interpolation = cv2.INTER_AREA)
        image = Image.fromarray(upload_ar)

        bardejov = ImageTk.PhotoImage(image)
        self.area = Label(self, image=bardejov)
        self.area.image = bardejov
        
        self.area.grid(row=1, column=0, columnspan=4, rowspan=4,
            padx=0, sticky=E+W+S+N)

        Label(self,text="ชื่ออาหาร",font = fontStyle).grid(row=1, column=1,sticky='W', padx=1, pady=1)
        Label(self,text="", font = fontStyle).grid(row=1, column=2, sticky='W', padx=1, pady=1)

        Label(self,text="น้ำหนักประมาณ",font = fontStyle).grid(row=2, column=1, sticky='W', padx=1, pady=1)
        Label(self,text="0 g",font = fontStyle).grid(row=2, column=2, sticky='W', padx=1, pady=1)


        Label(self,text="พลังงาน",font = fontStyle).grid(row=3, column=1,  sticky='W', padx=1, pady=1)
        # Label(self,text="250",font = fontStyle).grid(row=3, column=2, sticky='W', padx=1, pady=1)
        # Label(self,text="kcal",font = fontStyle).grid(row=3, column=3, sticky='W', padx=1, pady=1)

        hbtn = Button(self, text="เลือกภาพจากคอมพิวเตอร์", command=self.select_image)
        hbtn.grid(row=5, column=0, padx=150)

    def select_image(self):
        # grab a reference to the image panels
        path = filedialog.askopenfilename()
        # ensure a file path was selected
        if len(path) > 0:
            # load the image from disk, convert it to grayscale, and detect
            # edges in it
            image = cv2.imread(path)
            json_label = get_label(path)
            Label(self,text=json_label['name']+" accuracy: "+json_label['accurate'],font = fontStyle).grid(row=1, column=2, sticky='W', padx=1, pady=1)

            # calories_from_myfisness = get_calories_from_keyword(json_label)
           

            mass, final_calories = calories(json_label, image)
            Label(self,text=str(mass)+ "  g" ,font = fontStyle).grid(row=2, column=2, sticky='W', padx=1, pady=1)
            Label(self,text=str(final_calories)+ "  kcal" ,font = fontStyle).grid(row=3, column=2, sticky='W', padx=1, pady=1)
            # image_cv = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # convert the images to PIL format...
            display_img = image.copy()
            image_resize = cv2.resize(display_img, (400, 400), interpolation = cv2.INTER_AREA)
            image = Image.fromarray(image_resize)

            # ...and then to ImageTk format
            image = ImageTk.PhotoImage(image)

            # if the panels are None, initialize them
            if self.area is None:
                # the first panel will store our original image
                self.area = Label(image=image)
                self.area.image = image
                self.area.pack(side="left", padx=10, pady=10)
                # while the second panel will store the edge map

            # otherwise, update the image panels
            else:
                # update the pannels
                # area, bin_fruit, img_food, skin_area, fruit_contour, pix_to_cm_multiplier, raduis = getAreaOfFood(image_resize)
                img_food = cv2.cvtColor(image_resize, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(img_food)
                # ...and then to ImageTk format
                image = ImageTk.PhotoImage(image)
                self.area.configure(image=image)
                self.area.image = image

def main():

    root = Tk()
    root.geometry("900x500+200+200")
    app = Example()
    root.mainloop()


if __name__ == '__main__':
    main()