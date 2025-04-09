import gradio as gr
from utils import extract_text_from_pdf, clean_and_parse, analyze_transactions

def full_analysis(pdf):
    text = extract_text_from_pdf(pdf)
    df = clean_and_parse(text)
    insights = analyze_transactions(df)
    return df, insights

with gr.Blocks() as demo:
    gr.Markdown("# UPI Usage & Financial Analyzer using LLMs")
    file_input = gr.File(label="Upload UPI PDF")
    btn = gr.Button("Analyze")
    df_output = gr.DataFrame()
    summary_output = gr.Textbox(label="AI-Generated Insights")

    btn.click(fn=full_analysis, inputs=file_input, outputs=[df_output, summary_output])

demo.launch()
