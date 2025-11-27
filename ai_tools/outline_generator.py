import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("ERROR: OPENAI_API_KEY not found in .env")
    sys.exit(1)

# Create OpenAI client
client = OpenAI(api_key=api_key)


def generate_outline(seed_idea: str, beats: int = 10) -> str:
    """
    Generate a Shrouded Ledger–style documentary horror outline
    from a short seed idea.
    """

    prompt = f"""
You are writing an outline for an episode of *The Shrouded Ledger*, a documentary-style horror YouTube channel.

TONE & STYLE:
- Investigative, methodical, and atmospheric.
- Feels like a blend of true-crime documentary, paranormal investigation, and urban legend.
- Focus on unsettling details, eerie implications, and concrete images the narrator could describe on screen.
- No cheap jump scares; favor creeping dread, strange logic, and uncanny patterns.

TASK:
Using the following story seed, create a {beats}-beat outline for a 15–25 minute documentary-style video.

STORY SEED:
\"\"\"{seed_idea}\"\"\"

STRUCTURE:
- Number the beats clearly from 1 to {beats}.
- Each beat should be 2–5 sentences.
- Each beat should describe:
  - What the viewer "sees" (B-roll, locations, archival material, interviews).
  - What the narrator "reveals" (facts, rumors, contradictions, emotional turns).
- Start by establishing the surface story and its public perception.
- Then escalate with new discoveries, inconsistencies, and darker interpretations.
- End on a disturbing but not fully resolved implication or image that ties back to the opening.

REQUIREMENTS:
- Make sure you reach beat {beats}. Do not stop early.
- The final beat (beat {beats}) must function as a closing image or chilling final revelation.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert documentary-horror story crafter for a channel "
                    "called The Shrouded Ledger. Your outlines are unnerving, structured, "
                    "atmospheric, and cinematic."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=1200,
        temperature=0.7,
    )

    # New OpenAI client: message is an object, not a dict
    return response.choices[0].message.content


if __name__ == "__main__":
    # Require at least one argument (the story seed)
    if len(sys.argv) < 2:
        print("Usage: python3 ai_tools/outline_generator.py 'Your story seed here'")
        sys.exit(1)

    # Join all arguments after the script name into one seed string
    seed_idea = " ".join(sys.argv[1:])

    outline = generate_outline(seed_idea)

    print("\n=== GENERATED OUTLINE ===\n")
    print(outline)
