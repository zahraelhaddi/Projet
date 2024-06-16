import streamlit as st
from PIL import Image
import os

# Directory to save uploaded images
IMAGE_DIR = 'uploaded_images'

# Create the directory if it does not exist
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# Title of the website
st.title("مسابقة احسن صورة لصلاة العيد في المغرب")

# File uploader
uploaded_file = st.file_uploader("ادخل صورة مصلى العيد ", type=["jpg", "jpeg", "png"])

# Save and display the uploaded image
if uploaded_file is not None:
    # Save the uploaded file
    with open(os.path.join(IMAGE_DIR, uploaded_file.name), 'wb') as f:
        f.write(uploaded_file.getbuffer())
    
    st.success("تمت اضافة الصورة بنجاح!")

# Display the catalog of uploaded images
st.subheader("مجلد الصور")

# Define the number of columns for the grid
num_columns = 3
image_files = os.listdir(IMAGE_DIR)
columns = st.columns(num_columns)

for idx, image_file in enumerate(image_files):
    image_path = os.path.join(IMAGE_DIR, image_file)
    image = Image.open(image_path)
    # Place the image in the appropriate column
    with columns[idx % num_columns]:
        st.image(image, caption=image_file, width=150)
