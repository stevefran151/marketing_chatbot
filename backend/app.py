from __future__ import annotations
from flask import Flask, render_template, jsonify, request


from src.helper import download_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

from src.prompt import * 
import os
from langchain_groq import ChatGroq

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

load_dotenv()
 
PINECONE_API_KEY=os.environ.get('PINECONE_API_KEY')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GROQ_API_KEY"] = GROQ_API_KEY



embeddings=download_embeddings()

index_name="marketing-chatbot"

docsearch=PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever=docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})

chatModel = ChatGroq(model="llama-3.1-8b-instant")
# --- Context Awareness Setup ---
from langchain_core.prompts import MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# 1. Contextualize Question Prompt (Rephrases follow-up questions)
contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)

contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

# 2. Create History-Aware Retriever
# This chain takes the history + new question -> standalone question -> retriever
history_aware_retriever = create_history_aware_retriever(
    chatModel, retriever, contextualize_q_prompt
)

# 3. Update QA Chain to use History
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(chatModel, qa_prompt)
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

# 4. Session History Management
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
)


@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    try:
        msg = request.form["msg"]
        input = msg
        print(input)
        
        # Use a fixed session ID for this demo (or generate one per user)
        session_id = "default_session"
        
        response = conversational_rag_chain.invoke(
            {"input": msg},
            config={"configurable": {"session_id": session_id}}
        )
        print("Response : ", response["answer"])
        return str(response["answer"])
    except Exception as e:
        print(f"Error: {e}")
        return f"Sorry, I encountered an error: {str(e)}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)