import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ocr-tesseract-wrapper",
    version="0.0.7",
    author="Petar Jalusic",
    author_email="pjalusic@gmail.com",
    description="Tiny wrapper around pytesseract with image preprocessing and OCR configurations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pjalusic/ocr-tesseract-wrapper",
    packages=setuptools.find_packages(),
    package_dir={"ocr-tesseract-wrapper": "ocr_tesseract_wrapper"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pytesseract',
        'Pillow'
    ],
    python_requires='>=3.6',
)
