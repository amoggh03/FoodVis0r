# gpt.py

import openai

# Replace 'your_api_key' with your actual API key
api_key = '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'

# Set up the OpenAI API key
openai.api_key = api_key

# System prompt to analyze the medical report
system_prompt_medical = """
You are a medical doctor. Read the following medical report and categorize the findings into allergies, deficiencies, excessiveness, and diseases. Provide your findings as a list under each category.
"""

def extract_medical_info(report):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[
            {"role": "system", "content": system_prompt_medical},
            {"role": "user", "content": report}
        ],
        temperature=0.7
    )
    return response.choices[0].message['content']

# System prompt for analyzing ingredients
system_prompt_ingredients = """
You are supposed to give the possible quantity of a particular ingredient (in numbers only) in a product of given quantity. ALWAYS refer to the product's official website or other reliable source. Add source information also. Never give a blank answer or not specified or Quantity not specified, if you are not sure, try to use your knowledge and give an approximate value. I want a quantity at any cost.
Only respond with all ingredients and its quantity.
"""

def analyze_ingredients(ingredients):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[
            {"role": "system", "content": system_prompt_ingredients},
            {"role": "user", "content": ingredients}
        ],
        temperature=0.7
    )
    return response.choices[0].message['content']
