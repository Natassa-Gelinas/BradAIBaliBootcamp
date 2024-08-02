import streamlit as st
import requests
import json
import time


# Define the functions
def analyze_sales_call(base_url, api_key, transcript):
    url = f"{base_url}/chat/completions"

    payload = json.dumps({
        "model": "gpt-4o",
        "messages": [
            {
                "role": "system",
                "content": "You are a high ticker closer and you are looking for valuable personal information, pain points, goals and objections in this sales call transcript to be able to create personalized follow up emails and messages that lead the prospect to convert. Give the information in bullet points within each category (valuable personal information, pain points, goals, and objections). Also clearly include the reason they did not buy."
            },
            {
                "role": "user",
                "content": transcript
            }
        ]
    })

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    response = requests.post(url, headers=headers, data=payload)
    return response.json()['choices'][0]['message']['content']


def generate_follow_up_sequence(base_url, api_key, info):
    url = f"{base_url}/chat/completions"

    payload = json.dumps({
        "model": "gpt-4",
        "messages": [
            {
                "role": "system",
                "content": ("Generate a follow-up sequence for text messages for a simulated high-ticket sales call "
                            "that did not close according to the information provided from the example. The information "
                            "about the sales call will be given to you under 4 main categories, create the messages "
                            "incorporating elements of 1 or 2 categories at a time. The follow-ups should be business-oriented "
                            "but can also just be a friendly check-in to nurture the relationship. Present the messages in bullet form "
                            "and create them logically for the following timeline. Follow up 1: 24 hours after the call. Follow up 2: 3 days after the call. "
                            "Follow up 3: 1 week after the call. Follow up 4, 5, 6, 7, 8, 9, and 10 are to be weekly.")
            },
            {
                "role": "system",
                "content": (
                    "You are a dedicated, empathetic, and highly professional high-ticket closer. You have a fun and very loving personality. "
                    "The follow-up sequence should maintain and nurture the relationship by always ending with a question. The messaging should align "
                    "with Alex Hormozi's approach, focusing on value, consistency, and building trust. It should also align with NEPQ sales strategy of powerful questions. "
                    "It should be highly personalized and include unique details from the sales call to make the prospect feel validated. The tone is respectful, caring, value-driven, "
                    "and relationship-focused, with an emphasis on persistence without being pushy.")
            },
            {
                "role": "user",
                "content": info
            }
        ]
    })

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=payload)
    return response.json()['choices'][0]['message']['content']


# Streamlit UI
st.title("High-Ticket Sales Follow-Up Generator")

# Input fields
st.markdown(
    "To use this tool, you'll need an OpenAI API key. [Click here to learn how to get your API key](https://platform.openai.com/docs/quickstart).")
api_key = st.text_input("API Key", type="password")
transcript = st.text_area("Enter Sales Call Transcript (up to 20,000 words)", height=300)

# Ensure the user has provided an API key
if api_key and st.button("Generate Follow-Up Sequence"):
    with st.spinner('Use this time to take a few deep breaths and meditate...'):
        # Hardcoded API URL
        base_url = "https://api.openai.com/v1"

        # Process the transcript
        result = analyze_sales_call(base_url, api_key, transcript)
        result2 = generate_follow_up_sequence(base_url, api_key, result)
        time.sleep(1)  # Simulating processing time

    # Display the output
    st.subheader("Generated Follow-Up Messages")
    st.write(result2)
else:
    if st.button("Generate Follow-Up Sequence"):
        st.warning("Please provide a valid API key to proceed.")
