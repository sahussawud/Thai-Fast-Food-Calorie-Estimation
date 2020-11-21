# import the necessary packages
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import cv2

from tkinter import Tk, Text, BOTH, W, N, E, S
from tkinter.ttk import Frame, Button, Label, Style

zoom = 0.2
upload = Image.open("upload.png")

class Example(Frame):
    area = None
    pixels_x, pixels_y = tuple([int(zoom * x)  for x in upload.size])
    
    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.master.title("Thai Food Calories Estimate Program")
        self.pack(fill=BOTH, expand=True)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)

        lbl = Label(self, text="เลือกภาพ")
        lbl.grid(sticky=W, pady=4, padx=5)

        
        bardejov = ImageTk.PhotoImage(upload.resize((self.pixels_x, self.pixels_y)))
        self.area = Label(self, image=bardejov)
        self.area.image = bardejov
        
        self.area.grid(row=1, column=0, columnspan=2, rowspan=2,
            padx=2, sticky=E+W+S+N)



        abtn = Button(self, text="Activate")
        abtn.grid(row=1, column=3)

        cbtn = Button(self, text="Close")
        cbtn.grid(row=2, column=3, pady=4)

        hbtn = Button(self, text="เลือกภาพจากคอมพิวเตอร์", command=self.select_image)
        hbtn.grid(row=5, column=0, padx=5)

        obtn = Button(self, text="OK")
        obtn.grid(row=5, column=3)

    def select_image(self):
        # grab a reference to the image panels
        path = filedialog.askopenfilename()
        # ensure a file path was selected
        if len(path) > 0:
            # load the image from disk, convert it to grayscale, and detect
            # edges in it
            image = cv2.imread(path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
            # OpenCV represents images in BGR order; however PIL represents
            # images in RGB order, so we need to swap the channels
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # convert the images to PIL format...
            image = Image.fromarray(image)

            # ...and then to ImageTk format
            image = ImageTk.PhotoImage(image)

            # if the panels are None, initialize them
            if self.area is None:
                # the first panel will store our original image
                self.area = Label(image=image)
                self.area.image = image.resize((self.pixels_x, self.pixels_y))
                self.area.pack(side="left", padx=10, pady=10)
                # while the second panel will store the edge map

            # otherwise, update the image panels
            else:
                # update the pannels
                self.area.configure(image=image)
                self.area.image = image.resize((self.pixels_x, self.pixels_y))


def main():

    root = Tk()
    root.geometry("350x300+300+300")
    app = Example()
    root.mainloop()


if __name__ == '__main__':
    main()