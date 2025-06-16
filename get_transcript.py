import sys
import json
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable

video_id = sys.argv[1]

try:
    # Attempt to fetch the transcript
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    full_text = " ".join([item['text'] for item in transcript])
    print(full_text)

except VideoUnavailable:
    print("ERROR: The video is unavailable or does not exist.")

except TranscriptsDisabled:
    print("ERROR: Transcripts are disabled for this video.")

except NoTranscriptFound:
    print("ERROR: No transcript found. The video may not have captions.")

except Exception as e:
    print(f"ERROR: {str(e)}")