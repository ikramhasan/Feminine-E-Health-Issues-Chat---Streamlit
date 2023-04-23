import csv
from fuzzywuzzy import fuzz 
from fuzzywuzzy import process 
import streamlit as st
import time
from gtts import gTTS
import os
import playsound


st.title('A Tale of Untold')
st.subheader('Finding the Gap in Feminine E-Health Issues in Bangladesh from Privileged and Marginalized Individuals Perspective')

search_result = ""

def return_result(dict, query, threshold):
    try:
        time.sleep(1)
        scores = []
        for key, value in enumerate(dict):
            ratios = [fuzz.ratio(str(query), str(value))] # ensure both are in string
            scores.append({ "index": key, "score": max(ratios)})

        filtered_scores = [item for item in scores if item['score'] >= threshold]
        sorted_filtered_scores = sorted(filtered_scores, key = lambda k: k['score'], reverse=True)
        index = sorted_filtered_scores[0]['index']
        result = list(list(dict.items())[index])
        return result[1]
    except:
        return "No result found :("

    

def open_dataset():
    with open('test.csv', mode='r', encoding="utf8") as infile:
        reader = csv.reader(infile)
        mydict = {rows[0]:rows[1] for rows in reader}
        return mydict
    
with st.spinner('Loading dataset...'):
    dataset = open_dataset()


tab1, tab2 = st.tabs(["Home", "Settings"])

with tab2:
    threshold = st.slider("Threshold", 0, 100, 35) # a number which ranges from 0 to 100, adjust it as per your requirement
    allow_text_to_speech = st.checkbox('Read out answers', value=True)


with tab1:
    query = st.text_input("Enter your question", "How can menstrual cramps be treated?")

    with st.spinner('Searching...'):
        with st.empty():
            search_result = return_result(dataset, query, threshold)
            st.write(search_result)
    if allow_text_to_speech:
        tts = gTTS(text=search_result, lang='bn', slow=False)
        filename = os.path.dirname(__file__)+ "/" + "result.mp3"
        tts.save(filename)
        playsound.playsound(filename)
        os.remove(filename)



            