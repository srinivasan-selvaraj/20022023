"""
Take a two pdf and compare the image find the difference
do not use any ml library like pilllow, opencv
use library like fitz
PyMuPDF
"""


import fitz



def extract_image(doc):
    temp = {}
    for page_index in range(len(doc)): # iterate over pdf pages
        image_list = doc[page_index].get_images(full=True) if len(doc) != 0 else None
        temp[page_index] = len(image_list) if image_list else 0
    return temp


def count_images(left,right):
    right_doc = fitz.open(right)
    left_doc = fitz.open(left)
    right_value = extract_image(doc=right_doc)
    left_value = extract_image(doc=left_doc)
    pages = set(list(right_value.keys()) + list(left_value.keys()))
    output = {}
    for i in pages:
        output[f'page_{i}'] = (left_value[i] if left_value.get(i) else 0,right_value[i] if right_value.get(i) else 0)
    return output
    

val = count_images(left="test_4.pdf",right="testA.pdf")
print(val)
    