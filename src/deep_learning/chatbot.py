import os
from dotenv import load_dotenv
import langchain_tavily
from typing_extensions import TypedDict, Annotated
# from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage
from langchain_tavily import TavilySearch

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from google import genai
from langchain_ollama import OllamaLLM
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()
client = genai.Client()

API_KEY=os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)
class State(TypedDict):
    messages: Annotated[BaseMessage, add_messages]
    
# llm = OllamaLLM(model="olmo3")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7
)

tool = TavilySearch(max_results=2)
tools = [tool]

llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition
)

#Anytime a time is called , we return to the chatbot to decide the next steps
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")

from langgraph.checkpoint.memory import MemorySaver
memory = MemorySaver()

graph=graph_builder.compile(checkpointer=memory)
import streamlit as st

st.title("Chatbot App ")

if "messages" not in st.session_state:
    st.session_state.messages = []

def stream_graph_updates(user_input: str):
    assistant_response = ""

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        with st.spinner("Thinking..."):
            # Build full conversation history from session state
            full_messages = []
            for role, content in st.session_state.messages:
                full_messages.append({"role": role, "content": content})
            
            # Add the new user message
            full_messages.append({"role": "user", "content": user_input})
            
            for event in graph.stream(
                {"messages": full_messages},
                {"configurable": {"thread_id": "chat"}}
            ):
                # Only process events from chatbot node, skip tools node
                for node_name, value in event.items():
                    if node_name == "chatbot":  # Filter: only show chatbot responses
                        content = value["messages"][-1].content
                        
                        if isinstance(content, list):
                            new_text = content[0]['text']
                        else:
                            new_text = content
                        
                        # Only display if there's actual text content (skip tool calls)
                        if new_text and isinstance(new_text, str):
                            print("new text::", new_text)
                            assistant_response = new_text
                            message_placeholder.markdown(assistant_response)

    return assistant_response


# Display chat history
for role, message in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(message)

# Handle new input
if prompt := st.chat_input("What is your question?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state.messages.append(("user", prompt))
    
    response = stream_graph_updates(prompt)
    
    st.session_state.messages.append(("assistant", response))