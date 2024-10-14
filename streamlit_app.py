import os
import json
import openai
import pandas as pd
import streamlit as st

def description_creator(description):
    # Load the configuration from the JSON file
    with open('OAI_CONFIG_LIST', 'r') as config_file:
        config = json.load(config_file)

    # Set the OpenAI API parameters from the loaded configuration
    openai.api_type = config[0]['api_type']
    openai.api_key = config[0]['api_key']
    openai.azure_endpoint = config[0]['base_url']
    openai.api_version = config[0]['api_version']

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

    prompt_description = f"""
        1. From the Bill of Material (BOM) description {description}, read this description and convert it into natural language
        2. Output format will be its natural language description in consise
        3. Note that output will be in no short form proper sentence(no stop words please))
        4. Just give the output and no helping structure"""

    natural_language_description, out_tokens, in_tokens = call_gpt(prompt_description)
    return natural_language_description
