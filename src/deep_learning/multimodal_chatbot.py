import os
from dotenv import load_dotenv
load_dotenv()

API_KEY=os.getenv("GEMINI_API_KEY")

from google import genai
from PIL import Image
import streamlit as st
from io import BytesIO
from google.genai import types


client = genai.Client()



client = genai.Client(api_key=API_KEY)


st.title("AI Assistant")

user_prompt = st.text_input("Ask something")

if st.button("Generate"):
    if not user_prompt:
        st.warning("Please enter the prompt!")
    else:
        try:
            with st.spinner("Generating response..."):
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=user_prompt
                )

            st.subheader("Generated Response")
            st.write(response.text)

        except Exception as e:
            st.error("Error")
            st.write(e)
            
            



     