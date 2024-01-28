# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 19:22:29 2024

@author: ben
"""

import streamlit as st
from openai import OpenAI
import json

client = OpenAI(api_key = 'sk-PUtYourKeyHere')


def create_system_prompt(conversation, character_description):
    prompt = """ You are playing a character in a conversation. You are to
    respond to the current conversation, yet staying in your character. This
    is a conversation, so be open ended. Bring up things, pose questions. 
    Give the other characters stuff to work with. If you were the last person
    to speak, but it's your turn again, then assume you should guide the 
    conversation to new topics. 
    
    **Your Character:**
    
    """
    # add character to prompt
    prompt += character_description + "\n\n **The conversation history**"
    
    # add conversation history to prompt
    for message in conversation:
        prompt += f"\n{message['role']}: {message['content']}"
    
    # instructions on format
    prompt += """ answer in JSON with key 'answer'.
    For example, if you wanted to say "That's not right, it was 8 o clock",
    your response should be:
        {"answer": "That's not right, it was 8 o clock"} """
    
    return(prompt)

def get_response_from_bot(formatted_prompt):
    try:

        response = client.chat.completions.create(
          model="gpt-4-1106-preview",
          messages=[
            {"role": "system", "content": formatted_prompt}
          ]
        )
        answer = response.model_dump()['choices'][0]['message']['content']
        answer = json.loads(answer)['answer']
        return answer
    except Exception as e:
        return f"An error occurred: {e}"


def message_func(text, avatar_name, avatar_url, is_user=True):
    if is_user:
        message_alignment = "flex-end"
        message_bg_color = "linear-gradient(135deg, #00B2FF 0%, #006AFF 100%)"
    else:
        message_alignment = "flex-start"
        message_bg_color = "#71797E"

    avatar_class = f"{avatar_name}-avatar"
    # create the html to display with f string
    s = f'<div style="display: flex; align-items: center; margin-bottom: 10px; justify-content: {message_alignment};">'
    if not is_user:
        s += f'<img src="{avatar_url}" class="{avatar_class}" alt="avatar" style="width: 50px; height: 50px;" />'
    s += f'<div style="background: {message_bg_color}; color: white; border-radius: 20px; padding: 10px; margin-right: 5px; max-width: 75%; font-size: 14px;">{text} \n </div>'
    if is_user:
        s += f'<img src="{avatar_url}" class="{avatar_class}" alt="avatar" style="width: 50px; height: 50px;" />'
    s += '</div>'
    # display html with st.write
    st.write(s, unsafe_allow_html=True)


def generate_response(conversation, bot_name, character_prompt, is_user):
    prompt = create_system_prompt(conversation, character_prompt)
    answer = get_response_from_bot(prompt)
    conversation.append({'role': bot_name, 'content': answer })
    return(answer, conversation)
        
        