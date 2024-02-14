import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import easyocr
import pymysql
from PIL import Image
import cv2
import os
import matplotlib.pyplot as plt
import re

# SETTING PAGE CONFIGURATIONS
icon = Image.open("C:/Users/hp/Downloads/zen class 1/project/icon.png")
st.set_page_config(page_title= "BizCardX: Extracting Business Card Data with OCR | By Ponishadevi",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This OCR app is created by *Ponishadevi*!"""})
st.markdown("<h1 style='text-align: center; color: white;'>BizCardX: Extracting Business Card Data with OCR</h1>", unsafe_allow_html=True)


# SETTING-UP BACKGROUND IMAGE


def setting_multicolor_bg():
    st.markdown(""" <style>
                        .stApp {
                            background: linear-gradient(to right, #3498db, #e74c3c, #2ecc71); /* Replace with your desired color stops */
                            background-size: cover;
                        }
                     </style>""", unsafe_allow_html=True) 

setting_multicolor_bg()

# CONNECTING WITH MYSQL DATABASE
pysql_connect = pymysql.connect(host='127.0.0.1', user='root', password='new_password', database="business")
cur = pysql_connect.cursor()

# TABLE CREATION
cur.execute('''CREATE TABLE IF NOT EXISTS card_data
                   (id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    company_name TEXT,
                    card_holder TEXT,
                    designation TEXT,
                    mobile_number VARCHAR(50),
                    email TEXT,
                    website TEXT,
                    area TEXT,
                    city TEXT,
                    state TEXT,
                    pin_code VARCHAR(10),
                    image LONGBLOB
                    )''')


def option_menu(options, selected_option, icons):
    """
    Custom option menu function to display icons and options horizontally.
    """
    col_space = st.columns(len(options))  # Create a column for each option

    for i, (col, option) in enumerate(zip(col_space, options)):
        is_selected = option == selected_option
        background_color = '#6495ED' if is_selected else '#F0F0F0'
        text_color = 'white' if is_selected else 'black'
        button_style = f"background-color: {background_color}; color: {text_color}"

        col.markdown(
            f'<div class="option" onclick="updateSelection({i})" style="{button_style}">'
            f'<span class="icon" style="font-size: 30px; margin-right: 10px;">{icons[i]}</span>'
            f'{option}'
            f'</div>',
            unsafe_allow_html=True
        )

# JavaScript to update the selected option
update_script = """
    <script>
        function updateSelection(index) {
            const options = document.querySelectorAll('.option');
            options.forEach((option, i) => {
                option.style.backgroundColor = i === index ? '#6495ED' : '#F0F0F0';
                option.style.color = i === index ? 'white' : 'black';
            });
        }
    </script>
"""

# Define options and icons
options_with_icons = {
    "Home": "🏠",
    "Upload & Extract": "☁️",
    "Modify": "✏️",
}

# Use custom option_menu function
selected_option = st.selectbox("Select an option:", list(options_with_icons.keys()))
option_menu(list(options_with_icons.keys()), selected_option, list(options_with_icons.values()))

# Display the JavaScript for updating selection
st.markdown(update_script, unsafe_allow_html=True)

# INITIALIZING THE EasyOCR READER
reader = easyocr.Reader(['en'])

# CONNECTING WITH MYSQL DATABASE
pysql_connect = pymysql.connect(host='127.0.0.1', user='root', password='new_password', database="business")
cur = pysql_connect.cursor()

# TABLE CREATION
cur.execute('''CREATE TABLE IF NOT EXISTS card_data
                   (id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    company_name TEXT,
                    card_holder TEXT,
                    designation TEXT,
                    mobile_number VARCHAR(50),
                    email TEXT,
                    website TEXT,
                    area TEXT,
                    city TEXT,
                    state TEXT,
                    pin_code VARCHAR(10),
                    image LONGBLOB
                    )''')


##-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###

# HOME MENU
if selected_option == "Home":
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            "<h2 style='color:#26547C;'>⭐ Technologies Used</h2>"
            "<p style='color:#2E3D49;'>Python, Easy OCR, Streamlit, SQL, Pandas</p>",
            unsafe_allow_html=True,
        )

        st.markdown(
            "<h2 style='color:#26547C;'>⭐ Objective</h2>"
            "<ul>"
            "<li>Upload an image of a business card.</li>"
            "<li>Extract relevant information using Easy OCR.</li>"
            "<li>View, modify, or delete extracted data.</li>"
            "<li>Save extracted information into a database.</li>"
            "<li>Intuitive user interface for easy interaction.</li>"
            "<li>Support for multiple entries in the database.</li>"
            "</ul>",
            unsafe_allow_html=True,
        )

    with col2:
        st.image("home.png", caption="App Overview", use_column_width=True)

    # Add some decorations
    st.markdown(
        "<div style='border: 2px solid #26547C; border-radius: 10px; box-shadow: 5px 5px 15px #888888; padding: 20px;'>"
        "<h3 style='color:#26547C; text-align:center; font-weight:bold; margin-bottom: 10px;'>"
        "Welcome to the Business Card Extractor App"
        "</h3>"
        "</div>",
        unsafe_allow_html=True,
    )

##----------------------------------------------------------------------------------------------------------------------------------------------------------##

# Check the selected option and perform actions accordingly
elif selected_option == "Upload & Extract":
    st.markdown("### Upload a Business Card")
    uploaded_card = st.file_uploader("Upload Business Card Image", type=["jpg", "jpeg", "png"], key="business_card_uploader")
    
    if uploaded_card is not None:
        # Create the folder if it doesn't exist
        os.makedirs("uploaded_cards", exist_ok=True)

        def save_card(uploaded_card):
            with open(os.path.join("uploaded_cards", uploaded_card.name), "wb") as f:
                f.write(uploaded_card.getbuffer())   
        save_card(uploaded_card)


# ...

        def image_preview(image, res): 
            for (bbox, text, prob) in res: 
                # unpack the bounding box
                (tl, tr, br, bl) = bbox
                tl = (int(tl[0]), int(tl[1]))
                tr = (int(tr[0]), int(tr[1]))
                br = (int(br[0]), int(br[1]))
                bl = (int(bl[0]), int(bl[1]))
                cv2.rectangle(image, tl, br, (0, 255, 0), 2)
                cv2.putText(image, text, (tl[0], tl[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

            return image

        # ...p; 

        # Displaying the uploaded card and preprocessed card with OCR highlights
# ...

# Displaying the uploaded card and preprocessed card with OCR highlights
        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.markdown("### Uploaded Business Card")
            st.image(uploaded_card, caption="Original Card", use_column_width=True)

        with col2:
            st.markdown("### Processed Business Card")
            with st.spinner("Processing image..."):
                st.set_option('deprecation.showPyplotGlobalUse', False)
                saved_img_path = os.path.join("uploaded_cards", uploaded_card.name)
                image = cv2.imread(saved_img_path)
                ocr_results = reader.readtext(saved_img_path)
                ocr_preview_image = image_preview(image.copy(), ocr_results)
                st.image(ocr_preview_image, caption="OCR Preview", use_column_width=True)


                #easy OCR
        saved_img = os.getcwd()+ "\\" + "uploaded_cards"+ "\\"+ uploaded_card.name
        result = reader.readtext(saved_img,detail = 0,paragraph=False)
        
        # CONVERTING IMAGE TO BINARY TO UPLOAD TO SQL DATABASE
        def img_to_binary(file):
            # Convert image data to binary format
            with open(file, 'rb') as file:
                binaryData = file.read()
            return binaryData

        data = {"company_name" : [],
                "card_holder" : [],
                "designation" : [],
                "mobile_number" :[],
                "email" : [],
                "website" : [],
                "area" : [],
                "city" : [],
                "state" : [],
                "pin_code" : [],
                "image" : img_to_binary(saved_img)
               }

        def get_data(res):
            for ind,i in enumerate(res):

                # To get WEBSITE_URL
                if "www " in i.lower() or "www." in i.lower():
                    data["website"].append(i)
                elif "WWW" in i:
                    data["website"] = res[4] +"." + res[5]

                # To get EMAIL ID
                elif "@" in i:
                    data["email"].append(i)

                # To get MOBILE NUMBER
                elif "-" in i:
                    data["mobile_number"].append(i)
                    if len(data["mobile_number"]) ==2:
                        data["mobile_number"] = " & ".join(data["mobile_number"])

                # To get COMPANY NAME  
                elif ind == len(res)-1:
                    data["company_name"].append(i)

                # To get CARD HOLDER NAME
                elif ind == 0:
                    data["card_holder"].append(i)

                # To get DESIGNATION
                elif ind == 1:
                    data["designation"].append(i)

                # To get AREA
                if re.findall('^[0-9].+, [a-zA-Z]+',i):
                    data["area"].append(i.split(',')[0])
                elif re.findall('[0-9] [a-zA-Z]+',i):
                    data["area"].append(i)

                # To get CITY NAME
                match1 = re.findall('.+St , ([a-zA-Z]+).+', i)
                match2 = re.findall('.+St,, ([a-zA-Z]+).+', i)
                match3 = re.findall('^[E].*',i)
                if match1:
                    data["city"].append(match1[0])
                elif match2:
                    data["city"].append(match2[0])
                elif match3:
                    data["city"].append(match3[0])

                # To get STATE
                state_match = re.findall('[a-zA-Z]{9} +[0-9]',i)
                if state_match:
                     data["state"].append(i[:9])
                elif re.findall('^[0-9].+, ([a-zA-Z]+);',i):
                    data["state"].append(i.split()[-1])
                if len(data["state"])== 2:
                    data["state"].pop(0)

                # To get PINCODE        
                if len(i)>=6 and i.isdigit():
                    data["pin_code"].append(i)
                elif re.findall('[a-zA-Z]{9} +[0-9]',i):
                    data["pin_code"].append(i[10:])
        get_data(result)
        #FUNCTION TO CREATE DATAFRAME
        def create_df(data):
            df = pd.DataFrame(data)
            return df
        df = create_df(data)
        st.success("### Data Extracted!")
        st.write(df)

        if st.button("Upload to Database"):
            for i,row in df.iterrows():
                #here %S means string values 
                sql = """INSERT INTO card_data(company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code,image)
                         VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                cur.execute(sql, tuple(row))
                # the connection is not auto committed by default, so we must commit to save our changes
                pysql_connect.commit()
            st.success("#### Uploaded to database successfully!")
        
##----------------------------------------------------------------------------------------------------------------------------------------------##

if selected_option == "Modify":
    st.write("You selected 'Modify'. Perform relevant actions here.")
    # You may want to modify data or perform other actions.
    col1,col2,col3 = st.columns([3,3,2])
    st.markdown("## Alter or Delete the data here")
    column1,column2 = st.columns(2,gap="large")
    try:
        with column1:
            cur.execute("SELECT card_holder FROM card_data")
            result = cur.fetchall()
            business_cards = {}
            for row in result:
                business_cards[row[0]] = row[0]
            selected_card = st.selectbox("Select a card holder name to update", list(business_cards.keys()))
            st.markdown("#### Update or modify any data below")
            cur.execute("select company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code from card_data WHERE card_holder=%s",
                            (selected_card,))
            result = cur.fetchone()
                        # DISPLAYING ALL THE INFORMATIONS
            company_name = st.text_input("Company_Name", result[0])
            card_holder = st.text_input("Card_Holder", result[1])
            designation = st.text_input("Designation", result[2])
            mobile_number = st.text_input("Mobile_Number", result[3])
            email = st.text_input("Email", result[4])
            website = st.text_input("Website", result[5])
            area = st.text_input("Area", result[6])
            city = st.text_input("City", result[7])
            state = st.text_input("State", result[8])
            pin_code = st.text_input("Pin_Code", result[9])

            if st.button("Commit changes to DB"):
            # Update the information for the selected business card in the database
                cur.execute("""UPDATE card_data SET company_name=%s,card_holder=%s,designation=%s,mobile_number=%s,email=%s,website=%s,area=%s,city=%s,state=%s,pin_code=%s
                                    WHERE card_holder=%s""", (company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code,selected_card))
                pysql_connect.commit()
                st.success("Information updated in database successfully.")


        with column2:
            cur.execute("SELECT card_holder FROM card_data")
            result = cur.fetchall()
            business_cards = {}
            for row in result:
                business_cards[row[0]] = row[0]
            selected_card = st.selectbox("Select a card holder name to Delete", list(business_cards.keys()))
            st.write(f"### You have selected :green[**{selected_card}'s**] card to delete")
            st.write("#### Proceed to delete this card?")

            if st.button("Yes Delete Business Card"):
                cur.execute(f"DELETE FROM card_data WHERE card_holder='{selected_card}'")
                pysql_connect.commit()
                st.success("Business card information deleted from database.")

                if st.button("View updated data"):
                    cur.execute("select company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code from card_data")
                    updated_df = pd.DataFrame(cur.fetchall(),columns=["Company_Name","Card_Holder","Designation","Mobile_Number","Email","Website","Area","City","State","Pin_Code"])
                    st.write(updated_df)
    except:
        st.warning("There is no data available in the database")
    
    if st.button("View updated data"):
        cur.execute("select company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code from card_data")
        updated_df = pd.DataFrame(cur.fetchall(),columns=["Company_Name","Card_Holder","Designation","Mobile_Number","Email","Website","Area","City","State","Pin_Code"])
        st.write(updated_df)

    else:
        st.write("You selected:", selected_option)
        # Handle other options or provide default content for Home.    