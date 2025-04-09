import google.generativeai as genai

# Replace with your actual API key or load from env
genai.configure(api_key="YOUR_GEMINI_API_KEY")

model = genai.GenerativeModel("gemini-pro")

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
