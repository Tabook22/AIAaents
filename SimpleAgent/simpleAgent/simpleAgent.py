#source: https://www.youtube.com/watch?v=q6QLGS306d0
# This is a simple agent with one task only for demonstarion to see how agents works
import os
from crewai import Agent,Task, Crew, Process
from dotenv import load_dotenv

# load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"]=os.environ["OPENAI_API_KEY"]
os.environ["OPENAI_MODEL_NAME"]="gpt-4o"

info_agent=Agent(
    role="Information Agent",
    goal="Give Complelling information about a certain topic",
    backstory="""
you love to know information. People love and hate you for it. You win most of the
quizzers at your local pub.
"""
)

task1=Task(
    description="Tell me all about the blue-oring octopus.",
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



