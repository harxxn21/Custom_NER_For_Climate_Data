
# library for streamlit
import streamlit as st
import spacy
#importing libraries for NER
from spacy import displacy

nlp = spacy.load("custom_climate_ner_model") #loading custom NER model

#library for extracting text from URL
from newspaper import Article

#function to extract NER
def ner_analyser(text):
    doc = nlp(text)
    ent_html = displacy.render(doc, style="ent", jupyter=False)
    st.markdown(ent_html, unsafe_allow_html=True)
    return
#UI code
st.title("Climate Change NER Analyser")
url = st.text_input("Enter URL")
st.write("OR")
text= st.text_area("Enter paragraph")

#button to analyze
if(st.button("Analyze")):
#checking if both URL and Text are entered
    if text and url:
        st.write("Please enter either URL or Text to analyze")
#checking if only text is entered
    elif text:
        ner_analyser(text)
#checking if only URL is entered
    elif url :
        #extracting text from URL
        try:
            article = Article(url)
            article.download()
            article.parse()
            url_text = article.text
            ner_analyser(url_text)

        except Exception as e:
            st.write("Please enter valid URL")
#checking if nothing is entered
    else:
        st.write("Please enter URL or Text to analyze")