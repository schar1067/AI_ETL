
from enum import Enum, auto
from prompt_templates import *


class PromptType(Enum):
    EXECUTIVE_SUMMARY = auto()
    CONCEPT_EXTRACTION = auto()

    def __str__(self) -> str:
        return self.value


PROMPTS : dict[str, tuple[str , str]] = {
    PromptType.EXECUTIVE_SUMMARY: (template_system,template_user),
    PromptType.CONCEPT_EXTRACTION: (template_system_concept_extraction,template_user_concept_extraction)
     
}