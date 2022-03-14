## Engineering Project MVP
A public app that performs question answering using documents from the Assembly as context, with an option to filter by Assembly Member so the question is answered based on Norm Proposals signed by that Assembly Member and/or transcripts of their speeches in the chamber.


My pipeline for the project is:
- Scrape data from web/PDFs to MongoDB database.
- Preprocess data from database and reinsert it clean.
- Streamlit app that runs pretrained model on clean data from db.


I made a Streamlit app hosted in my local machine that performs Q&A, selecting the context based on 1 filter.

![](https://github.com/Lwaggaman/Engineering_Project/blob/main/Deliverables/ezgif.com-gif-maker.gif)

*An Assemblymember is selected from a dropdown menu (from a pool of 3) and the question "What is lacking?" is typed in. After buffering, *gender perspective* is printed out.*


On next iterations I hope to:
- Add more fields so there are more filters (topic, party, etc).
- Scale, since I am working off only 3 Norm Proposals / datapoints.
- Deploy 