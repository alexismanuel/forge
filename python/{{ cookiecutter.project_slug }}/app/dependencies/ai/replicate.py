from langchain_community.llms import Replicate
from .llm import LLMModel

from pydantic import model_validator
import logging
from typing import Dict, Any
from langchain_core.utils.pydantic import get_fields

logger = logging.getLogger()

class ReplicateCustom(Replicate):
    @model_validator(mode="before")
    @classmethod
    def build_extra(cls, values: Dict[str, Any]) -> Any:
        """Build extra kwargs from additional params that were passed in."""
        all_required_field_names = {field.alias for field in get_fields(cls).values()}
        print(values)

        input = values.pop("input", {})
        if input:
            logger.warning(
                "Init param `input` is deprecated, please use `model_kwargs` instead."
            )
        extra = {**values.pop("model_kwargs", {}), **input}
        for field_name in list(values):
            if field_name == 'model':
                continue
            if field_name not in all_required_field_names:
                if field_name in extra:
                    raise ValueError(f"Found {field_name} supplied twice.")
                logger.warning(
                    f"""{field_name} was transferred to model_kwargs.
                    Please confirm that {field_name} is what you intended."""
                )
        values["model_kwargs"] = extra
        return values

class ReplicateLLMModel(LLMModel):
    def chat(self, msg: str, **kwargs) -> str:
        input = kwargs
        llm = ReplicateCustom(
            model=self.model_name,
            model_kwargs=input,
        )
        output = llm(msg)
        return output

