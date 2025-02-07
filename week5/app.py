import os
import json
from dotenv import load_dotenv
import gradio as gr
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
# from langchain.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.callbacks import StdOutCallbackHandler

MODEL = "gpt-4o-mini"
db_name = "vector_db"

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', 'your-key-if-not-using-env')

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

if os.path.exists(db_name):
    vectorstore = Chroma(persist_directory=db_name, embedding_function=embeddings)
print('Vector DB has been loaded')

# create a new Chat with OpenAI
# llm = ChatOpenAI(temperature=0.7, model_name=MODEL)
llm = ChatOpenAI(temperature=0.7, model_name=MODEL, streaming=True)

# Alternative - if you'd like to use Ollama locally, uncomment this line instead
# llm = ChatOpenAI(temperature=0.7, model_name='llama3.2', base_url='http://localhost:11434/v1', api_key='ollama')

# set up the conversation memory for the chat
memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

# the retriever is an abstraction over the VectorStore that will be used during RAG
# retriever = vectorstore.as_retriever()
retriever = vectorstore.as_retriever(search_kwargs={"k": 50})

# putting it together: set up the conversation chain with the GPT 3.5 LLM, the vector store and memory
conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever, memory=memory, callbacks=[StdOutCallbackHandler()])
print('Conversation Chain has been created')

# def chat(question, history):
#     result = conversation_chain.invoke({"question": question})
#     return result["answer"]

def chat(question, history):
    docs = retriever.get_relevant_documents(question)

    # Store retrieved documents in a JSON structure
    retrieved_docs = {f"Doc {i+1}": doc.page_content for i, doc in enumerate(docs)}

    # Save the JSON structure to a file
    with open('search_results.json', 'w') as f:
        json.dump(retrieved_docs, f, indent=4)

    # Print the JSON structure
    print("\n=== Retrieved Documents ===")
    print(json.dumps(retrieved_docs, indent=4))
    print("=== End Retrieved Documents ===\n")

    for response in conversation_chain.stream({"question": question}):
        print('Chunk retrieved: {}'.format(response["answer"]))
        yield response["answer"]

# view = gr.ChatInterface(chat, type="messages").launch()
view = gr.ChatInterface(chat, type="messages").launch(inbrowser=True)