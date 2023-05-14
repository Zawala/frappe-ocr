# Copyright (c) 2023, zw and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import cv2
import numpy as np 
import os
from frappe.utils import cstr
import pytesseract

class FileManager(Document):
    def before_save(self):
        try:
            path = os.getcwd()
            site = cstr(frappe.local.site)
            img = cv2.imread(f'{path}/{site}{self.file}')
            gray = self.get_grayscale(img)
            thresh = self.thresholding(gray)
            custom_config = r'--oem 3 --psm 6'
            self.scanned_contents = pytesseract.image_to_string(img, config=custom_config)
        except Exception as e:
            frappe.msgprint('Please Check file')

    def get_grayscale(self,image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # noise removal
    def remove_noise(self, image):
        return cv2.medianBlur(image, 5)

    # thresholding
    def thresholding(self, image):
        return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # dilation
    def dilate(self, image):
        kernel = np.ones((5, 5), np.uint8)
        return cv2.dilate(image, kernel, iterations=1)

    # erosion
    def erode(self,image):
        kernel = np.ones((5, 5), np.uint8)
        return cv2.erode(image, kernel, iterations=1)

    # opening - erosion followed by dilation
    def opening(self, image):
        kernel = np.ones((5, 5), np.uint8)
        return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

    # canny edge detection
    def canny(self, image):
        return cv2.Canny(image, 100, 200)

    # skew correction
    def deskew(self, image):
        coords = np.column_stack(np.where(image > 0))
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC,
                                 borderMode=cv2.BORDER_REPLICATE)
        return rotated

    # template matching
    def match_template(self, image, template):
        return cv2.matchTemplate(image, template,cv2.TM_CCOEFF_NORMED)