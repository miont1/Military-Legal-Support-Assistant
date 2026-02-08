from abc import ABC, abstractmethod
import os

class LLMAdapter(ABC):
    """
    Interface for LLM interactions.
    """
    @abstractmethod
    def generate_answer(self, context: str, question: str) -> str:
        pass

class OpenAIAdapter(LLMAdapter):
    """
    Concrete adapter for OpenAI API.
    """
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        from openai import OpenAI
        self.client = OpenAI(api_key=self.api_key)

    def generate_answer(self, context: str, question: str) -> str:
        """
        Generates an answer using OpenAI GPT-4.
        """
        prompt = f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": """You are an expert military lawyer for the Armed Forces of Ukraine.
Your goal is to provide accurate, legally grounded advice to soldiers.

RULES:
1. **Cross-Referencing**: Connect different laws. If a user asks about "leaving unit", ALWAYS check the Criminal Code (Art. 407/408) for liability.
2. **No Generic Advice**: Do NOT say "Consult a lawyer" if the answer is in the context. Use the provided laws.
3. **Warning Protocol**: If the user asks about an illegal action (e.g., СЗЧ, refusing orders), you MUST warn them about criminal liability (Art. 402, 407, 408) BEFORE answering the rest.
4. **Procedure**: If asked "how to do X", look for "Instructions" (e.g., Instruction 124) to provide specific steps (e.g., "Send Report via registered mail").
5. **Tone**: Professional, authoritative, but supportive.
6. **Language**: Ukrainian.
7. **Terminology**: Never use American acronyms like AWOL. Use Ukrainian legal terms: СЗЧ, дезертирство.

If the answer is not in the context, state clearly what is missing, but try to infer from general military legal principles if possible, while adding a disclaimer."""},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating answer: {str(e)}"
