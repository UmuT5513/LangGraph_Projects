from typing import TypedDict, Dict
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END

class BlogState(TypedDict):
    topic: str
    draft : str
    critique : str
    revision_number : int

load_dotenv()

OPENAI_API = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(api_key=OPENAI_API, model="gpt-4o-mini") # type: ignore



def write(state: BlogState):

    if state["critique"]:
        system_rewrite_prompt = f"""
        Refine the following draft based on this critique: {state['critique']}
        Original Draft: 
        {state['draft']}
        """
        response = llm.invoke([SystemMessage(content=system_rewrite_prompt)])
    else:
        user_prompt = f"""Write a blog consist of at most 50 words about {state['topic']}"""
        response = llm.invoke(user_prompt)

    draft = response.content
    print(f"\nVERSION {state['revision_number']+1}")
    print(draft)
    return {"draft":draft}


def critique(state: BlogState):
    
    system_critique_prompt = f"""
    You are a Senior Editor. Your job is to critique a blog post draft.

    1. Read the draft below carefully.
    2. If the draft is excellent, concise, and covers the topic well, reply with ONLY the word: PERFECT
    3. If the draft needs improvement, list 3 specific, actionable changes the writer should make. Be brief and harsh.

    DO NOT provide a rewritten version. Only provide the critique. Don't forget It must be at most 50 words.

    The draft is here:
    
    {state['draft']}
    """

    response = llm.invoke([SystemMessage(content=system_critique_prompt)])
    critique = response.content
    state["revision_number"]+=1

    return {"critique":critique, "revision_number":state["revision_number"]+1}


def decide_next_node(state: BlogState):
    if state["revision_number"] >= 3:
        return "stop"
    elif state["critique"] == "PERFECT":
        return "stop"
    else:
        return "rewrite"
    

workflow = StateGraph(BlogState)

workflow.add_node("blogger", write)
workflow.add_node("critic", critique)

workflow.add_edge(START, "blogger")
workflow.add_edge("blogger", "critic")
workflow.add_conditional_edges("critic", decide_next_node,
                               {
                                   # Edge: Node
                                   "stop" : END,
                                   "rewrite" : "blogger"
                               }
                               )

app = workflow.compile()

initial_state: BlogState = {"topic":"holocoust industry", "draft": "", "critique":"", "revision_number":0}
final_state = app.invoke(input=initial_state)


