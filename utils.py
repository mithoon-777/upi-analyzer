import fitz  # PyMuPDF
import pandas as pd
import re
import google.generativeai as genai
import os

# Configure Gemini API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def clean_and_parse(text):
    pattern = re.compile(r"(\d{2}-\d{2}-\d{4}).*?to\s(.*?).*?Rs\.\s?([0-9,]+.\d{2})", re.IGNORECASE)
    matches = pattern.findall(text)

    data = []
    for match in matches:
        date, receiver, amount = match
        amount = float(amount.replace(',', ''))
        data.append([date, receiver.strip(), amount])

    df = pd.DataFrame(data, columns=["Date", "To", "Amount"])
    return df

def analyze_transactions(df):
    text = df.to_string(index=False)
    prompt = f"""
    You are a financial assistant. Analyze the following UPI transactions:

    {text}

    Provide:
    - Top 3 spending categories
    - Any wasteful or unusual expenses
    - Smart suggestions to save money next month
    """
    response = model.generate_content(prompt)
    return response.text
