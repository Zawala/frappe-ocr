# Copyright (c) 2023, zw and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import cv2 
import os
from frappe.utils import cstr
import pytesseract


class ScannedDocument(Document):
	def before_save(self):
		path=os.getcwd()
		print(path)
		site=cstr(frappe.local.site)
		img = cv2.imread(f'{path}/{site}{self.file}')
# Adding custom options
		custom_config = r'-c preserve_interword_spaces=1 --oem 1 --psm 1 -l eng+ita'
		self.scanned_contents=pytesseract.image_to_string(img, config=custom_config)
		print(pytesseract.image_to_string(img, config=custom_config))
