#source: https://www.youtube.com/watch?v=q6QLGS306d0
# In this code we use a local llama3 locally, and testing it
import os
from crewai import Agent,Task, Crew, Process
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"]=os.environ["OPENAI_API_KEY"]
#os.environ["OPENAI_MODEL_NAME"]=os.environ["OPENAI_MODEL_NAME"]

llm=ChatOpenAI(
    model="llama3",
    base_url="http://localhost:11434/v1"
)

search_topic=input("Please select the main animal you want to search for ..: ")

info_agent=Agent(
    role="Information Agent",
    goal="Give Complelling information about a certain topic",
    backstory="""
you love to know information. People love and hate you for it. You win most of the
quizzers at your local pub.
""",
llm=llm
)

task1=Task(
    description=f"Tell me all about the {search_topic}.",
    expected_output="Give me a quick summary and then also give me 7 bullets points describing it",
    agent=info_agent
)

crew=Crew(
    agents=[info_agent],
    tasks=[task1],
    verbose=2
)

result=crew.kickoff()
print("**********************************************")
print(result)



