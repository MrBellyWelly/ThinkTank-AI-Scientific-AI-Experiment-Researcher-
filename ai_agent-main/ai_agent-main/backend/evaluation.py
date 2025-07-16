import json
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np

class Evaluator:
    def __init__(self, embedding_model=None, llm=None):
        """
        embedding_model: SentenceTransformer (for similarity)
        llm: a function taking a prompt and returning text (e.g. chat_model.invoke().content)
        """
        print("Initializing Evaluator...")
        self.embedding_model = embedding_model or SentenceTransformer('all-MiniLM-L6-v2')
        if llm is None:
            raise ValueError("An llm callable must be provided to Evaluator")
        self.llm = llm

        # Placeholders, to be filled once topics are extracted:
        self.topics = []
        self.topic_embeddings = None
        print("Evaluator initialized successfully.")

    def extract_topics(self, chunks: list[str], num_topics: int = 8) -> list[str]:
        print(f"Extracting {num_topics} topics from chunks...")
        combined = "\n\n".join(chunks)
        prompt = f"""
            Extract {num_topics} key scientific topics or keywords from the following research document chunks.
            Return them as a JSON array of strings, with no extra text:

            {combined}
        """
        resp = self.llm(prompt).strip()
        print(f"Raw LLM response for topics:\n{resp}")

        try:
            topics = json.loads(resp)
            print(f"Parsed topics as JSON: {topics}")
        except json.JSONDecodeError:
            print("Failed to parse topics as JSON, falling back to splitting lines.")
            lines = [line.strip("-• ").strip() 
                     for line in resp.splitlines() if line.strip()]
            topics = lines if len(lines) >= num_topics else [t.strip() for t in resp.split(",") if t.strip()]
            print(f"Fallback topics: {topics}")

        # cache and compute embeddings
        self.topics = topics
        self.topic_embeddings = self.embedding_model.encode(self.topics)
        print("Topic embeddings computed.")
        return self.topics

    def topic_alignment_score(self, query: str) -> float:
        print(f"Calculating topic alignment score for query: {query}")
        q_emb = self.embedding_model.encode([query])
        sims = cosine_similarity(q_emb, self.topic_embeddings)[0]
        score = float(max(sims))
        print(f"Topic alignment score: {score}")
        return score

    def chunk_relevance_score(self, chunks: list[str], query: str) -> float:
        print(f"Calculating chunk relevance score for query: {query}")
        if not chunks:
            print("No chunks provided, relevance score is 0.0")
            return 0.0
        chunk_embs = self.embedding_model.encode(chunks)
        q_emb = self.embedding_model.encode([query])
        sims = cosine_similarity(q_emb, chunk_embs)[0]
        score = float(np.mean(sims))
        print(f"Chunk relevance score: {score}")
        return score

    def novelty_score(self, response: str, chunks: list[str]) -> float:
        print("Calculating novelty score...")
        chunk_embs = self.embedding_model.encode(chunks)
        resp_emb = self.embedding_model.encode([response])
        sims = cosine_similarity(resp_emb, chunk_embs)[0]
        score = float(1 - max(sims))
        print(f"Novelty score: {score}")
        return score

    def feasibility_score(self, response: str) -> int | str:
        print("Calculating feasibility score...")
        prompt = f"""Rate the feasibility of the following scientific response from 1 (impossible) to 5 (highly feasible):
                        
                Response:
                {response}

                Only return a single number between 1 and 5.
                """
        rating = self.llm(prompt)
        print(f"Raw feasibility rating from LLM: {rating}")
        try:
            score = int(rating.strip())
            clamped_score = max(1, min(score, 5))
            print(f"Feasibility score (clamped between 1 and 5): {clamped_score}")
            return clamped_score
        except:
            print("Error parsing feasibility score.")
            return "Error"

    def evaluate(self, query: str, chunks: list[str], response: str) -> dict:
        print("Starting full evaluation...")
        topics = self.extract_topics(chunks)
        results = {
            "topics": topics,
            "topic_alignment_score": round(self.topic_alignment_score(query), 3),
            "chunk_relevance_score": round(self.chunk_relevance_score(chunks, query), 3),
            "novelty_score": round(self.novelty_score(response, chunks), 3),
            "feasibility_score": self.feasibility_score(response)
        }
        print(f"Evaluation results: {results}")
        return results
