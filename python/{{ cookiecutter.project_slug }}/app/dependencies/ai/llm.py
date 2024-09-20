class LLMModel:
    def __init__(self, model_name: str) -> None:
        self.model_name = model_name

    def chat(self, msg: str, **kwargs) -> str:
        raise NotImplementedError()
