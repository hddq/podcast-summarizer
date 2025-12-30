import os
from google import genai
from config import GEMINI_API_KEY, SUMMARY_DIR, PROMPT_FILE, TRANSCRIPT_DIR

def summarize(transcript_path):
    """
    Summarizes the given transcript file using Gemini.
    """
    if not transcript_path or not os.path.exists(transcript_path):
        print(f"Transcript not found: {transcript_path}")
        return

    # Determine relative path to maintain structure
    try:
        abs_transcript = os.path.abspath(transcript_path)
        abs_transcript_dir = os.path.abspath(TRANSCRIPT_DIR)
        if abs_transcript.startswith(abs_transcript_dir):
            rel_path = os.path.relpath(abs_transcript, start=abs_transcript_dir)
        else:
            rel_path = os.path.basename(transcript_path)
    except Exception:
        rel_path = os.path.basename(transcript_path)

    # Remove .txt suffix if present
    if rel_path.endswith(".txt"):
        rel_path = rel_path[:-4]
    
    output_filename = rel_path + ".md"
    output_path = os.path.join(SUMMARY_DIR, output_filename)

    if os.path.exists(output_path):
        print(f"Summary already exists: {output_path}")
        return

    # Ensure output dir
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

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
        client = genai.Client(api_key=GEMINI_API_KEY)
        print(f"Summarizing {os.path.basename(transcript_path)}...")
        response = client.models.generate_content(
            model='gemini-3-flash-preview', 
            contents=prompt
        )
        
        summary_text = response.text

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(summary_text)
        
        print(f"Summary saved to {output_path}")

    except Exception as e:
        print(f"Summarization failed: {e}")