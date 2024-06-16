import streamlit as st
from PIL import Image
import os
import phonenumbers
import json

# Directory to save uploaded images
IMAGE_DIR = 'uploaded_images'
# File to save likes data
LIKES_FILE = 'likes.json'

# Create the directory if it does not exist
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# Initialize likes data
if not os.path.exists(LIKES_FILE):
    with open(LIKES_FILE, 'w') as f:
        json.dump({}, f)

# Load likes data
def load_likes():
    with open(LIKES_FILE, 'r') as f:
        return json.load(f)

# Save likes data
def save_likes(likes):
    with open(LIKES_FILE, 'w') as f:
        json.dump(likes, f)

likes = load_likes()

# Set the admin phone number (replace with your actual phone number)
ADMIN_PHONE_NUMBER = '+212684472115'

# Initialize session state for user login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.phone_number = ''
    st.session_state.name = ''

# Function to validate phone number
def validate_phone_number(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        return phonenumbers.is_valid_number(parsed_number)
    except phonenumbers.phonenumberutil.NumberParseException:
        return False

# Function to log in user
def login():
    name = st.text_input("ادخل اسمك", value=st.session_state.name)
    phone_number = st.text_input("ادخل رقم هاتفك يبدا ب + 2126", value=st.session_state.phone_number)
    if st.button(" دخول"):
        if validate_phone_number(phone_number):
            st.session_state.name = name
            st.session_state.phone_number = phone_number
            st.session_state.logged_in = True
            st.success("تم الدخول بنجاح!")
        else:
            st.error("رقم هاتف خاطئ")

# Function to log out user
def logout():
    st.session_state.logged_in = False
    st.session_state.phone_number = ''
    st.session_state.name = ''
    st.success("Logged out successfully!")

# Function to toggle like
def toggle_like(image_file):
    if image_file not in likes:
        likes[image_file] = []
    if st.session_state.phone_number in likes[image_file]:
        likes[image_file].remove(st.session_state.phone_number)
    else:
        likes[image_file].append(st.session_state.phone_number)
    save_likes(likes)
    st.experimental_rerun()

# Display login or logout based on session state
if not st.session_state.logged_in:
    st.title(" مشاركات احسن صورة مصلى لعيد الاضحى")
    login()
else:
    st.title("خروف العيد")
    st.subheader(f"السلام عليكم, {st.session_state.name}")
    st.subheader(" الله اكبر سبحان الله الحمد لله لا اله الا الله")
    if st.session_state.phone_number == ADMIN_PHONE_NUMBER:
        st.subheader("You are logged in as admin")

    # File uploader
    uploaded_file = st.file_uploader("اضف صورة المصلى", type=["jpg", "jpeg", "png"])

    # Save and display the uploaded image
    if uploaded_file is not None:
        # Save the uploaded file
        with open(os.path.join(IMAGE_DIR, uploaded_file.name), 'wb') as f:
            f.write(uploaded_file.getbuffer())
        
        st.success("تمت اضافة الصورة بنجاح")

    # Display the catalog of uploaded images
    st.subheader(" المشاركات")

    # Define the number of columns for the grid
    num_columns = 3
    image_files = os.listdir(IMAGE_DIR)
    columns = st.columns(num_columns)

    for idx, image_file in enumerate(image_files):
        image_path = os.path.join(IMAGE_DIR, image_file)
        image = Image.open(image_path)
        
        # Place the image in the appropriate column
        with columns[idx % num_columns]:
            st.image(image, width=150)
            # Add a like button with heart icon
            liked = st.session_state.phone_number in likes.get(image_file, [])
            like_button_text = "❤️ Unlike" if liked else "🤍 Like"
            if st.button(like_button_text, key=f"like_{image_file}"):
                toggle_like(image_file)
            # Display like count
            like_count = len(likes.get(image_file, []))
            st.write(f"Likes: {like_count}")
            # Add a delete button for admin only
            if st.session_state.phone_number == ADMIN_PHONE_NUMBER:
                if st.button("Delete", key=f"delete_{image_file}"):
                    os.remove(image_path)
                    if image_file in likes:
                        del likes[image_file]
                        save_likes(likes)
                    st.experimental_rerun()

    # Add logout button
    if st.button("تسجيل الخروج"):
        logout()
