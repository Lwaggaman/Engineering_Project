## Data Engineering Project Proposal
#### Question/Need
Chile is in the process of writing a new constitution. Should it be approved, it will shape the laws, way of governance, and future of the country. With the polarization of the country and the proliferation of biased independent reporting in social media, tranparency and unbiased metrics of the nature of the proposals being put forth is critical for electors to make an informed decision when they vote in the exit plebiscite.


I set out to make a public app that performs question answering with [BETO](https://huggingface.co/dccuchile/bert-base-spanish-wwm-cased) (spanish BERT) using documents from the Assembly as context, with an option to filter by Assembly Member so the question is answered based on Norm Proposals signed by that Assembly Member and/or transcripts of their speeches in the chamber. This is a quick way to see Members' positions on certain topics and the overall bias of the Convention on certain topics.


In tests, I asked 'What has the State done?' using a few different Norm Proposals as context and got very different answers like "perpetuate the patriarchy", "abandoned its citizens by not imposing the rule of law", and "political inprisonment of prisoners of the [revolution](https://en.wikipedia.org/wiki/2019%E2%80%932021_Chilean_protests)", which gives you a better understanding of the signing Member's perspectives.

#### Data Description
- 1328 Norm Proposals scraped from the Assembly's [website](https://www.chileconvencion.cl/iniciativas-normas/)
- 65 Session Transcripts, to be divided into individual speeches.
- 165 Session Acts containing information about Each Session.
- ~195 Table Agreements containing additional information about each session.
- [Spanish](https://github.com/ccasimiro88/TranslateAlignRetrieve) version of the Stanford Question Answering Dataset ([SQuAD](https://rajpurkar.github.io/SQuAD-explorer/))

#### Pipeline
![pipeline](https://i.imgur.com/ri5jyT1.png)

I plan on saving trained model to database with code from this [article](https://medium.com/up-engineering/saving-ml-and-dl-models-in-mongodb-using-python-f0bbbae256f0)

#### Tools
-   Selenium, requests, pdf2image, and pytesseract to scrape PDFs and retrieve text.
-   Huggingface's transformer library, squad_utils, and PyTorch for modeling, with code from this [notebook](https://github.com/vgaraujov/Question-Answering-Tutorial/blob/master/Question_Answering_BERT_Spanish.ipynb).
-   MongoDB and PyMongo for CRUD operations.
-   Flask to develop public app.

#### MVP Goal
Trained model in local machine able to answer questions from database which has the Norm Proposals loaded. 
