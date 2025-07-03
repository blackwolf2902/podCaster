import markdown
from django.utils.safestring import mark_safe
from django.shortcuts import render, redirect
from django.contrib import messages
from .main import podCaster_init, podCaster_chat, generate_topic_suggestions, save_podcast_script
import os
from django.http import JsonResponse
from datetime import datetime
import subprocess
from bs4 import BeautifulSoup
import re
import traceback

def markdown_to_plaintext(md_text):
    """Convert Markdown text to plain readable text."""
    html = markdown.markdown(md_text)
    soup = BeautifulSoup(html, features="html.parser")
    return soup.get_text(separator="\n")

def remove_non_speech_chars(text):
    """Remove emojis and unusual symbols (keep only ASCII)."""
    return re.sub(r'[^\x00-\x7F]+', '', text)

def generate_podcast(request):
    """Generate podcast audio from the latest markdown script using local Piper TTS."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    # Get latest script file path from session
    script_file = request.session.get('latest_script_file')
    if not script_file or not os.path.exists(script_file):
        return JsonResponse({'error': 'No script found for this session.'}, status=404)

    # Read and clean the script
    with open(script_file, 'r', encoding='utf-8') as f:
        raw_md = f.read()

    plain_text = markdown_to_plaintext(raw_md)
    script_content = remove_non_speech_chars(plain_text)

    # Prepare Piper paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    piper_bin = os.path.join(base_dir, 'piper', 'piper')
    model_path = os.path.join(base_dir, 'piper', 'en_US-amy-medium.onnx')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(base_dir, 'piper', f'podcast_audio_{timestamp}.wav')  # WAV preferred for Piper

    if not os.path.exists(piper_bin) or not os.path.exists(model_path):
        return JsonResponse({'error': 'Piper binary or model not found'}, status=500)

    try:
        # Call Piper via subprocess
        process = subprocess.run(
            [piper_bin, '--model', model_path, '--output_file', output_file],
            input=script_content,
            text=True,
            capture_output=True
        )

        if process.returncode != 0:
            return JsonResponse({
                'error': 'Failed to generate audio',
                'stderr': process.stderr,
                'stdout': process.stdout
            }, status=500)

        # Return audio file URL
        audio_url = '/media/' + os.path.basename(output_file)
        return JsonResponse({'audio_url': audio_url})

    except Exception as e:
        return JsonResponse({
            'error': 'Exception occurred',
            'details': str(e),
            'traceback': traceback.format_exc()
        }, status=500)

def initial(request):
    title = ''
    topics = []
    suggestions = []
    
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        topics = [t.strip() for t in request.POST.getlist('topics') if t.strip()]
        
        if 'add_topic' in request.POST:
            topics.append('')
            suggestions = generate_topic_suggestions(title) if title else []
        
        elif 'submit' in request.POST:
            if not title:
                messages.error(request, 'Please enter a podcast title')
                topics = topics or ['']
            elif not topics:
                messages.error(request, 'Please add at least one topic')
                topics = ['']
            else:
                try:
                    response = podCaster_init(title, topics)
                    response_html = markdown.markdown(response)

                    # Save the script
                    script_file = save_podcast_script(title, response, request)
                    if script_file:
                        messages.success(request, f'Podcast script saved to {script_file}')

                    # Store in session
                    request.session['title'] = title
                    request.session['topics'] = topics
                    request.session['conversation'] = [('Bot', mark_safe(response_html))]

                    return redirect('mainChatter')
                except Exception as e:
                    messages.error(request, f'Error generating podcast script: {str(e)}')
    else:
        topics = ['']
    
    if not topics:
        topics = ['']
        
    return render(request, './asker.html', {
        'title': title,
        'topics': topics,
        'suggestions': suggestions,
    })

def mainChatter(request):
    # Retrieve stored conversation and context
    title = request.session.get('title', '')
    topics = request.session.get('topics', [])
    conversation = request.session.get('conversation', [])

    if request.method == 'POST':
        user_msg = request.POST.get('user_message', '').strip()
        if user_msg:
            try:
                # Get AI response
                bot_reply = podCaster_chat(user_msg)
                bot_reply_html = markdown.markdown(bot_reply)

                # Append to conversation
                conversation.append(('You', user_msg))
                conversation.append(('Bot', mark_safe(bot_reply_html)))

                # Save updated conversation
                request.session['conversation'] = conversation
            except Exception as e:
                messages.error(request, f'Error generating response: {str(e)}')

    return render(request, 'asker.html', {
        'title': title,
        'topics': topics,
        'conversation': conversation,
        'chat_mode': True,  # Flag to switch template into chat mode
    })