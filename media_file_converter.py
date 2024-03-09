import os
from pathlib import Path
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from ui import UI
from openai_models import (OpenaiModel,
                           transcribe_multiple_audios_with_whisper, 
                           transcribe_single_audio_with_whisper)

def extract_audio(video_path: str, audio_output_path: str)->None:
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_output_path)
    audio.close()

def list_media_files_in_folder(folder):
    media_files = [file for file in os.listdir(folder) if file.lower().endswith(('.mp4', '.avi', '.mkv', '.wav', '.mp3','.m4a'))]
    return media_files


def type_of_media_file(media_file_path: str)-> str:
    """ Check if it's a video or audio file and return a string with the category
    """
    if media_file_path.lower().endswith(('.mp4', '.avi', '.mkv')):
        return "video"
    elif media_file_path.lower().endswith(('.mp3', '.m4a', '.wav')):
        return "audio"
    else:
        raise ValueError("File type not supported") 
    

def clean_dir(dir_path):
    for file in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

    # Remove the temporary audio_chunks directory
    os.rmdir(dir_path)

def send_transcript_to_dir(media_file_path:str, destination_dir_path: str, transcript: str)-> None:
    filename_w_ext= Path(media_file_path).name
    filename= f"{os.path.splitext(filename_w_ext)[0]}.txt"
    transcript_file_path = os.path.join(destination_dir_path,filename)
    with open(transcript_file_path, "w", encoding="utf-8") as file:
        file.write(transcript)

def m4a_to_mp3(media_file_path: str,output_folder_path: str)-> str:

    output_path = os.path.join(output_folder_path, os.path.splitext(media_file_path)[0] + ".mp3")
    audio = AudioSegment.from_file(media_file_path, format="m4a")
    audio.export(output_path, format="mp3")
    return output_path

def audio_file_bigger_than_25mb(audio_file_path: str)-> bool:

    file_size_bytes = os.path.getsize(audio_file_path)
    
    # Convert bytes to megabytes
    file_size_mb = file_size_bytes / (1024 * 1024)

    # Check if the file size is bigger than 25 MB
    return file_size_mb > 25

def divide_audio_into_chunks(audio_file_path: str, 
                             temp_dir: str,
                             chunk_duration: int= 25 * 60 * 1000)-> str:
    # Load the audio file
    audio = AudioSegment.from_file(audio_file_path)

    # Calculate the duration of the audio in milliseconds
    audio_duration = len(audio)

    # Initialize variables
    chunks = []
    start_time = 0
    end_time = min(chunk_duration, audio_duration)
    chunk_id = 0
    # Create a directory to store the audio chunks
    output_dir = temp_dir
    os.makedirs(output_dir, exist_ok=True)

    # Loop until the end of the audio is reached
    while start_time < audio_duration:
        # Extract the chunk based on start and end times
        chunk = audio[start_time:end_time]

        # Save the chunk as a separate audio file
        chunk_path = os.path.join(output_dir, f"chunk_{chunk_id}.mp3")
        chunk.export(chunk_path, format="mp3")

        # Add the path of the chunk to the list
        chunks.append(chunk_path)

        # Move the start and end times for the next chunk
        start_time += chunk_duration
        end_time = min(start_time + chunk_duration, audio_duration)

        chunk_id += 1

    return chunks


def get_transcription(openai_model: OpenaiModel, audio_file_path: str,
                      temp_dir: str, ui: UI):

    if audio_file_bigger_than_25mb(audio_file_path):
        chunks = divide_audio_into_chunks(audio_file_path,temp_dir)
        send= ui.send_request_openai_whisper(list_chunks= chunks)

        if send:
            transcript= transcribe_multiple_audios_with_whisper(
                openai_model = openai_model,
                list_audio_chunks = chunks )

            clean_dir(dir_path= temp_dir)
            return transcript
        else:
            ui.display_terminating_process() 
            
    transcript= transcribe_single_audio_with_whisper(
                openai_model = openai_model,
                audio_file_path = audio_file_path
                )
    os.remove(audio_file_path)
    return transcript
 
