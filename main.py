import streamlit as st

import prompt_admin as pa
from characters import bot_options


# Initialize the conversation or hardcode a basic conversation here
if 'conversation' not in st.session_state:
    bots = []
    for bot in bot_options:
        if bot != 'user':
            bots.append(bot)
    st.session_state.conversation = [
        {'role': 'user', 'content': "I'm the moderator now! You speak when I ask, how ya feel about that?"},
        {'role': bots[0], 'content': "I'm not fond of it"},
        {'role': bots[1], 'content': "I'll be ok, I can follow orders"},
        {'role': bots[2], 'content': "This is silly"},
    ]

# sidebar bot selecter 
for bot in bot_options:
    if bot != 'user':
        st.sidebar.title(bot_options[bot]["snippet"])
        st.sidebar.image(bot_options[bot]["avatar"], width=100)
        
        if st.sidebar.button(f'Have {bot} Respond'):
            # Use the current value from session state
            answer, st.session_state.conversation = pa.generate_response(
                                                        st.session_state.conversation, 
                                                        bot_name=bot, 
                                                        character_prompt=bot_options[bot]['character_description'],
                                                        is_user=False)

# Streamlit main area layout
st.title("Chat Simulation")

# Prompt for user input and save
if prompt := st.chat_input():
    st.session_state.conversation.append({'role': 'user', 'content': prompt})

for message in st.session_state.conversation:
    pa.message_func(
        message["content"],
        avatar_name=bot_options[message['role']],
        avatar_url=bot_options[message['role']]['avatar'], 
        is_user=message['role']=='user')
