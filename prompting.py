from langchain import PromptTemplate
from prompt_templates import template_system,template_user

from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

def set_chat_prompt(template_system: str, template_user: str):
    system_message_prompt= SystemMessage(content= template_system)

    human_message_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template= template_user,
                input_variables=["transcript"]
            )
        )

    return ChatPromptTemplate.from_messages([system_message_prompt,human_message_prompt])

