import streamlit as st
import openai
import re
import os
import tiktoken

# Initialize OpenAI API
openai.api_key = os.environ["openai_api_key"]
encoding = tiktoken.encoding_for_model("gpt-4")

def translate_text(text):
    # Initialize conversation with a detailed system message
    system_message = """
    Given the English text as a task, go through the English text word by word and first exhaustively identify all the terminology words in the below English text and then use the most appropriate pure Hindi word for those terminologies as per the usage of that word in that context (refer point 1 of below-mentioned translation guidelines). And once done for all the terminology present in the text, first prepare a draft translation and then refine it based on style guides and the original English text to produce the final translation of the following English text into Hindi, strictly adhering to the below pointwise translation style guidelines:

    Guidelines:
    1. Pure Hindi Vocabulary: Use pure Hindi words and avoid any English words transliterated into Devanagari script.
    2. Devanagari Script: The translation must be in Devanagari script.
    3. Faithful Translation: Aim to preserve the original meaning and nuances of the English text as closely as possible.
    4. Complex Words: If a Hindi term is used that is not commonly employed in day-to-day language, provide the corresponding English word in brackets next to it for ease of comprehension.
    5. No Shortcuts: Do not abbreviate or take shortcuts in the translation; it should be complete and comprehensive.
    6. Terminology: If the English text contains specialized terminology, find the closest possible authentic Hindi equivalent or synthesize a new word which conveys the same meaning as of the original English terminology.
    7. Consistent vocabulary: Use consistent Hindi vocabulary throughout the translation process.
    8. Fluency: Translated text should be fluent.
    9. Error-Free: There should not be any linguistic error in the final translation.
    10. No information loss: There should not be any information loss in the translated Hindi text.

    Please make sure you strictly adhere to these guidelines during the translation process.
    """
    
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"TASK:\nEnglish Text:\n{text}"}
    ]
    
    # Call OpenAI API for translation
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )
    
    # Extract the translated text from the assistant's reply
    translated_text = response['choices'][0]['message']['content'].strip()
    
    return translated_text, response['usage']['prompt_tokens'], response['usage']['completion_tokens']



# Streamlit App
st.title("English to Hindi Translator")

# Instructions
st.write("## Instructions")
st.write("1. Enter the text you want to translate in the text box below. I kept the word limit to reduce the cost as the prompt size is already too high (~400 tokens).")
st.write("2. Click the 'Translate' button and wait for the process to complete.")
st.write("3. The translated text will appear below, which you can post-edit.")

# Text Input
user_input = st.text_area("Enter text to translate (Max 250 words):", max_chars=500)
word_count = len(re.findall(r'\w+', user_input))

# Word Counter
st.write(f"Word Count: {word_count}/250")

# Disable button if word count exceeds 250
if word_count > 250:
    st.warning("Word limit exceeded!")
    st.stop()

# Translate Button
# Create a placeholder for the "Translation in progress..." message
progress_placeholder = st.empty()

if st.button("Translate"):
    input_token_count = len(encoding.encode(user_input))
    st.write(f"Token count of input english text: {input_token_count}")
    with st.spinner("Translating..."):
        # Display the "Translation in progress..." message
        progress_placeholder.write("Translation in progress...")
        progress_placeholder.write("Please wait...")
        
        # Call the translation function
        translated_text, experiment_prompt_token, experiment_completion_token = translate_text(user_input)
        
        # Clear the "Translation in progress..." message
        progress_placeholder.empty()
        
        # Display the translated text
        st.write("## Translated Text")
        USD2INR = 83
        COST = round(((experiment_prompt_token * 0.03/1000 + experiment_completion_token*0.06/1000)*USD2INR),2)
        st.write(f"Prompt token: {experiment_prompt_token } and completion token: {experiment_completion_token}")
        st.write(f"cost calculation = (experiment_prompt_token * 0.03/1000 + experiment_completion_token*0.06/1000)*USD2INR)")
        st.write(f"Cost of this translation: {COST} INR ")
        st.text_area("You can post-edit the text below:", value=translated_text, max_chars=None)
