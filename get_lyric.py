def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="path to input MP3 file")
    args = parser.parse_args()

    # Load the audio file
    audio_file = AudioSegment.from_file(args.input, format="mp3")

    # Export the audio file as WAV
    audio_file.export("temp.wav", format="wav")

    # Initialize the recognizer
    r = sr.Recognizer()

    # Load the audio file into the recognizer
    with sr.AudioFile("temp.wav") as source:
        audio = r.record(source)

    # Transcribe the audio
    text = r.recognize_google(audio)

    # Save the text to a file with the same name as the input file, but with a .lrc extension
    output_file = os.path.splitext(args.input)[0] + ".lrc"
    with open(output_file, "w") as f:
        f.write(text)

    # Delete the temporary WAV file
    os.remove("temp.wav")

if __name__ == "__main__":
    main()