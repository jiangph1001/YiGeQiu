import moviepy.editor as mp
import os
import argparse


def split_videos(input_file,song_times):
    # input_file = "path/to/input/video.mp4"
    # song_times = [(10, 20), (30, 40), (50, 60)]

    video = mp.VideoFileClip(input_file)
    for i, (start, end) in enumerate(song_times):
        # Use the subclip() method of the MoviePy video object to extract each song as a separate video
        song = video.subclip(start, end)
        # Use the audio attribute of each song video to extract the audio as a separate audio file
        audio = song.audio
        # Save each audio file as an MP3 file
        audio.write_audiofile(f"song_{i}.mp3")

    # Close the video object
    video.close()



def get_song_times_by_pydub(input_file):
    import moviepy.editor as mp
    from pydub import AudioSegment
    # Load the MP4 file and extract the audio
    video = mp.VideoFileClip(input_file)
    audio = video.audio.to_audiofile("temp_audio.wav")

    # Load the audio file and split it into segments of silence and non-silence
    sound = AudioSegment.from_wav("temp_audio.wav")
    chunks = split_on_silence(sound, min_silence_len=1000, silence_thresh=-50)

    # Get the start and end times of each non-silent segment
    song_times = []
    for i, chunk in enumerate(chunks):
        if i == 0:
            start_time = 0
        else:
            start_time = chunks[i-1].duration_seconds
        end_time = start_time + chunk.duration_seconds
        if chunk.dBFS > -50:
            song_times.append((start_time, end_time))

    # Delete the temporary audio file
    os.remove("temp_audio.wav")

    return song_times



def get_song_times_by_librosa(input_file):
    import librosa
    # Load the audio file
    y, sr = librosa.load(input_file)

    # Detect onsets
    onsets = librosa.onset.onset_detect(y=y, sr=sr)

    # Get the start and end times of each segment
    song_times = []
    for i, onset in enumerate(onsets):
        if i == 0:
            start_time = 0
        else:
            start_time = librosa.samples_to_time(onsets[i-1], sr=sr)
        end_time = librosa.samples_to_time(onset, sr=sr)
        song_times.append((start_time, end_time))

    return song_times


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to input video file")
    parser.add_argument("--engine", default="pydub", choices=["pydub", "librosa"], help="Audio processing engine to use")
    args = parser.parse_args()

    # Get the song times from the input file
    if args.engine == "pydub":
        get_song_times = get_song_times_by_silence
    elif args.engine == "librosa":
        get_song_times = get_song_times_by_librosa


    song_times = get_song_times(args.input)
    # Split the input video into separate song videos
    split_videos(args.input, song_times)

    # Delete the temporary audio file
if __name__ == "__main__":
    main()