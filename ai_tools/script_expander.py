import os
import sys
import argparse

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env in Week 1
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("ERROR: No OPENAI_API_KEY found in .env.")
    sys.exit(1)

client = OpenAI(api_key=api_key)


def build_prompt(beat_text: str, channel: str) -> str:
    """
    Build a prompt that expands a beat into a 2–4 minute narrated
    Shrouded Ledger-style documentary segment.
    """

    if channel == "shrouded":
        style_block = """
Write in the exact voice and narrative style of *The Shrouded Ledger*:

TONE:
- Investigative and atmospheric.
- Cinematic documentary narration.
- A slow, ominous build—never melodramatic or sensational.
- Relies on sensory detail, historical texture, and subtle dread.
- Avoid clichés. Make the horror tasteful, uncanny, and intelligent.

STRUCTURE:
Your response MUST be formatted into three sections:

1) NARRATION:
   - 4–8 paragraphs.
   - Crisp, documentary-style voiceover.
   - Each paragraph should advance the viewer’s understanding or deepen the mystery.
   - Include tension, contradictory rumors, archival notes, or expert testimony.

2) B-ROLL SUGGESTIONS (bullet list):
   - 6–10 highly visual ideas.
   - Use The Shrouded Ledger B-Roll System:
       * Wide location shots
       * Archival stills
       * Interview room setups
       * Detail/macro shots
       * Environmental cutaways
       * Quiet, uncanny movement

3) CLOSING BEAT:
   - 1 paragraph that ends on subtle dread or an unanswered implication.
"""
    else:
        # Placeholder for future Aperture Black narrative expansions
        style_block = """
Write a surreal, image-driven narration suitable for a short Aperture Black video.
Focus on liminal visuals, analog-photo textures, and quiet dread.
"""

    return f"""
{style_block}

TASK:
Expand the following outline beat into a fully narrated segment:

BEAT:
\"\"\"{beat_text}\"\"\"

Begin now.
"""


def expand_script(beat_text: str, channel: str = "shrouded") -> str:
    """
    Call the OpenAI API to expand one beat into full narration.
    """

    prompt = build_prompt(beat_text, channel)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert documentary narrator and scriptwriter for atmospheric horror channels."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=1400,
        temperature=0.75,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Expand an outline beat into full Shrouded Ledger-style narration."
    )

    parser.add_argument(
        "beat",
        nargs="+",
        help="The outline beat text to expand.",
    )

    parser.add_argument(
        "--channel",
        choices=["shrouded", "aperture"],
        default="shrouded",
        help="Tone preset. Default: shrouded.",
    )

    args = parser.parse_args()

    beat_text = " ".join(args.beat)
    channel = args.channel

    print(f"\n[Creator Assistant] Expanding beat (channel='{channel}')...\n")

    narration = expand_script(beat_text, channel=channel)

    print("=== EXPANDED SCRIPT ===\n")
    print(narration)
