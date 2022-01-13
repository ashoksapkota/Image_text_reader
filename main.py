# importing tkinter for gui
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import cv2
import pytesseract

# location of tesseract.exe file
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Create root Windows with title Text from Image and center as initial place to start.
root = Tk()
root.title('Text from Image')
root.eval('tk::PlaceWindow . center')

newline = Label(root)
uploaded_img = Label(root)
v = Scrollbar(root, orient='vertical')
v.pack(side=RIGHT, fill=Y)

h = Scrollbar(root, orient='horizontal')
h.pack(side=BOTTOM, fill=X)


def extract(path):
    actual_image = cv2.imread(path)

    # resize
    resize = (450, 400)

    # resize image
    altered_img = cv2.resize(actual_image, resize)

    image_ht, image_wd, _ = altered_img.shape
    altered_img = cv2.cvtColor(altered_img, cv2.COLOR_BGR2RGB)
    texts = pytesseract.image_to_data(altered_img)
    mytext = ""
    prevy = 0
    for cnt, text in enumerate(texts.splitlines()):
        if cnt == 0:
            continue
        text = text.split()
        if len(text) == 12:
            x, y, w, h = int(text[6]), int(text[7]), int(text[8]), int(text[9])
            if len(mytext) == 0:
                prey = y
            if prevy - y >= 10 or y - prevy >= 10:
                print(mytext)
                Label(root, text=mytext, font=('Times', 15, 'bold')).pack()
                mytext = ""
            mytext = mytext + text[11] + " "
            prevy = y
    Label(root, text=mytext, font=('Times', 15, 'bold')).pack()


def show_extract_button(path):
    extractBtn = Button(root, text="Extract text", command=lambda: extract(path), bg="#800000", fg="white", pady=15,
                        padx=15, font=('Garamond', 15, 'bold'))
    extractBtn.pack()


def upload():
    try:
        path = filedialog.askopenfilename()
        image = Image.open(path)
        img = ImageTk.PhotoImage(image)
        uploaded_img.configure(image=img)
        uploaded_img.image = img
        show_extract_button(path)
    except:
        pass


Button(root, text="Upload an image", command=upload, bg="#800000", fg="white", height=2, width=20,
       font=('Garamond', 15, 'bold')).pack()
newline.configure(text='\n')
newline.pack()
uploaded_img.pack()

root.mainloop()
