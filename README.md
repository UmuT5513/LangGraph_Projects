# LangGraph_Projects
It includes projects about agentic AI, the projects that I've coded while I'm learning.  

## AI Blog Writing Workflow
The workflow includes two node. Former is writer, the latter is critic. They work with OpenAI API. The writer sends the draft to critic. If the critic turns back with "PERFECT" or if the review numbers exceeds 3, the loop is broken, and END. 

## Basic ChatBot with Langgraph
Takes input from user. Sends it OpenAI and gets a response. It does these with a loop so you can talk with him until you say "exit". Also, It saves the conversation history, that's mean, for example, when you say your name it remembers you.

## Customer Service Bot
The main purporse of that bot is routing the question of customer (possibly asked to a website chatbot) to the specific departmant of company includes. By this way, the agents that are being to other departments can answer accurately.
