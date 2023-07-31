from dataclasses import dataclass, field
from pathlib import Path
from typing  import Optional
import openai
from tqdm import tqdm
from langchain.chat_models import ChatOpenAI
from prompt_templates import template_system,template_user

from prompting import set_chat_prompt

@dataclass
class OpenaiModel:
    api_key: str 
    language: str
    messages: Optional[list] = field(default_factory=list)
    temperature: Optional[int] = 0

    def call_whisper(self,file_path: str):
        with open(file_path, "rb") as file:
                response = openai.Audio.transcribe(
                    file=file,
                    model="whisper-1",
                    language=self.language
                )
        return response['text']

    def create_summary_chatgpt(self):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            temperature = self.temperature)
        return response['text']
    
    
def transcribe_multiple_audios_with_whisper(openai_model: OpenaiModel,
                             list_audio_chunks: list)-> str:
    
    chunk_responses = []
    for chunk_path in tqdm(list_audio_chunks):
       response = openai_model.call_whisper(file_path= chunk_path)
       chunk_responses.append(response)
       return "\n".join(chunk_responses)

def transcribe_single_audio_with_whisper(openai_model: OpenaiModel,audio_file_path: str)-> str:
    response = openai_model.call_whisper(file_path= audio_file_path)
    return response

def create_summary(input_file_path: str, 
                   temperature: float = 0.3,
                   model: str = 'gpt-3.5-turbo')-> str:
    
    chat = ChatOpenAI(temperature= temperature, model= model)
    p = Path(input_file_path)
    transcript = p.read_text()
    message = set_chat_prompt(template_system,template_user,transcript)
    response = chat(message)
    return response.content
