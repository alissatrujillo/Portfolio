import streamlit as st  
import pandas as pd  
import numpy as np
import os
from fpdf import FPDF

from ast import literal_eval

## cd "ali/Documents/Grad/DSC 680/Projects/Project 3"

st.title('Generate a Trivia Quiz for Your Next Event!')

trivia_db = pd.read_csv('questions.csv', converters={'Category': literal_eval})

## Generating the Trivia Question Set

def generate(category, diff, q):
    
    trivia_db = pd.read_csv('questions.csv', converters={'Category': literal_eval})
    trivia_db['Topical'] = False

    if diff == 'Any':
        diff = ['Easy', 'Medium', 'Hard']
    
    for i, question in trivia_db.iterrows():
        if category == 'General':
            trivia_db = trivia_db.assign(Topical=True)
        elif (category in question['Category']) and (question['Difficulty'] in diff):
            trivia_db.at[i, 'Topical'] = True
            
    valid_qs = trivia_db.loc[trivia_db['Topical'] == True]
    
    if valid_qs.shape[0] < q:
        print('There are only', valid_qs.shape[0], 'questions that match your topic.', 
              valid_qs.shape[0], 'questions will be generated.')
        
    select = valid_qs.sample(n=q)
    select = select.reset_index()
    
    topics = []
    
    for i, question in select.iterrows():
        if question['Topic'] not in topics:
            topics.append(question['Topic'])
    
    create_pdf(select, category, topics)
    
## Creating the Trivia Host PDF
    
def create_pdf(select, category, topics):
    pdf = FPDF()
    pdf.add_page()
    
    pg_w = pdf.w - 2*pdf.l_margin
    
    title = category + ' Trivia Night - Host Sheet'
    pdf.set_font('helvetica', 'B', size=20)
    pdf.cell(200, 10, txt=title, ln=1, align='C')
    
    topics = ', '.join(topics)
    tpc = 'Topics included: ' + topics
    pdf.set_font('helvetica', size=10)
    pdf.multi_cell(pg_w, 5, txt=tpc, ln=1, align='C')
    pdf.ln(5)

    for i, question in select.iterrows():
        ques = 'Question #' + str(i+1) + ': ' + question['Question']
        pdf.set_font('helvetica', 'B', size=14)
        pdf.multi_cell(pg_w, 7.5, txt=ques, ln=1, align='C')
        
        top_dif = 'Topic: ' + question['Topic'] + ' // Difficulty: ' + question['Difficulty']
        pdf.set_font('helvetica', size=10)
        pdf.cell(200, 5, txt=top_dif, ln=1, align='C')
        
        ans = 'Correct Answer: ' + question['Correct Answer']
        pdf.set_font('helvetica', 'B', size=12)
        pdf.cell(200, 5, txt=ans, ln=1, align='C')
        
        src = 'Source: ' + str(question['Source'])
        pdf.set_font('helvetica', size=10)
        pdf.multi_cell(pg_w, 5, txt=src, ln=1, align='C')
        pdf.ln(5)
        
    return pdf.output(name='ths.pdf', dest='S')

### Inputting User Settings

trivia_db['Topical'] = False

##### Category

categories = trivia_db['Category'].explode().value_counts()
categories = categories[categories > 10].index.tolist()

topic_cat = trivia_db['Topic'].value_counts()
topic_cat = topic_cat[topic_cat > 10].index.tolist()

try:
    categories.append(topic_cat[0])
except:
    pass

categories.insert(0, 'General')

category = st.selectbox(
   "Select Category:",
   (categories),
   index=0)

##### Difficulty

for i, question in trivia_db.iterrows():
    if category == 'General':
        trivia_db = trivia_db.assign(Topical=True)
    elif category in question['Category']:
        trivia_db.at[i, 'Topical'] = True

valid_qs = trivia_db.loc[trivia_db['Topical'] == True]

diff_opts = valid_qs['Difficulty'].value_counts()
diff_opts = diff_opts[diff_opts >= 10].index.tolist()
diff_opts = diff_opts
diff_opts.insert(0, 'Any')

diff = st.radio("Difficulty:", diff_opts, index=0, horizontal=True)

##### Questions

if diff == 'Any':
    diff = ['Easy', 'Medium', 'Hard']
else:
    diffic = []
    diffic.append(diff)
    diff = diffic

valid_qs = trivia_db.loc[trivia_db['Topical'] == True]
valid_qs = valid_qs.loc[trivia_db['Difficulty'].isin(diff)]
            
num_qs = valid_qs.shape[0]

max_qs = min(num_qs, 50)

q = st.slider("Number of Questions:", 5, max_qs, value=10, step=1)

### Generating the PDF

pdf = generate(category, diff, q)

with open("ths.pdf", "rb") as file:
    btn=st.download_button(
    label="Generate Trivia Host Sheet",
    data=file,
    file_name="TriviaHostSheet.pdf",
    mime="application/octet-stream"
)