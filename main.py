import argparse
import os
from pathlib import Path
import time

import openai
from cli import CLI
from openai_models import OpenaiModel
from media_file_converter import (extract_audio, 
                                   list_media_files_in_folder, 
                                   send_transcript_to_dir, 
                                   type_of_media_file,
                                   m4a_to_mp3,
                                   get_transcription)

TEMP_FILE = "temp_audio.mp3"
TEMP_DIR= "audio_chunks"
CHUNK_SIZE = 25 * 1024 * 1024  # 25 MB in bytes
ABS_PATH= Path("/Users/schar/Dropbox/AI_Stuff/Transcripts")

def main():
    parser = argparse.ArgumentParser(description="Video/Audio-to-Transcript ETL using OpenAI's Whisper")
    parser.add_argument("--api_key",default=os.getenv("OPENAI_API_KEY") ,help="Your OpenAI API key")
    parser.add_argument("folder_path", help="Path to the folder containing media files")
    parser.add_argument("--language",default="en",help="language of the media file")
    parser.add_argument("--destination_dir_path",default= ABS_PATH.absolute(),help="Path to allocate the transcripts")
    args = parser.parse_args()

    api_key = args.api_key
    folder_path = args.folder_path
    destination_dir_path = args.destination_dir_path
    language=args.language
    temp_file = TEMP_FILE
    temp_dir = TEMP_DIR

    cli = CLI()

    openai_model = OpenaiModel(api_key= api_key, 
                               language= language
                               )
    
    if not os.path.exists(folder_path):
        cli.diplay_system_action("Folder empty")
        return

    media_files = list_media_files_in_folder(folder_path)

    if not media_files:
        cli.diplay_system_action("No media files found in the folder.")
        return

   
    choice_path= cli.choose_option(list_choices= media_files, 
                                   prompt_message_to_user= "Enter the number of the media file you want to transcribe: ")
    media_file_path = os.path.join(folder_path, choice_path)

    # Check if it's a video or audio file
    if type_of_media_file(media_file_path= media_file_path) == "video":
        extract_audio(video_path= media_file_path, audio_output_path= temp_file)
        cli.diplay_system_action("Transcribing video...")
        media_file_path= os.path.join(folder_path, temp_file)

    else: # Audio file
        cli.diplay_system_action("Transcribing audio...")

        if media_file_path.lower().endswith(('.m4a')):
            media_file_path= m4a_to_mp3(media_file_path= media_file_path, 
                                            output_folder_path= destination_dir_path) 
    try:   
        transcript = get_transcription(openai_model= openai_model,
                                        audio_file_path= media_file_path,
                                        temp_dir= temp_dir,
                                        ui= cli
                                        )
        

    except openai.error.RateLimitError:
        print("Rate limit exceeded. Waiting for 60 seconds before retrying.")
        time.sleep(60)
                                    
    send_transcript_to_dir(media_file_path= media_file_path,
                           destination_dir_path= destination_dir_path,
                           transcript= transcript)

    cli.display_destination_directory(destination_dir_path= destination_dir_path)

if __name__ == "__main__":
    main()
