import json
import os
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import cv2

with open('data.json', 'r') as json_file: # data to be imported
    data = json.load(json_file)

list_of_names = []
list_of_events = []

for item in data:
    list_of_names.append(item['name']) # tags to be stored in arrays
    list_of_events.append(item['desc'])

def delete_old_data():
    for i in os.listdir("temp-imgs/"):
        os.remove("temp-imgs/{}".format(i))

def cleanup_data():
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)

    list_of_names = []
    list_of_events = []

    for item in data:
        list_of_names.append(item['name'])
        list_of_events.append(item['desc'])

def generate_certificates():

    for index, (name,events) in enumerate(zip(list_of_names, list_of_events)): # add in the () to add more stuff to the certificate
        certificate_template_image = cv2.imread("certificate-template.jpg") # template of the certificate

        im_p = Image.fromarray(certificate_template_image)

        draw = ImageDraw.Draw(im_p)
        monospace = ImageFont.truetype("Alegreya.ttf",42) # change here to change font
        draw.text((325, 458),name,(255,255,255),font=monospace) # copy this and change name to anything to use the different arrays
        draw.text((325, 683),events,(255,255,255),font=monospace)

        result_o = np.array(im_p)

        cv2.imwrite("temp-imgs/{}.jpg".format(name), result_o) # store the pngs temporarily to convert
        print("Processing {} / {}".format(index + 1,len(list_of_names)))
      
def convert_images_to_pdfs(image_folder, pdf_destination):
    images = [f for f in os.listdir(image_folder) if f.endswith(".jpg") or f.endswith(".png")]
    
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
    generate_certificates()

    image_folder = "temp-imgs" # folder with the temporary images of the certificates
    pdf_destination = "cert-pdfs" # folder for the destination for the pdfs
    convert_images_to_pdfs(image_folder, pdf_destination)

    delete_old_data() # deleting the tempoary images

if __name__ == '__main__':
    main()


