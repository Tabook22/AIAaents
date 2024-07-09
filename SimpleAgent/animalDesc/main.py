#descripting animal and generate its image store it in "aimg" folder and save description in txt file store it in "docs" folder:

import os
import time
from datetime import datetime
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.environ["OPENAI_API_KEY"]
os.environ["OPENAI_MODEL_NAME"] = "gpt-4"

# Create directories if they don't exist
os.makedirs("aimg", exist_ok=True)
os.makedirs("docs", exist_ok=True)

# Streamlit interface
st.title("Animal Information and Art Generator")

# Animal input
animal = st.text_input("Enter an animal name:")

if st.button("Generate Information and Art"):
    if animal:
        # Information Agent
        info_agent = Agent(
            role="Information Agent",
            goal="Give compelling information about a certain topic",
            backstory="""
            You love to know information. People love and hate you for it. You win most of the
            quizzes at your local pub.
            """
        )

        # Art Generation Agent
        art_agent = Agent(
            role="Art Generation Agent",
            goal="Generate an image based on the provided information",
            backstory="""
            You are a talented artist who can create stunning visual representations of animals
            based on textual descriptions.
            """
        )

        # Information Task
        info_task = Task(
            description=f"Tell me all about the {animal}.",
            expected_output="Give me a quick summary and then also give me 7 bullet points describing it",
            agent=info_agent
        )

        # Art Generation Task
        art_task = Task(
            description=f"Generate an image of a {animal} based on the information provided.",
            expected_output="A URL to the generated image",
            agent=art_agent
        )

        # Create and run the crew
        crew = Crew(
            agents=[info_agent, art_agent],
            tasks=[info_task, art_task],
            verbose=2
        )

        results = crew.kickoff()

        # Process and display results
        info_result, art_result = results

        # Display information
        st.subheader("Animal Information")
        st.write(info_result)

        # Save information to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        info_filename = f"docs/{animal}_{timestamp}.txt"
        with open(info_filename, "w") as f:
            f.write(info_result)

        # Display and save image
        st.subheader("Generated Image")
        try:
            image_url = art_result.strip()
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))
            st.image(img, caption=f"Generated image of {animal}")

            # Save image
            img_filename = f"aimg/{animal}_{timestamp}.png"
            img.save(img_filename)

            st.success(f"Information saved to {info_filename}")
            st.success(f"Image saved to {img_filename}")
        except Exception as e:
            st.error(f"Error processing the image: {str(e)}")

    else:
        st.warning("Please enter an animal name.")