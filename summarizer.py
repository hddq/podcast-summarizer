import os
import google.generativeai as genai
from config import GEMINI_API_KEY, SUMMARY_DIR, PROMPT_FILE

def summarize(transcript_path):
    """
    Summarizes the given transcript file using Gemini.
    """
    if not transcript_path or not os.path.exists(transcript_path):
        print(f"Transcript not found: {transcript_path}")
        return

    # Prepare output path
    filename = os.path.basename(transcript_path)
    # usually file is like "podcast.mp3.txt" -> "podcast.mp3.md"
    if filename.endswith(".txt"):
        base_name = filename[:-4]
    else:
        base_name = filename
    
    output_filename = base_name + ".md"
    output_path = os.path.join(SUMMARY_DIR, output_filename)

    if os.path.exists(output_path):
        print(f"Summary already exists: {output_path}")
        return

    # Ensure output dir
    if not os.path.exists(SUMMARY_DIR):
        os.makedirs(SUMMARY_DIR)

    # Read transcript
    try:
        with open(transcript_path, "r", encoding="utf-8") as f:
            transcript_text = f.read()
    except Exception as e:
        print(f"Error reading transcript: {e}")
        return

    # Read prompt
    if not os.path.exists(PROMPT_FILE):
        print(f"Prompt file not found: {PROMPT_FILE}")
        return

    try:
        with open(PROMPT_FILE, "r", encoding="utf-8") as f:
            prompt_template = f.read()
    except Exception as e:
        print(f"Error reading prompt file: {e}")
        return

    # Construct prompt
    prompt = prompt_template.replace("{transcript}", transcript_text)

    # Call Gemini
    if not GEMINI_API_KEY:
        print("GEMINI_API_KEY is not set.")
        return

    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-3-flash-preview')
        print(f"Summarizing {filename}...")
        response = model.generate_content(prompt)
        
        summary_text = response.text

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(summary_text)
        
        print(f"Summary saved to {output_path}")

    except Exception as e:
        print(f"Summarization failed: {e}")