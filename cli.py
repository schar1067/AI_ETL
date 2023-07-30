
class CLI:
    def diplay_system_action(self, system_action: str) -> None:
        print(system_action)

    
    def display_num_audios_to_send_openai(self,list_files_path:list) ->None:
        print(f"{len(list_files_path)} chunks generated...")
    
    def display_destination_directory(self, destination_dir_path: str)-> None:
         print(f"Transcript saved to: {destination_dir_path}")
    
    def display_terminating_process(self)-> None:
         raise InterruptedError("Process terminated.")

    def choose_option(self,list_choices:list, prompt_message_to_user: str) -> str:
        try:
            print("Available options:")
            for i, media_file in enumerate(list_choices):
                print(f"{i + 1}. {media_file}")
            choice = int(input(prompt_message_to_user))

            if 0 < choice <= len(list_choices):
                return list_choices[choice - 1]
        except ValueError:
            print("Invalid choice.")

    def send_request_openai_whisper(self,list_chunks: list)-> bool:
        """ Choose if send request to OpenAi based on the audio chunks generated
        """
        self.display_num_audios_to_send_openai(list_chunks)
        choice= self.choose_option(list_choices=['Yes','No'],prompt_message_to_user= "Send request to OpenAi?")
        if choice == "Yes":
            return True
        else:
            False
