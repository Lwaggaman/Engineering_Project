# Engineering_Project

#### Tools
**Data Ingestion**:
- Selenium, beautifulsoup, time, random, and fake-useragent for scraping and parsing data.
- requests to get PDFs.

**Data Processing**
- textract to extract text.
- pdf2image and poppler to convert pdf to image.
- pytesseract, tesseract, and [https://github.com/tesseract-ocr/tessdata/blob/main/spa.traineddata](spa.traineddata) to perform Optical Character Recognition in Spanish.
- regex to clean and format text.
**Data Storage**:
- Pymongo to create and update MongoDB database.
- AWS EC2 instance to host database.

**Robustness**
- logging to track processes and errors.
- tqdm and contextlib for progress reports while scripts are running.
