# Import required packages
import cv2
import pytesseract
from os import path

# Mention the installed location of Tesseract-OCR in your system
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # In case using colab after installing above modules


# Set the tesseract config to recognize special characters
def set_config():
    global config
    # config = '-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZéèêç(),- --psm 6'
    # config = '-c tessedit_char_whitelist=0123456789abc-:defghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZéèêç( ), --psm 6'
    config = "-c tessedit_char_whitelist=01-,23456789 --psm 6"


set_config()


def read_img(picture_path):
    # Read image from which text needs to be extracted

    output_file = picture_path.replace(path.splitext(picture_path)[1], ".txt")
    # Read image from which text needs to be extracted
    img = cv2.imread(picture_path)
    # Preprocessing the image starts
    # Preprocessing the image starts

    # Convert the image to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Performing OTSU threshold
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    # Specify structure shape and kernel size.
    # Kernel size increases or decreases the area
    # of the rectangle to be detected.
    # A smaller value like (10, 10) will detect
    # each word instead of a sentence.
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

    # Applying dilation on the threshold image
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

    # Finding contours
    contours, hierarchy = cv2.findContours(
        dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
    )

    # Creating a copy of image
    im2 = img.copy()

    # A text file is created and flushed
    file = open(output_file, "w+", encoding="utf-8")
    file.write("")
    file.close()

    # Looping through the identified contours
    # Then rectangular part is cropped and passed on
    # to pytesseract for extracting text from it
    # Extracted text is then written into the text file
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        # Drawing a rectangle on copied image
        cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Cropping the text block for giving input to OCR
        cropped = im2[y : y + h, x : x + w]
        # Open the file in append mode
        file = open(output_file, "a", encoding="utf-8")
        # Apply OCR on the cropped image
        text = pytesseract.image_to_string(cropped, lang="fra", config=config)
        # text = pytesseract.image_to_string(cropped,lang='fra', config='-c tessedit_char_whitelist=0123456789abA(),- --psm 6')
        # print(text)
        # Appending the text into file
        file.write(text)
        file.write("\n")
        # Close the file
        file.close()


def read_info_from_actual_turn(picture_path):
    # Read image from which text needs to be extracted

    output_file = picture_path.replace(path.splitext(picture_path)[1], ".txt")
    # print(output_file)
    # Read image from which text needs to be extracted
    img = cv2.imread(picture_path)
    # Preprocessing the image starts
    # Preprocessing the image starts

    # Convert the image to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Performing OTSU threshold
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    # Specify structure shape and kernel size.
    # Kernel size increases or decreases the area
    # of the rectangle to be detected.
    # A smaller value like (10, 10) will detect
    # each word instead of a sentence.
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

    # Applying dilation on the threshold image
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

    # Finding contours
    contours, hierarchy = cv2.findContours(
        dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
    )

    # Creating a copy of image
    im2 = img.copy()

    # A text file is created and flushed
    file = open(output_file, "w+", encoding="utf-8")
    file.write("")
    file.close()

    # Looping through the identified contours
    # Then rectangular part is cropped and passed on
    # to pytesseract for extracting text from it
    # Extracted text is then written into the text file
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        # Drawing a rectangle on copied image
        cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Cropping the text block for giving input to OCR
        cropped = im2[y : y + h, x : x + w]
        # Open the file in append mode
        file = open(output_file, "a", encoding="utf-8")
        # Apply OCR on the cropped image
        text = pytesseract.image_to_string(cropped, lang="fra", config=config)
        # text = pytesseract.image_to_string(cropped,lang='fra', config='-c tessedit_char_whitelist=0123456789abA(),- --psm 6')
        # print(text)
        # Appending the text into file
        file.write(text)
        file.write("\n")
        # Close the file
        file.close()
    # This code is modified by Susobhan Akhuli


# read_img(r'C:\Users\apeir\Documents\code\dofus\temp\temp_pict_2.png')
