import os
import streamlit as st
#import openai
from openai import OpenAI

client = OpenAI(api_key=st.secrets["api_key"])

#openai.api_key = st.secrets["api_key"]

st.title("Kevin의 AI 이미지 생성기")

with st.form("form"):
    user_input = st.text_input("Prompt")
    size = st.selectbox("Size", ["1024x1024", "512x512", "256x256"])
    submit = st.form_submit_button("Submit")


if submit and user_input:
    gpt_prompt = [{
        "role": "system",
        "content": (
            "You are now a Dall-E prompt engineer."
            "Your job is to configure the prompts to generate the best image in Dall-E for what I ask."

            "If I ask you a question and the following conditions are present, please continue with the question to build a good prompt."
            "1. I didn't clearly recognize my question.\n"
            "2. I'm talking about an image that Dall-E can't generate.\n"
            "3. I've used words that are too abstract or imprecise.\n"
            "4. Until I entered the information I needed and said, 'Make me a prompt like this'. \n"

            "I want to know how well you understood my question and faithfully reflected it in your prompt."
            "So at the end of each question I ask, give me a confidence score from 0 to 100."

            "The elements of the prompt you need to create must meet all of the following conditions"
            "1. Make every effort to satisfy my question.\n"
            "2. Contextual understanding, background, and creative thinking about the question.\n"
            "3. How and what you use in your answer\n"
            "4. Includes what style you should use when creating your answer, etc.\n"
            "5. Generating ideal prompts for every topic you can imagine.\n"

            "When you write out the prompt, make sure you fulfill all of the following conditions"
            "1. Use literal, clear language\n"
            "2. Act like an expert on the topic.\n"
            "3. Act like a specific artist or combination of artists.\n"
            "4. Keep it to one sentence whenever possible.\n"
            "5. Output the prompt in English.\n"
        )
    }]

    gpt_prompt.append({
        "role": "user",
        "content": user_input + "json"
    })

    with st.spinner("Waiting for ChatGPT..."):
        gpt_response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=gpt_prompt
        )

    prompt = gpt_response["choices"][0]["message"]["content"]
    st.write(prompt)

    with st.spinner("Waiting for DALL-E..."):
        dalle_response = client.images.generate(
        model="dall-e-3",
          prompt=prompt,
          size=size,
          quality="standard",
          n=1,
        )

    st.image(dalle_response["data"][0]["url"])
