import streamlit as st
import openai
import re
import os

# Initialize OpenAI API
openai.api_key = os.environ["openai_api_key"]

def translate_text(text):
    # Call OpenAI API for translation (Replace this with your actual API call)
    # prompt = f"Translate the following English text to Hindi: {text}"
    # response = openai.Completion.create(
    #     engine="text-davinci-002",
    #     prompt=prompt,
    #     max_tokens=100
    # )
    # translated_text = response.choices[0].text.strip()
    translated_text = text
    return translated_text

# Streamlit App
st.title("English to Hindi Translator")

# Instructions
st.write("## Instructions")
st.write("1. Enter the text you want to translate in the text box below.")
st.write("2. Click the 'Translate' button and wait for the process to complete.")
st.write("3. The translated text will appear below, which you can post-edit.")

# Text Input
user_input = st.text_area("Enter text to translate (Max 50 words):", max_chars=500)
word_count = len(re.findall(r'\w+', user_input))

# Word Counter
st.write(f"Word Count: {word_count}/50")

# Disable button if word count exceeds 50
if word_count > 50:
    st.warning("Word limit exceeded!")
    st.stop()

# Translate Button
# Create a placeholder for the "Translation in progress..." message
progress_placeholder = st.empty()

if st.button("Translate"):
    with st.spinner("Translating..."):
        # Display the "Translation in progress..." message
        progress_placeholder.write("Translation in progress...")
        progress_placeholder.write("Please wait...")
        
        # Call the translation function
        translated_text = translate_text(user_input)
        
        # Clear the "Translation in progress..." message
        progress_placeholder.empty()
        
        # Display the translated text
        st.write("## Translated Text")
        st.text_area("You can post-edit the text below:", value=translated_text, max_chars=None)
