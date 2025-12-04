# Creator Assistant Tools Guide

This guide documents what each command does, best practices, and example usage.

## Outline Tool
- Generates 8–12 beat outlines.
- Format: documentary horror / Shrouded Ledger tone.
- Example:
  python3 tools/ai_tools/creator_assistant.py outline "Seed here"


## Expand Tool
- Expands a beat into a narrated section.
- Includes B-roll suggestions.
- Example:
python3 ai_tools/creator_assistant.py expand "Beat text here"


## Metadata Tool
- Generates YouTube title, description, tags, and hashtags.
- Example:
python3 ai_tools/creator_assistant.py metadata "Short summary of the video"


## Thumbnail Tool
- Generates thumbnail concepts + multiple Leonardo prompts.
- Example:
python3 ai_tools/creator_assistant.py thumbnail "Core visual or hook for the video"


## New Project Tool
- Creates a full project folder for:
  - Shrouded Ledger
  - Aperture Black
  - Novel/Writing
  - Example:
  # Shrouded Ledger episode
python3 ai_tools/creator_assistant.py new-project "Episode Title Here" --type shrouded

# Aperture Black video
python3 ai_tools/creator_assistant.py new-project "Visual Concept Here" --type aperture

# Novel / Story project
python3 ai_tools/creator_assistant.py new-project "Story Title Here" --type novel

Environment & API

Requires Python 3.

Requires a .env file in the project root with:
OPENAI_API_KEY=your_openai_key_here
pip install openai python-dotenv


## Coming soon:
- Auto-fill outline.md
- Auto-fill script.md
- Auto-fill metadata.md
- File updater tools
