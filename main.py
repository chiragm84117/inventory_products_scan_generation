import streamlit as st
import cv2
import numpy as np
import os
import pyimgur
from serpapi import GoogleSearch
from api_access_key import imgur_CLIENT_ID,lens_api_key


def save_uploaded_file(uploaded_image):
    try:
        with open(os.path.join('uploads', uploaded_image.name), 'wb') as f:
            f.write(uploaded_image.getbuffer())
        return True
    except:
        return False


def call_llm(information_graph,count):
    if count == 1:
        text1 = "chirag"
        return text1
    elif count == 2:
        text2 = "lavish"
        return text2


def generated_text_box(information_graph,count):
    text = call_llm(information_graph,count)
    # here the llm model will be called to generate the text from the data can from the google lens
    st.text_area(label="Generating", value=text, placeholder="This might take the moment.........", disabled=True,
                 height=200)
    st.write(f'The generated text have {len(text)} characters')
    return text


def upload(name):
    CLIENT_ID = imgur_CLIENT_ID
    folder_path = r'C:\code\inventory_product_desc\uploads'
    file_path = name
    PATH = os.path.join(folder_path, file_path)
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH)
    link = uploaded_image.link
    print(link)
    return link


def call_lens_api(link):
    params = {
        "engine": "google_lens",
        "hl":"en",
        "country" : "in",
        "url": link,
        "api_key": lens_api_key
    }
    search = GoogleSearch(params)
    results = search.get_json()
    # for checking if both are present in json or not

    visual_matches_exist = 'visual_matches' in results
    text_results_exist = 'text_results' in results
    knowledge_exist = 'knowledge_graph' in results
    related_content_exist ='related_content' in results

    information_graph = []

    if related_content_exist:
        for item in results['related_content']:
            content = item['query']
            information_graph.append(content)

    if knowledge_exist:
        for item in results['knowledge_graph']:
            title = item['title']
            information_graph.append(title)
            subtitle = item['subtitle']
            information_graph.append(subtitle)
        for knowledge_entry in results.get("knowledge_graph", []):
            # Check if "shopping_results" key is available in the current entry
            if "shopping_results" in knowledge_entry:
                # Access shopping_results for the current entry
                shopping_results = knowledge_entry["shopping_results"]
                # Iterate through shopping results
                for shopping_result in shopping_results:
                    price = shopping_result.get("price", "")
                    information_graph.append(price)
                    snippet = shopping_result.get("snippet", "")
                    information_graph.append(snippet)

    if text_results_exist:
        text_result = ' '.join(item['text'] for item in results.get('text_results', []))
        information_graph.append(text_result)

    if visual_matches_exist:
        for item in results['visual_matches']:
            visual = item['title']
            information_graph.append(visual)



    print(information_graph)
    return information_graph


# print the title on the UI
st.set_page_config(page_title="inventory product", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<h1 style='text-align: center; color: white'>INVENTORY DESCRIPTION GENERATOR</h1>", unsafe_allow_html=True)


# taking the image here
col3, col4, col5 = st.columns((0.25, 0.50, 0.25))
with col3:
    st.write("")
with col4:
    picture = st.camera_input("Take the product image")
with col5:
    st.write("")


# uploaded image processing
if picture is not None:
    # taking the imput of the image
    bytes_data = picture.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    # saving the image to local
    save_uploaded_file(picture)

    # upload the image to ingur
    link = upload(picture.name)

    # call the google lens API
    information_graph = call_lens_api(link)


    # print the upload picture
    col1, col2 = st.columns((1, 4), gap="small")

    with col1:
        st.header('Product')
        st.write("Sending the information !!")
        st.image(picture, width=200)

    # output text box of generated text
    with col2:
        count = 1
        st.header("Description :")
        text1 = generated_text_box(information_graph,count)
        count = count + 1
        next_decs1 = st.button(label="generate other")
        if next_decs1 == True:
            text2 = generated_text_box(information_graph,count)
            count = count + 1
