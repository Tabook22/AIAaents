#source: https://www.youtube.com/watch?v=q6QLGS306d0
# This is the math agents how solves equations and then give explainaitons bout it and save the explainaiton in a markdown file
import os
from crewai import Agent,Task, Crew, Process
from dotenv import load_dotenv
from calculatorTool import calculate

# load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"]=os.environ["OPENAI_API_KEY"]
os.environ["OPENAI_MODEL_NAME"]=os.environ["OPENAI_MODEL_NAME"]

print("***** Welecom to the Math Whiz *****")

math_input=input("What is your math equation: ")

math_agent=Agent(
    role="Math Magician",
    goal="You are able to evaluate any math expression",
    backstory="You are a math whiz.",
    verbose=True,
    tools=[calculate]
)

writer=Agent(
    role="Writer",
    goal="Craft compelling explanations based from results of math equations.",
    backstory="""
you are a renowned Content Strategist, known for you insightful, and engaging articles.
You transfomr complex concepts into compelling narratives.
""",
verboser=True
)

task1=Task(
    description=f"{math_input}.",
    expected_output="Give full details in bullet points",
    agent=math_agent
)

task2=Task(
    description=""" using the insights provided, explain in great detail how the equation and result were formed.""",
    expected_output="""" Explain in great detail and save in markdown, Don't add the triple tick marks at the
    beginning or end of the file. Also don't say what type it is in the first line.""",
    output_file="math.md",
    agent=writer
)

crew=Crew(
    agents=[math_agent, writer],
    tasks=[task1,task2],
    process=Process.sequential,
    verbose=2
)

result=crew.kickoff()
print("**********************************************")
print(result)



