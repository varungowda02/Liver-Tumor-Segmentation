'''
import streamlit as st
import utils
import os
import tensorflow as tf
from model import dice_coef_loss, dice_coef
from PIL import Image
import keras
import model
import io
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import tempfile
import numpy as np
import re


def create_report(name, phone_number, image1_path, image2_path, text, report_path):
    c = canvas.Canvas(report_path, pagesize=letter)
    width, height = letter

    # Add text to the report
    c.drawString(280, height - 60,  "REPORT")
    c.drawString(100, height - 100, f"Name: {name}")
    c.drawString(100, height - 120, f"Phone Number: {phone_number}")
    c.drawString(100, height - 140, text)

    # Add images to the report
    # Adjust these coordinates and sizes as needed
    c.drawString(100, height - 180, 'CT Scan')
    if os.path.exists(image1_path):
        c.drawImage(ImageReader(image1_path), 100, height - 380, width=400, height=200, preserveAspectRatio=True)

    c.drawString(100, height - 420, 'Segmentation Result')
    if os.path.exists(image2_path):
        c.drawImage(ImageReader(image2_path), 100, height - 640, width=400, height=200, preserveAspectRatio=True)

    c.save()


def save_uploaded_file(save_path, uploaded_file):
    try:
        with open(os.path.join(save_path, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.read())
        return uploaded_file.name
    except Exception as e:
        return False


# Main app function
def app():

    # if not st.session_state['logged_in']:
    #     return  # Stop execution if not logged in
    st.title('Liver Tumor Classification and Segmentation')

    save_path = './uploads'
    data_path = './data'

    #name = st.text_input("Name")
    #phone_number = st.text_input("Phone Number")
    name = st.text_input("Name")
    if not name.replace(" ", "").isalpha():  # Check if the name contains only alphabetic characters and spaces
        st.warning("Please enter a valid name with only alphabetic characters and spaces.")
        return
    phone_number = st.text_input("Phone Number")
    text = st.text_area("Additional Information")
    # Validate Name
    if not name.strip():  # Check if the name is not just whitespace
        st.warning("Please enter a valid name.")
        return

    # Validate Phone Number
    phone_pattern = re.compile(r'^[6789]\d{9}$')  # Regular expression for a valid Indian phone number
    if not phone_pattern.match(phone_number):
        st.warning("Please enter a valid 10-digit phone number.")
        return
    elif len(set(phone_number)) == 1:
        st.warning("Please enter a valid phone number, not repeating the same digit.")
        return

    img = st.file_uploader('Upload CT Scan', type=['png', 'jpeg', 'jpg'])

    predict_btn =  st.button('Predict')
    if predict_btn and img:
        # print(img.name)
        cls_model = tf.keras.models.load_model('./models/liver_tumor_resnet50.h5')
        seg_model = model.ResUNet()
        adam = keras.optimizers.Adam()
        seg_model.compile(optimizer=adam, loss=dice_coef_loss, metrics=["acc", dice_coef])
        seg_model.load_weights('./models/liver_model_final_resunet.h5')
        uploaded_res = save_uploaded_file(save_path, img)
        
        st.session_state['uploaded_res'] = uploaded_res

        valid_gen = utils.DataGen(image_path=os.path.join(save_path, uploaded_res), mask_path=uploaded_res)
        x, y = valid_gen.__getitem__()
        result = seg_model.predict(x)
        normalized_img = (result[0] * 255).squeeze().astype(np.uint8)

        sav_img = Image.fromarray(normalized_img)
        sav_img.save(save_path+'/result.png')

        predicted_class, prediction = utils.predict_tumor_class(cls_model, os.path.join(save_path, uploaded_res))
        result_text = f'Predicted Class: {predicted_class}'
        st.warning(result_text)

        st.session_state['result_text'] = result_text
        st.session_state['result_img_path'] = save_path + '/result.png'
        st.session_state['prediction_done'] = True

        if st.session_state['prediction_done']:

            image1 = Image.open(save_path+'/'+uploaded_res)
            col1, col2 = st.columns(2)
            with col1:
                st.image(image1, caption='Original Image', width=300)

            with col2:
                st.image(result[0], caption='Predicted Segmentation', width=300)


        # Downloadable report

    if st.session_state['prediction_done']:
        report_btn = st.button("Create Report")
        if report_btn:
            if st.session_state['uploaded_res'] and st.session_state['result_img_path']:
                image1_path = save_path+'/'+st.session_state['uploaded_res']
                image2_path = save_path+'/result.png'

                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
                    create_report(name, phone_number, image1_path, image2_path, st.session_state['result_text'], tmpfile.name)

                    # Provide the PDF for download
                    with open(tmpfile.name, "rb") as f:
                        st.download_button(
                            label="Download Report",
                            data=f,
                            file_name="report.pdf",
                            mime="application/pdf"
                        )


# Run the app

if 'prediction_done' not in st.session_state:
    st.session_state['prediction_done'] = False
if 'uploaded_res' not in st.session_state:
    st.session_state['uploaded_res'] = None
if 'result_img_path' not in st.session_state:
    st.session_state['result_img_path'] = None
if 'result_text' not in st.session_state:
    st.session_state['result_text'] = None


app()
'''
import streamlit as st
import utils
import os
import tensorflow as tf
from model import dice_coef_loss, dice_coef
from PIL import Image
import keras
import model
import io
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import tempfile
import numpy as np


