import os
import openai
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Initialize OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_social_media_reply(comment):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for a social media website. Your job is to reply to comments."},
            {"role": "user", "content": comment},
        ]
    )
    reply = response['choices'][0]['message']['content']
    return reply

def generate_blog_post(topic, length='medium'):
    length_map = {
        'short': 'a brief yet informative blog post',
        'medium': 'a detailed and engaging blog post',
        'long': 'an in-depth and comprehensive blog post'
    }
    
    length_description = length_map.get(length, 'a detailed and engaging blog post')
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert blog writer."},
            {"role": "user", "content": f"Write {length_description} on the topic: {topic}. Ensure it is engaging and relevant."},
        ]
    )
    
    blog_post = response['choices'][0]['message']['content']
    return blog_post

def fetch_post_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    content = soup.get_text()
    return content

def generate_comments_for_post(url, num_comments=5):
    post_content = fetch_post_content(url)
    
    if not post_content:
        return ["Could not fetch post content."]
    
    comments = []
    for _ in range(num_comments):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Your job is to generate comments for social media posts."},
                {"role": "user", "content": f"Here is the content of the post: {post_content}\nPlease generate a relevant comment."},
            ]
        )
        comment = response['choices'][0]['message']['content']
        comments.append(comment)
    
    return comments

def check_appropriateness(content):
    prompt = f"""
    You are a content moderation AI. Review the following content and determine if it adheres to the community guidelines.
    
    Content: {content}
    
    Respond with "Appropriate" if the content is suitable, and "Inappropriate" if the content violates guidelines. Additionally, provide a brief explanation for your decision.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a content moderation AI."},
            {"role": "user", "content": prompt}
        ]
    )
    
    result = response['choices'][0]['message']['content']
    print("DEBUG: Response from AI:", result)  # Debug print statement
    is_appropriate = "Appropriate" in result
    explanation = result.split("Explanation:")[-1].strip() if "Explanation:" in result else result.strip()
    
    return {"appropriate": is_appropriate, "explanation": explanation}


def gradio_chatbot_response(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for a social media platform."},
            {"role": "user", "content": user_input},
        ]
    )
    chatbot_reply = response['choices'][0]['message']['content']
    return chatbot_reply
