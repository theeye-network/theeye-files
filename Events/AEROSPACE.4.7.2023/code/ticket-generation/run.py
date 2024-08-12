import json
import os
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import cv2
import barcode
from barcode import generate
from barcode.writer import ImageWriter


with open('details.json', 'r') as json_file:
    data = json.load(json_file)

list_of_names = []
list_of_rollno = []
list_of_stream = []
list_of_wno = []

for participant in data:
    list_of_names.append(participant['Name'])
    list_of_stream.append(participant['Interest'])
    list_of_rollno.append(participant['Roll #'])
    list_of_wno.append(participant['WhatsApp #'])

def delete_old_data():
    for i in os.listdir("temp-imgs/"):
        os.remove(os.path.join("temp-imgs", i))
    for i in os.listdir("barcodes/"):
        os.remove(os.path.join("barcodes", i))

def cleanup_data():
    global list_of_names, list_of_stream,list_of_rollno,list_of_wno
    list_of_names = []
    list_of_rollno = []
    list_of_stream = []
    list_of_wno = []

    for participant in data:
        list_of_names.append(participant['Name'])
        list_of_stream.append(participant['Interest'])
        list_of_rollno.append(participant['Roll #'])
        list_of_wno.append(participant['WhatsApp #'])

def generate_barcode_images():
    barcode_folder = "barcodes"
    if not os.path.exists(barcode_folder):
        os.makedirs(barcode_folder)

    for rollno in list_of_rollno:
        code39 = barcode.get_barcode_class('code39')
        code = code39(rollno, writer=ImageWriter())
        barcode_path = os.path.join(barcode_folder, f"{rollno}")
        code.save(barcode_path,options={"write_text": False})

        print(f"Barcode image for {rollno} saved: {barcode_path}")

def generate_tickets():

    barcode_folder = "barcodes"

    for index, (name,events,roll,wno) in enumerate(zip(list_of_names, list_of_stream,list_of_rollno,list_of_wno)): # add in the () to add more stuff to the certificate
        ticket_template_image = cv2.imread("ticket-template.png") # template of the certificate

        im_p = Image.fromarray(ticket_template_image)

        draw = ImageDraw.Draw(im_p)
        monospace = ImageFont.truetype("Alegreya.ttf",42) # change here to change font
        draw.text((170, 1485),name,(0,0,0),font=monospace) # copy this and change name to anything to use the different arrays
        draw.text((170, 1810),events,(0,0,0),font=monospace)
        draw.text((870, 1485),roll,(0,0,0),font=monospace)
        draw.text((870, 1810),wno,(0,0,0),font=monospace)

        barcode_path = os.path.join(barcode_folder, f"{roll}.png")
        barcode_image = Image.open(barcode_path)
        im_p.paste(barcode_image, (400, 2080))

        result_o = np.array(im_p)

        cv2.imwrite("temp-imgs/{}.png".format(roll), result_o) # store the pngs temporarily to convert
        print("Processing {} / {}".format(index + 1,len(list_of_names)))
      
def convert_images_to_pdfs(image_folder, pdf_destination):
    images = [f for f in os.listdir(image_folder) if f.endswith(".png") or f.endswith(".png")]
    
    if not images:
        print("No images found in the specified folder.")
        return
    
    for image in images:
        image_path = os.path.join(image_folder, image)
        pdf_path = os.path.join(pdf_destination, f"{os.path.splitext(image)[0]}.pdf")
        
        with Image.open(image_path) as img:
            img.save(pdf_path, "PDF")
        
        print(f"Image '{image}' saved as PDF: {pdf_path}")

def main():
    delete_old_data()
    cleanup_data()
    generate_barcode_images()
    generate_tickets()

    image_folder = "temp-imgs" # folder with the temporary images of the certificates
    pdf_destination = "ticket-pdfs" # folder for the destination for the pdfs
    convert_images_to_pdfs(image_folder, pdf_destination)

    delete_old_data() # deleting the tempoary images

if __name__ == '__main__':
    main()