def create_report(name, phone_number, image1_path, image2_path, text, report_path):
    c = canvas.Canvas(report_path, pagesize=letter)
    width, height = letter

    # Add text to the report
    c.drawString(280, height - 60,  "REPORT")
    c.drawString(100, height - 100, f"Name: {name}")
    c.drawString(100, height - 120, f"Phone Number: {phone_number}")
    c.drawString(100, height - 140, text)

    # Add images to the report
    # Adjust these coordinates and sizes as needed
    c.drawString(100, height - 180, 'CT Scan')
    if os.path.exists(image1_path):
        c.drawImage(ImageReader(image1_path), 100, height - 380, width=400, height=200, preserveAspectRatio=True)

    c.drawString(100, height - 420, 'Segmentation Result')
    if os.path.exists(image2_path):
        c.drawImage(ImageReader(image2_path), 100, height - 640, width=400, height=200, preserveAspectRatio=True)

    c.save()


def save_uploaded_file(save_path, uploaded_file):
    try:
        with open(os.path.join(save_path, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.read())
        return uploaded_file.name
    except Exception as e:
        return False


# Main app function
def app():

    # if not st.session_state['logged_in']:
    #     return  # Stop execution if not logged in
    st.title('Liver Tumor Classification and Segmentation')

    save_path = './uploads'
    data_path = './data'

    name = st.text_input("Name")
    phone_number = st.text_input("Phone Number")
    text = st.text_area("Additional Information")

    img = st.file_uploader('Upload CT Scan', type=['png', 'jpeg', 'jpg'])

    predict_btn =  st.button('Predict')
    if predict_btn and img:
        # print(img.name)
        cls_model = tf.keras.models.load_model('./models/liver_tumor_resnet50.h5')
        seg_model = model.ResUNet()
        adam = keras.optimizers.Adam()
        seg_model.compile(optimizer=adam, loss=dice_coef_loss, metrics=["acc", dice_coef])
        seg_model.load_weights('./models/liver_model_final_resunet.h5')
        uploaded_res = save_uploaded_file(save_path, img)
        
        st.session_state['uploaded_res'] = uploaded_res

        valid_gen = utils.DataGen(image_path=os.path.join(save_path, uploaded_res), mask_path=uploaded_res)
        x, y = valid_gen.__getitem__()
        result = seg_model.predict(x)
        normalized_img = (result[0] * 255).squeeze().astype(np.uint8)

        sav_img = Image.fromarray(normalized_img)
        sav_img.save(save_path+'/result.png')

        predicted_class, prediction = utils.predict_tumor_class(cls_model, os.path.join(save_path, uploaded_res))
        result_text = f'Predicted Class: {predicted_class}'
        st.warning(result_text)

        st.session_state['result_text'] = result_text
        st.session_state['result_img_path'] = save_path + '/result.png'
        st.session_state['prediction_done'] = True

        if st.session_state['prediction_done']:

            image1 = Image.open(save_path+'/'+uploaded_res)
            col1, col2 = st.columns(2)
            with col1:
                st.image(image1, caption='Original Image', width=300)

            with col2:
                st.image(result[0], caption='Predicted Segmentation', width=300)


        # Downloadable report

    if st.session_state['prediction_done']:
        report_btn = st.button("Create Report")
        if report_btn:
            if st.session_state['uploaded_res'] and st.session_state['result_img_path']:
                image1_path = save_path+'/'+st.session_state['uploaded_res']
                image2_path = save_path+'/result.png'

                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
                    create_report(name, phone_number, image1_path, image2_path, st.session_state['result_text'], tmpfile.name)

                    # Provide the PDF for download
                    with open(tmpfile.name, "rb") as f:
                        st.download_button(
                            label="Download Report",
                            data=f,
                            file_name="report.pdf",
                            mime="application/pdf"
                        )


# Run the app

if 'prediction_done' not in st.session_state:
    st.session_state['prediction_done'] = False
if 'uploaded_res' not in st.session_state:
    st.session_state['uploaded_res'] = None
if 'result_img_path' not in st.session_state:
    st.session_state['result_img_path'] = None
if 'result_text' not in st.session_state:
    st.session_state['result_text'] = None


app()
