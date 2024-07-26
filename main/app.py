import os
from dotenv import load_dotenv
import openai
import gradio as gr
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Import functions from backend.py
from backend import get_social_media_reply, generate_blog_post, generate_comments_for_post, check_appropriateness, fetch_post_content

# Load environment variables from a .env file
load_dotenv()

# Initialize OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize LangChain model
llm = OpenAI(api_key=openai.api_key)
prompt_template = PromptTemplate(
    input_variables=["input"],
    template="You are a helpful assistant for a social media platform. Answer the following query: {input}"
)
llm_chain = LLMChain(
    llm=llm,
    prompt=prompt_template
)

def gradio_social_media_reply(comment):
    return get_social_media_reply(comment)

def gradio_generate_blog_post(topic, length):
    return generate_blog_post(topic, length)

def gradio_generate_comments_for_post(url, num_comments):
    comments = generate_comments_for_post(url, num_comments)
    formatted_comments = "\n\n".join(f"Comment {i+1}:\n{comment}" for i, comment in enumerate(comments))
    return formatted_comments

def gradio_check_post_appropriateness(url):
    result = check_appropriateness(fetch_post_content(url))
    status = "Appropriate" if result["appropriate"] else "Inappropriate"
    return f"Status: {status}\nExplanation: {result['explanation']}"

def gradio_chatbot(user_input):
    response = llm_chain.run(user_input)
    return response

with gr.Blocks() as demo:
    gr.Markdown("# Social Media Assistant Bot")
    
    with gr.Tab("Generate Comment Replies"):
        gr.Markdown("Paste the comment you want to generate a reply for and press enter")
        comment_input = gr.Textbox(label="Enter your comment:")
        reply_output = gr.Textbox(label="Generated Reply:", lines=2)
        comment_input.submit(gradio_social_media_reply, inputs=comment_input, outputs=reply_output)
    
    with gr.Tab("Generate Blog Post"):
        topic_input = gr.Textbox(label="Enter the blog post topic:")
        length_input = gr.Dropdown(label="Select length:", choices=["short", "medium", "long"], value="short")
        blog_post_output = gr.Textbox(label="Generated Blog Post:", lines=8)
        gr.Button("Generate Blog Post").click(gradio_generate_blog_post, inputs=[topic_input, length_input], outputs=blog_post_output)
    
    with gr.Tab("Generate Comments for Post"):
        url_input = gr.Textbox(label="Enter the URL of the post:")
        num_comments_input = gr.Slider(label="Number of comments:", minimum=1, maximum=9, step=1, value=4)
        comments_output = gr.Textbox(label="Generated Comments:", lines=15)
        gr.Button("Generate Comments").click(gradio_generate_comments_for_post, inputs=[url_input, num_comments_input], outputs=comments_output)
    
    with gr.Tab("Content Moderation"):
        post_url_input = gr.Textbox(label="Enter the URL of the post:")
        moderation_output = gr.Textbox(label="Moderation Result:", lines=5)
        gr.Button("Check Appropriateness").click(gradio_check_post_appropriateness, inputs=post_url_input, outputs=moderation_output)
    
    with gr.Tab("Chat with Bot"):
        gr.Markdown("I'll answer any questions you may have regarding the social media platform")
        user_input = gr.Textbox(label="Enter your message:")
        bot_output = gr.Textbox(label="Bot's response:", lines=5)
        user_input.submit(gradio_chatbot, inputs=user_input, outputs=bot_output)

# Launch the app
demo.launch()
