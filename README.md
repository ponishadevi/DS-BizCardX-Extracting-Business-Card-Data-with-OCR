# DS-BizCardX-Extracting-Business-Card-Data-with-OCR
BizCardX: Extracting Business Card Data with OCR Overview BizCardX is a Streamlit web application which extracts data from business cards using Optical Character Recognition (OCR). Users can upload an image of a business card and the application uses the easyOCR library to extract relevant information from the card. The extracted information is then displayed in a user-friendly format and can be stored in a MySQL database for future reference.
The application has three main sections: Home, Upload & Extract, and Modify

Home:
Displays an overview of the application, including technologies used and its purpose.
Provides an image with some static content.

Upload & Extract:
Allows users to upload an image of a business card.
Uses EasyOCR to perform OCR on the uploaded business card image and extracts relevant information.
Displays the uploaded and processed business card images side by side.
Extracted information is displayed in a Pandas DataFrame.
Allows users to upload the extracted data to a MySQL database.

Modify:
Provides options to alter or delete data from the MySQL database.
Users can select a business card holder's name to update or delete the information.
Displays the existing data for the selected card holder.
Allows users to update the information for the selected card holder in the database.
Provides an option to delete the information of the selected card holder from the database.
Users can view the updated data from the database.
