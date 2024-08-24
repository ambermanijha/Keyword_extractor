import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load model directly
tokenizer = AutoTokenizer.from_pretrained("ilsilfverskiold/tech-keywords-extractor")
model = AutoModelForSeq2SeqLM.from_pretrained("ilsilfverskiold/tech-keywords-extractor")

# Streamlit app
st.title('Tech Keywords Extractor')

input_text = st.text_area("Enter the text for keyword extraction:")

if st.button('Extract Keywords'):
    if input_text:
        inputs = tokenizer.prepare_seq2seq_batch([input_text], return_tensors="pt")
        outputs = model.generate(**inputs)
        keywords = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
        st.write('Extracted Keywords:')
        st.write(keywords)
    else:
        st.write('Please enter some text.')
