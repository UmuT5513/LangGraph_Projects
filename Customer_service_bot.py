from typing import TypedDict
from langchain.tools import tool
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START, END
from langchain.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class AgentState(TypedDict):
    question :str # kullanıcının ilk sorusu
    category :str # router tarafından belirlenen kategori (refund, technical, general)
    response :str # departman node un verdiği cevap


llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4o-mini") #type: ignore


def router_node(state: AgentState):
    user_input = HumanMessage(content=state['question'])
    system_prompt = """Sen bir müşteri hizmetleri yönlendiricisisin. Gelen mesajı analiz et ve şu 3 kategoriden birine ata: 'refund', 'technical', 'general'. Sadece tek kelime çıktı ver. Kategoriler küçük harfle yazılmış olmalı"""
    system_input = SystemMessage(content=system_prompt)
    category = llm.invoke( [system_input] + [user_input] ) # response= "refund, technical, general"

    return {'category': [category.content.strip().lower()]} # LLM kategoriyi uygun şartlarda dönmezse diye. #type: ignore 


def general_node(state: AgentState):
    system_prompt = """Sen genel asistanısn. Şirket hakkında genel soruları yanıtla ve kullanıcıyı web sitesindeki SSS sayfasına yönlendir."""
    
    system_input = SystemMessage(content=system_prompt)
    user_input = state['question'] # user_input= kullanıcının sorduğu soru
    
    response = llm.invoke([system_input] + [user_input])
    
    return {'response': [response.content]}


def refund_node(state: AgentState):
    system_prompt = """Sen iade departmanısın. Kullanıcı iade istiyor. Çok resmi bir dille ondan iade politikasını talep et ve iade politikasını hatırlat."""
    
    system_input = SystemMessage(content=system_prompt)
    user_input = state['question'] # user_input= kullanıcının sorduğu soru
    
    response = llm.invoke([system_input] + [user_input])
    
    return {'response': [response.content]}



def technical_node(state: AgentState):
    system_prompt = """Sen Teknik Destek uzmanısın. Kullanıcının sorununu çözmek için ondan 'Hata Kodu'nu veya ekran görüntüsü detaylarını iste. Empati kurarak konuş."""
    
    system_input = SystemMessage(content=system_prompt)
    user_input = state['question'] # user_input= kullanıcının sorduğu soru
    
    response = llm.invoke([system_input] + [user_input])
    
    return {'response': [response.content]}



def route_decision(state: AgentState):
    category = state['category']

    if category == "refund":
        return "refund_category"
    elif category == "technical":
        return "technical_category"
    else:
        return "general_category"


workflow = StateGraph(AgentState)

workflow.add_node("router", router_node)
workflow.add_node("refund_node", refund_node)
workflow.add_node("technical_node", technical_node)
workflow.add_node("general_node", general_node)

workflow.add_edge(START, "router")
workflow.add_conditional_edges("router", route_decision,
                               {
                                   # Edge: Node
                                   "refund_category": "refund_node",
                                   "technical_category": "technical_node",
                                   "general_category": "general_node"
                               })
workflow.add_edge("refund_node", END)
workflow.add_edge("technical_node", END)
workflow.add_edge("general_node", END)

app = workflow.compile()


print(app.get_graph().draw_ascii())




user_question = input("How can I assist you?: ")
initial_state = {'question': user_question}
print(app.invoke(initial_state)) #type: ignore
while user_question != "exit":
    user_question = input("Any other thing?: ")
    initial_state = {'question': user_question}
    print(app.invoke(initial_state)) #type: ignore
