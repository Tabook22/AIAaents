import os
from datetime import datetime
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from langchain.agents import Tool

# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.environ["OPENAI_API_KEY"]
os.environ["OPENAI_MODEL_NAME"] = "gpt-4"

# Create directories if they don't exist
os.makedirs("aimg", exist_ok=True)
os.makedirs("docs", exist_ok=True)

# Set up the DALL-E tool
dalle_tool = DallEAPIWrapper()

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

        # Information Task
        info_task = Task(
            description=f"Tell me all about the {animal}.",
            expected_output="Give me a quick summary and then also give me 7 bullet points describing it",
            agent=info_agent
        )

        # Create and run the info crew
        info_crew = Crew(
            agents=[info_agent],
            tasks=[info_task],
            verbose=2
        )

        info_result = info_crew.kickoff()

        # Display information
        st.subheader("Animal Information")
        st.write(info_result.strip())

        # Save information to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        info_filename = f"docs/{animal}_{timestamp}.txt"
        with open(info_filename, "w") as f:
            f.write(info_result.strip())

        # Art Generation Agent
        art_agent = Agent(
            role="Art Generation Agent",
            goal="Draw an image based on the provided information",
            backstory="""
            You are a talented artist who can create stunning visual representations of animals
            based on textual descriptions.
            """,
            tools=[
                Tool(
                    name="DALL-E Image Generator",
                    func=dalle_tool.run,
                    description="Use this tool to draw an images based on text descriptions"
                )
            ],
            verbose=True
        )

        # Art Generation Task
        art_task = Task(
            description=f"Draw and image of a {animal} based on the following information: {info_result}. Use the DALL-E Image Generator tool to create the image drawings. Respond with only the URL to the generated image.",
            expected_output="A URL to the generated drawing image",
            agent=art_agent
        )

        # Create and run the art crew
        art_crew = Crew(
            agents=[art_agent],
            tasks=[art_task],
            verbose=2
        )

        art_result = art_crew.kickoff()

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