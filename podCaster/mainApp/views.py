from django.shortcuts import render, redirect
from .main import podCaster_init, podCaster_chat
import markdown
from django.utils.safestring import mark_safe

def initial(request):
    title = ''
    topics = []
    
    if request.method == 'POST':
        title = request.POST['title']
        topics = request.POST.getlist('topics')
        
        if 'add_topic' in request.POST:
            topics.append('')
        
        elif 'submit' in request.POST:
           response = podCaster_init(title, topics)

           # Store in session
           request.session['title'] = title
           request.session['topics'] = topics
           request.session['conversation'] = [('Bot', response)]

           return redirect('mainChatter')
    
    else:
        topics = ['']
    
    if not topics:
        topics = ['']
        
        
    return render(request, './asker.html',{
            'title' : title,
            'topics' : topics,
        })


def mainChatter(request):
    # Retrieve stored conversation and context
    title = request.session.get('title', '')
    topics = request.session.get('topics', [])
    conversation = request.session.get('conversation', [])

    if request.method == 'POST':
        user_msg = request.POST.get('user_message', '').strip()
        if user_msg:
            # Get AI response
            bot_reply = podCaster_chat(user_msg)
            bot_reply_html = markdown.markdown(bot_reply)

            # Append to conversation
            conversation.append(('You', user_msg))
            conversation.append(('Bot', mark_safe(bot_reply_html)))

            # Save updated conversation
            request.session['conversation'] = conversation

    return render(request, 'asker.html', {
        'title': title,
        'topics': topics,
        'conversation': conversation,
        'chat_mode': True,  # Flag to switch template into chat mode
    })