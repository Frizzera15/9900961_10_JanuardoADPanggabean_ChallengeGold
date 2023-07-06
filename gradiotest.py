import gradio as gr
from gradio import components

def analyze_sentiment(text):
    # Your sentiment analysis logic goes here
    # This is just a placeholder
    if "good" in text.lower():
        return "Positive sentiment"
    elif "bad" in text.lower():
        return "Negative sentiment"
    else:
        return "Neutral sentiment"

# Create the Gradio interface
gr.Interface(
    fn=analyze_sentiment,
    inputs=components.Textbox(label="Enter some text"),
    outputs=components.Textbox(label="Sentiment")
).launch()
