import os
import argparse
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import openai
from pathlib import Path

#AudioSegment.converter  = "C:\\Users\\Administrador\\Downloads\\ffmpeg-master-latest-win64-gpl-shared.zip\\ffmpeg-master-latest-win64-gpl-shared\\bin\\ffmpeg.exe"

CHUNK_SIZE = 25 * 1024 * 1024  # 25 MB in bytes

ABS_PATH= Path("/Users/schar/Dropbox/AI_Stuff/Transcripts")

def extract_audio(video_path, audio_output_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_output_path)
    audio.close()

def transcribe_audio_with_whispersync_single(api_key,audio_path,language):
    openai.api_key =api_key
    with open(audio_path, "rb") as file:
        response = openai.Audio.transcribe(
            model="whisper-1",
            file=file,
            language=language)
    return response['text']


def transcribe_audio_with_whispersync(api_key,audio_path,language):
    if not is_audio_file_bigger_than_25mb:
        single_transcript=transcribe_audio_with_whispersync_single(api_key, audio_path,language)
        return single_transcript

    openai.api_key = api_key
    # Perform chunked upload
    chunks = divide_audio_into_chunks(audio_path)
    chunk_responses = []
    for chunk_path in chunks:
        with open(chunk_path, "rb") as file:
            response = openai.Audio.transcribe(
                file=file,
                model="whisper-1",
                language=language
            )
            chunk_responses.append(response["text"])

    # Transcribe chunks
    transcript = "\n".join(chunk_responses)


    # Remove temporary chunk files
    for chunk_path in chunks:
        os.remove(chunk_path)

    # Remove the temporary audio_chunks directory
    os.rmdir("audio_chunks")

    return transcript

def m4a_to_mp3(media_file_path, output_folder_path)->str:

    output_path = os.path.join(output_folder_path, os.path.splitext(media_file_path)[0] + ".mp3")

    # Load the m4a audio
    audio = AudioSegment.from_file(media_file_path, format="m4a")

    # Export the audio as mp3
    audio.export(output_path, format="mp3")

    return output_path

def is_audio_file_bigger_than_25mb(audio_file):

  file_size = os.path.getsize(audio_file)
  return file_size > 25 * 1024**2  # 25 MB

def divide_audio_into_chunks(audio_path, chunk_duration=25 * 60 * 1000):
    # Load the audio file
    audio = AudioSegment.from_file(audio_path)

    # Calculate the duration of the audio in milliseconds
    audio_duration = len(audio)

    # Initialize variables
    chunks = []
    start_time = 0
    end_time = min(chunk_duration, audio_duration)
    chunk_id = 0

    # Create a directory to store the audio chunks
    output_dir = "audio_chunks"
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

def list_media_files_in_folder(folder):
    media_files = [file for file in os.listdir(folder) if file.lower().endswith(('.mp4', '.avi', '.mkv', '.wav', '.mp3','.m4a'))]
    return media_files

def main():
    parser = argparse.ArgumentParser(description="Video/Audio-to-Transcript ETL using OpenAI's Whisper")
    parser.add_argument("--api_key",default=os.getenv("OPENAI_API_KEY") ,help="Your OpenAI API key")
    parser.add_argument("folder_path", help="Path to the folder containing media files")
    parser.add_argument("--language",default="en",help="language of the media file")
    parser.add_argument("--output_folder_path",default= ABS_PATH.absolute(),help="Path to allocate the transcripts")
    args = parser.parse_args()

    api_key = args.api_key
    folder_path = args.folder_path
    output_folder_path = args.output_folder_path
    language=args.language

    if not os.path.exists(folder_path):
        print("Error: Folder path not found.")
        return

    media_files = list_media_files_in_folder(folder_path)

    if not media_files:
        print("No media files found in the folder.")
        return

    print("Available media files in the folder:")
    for i, media_file in enumerate(media_files):
        print(f"{i + 1}. {media_file}")

    choice = int(input("Enter the number of the media file you want to transcribe: "))

    if choice < 1 or choice > len(media_files):
        print("Invalid choice.")
        return

    media_file_path = os.path.join(folder_path, media_files[choice - 1])

    # Check if it's a video or audio file
    if media_file_path.lower().endswith(('.mp4', '.avi', '.mkv')):
        audio_output_path = "temp_audio.mp3"
        extract_audio(media_file_path, audio_output_path)
        print("Transcribing video...")
        transcript = transcribe_audio_with_whispersync(api_key, audio_output_path,language)
        os.remove(audio_output_path)
    else:  # Audio file
        print("Transcribing audio...")

        if media_file_path.lower().endswith(('.m4a')):
            new_media_file_path= m4a_to_mp3(media_file_path, output_folder_path)
            transcript = transcribe_audio_with_whispersync(api_key, new_media_file_path,language)
            os.remove(new_media_file_path)

        transcript = transcribe_audio_with_whispersync(api_key, media_file_path,language)

    filename_w_ext= Path(media_file_path).name
    filename= f"{os.path.splitext(filename_w_ext)[0]}.txt"
    transcript_file_path = os.path.join(output_folder_path,filename)
    with open(transcript_file_path, "w", encoding="utf-8") as file:
        file.write(transcript)

    print(f"Transcript saved to: {transcript_file_path}")

if __name__ == "__main__":
    main()
