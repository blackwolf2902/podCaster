import os
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from dotenv import load_dotenv
import json
from datetime import datetime
from typing import List, Optional
import re

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

extra_headers = {
    # "HTTP-Referer": os.getenv("YOUR_SITE_URL", "https://localhost"),  # optional
    # "X-Title": os.getenv("YOUR_SITE_NAME", "PodCaster"),              # optional
}

# Enhanced system prompt for better conversation
chat_history: List[ChatCompletionMessageParam] = [
    {
        "role": "system",
        "content": (
            "You are PodCasterGPT, a professional podcast script writer and conversation partner. "
            "Your primary role is to create engaging, structured podcast content and help users refine their ideas. "
            "Key responsibilities:\n"
            "1. Generate well-structured podcast scripts with clear sections\n"
            "2. Provide constructive feedback on topic selection\n"
            "3. Suggest improvements and additional angles\n"
            "4. Help maintain engaging conversation flow\n"
            "5. Use Markdown for formatting (headers, bold, lists)\n"
            "Remember to stay focused on podcast-related content while being helpful and encouraging."
        )
    }
]

def format_quests(items: List[str]) -> str:
    if not items:
        return ''
    elif len(items) == 1:
        return items[0]
    elif len(items) == 2:
        return ' and '.join(items)
    else:
        return ', '.join(items[:-1]) + ', and ' + items[-1]

def generate_topic_suggestions(title: str) -> List[str]:
    """Generate relevant topic suggestions based on the podcast title"""
    prompt = f"Given the podcast title '{title}', suggest 5 relevant topics that would make interesting segments. Format as a JSON list."
    
    suggestion_response = client.chat.completions.create(
        model="deepseek/deepseek-r1-0528-qwen3-8b:free",
        messages=[{
            "role": "user",
            "content": prompt
        }],
        extra_headers=extra_headers
    )
    
    try:
        content = suggestion_response.choices[0].message.content if suggestion_response.choices and suggestion_response.choices[0].message.content else None
        if content:
            suggestions = json.loads(content)
            return suggestions if isinstance(suggestions, list) else []
    except Exception as e:
        print(f"Error generating suggestions: {e}")
        return []
    return []

def podCaster_init(title: str = '', topics: Optional[List[str]] = None) -> str:
    if topics is None:
        topics = []
    # Generate initial script with enhanced structure
    user_prompt = (
        f"Create an engaging podcast script for **{title}**\n\n"
        f"Topics to cover:\n{format_quests(topics)}\n\n"
        "Please structure the response with:\n"
        "1. An attention-grabbing introduction\n"
        "2. Clear segment transitions\n"
        "3. Engaging discussion points\n"
        "4. A memorable conclusion\n"
        "Use Markdown formatting for clear section organization."
    )
    chat_history.append({
        "role": "user",
        "content": user_prompt
    })
    completion = client.chat.completions.create(
        model="deepseek/deepseek-r1-0528-qwen3-8b:free",
        messages=chat_history,
        extra_headers=extra_headers
    )
    reply = completion.choices[0].message.content if completion.choices and completion.choices[0].message.content else None
    if reply:
        chat_history.append({
            "role": "assistant",
            "content": reply
        })
        return reply
    return "I apologize, but I couldn't generate a response at this time."

def podCaster_chat(user_msg: str) -> str:
    # Enhanced chat with context awareness
    context_prompt = (
        f"User message: {user_msg}\n\n"
        "Remember to:\n"
        "1. Stay focused on podcast content\n"
        "2. Provide constructive suggestions\n"
        "3. Use Markdown for formatting\n"
        "4. Maintain conversation continuity"
    )
    
    chat_history.append({
        "role": "user",
        "content": context_prompt
    })

    completion = client.chat.completions.create(
        model="deepseek/deepseek-r1-0528-qwen3-8b:free",
        messages=chat_history,
        extra_headers=extra_headers
    )

    if completion.choices[0].message.content:
        reply = completion.choices[0].message.content
        chat_history.append({
            "role": "assistant",
            "content": reply
        })
        return reply
    return "I apologize, but I couldn't generate a response at this time."

def clean_podcast_script(text: str) -> str:
    """
    Remove *, [], and non-speech/scene direction words from the script.
    Removes markdown formatting, bracketed actions, and common sound cues.
    """
    # Remove markdown bold/italic/headers
    text = re.sub(r'[\*#_`>\-]', '', text)
    # Remove [bracketed] content (scene directions)
    text = re.sub(r'\[.*?\]', '', text)
    # Remove common sound cues (case-insensitive)
    cues = [
        r'outro music', r'wind whistling', r'background music', r'applause',
        r'cheering', r'laughter', r'fade out', r'fade in', r'sound effect[s]?',
        r'\(.*?\)', r'\{.*?\}', r'\<.*?\>'
    ]
    for cue in cues:
        text = re.sub(cue, '', text, flags=re.IGNORECASE)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def save_podcast_script(title: str, content: str, request=None) -> Optional[str]:
    """Save the cleaned podcast script to a file and store filename in session if request is provided."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"podcast_script_{timestamp}.md"
    try:
        cleaned = clean_podcast_script(content)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n{cleaned}")
        if request is not None:
            request.session['latest_script_file'] = filename
        return filename
    except Exception as e:
        print(f"Error saving podcast script: {e}")
        return None
