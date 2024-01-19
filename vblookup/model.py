import scrapetube
import chromadb
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms import OpenAI
from pprint import pprint

def get_client():
    return chromadb.PersistentClient(path="./chroma-db/")

def determine_author(transcript):
  
  transcript = transcript.lower()

  # If only "John" is mentioned, then it's a "Hank" video
  if "john" in transcript and "hank" not in transcript:
    return "hank" 
  # If only "hank" is mentioned, then it's a "john" video
  if "hank" in transcript and "john" not in transcript:
    return "john"
  
  # If "Tuesday" occurs after "john", then it's a "hank" video
  if "tuesday" in transcript and "john" in transcript:
    if transcript.rfind("tuesday") > transcript.rfind("john"):
      return "hank"
    
  # If "Friday" occurs after "hank", then it's a "john" video
  if "friday" in transcript and "hank" in transcript:
    if transcript.rfind("friday") > transcript.rfind("hank"):
      return "john"
    
  return "unknown"

def llm_summary(transcript):
  llm = OpenAI(temperature=0.9)

def fill_collection():
  # Scrape the last 100 videos from the Vlogbrothers channel
  videos = scrapetube.get_channel(channel_url="https://www.youtube.com/vlogbrothers", limit=100)

  # Import Chroma and instantiate a client.
  client = get_client()

  # Create a new Chroma collection to store transcripts
  try:
    client.delete_collection("green_brothers")
  except:
    print("Collection doesn't exist yet")
  collection = client.create_collection("green_brothers")

  # Embed and store the first 100 supports for this demo

  text_splitter = CharacterTextSplitter(
    separator = "\n",
    chunk_size = 1000,
    chunk_overlap  = 200,
    length_function = len,
    # is_separator_regex = False,
  )

  for video in videos:
    print ("importing " + video["videoId"])
    
    transcript = YouTubeTranscriptApi.get_transcript(video["videoId"])
    transcript_text = TextFormatter().format_transcript(transcript)

    author = determine_author(transcript_text)

    documents = text_splitter.split_text(transcript_text)
    collection.add(
      ids = [f"yt_{video['videoId']}_{j}" for j in range(len(documents))],
      documents=documents,
      metadatas = [{"author": author, 
                    "source": "YouTube", 
                    "source_key": video['videoId'], 
                    "title": video["title"]["runs"][0]["text"], 
                    "chunk": j,
                    "link": f"https://www.youtube.com/watch?v={video['videoId']}"} for j in range(len(documents))]
    )

    print(f"as {len(documents)} chunks")

