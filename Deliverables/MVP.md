## Engineering Project MVP
A public app that performs question answering using documents from the Assembly as context, with an option to filter by Assembly Member so the question is answered based on Norm Proposals signed by that Assembly Member and/or transcripts of their speeches in the chamber.


My pipeline for the project is:
- Scrape data from web/PDFs to MongoDB database.
- Preprocess data from database and reinsert it clean.
- Streamlit app that runs pretrained model on clean data from db.


I made a Streamlit app hosted in my local machine that performs Q&A, selecting the context based on 1 filter.

![](https://imgur.com/a/igjXR4c)

On next iterations I hope to:
- Add more fields so there are more filters (topic, party, etc).
- Scale, since I am working off only 3 Norm Proposals / datapoints.
- Deploy 