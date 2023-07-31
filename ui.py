from typing import Protocol



class UI(Protocol):
    def diplay_system_action(self, system_action: str) -> None:
        """Display the system action to the user
        """
        raise NotImplementedError()
    
    def display_num_audios_to_send_openai(self,list_files_path:list) -> None:
         """Display the number of requests of audio transcriptions to openai
         """
         raise NotImplementedError()
    
    def display_terminating_process(self) -> None:
         """Display the number of requests of audio transcriptions to openai
         """
         raise NotImplementedError()

    def choose_option(self,list_choices:list, prompt_message_to_user: str) -> None:
        """Prompt user to select an option and return the option chosen
        """
        raise NotImplementedError()
    
    def send_request_openai_whisper(self,list_chunks: list)-> bool:
        """Prompt user to select an option and return the option chosen
        """
        raise NotImplementedError()
    
    def display_destination_directory(self, destination_dir_path: str)-> None:

        raise NotImplementedError
   
