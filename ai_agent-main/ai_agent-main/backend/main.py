from fastapi import FastAPI, HTTPException
from models import ChatRequest
from generator import generate_scientific_idea, generate_general_response, is_valid_scientific_idea, chat_model
import os
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from evaluation import Evaluator

# Initialize FastAPI app
app = FastAPI()

# Initialize memory
memory = ConversationBufferMemory(memory_key="history", return_messages=True)

# Initialize evaluator
evaluator = Evaluator(llm=lambda prompt: chat_model.invoke(prompt).content)

@app.get("/")
def read_root():
    print("GET / - Root endpoint hit")
    return {"message": "Backend is running!"}

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        user_input = request.message
        print(f"Received user input: {user_input}")
        print(f"Mode: {request.mode}")

        # Add human message to memory
        memory.chat_memory.add_user_message(user_input)
        print("User message added to memory.")

        if request.mode == "scientific_idea":
            print("Handling scientific_idea mode.")
            if not is_valid_scientific_idea(user_input):
                print("Input is NOT a valid scientific idea.")
                bot_response = "This idea does not seem viable for a scientific experiment."
                evaluation = None
            else:
                print("Input is a valid scientific idea.")
                # generate_scientific_idea now returns (idea_text, retrieved_chunks)
                idea_text, retrieved_chunks = generate_scientific_idea(user_input, memory)
                print(f"Generated scientific idea: {idea_text}")
                print(f"Retrieved chunks: {retrieved_chunks}")

                # Evaluate the generated idea
                evaluation = evaluator.evaluate(
                    query=user_input,
                    chunks=retrieved_chunks,
                    response=idea_text
                )
                print(f"Evaluation result: {evaluation}")

                bot_response = idea_text

        elif request.mode == "general":
            print("Handling general mode.")
            bot_response = generate_general_response(user_input, memory)
            evaluation = None
            print(f"Generated general response: {bot_response}")

        else:
            print("Invalid mode received.")
            raise HTTPException(status_code=400, detail="Invalid mode. Use 'scientific_idea' or 'general'.")

        # Add AI response to memory
        memory.chat_memory.add_ai_message(bot_response)
        print("AI message added to memory.")

        return {"response": bot_response, "evaluation": evaluation}

    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# Health check endpoint (optional)
@app.get("/health")
def health():
    print("GET /health - Health check endpoint hit")
    return {"status": "healthy"}

@app.get("/history")
def get_history():
    print("GET /history - Fetching chat history")
    return {"history": [m.content for m in memory.chat_memory.messages]}

if __name__ == "__main__":
    import uvicorn
    print("Starting server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
