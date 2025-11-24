from typing import TypedDict, List, Union
from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4o-mini") # type: ignore


class ChatBot(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]


def process(state: ChatBot) -> ChatBot:

    response = llm.invoke(state["messages"])

    state["messages"].append(AIMessage(response.content))

    print(f"\nAI: {response.content}")

    print(f"CURRENT STATE: {state['messages']}\n")

    return state


workflow = StateGraph(ChatBot)

workflow.add_node("process", process)

workflow.set_entry_point("process")
workflow.set_finish_point("process")

app = workflow.compile()


conversation_history = []

input_user = input("Hi, How can I assist you today?\nYou: ")
while input_user.lower() != "exit":
    conversation_history.append(HumanMessage(content=input_user))
    
    response = app.invoke({"messages": conversation_history})

    conversation_history = response["messages"] # history güncelleme

    input_user = input("You: ")

    



