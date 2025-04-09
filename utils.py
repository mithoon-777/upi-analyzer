import fitz  # PyMuPDF
import pandas as pd
import re
from transformers import pipeline

summarizer = pipeline("text2text-generation", model="google/flan-t5-base")

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
    prompt = f"Analyze the following transaction table and give a summary with top spending categories and saving tips:\n{text}"
    result = summarizer(prompt, max_length=512, do_sample=False)
    return result[0]['generated_text']
