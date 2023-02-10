# OCR Pipeline

This project aims to compile some of the Chilean Constititional Assembly's more relevant data in a public access server in a standardized format, particularly so it can be used analyzed with ML techniques like NLP. An automated pipeline was engineered to acquire, transform, and store the data in a MongoDB database hosted in a AWS EC2 instance. For more information see accompanying Medium [post](https://medium.com/@laura.waggaman/pdf-text-extraction-pipeline-with-ocr-9c764645d2f).

Instructions on how to connect to the database and access the data gathered by this project can be found [here](https://github.com/Lwaggaman/OCR_Pipeline/blob/main/access_data.md)

### Tools
**Data Ingestion**:
- Selenium, beautifulsoup, time, random, and fake-useragent for scraping and parsing data.
- requests to get PDFs.

**Data Processing**
- textract to extract text.
- pdf2image and poppler to convert pdf to image.
- pytesseract, tesseract, and [spa.traineddata](https://github.com/tesseract-ocr/tessdata/blob/main/spa.traineddata) to perform Optical Character Recognition in Spanish.
- regex to clean and format text.

**Data Storage**:
- Pymongo to create and update MongoDB database.
- AWS EC2 instance to host database.


**Robustness**
- logging to track progress and errors.
- tqdm and contextlib for progress reports while scripts are running.

### Phase I

![](https://i.imgur.com/mzIuFwn.png)


### Phase II

![](https://i.imgur.com/SAtGznf.png)
