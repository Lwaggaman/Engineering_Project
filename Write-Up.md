## Engineering Tools Project
Chile is in the process of writing a new constitution. Should it be approved, it will shape the laws, way of governance, and future of the country. Tranparency and unbiased information of the nature of the proposals being put forth is critical for electors to make an informed decision when they vote in the exit plebiscite.

I set out to make a public app that performs question answering with BERT using documents from the Assembly as context, with an option to filter by Assembly Member so the question is answered based on Norm Proposals signed by that Assembly Member and/or transcripts of their speeches in the chamber. This is a quick way to see Members' positions on certain topics and the path that certain Norm Proposals and Commisions are taking.

#### Design

#### Data

#### Algorithms

#### Tools
**Data Ingestion**:
- Selenium, beautifulsoup, requests, and fake-useragent for scraping data.
- textract, pdf2image, pytesseract, tesseract, poppler, and regex to extract text from scraped PDFs.
**Data Storage**:
- mongoDB and pymongo to create database and 
**Deployment**
- Streamlit and Heroku

#### Communication
