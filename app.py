import streamlit as st
import joblib
import re
import string


# Required for loading the trained pickle model
def wordopt(text):
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>+', '', text)
    text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub(r'\n', '', text)
    text = re.sub(r'\w*\d\w*', '', text)
    return text


# Load trained model
with open("spam_mail.pkl", "rb") as file:
    model = joblib.load(file)


# Streamlit configuration
st.set_page_config(
    page_title="Spam Mail Detector",
    page_icon="📧"
)

st.title("📧 Spam Mail Detector")
st.write("Enter an email or message to check whether it is Spam or Ham.")

message = st.text_area(
    "Enter your message:",
    height=200,
    placeholder="Type or paste your email here..."
)

if st.button("Check Message"):

    if not message.strip():
        st.warning("Please enter a message.")
    else:
        cleaned_message = wordopt(message)

        try:
            prediction = model.predict([cleaned_message])

            result = prediction[0]

            if str(result).lower() == "spam" or result == 1:
                st.error("🚨 Spam Mail")
            else:
                st.success("✅ Ham Mail (Not Spam)")

        except Exception as e:
            st.error("Unable to make prediction.")
            st.code(str(e))
