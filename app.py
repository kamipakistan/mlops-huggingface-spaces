# app.py
from transformers import pipeline
import gradio as gr

summarizer = pipeline('summarization')


def summarize_text(text, max_length=120, min_length=30):
    if not text or len(text.strip()) == 0:
        return "Please supply some text to summarize."
    out = summarizer(text, max_length=int(max_length), min_length=int(min_length))[0]['summary_text']
    return out


with gr.Blocks() as demo:
    gr.Markdown('# Text Summarizer')
    with gr.Row():
        inp = gr.Textbox(label='Input text', lines=8)
        out = gr.Textbox(label='Summary', lines=4)
    maxlen = gr.Slider(30, 512, value=120, step=1, label='Max length')
    minlen = gr.Slider(5, 200, value=30, step=1, label='Min length')
    btn = gr.Button('Summarize')

    btn.click(summarize_text, inputs=[inp, maxlen, minlen], outputs=out)


if __name__ == '__main__':
    demo.launch()
