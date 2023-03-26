#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      adity
#
# Created:     26/03/2023
# Copyright:   (c) adity 2023
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import streamlit as st
import cv2
import imutils
import pytesseract
import tempfile

def extract(image):
    image = imutils.resize(image, width=300 )

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    st.image(gray_image,caption="greyed image")

    gray_image = cv2.bilateralFilter(gray_image, 11, 17, 17)
    st.image(gray_image,caption="smoothened image")

    edged = cv2.Canny(gray_image, 30, 200)
    st.image(edged,caption="edged image")

    cnts,new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    image1=image.copy()
    cv2.drawContours(image1,cnts,-1,(0,255,0),3)
    st.image(image1,caption="contours")

    cnts = sorted(cnts, key = cv2.contourArea, reverse = True) [:30]
    screenCnt = None
    image2 = image.copy()
    cv2.drawContours(image2,cnts,-1,(0,255,0),3)
    st.image(image2,caption="Top 30 contours")

    i=7
    for c in cnts:
            perimeter = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * perimeter, True)
            if len(approx) == 4:
                screenCnt = approx
                x,y,w,h = cv2.boundingRect(c)
                new_img=image[y:y+h,x:x+w]
                cv2.imwrite('./'+str(i)+'.png',new_img)
                i+=1
                break

    cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)
    st.image(image,caption="image with detected license plate")

    Cropped_loc = './7.png'
    st.image(cv2.imread(Cropped_loc),caption="cropped")
    plate = pytesseract.image_to_string(Cropped_loc, lang='eng')
    st.write("Number plate is:", plate)

def main():
    html_temp = """
    <div style="background-color:cyan;padding:10px">
    <h2 style="color:black;text-align:center;"> Vehicle Number Extraction </h2>
    </div><br>
    """
    st.markdown(html_temp,unsafe_allow_html=True)
    image_file = st.file_uploader("Upload Image", type=["png","jpg","jpeg"])
    if image_file is not None:
        st.image(image_file,caption="Uploaded Image")
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(image_file.read())
        image = cv2.imread(tfile.name)

        if st.button("Extract"):
            extract(image)


if __name__=='__main__':
    main()

