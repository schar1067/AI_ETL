import argparse
import os
from pathlib import Path
from cli import CLI
from openai_models import OpenaiModel, create_summary
from media_file_converter import (extract_audio, 
                                   list_media_files_in_folder, 
                                   get_absolute_file_path, list_text_files_in_folder, 
                                   type_of_media_file,
                                   m4a_to_mp3,
                                   get_transcription)

TEMP_FILE = "temp_audio.mp3"
TEMP_DIR= "audio_chunks"
CHUNK_SIZE = 25 * 1024 * 1024  # 25 MB in bytes
ABS_PATH= Path("/Users/schar/Dropbox/AI_Stuff/Transcripts")
ABS_PATH_SUMMARIES = Path("/Users/schar/Dropbox/Vault/obsidian_work_vault/Summaries")

def main():
    parser = argparse.ArgumentParser(description="Video/Audio-to-Transcript ETL using OpenAI's Whisper")
    parser.add_argument("--api_key",default=os.getenv("OPENAI_API_KEY") ,help="Your OpenAI API key")
    parser.add_argument("folder_path", help="Path to the folder containing media files")
    parser.add_argument("--language",default="en",help="language of the media file")
    parser.add_argument("--destination_dir_path",default= ABS_PATH.absolute(),help="Path to allocate the transcripts")
    parser.add_argument("--destination_dir_path_summ",default= ABS_PATH_SUMMARIES.absolute(),help="Path to allocate the summaries")
    parser.add_argument("--summarize", action="store_true", help="Enable summarization step")
    args = parser.parse_args()

    api_key = args.api_key
    folder_path = args.folder_path
    destination_dir_path = args.destination_dir_path
    destination_dir_path_summ = args.destination_dir_path_summ
    language=args.language
    temp_file = TEMP_FILE
    temp_dir = TEMP_DIR

    cli = CLI()
    openai_model = OpenaiModel(api_key= api_key, 
                               language= language)

    if args.summarize:

        if not os.path.exists(destination_dir_path):
            cli.diplay_system_action("Folder empty")
            return 

        summary_files = list_text_files_in_folder(destination_dir_path)

        if not summary_files:
            cli.diplay_system_action("No  files found in the folder.")
            return
        
        choice_path= cli.choose_option(list_choices= summary_files, 
                                   prompt_message_to_user= "Enter the number of the file you want to summarize: ")
        transcript_file_path = os.path.join(destination_dir_path, choice_path)

        cli.diplay_system_action("Summarizing transcript...")
        summary= create_summary(input_file_path= transcript_file_path,model= 'gpt-4')
        summary_file_path = get_absolute_file_path(file_path= media_file_path,
                      destination_dir_path= destination_dir_path_summ,
                      type_of_file= "md")
        
        Path(summary_file_path).write_text(data= summary)

        cli.display_destination_directory(destination_dir_path= destination_dir_path_summ)
        return


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
        media_file_path= Path(temp_file).absolute()

    else: # Audio file
        cli.diplay_system_action("Transcribing audio...")

        if media_file_path.lower().endswith(('.m4a')):
            media_file_path= m4a_to_mp3(media_file_path= media_file_path, 
                                        output_folder_path= destination_dir_path) 
       
    transcript = get_transcription(openai_model= openai_model,
                                    audio_file_path= media_file_path,
                                    temp_dir= temp_dir,
                                    ui= cli)
                                    
    transcript_file_path = get_absolute_file_path(file_path= media_file_path,
                      destination_dir_path= destination_dir_path)
    
    Path(transcript_file_path).write_text(data= transcript)

    cli.display_destination_directory(destination_dir_path= destination_dir_path)

    if args.summarize:
        cli.diplay_system_action("Summarizing transcript...")
        summary= create_summary(input_file_path= transcript_file_path,model= 'gpt-4')
        summary_file_path = get_absolute_file_path(file_path= media_file_path,
                      destination_dir_path= destination_dir_path_summ,
                      type_of_file= "md")
        
        Path(summary_file_path).write_text(data= summary)

        cli.display_destination_directory(destination_dir_path= destination_dir_path_summ)

if __name__ == "__main__":
    main()
