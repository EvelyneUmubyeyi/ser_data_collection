import streamlit as st
from streamlit_lottie import st_lottie
import requests
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2 import service_account
import time
import tempfile
from googleapiclient.http import MediaFileUpload
from streamlit_mic_recorder import mic_recorder

st.set_page_config(page_title="SER Data Collection", page_icon="🎙", layout='wide')
 
def load_lottie(url):
    r=requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
 
lottie_file = load_lottie("https://lottie.host/fdd88dc3-63c2-47b8-a2cd-ac725cf28b5e/4znksFa1nj.json")
 
data = {
    'emotion': ['angry 😠', 'disgust 🤢', 'fear 😱', 'happy 😊', 'neutral 😐', 'sad 😞'],
    'sentence': [
        'Kids are talking by the door.',
        'Kids are talking by the door.',
        'Dogs are sitting by the door.',
        'Kids are talking by the door.',
        'Dogs are sitting by the door.',
        'Kids are talking by the door.'
    ],
    'recording': [
        'examples/angry.wav',
        'examples/disgust.wav',
        'examples/fear.wav',
        'examples/happy.wav',
        'examples/neutral.wav',
        'examples/sad.wav'
    ]
}
 
sentences = {
    'emotion': ['angry 😠', 'disgust 🤢', 'fear 😱', 'happy 😊', 'neutral 😐', 'sad 😞'],
    'sentence': [
        [
            "I can't believe you did that!",
            "This is unacceptable!",
            "I'm so frustrated right now!",
            "Why do things always have to go wrong?",
            "I've had enough of this!"
        ],
        [
            "That's disgusting!",
            "I can't stand the sight of it.",
            "This is revolting!",
            "I feel sick just thinking about it.",
            "I'm repulsed by what I see."
        ],
        [
            "I'm terrified of what might happen.",
            "I can't shake this feeling of dread.",
            "I'm paralyzed with fear.",
            "I feel like I'm being watched.",
            "I'm too scared to move."
        ],
        [
            "I'm over the moon!",
            "This is the best day ever!",
            "I can't stop smiling!",
            "Life is beautiful!",
            "I feel like I'm on top of the world!"
        ],
        [
            "The weather today is quite pleasant.",
            "I have a meeting at 3 o'clock.",
            "I need to buy groceries on my way home.",
            "I finished reading a book yesterday.",
            "I'm planning to take a walk later."
        ],
        [
            "I feel so alone.",
            "I'm heartbroken.",
            "Nothing seems to go right.",
            "I miss you so much.",
            "I don't know how to cope with this pain."
        ]
    ]
}
 
def generate_unique_filename(emotion):
    current_time = time.strftime("%Y%m%d_%H%M%S")
    return f"{emotion}_{current_time}.wav"
 
scopes = ['https://www.googleapis.com/auth/drive']
service_account_info = st.secrets.service_account
parent_folder_id = '1Ep3TKh5MVrBYB2oIiJVd5M8SSmz680vy'
 
def authenticate():
    creds = service_account.Credentials.from_service_account_info(service_account_info, scopes = scopes)
    return creds 
 
def upload_photo(file_path, filename):
    creds = authenticate()
    service = build('drive', 'v3', credentials = creds)
 
    file_metadata = {
        'name': filename,
       'parents': [parent_folder_id]
    }
 
    media_body = MediaFileUpload(file_path)
 
    file = service.files().create(
        body=file_metadata,
        media_body=media_body
    ).execute()
 
def callback():
    if st.session_state.my_recorder_output:
        audio_bytes = st.session_state.my_recorder_output['bytes']
        st.session_state.recording = audio_bytes
        st.audio(st.session_state.recording)
    else:
        st.session_state.recording = None
            
def show_emotion(emotion_index):
    st.subheader(sentences['emotion'][emotion_index].capitalize())
    st.write('Record yourself expressing the given emotion with one of these sentences.')
    sentences_for_emotion = sentences['sentence'][emotion_index]
    for sentence in sentences_for_emotion:
        st.write(f"- {sentence}")
 
    mic_recorder(
    start_prompt="Start recording",
    stop_prompt="Stop recording",
    just_once=False,
    use_container_width=False,
    callback=callback,
    args=(),
    kwargs={},
    key='my_recorder'
    )

with st.container():
    left_column, right_column = st.columns(2)
    with left_column:
        # st.subheader('Hello :wave: How are you doing today😊')
        st.title('Welcome to SER Data Collection💝')
        st.write('''
            First things first, I want to express my gratitude for your support in my project. I'm developing a Speech 
            Emotion Recognition (SER) system for a mental health app. The current data I am using to train the SER model 
            lacks African accents, which affects the model's accuracy with African users. Therefore, I need your 
            help to diversify my training data and make the model work for us. You'll record sentences expressing various emotions. 
            We're focusing on six emotions: angry, disgust, fear, happy, neutral, and sad. Your contributions are invaluable. 
            Let's start recording!
        ''')
 
    with right_column:
        if lottie_file is not None:
            st_lottie(lottie_file, speed=1, key="animated_image")
        else:
            st.write("Failed to load Lottie animation.")
 
st.write('---')
 
with st.container():
    st.header('Examples')
    df = pd.DataFrame(data)
 
    col1, col2, col3 = st.columns(3)
 
    for i in range(0, len(df), 3):
        with col1:
            emotion_title_case = df.loc[i, 'emotion'].title()
            st.markdown(f"<h3><b>{emotion_title_case}</b></h3>", unsafe_allow_html=True)
            st.write(f"{df.loc[i, 'sentence']}")
            st.audio(df.loc[i, 'recording'], start_time=0)
        with col2:
            emotion_title_case = df.loc[i+1, 'emotion'].title()
            st.markdown(f"<h3><b>{emotion_title_case}</b></h3>", unsafe_allow_html=True)
            st.write(f"{df.loc[i+1, 'sentence']}")
            st.audio(df.loc[i+1, 'recording'], start_time=0)
        with col3:
            emotion_title_case = df.loc[i+2, 'emotion'].title()
            st.markdown(f"<h4><b>{emotion_title_case}</b></h4>", unsafe_allow_html=True)
            st.write(f"{df.loc[i+2, 'sentence']}")
            st.audio(df.loc[i+2, 'recording'], start_time=0)
 
 
with st.container():
    st.header('Guidelines for good quality recording!')
    st.write(''' 
        1. Please record in a quiet room to avoid any background noise.
        2. Before you submit a recording make sure you're audible i.e.the volume is enough.
    ''')
    st.write('---')
    st.header('Record here 🎤')
 
    if 'emotion_index' not in st.session_state:
        st.session_state.emotion_index = 0
    
    if 'recording' not in st.session_state:
        st.session_state.recording = None
 
    if st.session_state.emotion_index == 5:
        button_label = "Done"
    else:
        button_label = "Next Emotion"
    file_upload = show_emotion(st.session_state.emotion_index)
    st.session_state.button_disabled = False
    if st.button(button_label, disabled=st.session_state.button_disabled):
        if st.session_state.recording is None:
            st.error('Please record the audio before you proceed!')
        else:
            st.session_state.button_disabled = True
            if(len(st.session_state.recording) > 0):
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(st.session_state.recording)
                    temp_path = temp_file.name
                    filename = generate_unique_filename(sentences['emotion'][st.session_state.emotion_index].split(' ')[0]) 
                    upload_photo(temp_path, filename)
                    st.session_state.recording = None
            if st.session_state.emotion_index < 5:
                st.session_state.emotion_index += 1
                st.rerun()
            elif st.session_state.emotion_index == 5:
                st.success('Thank you for completing the audio recording process :)')
                