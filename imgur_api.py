from main import picture
import requests,json
import os
import pyimgur


CLIENT_ID="f8562b07ca9f126"
folder_path=r'C:\code\inventory_product_desc\uploads'
file_path=picture.name
PATH = os.path.join(folder_path,file_path)
im=pyimgur.Imgur(CLIENT_ID)
uploaded_image = im.upload_image(PATH,title="name_any")
title = uploaded_image.title
link = uploaded_image.link
print(title)
print(link)


