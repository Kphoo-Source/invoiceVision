from PIL import Image
import pytesseract
import streamlit as st

# Specify the path to the Tesseract executable if necessary
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'
  # Adjust path if necessary

# Title of the app
st.title("Image Text Extraction with Tesseract")

# Upload an image
uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    # Open the uploaded image
    image = Image.open(uploaded_image)
    
    # Display the image
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Extract text from the image using Tesseract
    extracted_text = pytesseract.image_to_string(image)
    
    # Display the extracted text
    st.write("Extracted Text:")
    st.write(extracted_text)

