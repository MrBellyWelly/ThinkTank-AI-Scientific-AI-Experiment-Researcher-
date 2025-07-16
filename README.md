# ThinkTank-AI-Scientific-AI-Experiment-Researcher-
#A Scientific Research Assistant Driven by AI

This project is an AI-powered assistant made to assist researchers in automating experiments and coming up with and assessing ideas for scientific research. It is designed to increase the productivity and creativity of research and is built with **FastAPI**, **Gemini 1.5 Flash**, **RAG (Retrieval-Augmented Generation)**, and **Aider**.


---

#Features

**Gemini 1.5 Flash** and **RAG** are used in **AI Research Idea Generation** to produce innovative and workable research concepts and strategies.
*Quality Assessment Using RAGAS**
  **RAGAS** was integrated for the evaluation of LLM output.
  Research ideas are quantitatively evaluated for **feasibility**, **novelty**, and overall quality.
*Automated Synthesis of Code**
  **Code generation** for CS research queries is supported.
  - Manages Git-tracked code suggestions and automates Python experiments with **Aider**.
**Intuitive UI/UX** - Shipped with **Docker** for portability and simplicity of setup.
  An easy-to-use interface that blends in seamlessly with researchers' workflows.


# Install Dependencies
bash
-pip install -r requirements.txt

# Run with Docker (Recommended)
bash
docker build -t research-assistant .
docker run -p 8000:8000 research-assistant
