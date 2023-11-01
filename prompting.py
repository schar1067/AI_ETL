from langchain import PromptTemplate
from prompt_templates import template_system,template_user
from langchain.chat_models import ChatOpenAI
from prompt_pairs import PromptType

from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

def set_chat_prompt(template_system: str,prompt_pair:dict, prompt_type: PromptType):

    message_pair = prompt_pair[prompt_type] 
    template_system = message_pair[0]
    template_user = message_pair[1]

    system_message_prompt= SystemMessage(content= template_system)

    human_message_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template= template_user,
                input_variables=["transcript"]
            )
        )

    summarizarion_message = ChatPromptTemplate.from_messages([system_message_prompt,
                                                 human_message_prompt]).format_messages(
                                                    transcript = transcript
                                                 )

    return summarizarion_message

if __name__== '__main__':
    chat = ChatOpenAI(temperature=0.2,model='gpt-4')
    p = Path('postmortem.txt')
    transcript = p.read_text()
    message = set_chat_prompt(template_system,template_user,transcript)
    response = chat(message)
    print(response.content)