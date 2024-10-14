import openai
import streamlit as st
import json

# Function to call the model
def call_gpt(prompt):
    response = openai.chat.completions.create(
        model="gpt-4o", 
        messages=[
            {"role": "user", "content": prompt}
        ],
        seed=42,
    )
    return response.choices[0].message.content, response.usage.completion_tokens, response.usage.prompt_tokens

# Function to create natural language description
def description_creator(description):
    # Set the OpenAI API parameters from the Streamlit secrets
    openai.api_type = st.secrets["openai"]["api_type"]
    openai.api_key = st.secrets["openai"]["api_key"]
    openai.azure_endpoint = st.secrets["openai"]["base_url"]
    openai.api_version = st.secrets["openai"]["api_version"]

    prompt_description = f"""
        1. From the Bill of Material (BOM) description {description}, read this description and convert it into natural language
        2. Output format will be its natural language description in concise
        3. Note that output will be in no short form proper sentence(no stop words please))
        4. Just give the output and no helping structure"""

    natural_language_description, out_tokens, in_tokens = call_gpt(prompt_description)
    return natural_language_description

# Streamlit app
st.title("BOM Description to Natural Language Converter")

# User input
description = st.text_area("Enter the BOM description:")

if st.button("Generate Description"):
    if description:
        natural_language_description = description_creator(description)
        st.write("### Natural Language Description")
        st.write(natural_language_description)
    else:
        st.write("Please enter a description.")
