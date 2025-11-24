# LangGraph_Projects
It includes projects about agentic AI, the projects that I coded while I'm learning.  

## AI Blog Writing Workflow
The workflow included two node. Former is writer, the latter is critic. They work with OpenAI API. The writer sends the draft to critic. If the critic turns with "PERFECT", the loop is broken, and END. The critic can do critique at most 3 times. When exceeded again END. 

## Basic ChatBot with Langgraph
Takes input from user. Sends it OpenAI and gets a response. It does these with a loop so you can talk with him until you say "exit". Also, Saves the conversation history, that's when you say your name, for example, it remember you.
