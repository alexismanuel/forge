from app.dependencies.ai.llm import LLMModel
from langchain_openai import ChatOpenAI

class OpenAILLM(LLMModel):
    def chat(self, msg: str, **kwargs) -> str:
        inputs = kwargs
        llm = ChatOpenAI(
            model=self.model_name,
            **inputs
        )
        output = llm.invoke(msg)
        return str(output.content)

