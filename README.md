# ocr-tesseract-wrapper
Tiny wrapper around pytesseract with image preprocessing and OCR configurations

## Requirements
- tesseract installed (https://github.com/tesseract-ocr/tesseract/wiki#installation)

## Basic usage
```python
from ocr_tesseract_wrapper import OCR
ocr_tool = OCR()
results = ocr_tool.ocr([image])  # where image is Pillow image or string image path
```

## Advanced usage
```python
from ocr_tesseract_wrapper import OCR
ocr_tool = OCR()
results = ocr_tool.ocr([image1, image2], config=[])
"""
where config parameter is list of additional configs and restrictions for each of the 
images given to the OCR. for instance: [None, 'tessedit_char_whitelist=0123456789'] will 
apply no restriction to the first but will only return numeric characters from the second image.
""" 
```

