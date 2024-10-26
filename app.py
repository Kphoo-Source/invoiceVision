#from PIL import Image
#import pytesseract
#import streamlit as st

# Specify the path to the Tesseract executable if necessary
#pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'
  # Adjust path if necessary

# Title of the app
#st.title("Image Text Extraction with Tesseract")

# Upload an image
#uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

#if uploaded_image is not None:
    # Open the uploaded image
    #image = Image.open(uploaded_image)
    
    # Display the image
    #st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Extract text from the image using Tesseract
    #extracted_text = pytesseract.image_to_string(image)
    
    # Display the extracted text
    #st.write("Extracted Text:")
    #st.write(extracted_text)

from PIL import Image
import pytesseract
import streamlit as st
import pandas as pd
from io import BytesIO
import re

# Specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'

# Title of the app
st.title("Invoice Data Extraction with Tesseract")

# Initialize session state to store data across uploads
if 'extracted_data' not in st.session_state:
    st.session_state['extracted_data'] = []

# File uploader (can accept multiple files)
uploaded_images = st.file_uploader("Choose images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# If there are uploaded files
if uploaded_images:
    for uploaded_image in uploaded_images:
        # Open the uploaded image
        image = Image.open(uploaded_image)
        
        # Display the image
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Extract text from the image using Tesseract
        extracted_text = pytesseract.image_to_string(image)
        
        # Display the extracted text for debugging purposes
        st.write("Extracted Text:")
        st.write(extracted_text)

        # Define regex patterns to extract specific fields
        address_pattern = r'Address:\s*(.)'  # Capture everything after "Address:"
        total_amount_pattern = r'TOTAL\s:\s*([\d,.]+)'  # Capture the total amount after "TOTAL:"
        tel_pattern = r'Tel[:.]?\s*([\+()\- \d]+)'  # Capture the telephone number
        date_pattern = r'(Invoice Date|Date)[:.]?\s*([\d]{1,2}-[A-Za-z]{3}-[\d]{4})'  # Capture date in DD-MMM-YYYY format
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'  # Email regex
        
        # Extracting the address using regex
        address_match = re.search(address_pattern, extracted_text, re.IGNORECASE)
        address = address_match.group(1).strip() if address_match else "Not found"
        
        # Extracting the total amount using regex
        total_amount_match = re.search(total_amount_pattern, extracted_text, re.IGNORECASE)
        total_amount = total_amount_match.group(1) if total_amount_match else "Not found"
        
        # Extracting the telephone number using regex
        tel_match = re.search(tel_pattern, extracted_text, re.IGNORECASE)
        telephone = tel_match.group(1).strip() if tel_match else "Not found"
        
        # Extracting the date using regex (DD-MMM-YYYY format)
        date_match = re.search(date_pattern, extracted_text, re.IGNORECASE)
        invoice_date = date_match.group(2) if date_match else "Not found"
        
        # Extracting the email using regex
        email_match = re.search(email_pattern, extracted_text)
        email = email_match.group(0).strip() if email_match else "Not found"

        # Append the extracted data to the session state list
        st.session_state['extracted_data'].append({
            'Invoice Date': invoice_date,
            'Address': address,
            'Email': email,
            'Telephone': telephone,
            'Total Amount': total_amount
        })
    
    # Create a DataFrame from the session state data
    df = pd.DataFrame(st.session_state['extracted_data'])
    
    # Display the cumulative DataFrame in the Streamlit app
    st.write("Extracted Data:")
    st.write(df)

    # Save the cumulative DataFrame to an Excel file
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='InvoiceData')
        output.seek(0)  # Reset the buffer to the beginning
    
    # Create a download button for the cumulative Excel file
    st.download_button(
        label="Download All Extracted Data as Excel",
        data=output,
        file_name="invoice_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
