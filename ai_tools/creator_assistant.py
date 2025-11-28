import os
import sys
import argparse

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env in the Week 1 folder
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("ERROR: OPENAI_API_KEY not found in .env")
    sys.exit(1)

client = OpenAI(api_key=api_key)


# ---------- OUTLINE TOOL ----------

def generate_outline(seed_idea: str, beats: int = 10, channel: str = "shrouded") -> str:
    """
    Generate a documentary-style horror outline.
    Currently tuned for The Shrouded Ledger tone.
    """

    if channel == "shrouded":
        system_tone = (
            "You are an expert documentary-horror story crafter for a channel "
            "called The Shrouded Ledger. Your outlines are unnerving, structured, "
            "atmospheric, and cinematic."
        )
        tone_block = """
You are writing an outline for an episode of *The Shrouded Ledger*, a documentary-style horror YouTube channel.

TONE & STYLE:
- Investigative, methodical, and atmospheric.
- Feels like a blend of true-crime documentary, paranormal investigation, and urban legend.
- Focus on unsettling details, eerie implications, and concrete visuals the narrator could describe.
- Avoid cheap jump scares; favor creeping dread and uncanny logic.
"""
    else:
        # Placeholder for future channel-specific outline tones (e.g., Aperture Black narrative episodes)
        system_tone = (
            "You are an expert at crafting eerie, image-driven narrative outlines "
            "for surreal horror channels."
        )
        tone_block = """
You are writing an outline for an eerie, image-driven horror video.
Focus on surreal visuals, liminal spaces, and atmospheric progression.
"""

    prompt = f"""
{tone_block}

TASK:
Using the following story seed, create a {beats}-beat outline for a 15–25 minute video.

STORY SEED:
\"\"\"{seed_idea}\"\"\"

STRUCTURE:
- Number the beats clearly from 1 to {beats}.
- Each beat should be 2–5 sentences.
- Each beat should describe both:
  - What the viewer "sees" (locations, B-roll, archival materials, interviews, etc.).
  - What the narrator "reveals" (facts, rumors, contradictions, emotional turns).
- Start with the surface story and public perception.
- Escalate with new discoveries, inconsistencies, and darker interpretations.
- End on a disturbing but not fully resolved implication or image that ties back to the opening.

REQUIREMENTS:
- Make sure you reach beat {beats}. Do not stop early.
- The final beat (beat {beats}) must function as a closing image or chilling final revelation.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_tone},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1200,
        temperature=0.7,
    )

    return response.choices[0].message.content


# ---------- METADATA TOOL ----------

def build_metadata_prompt(seed_idea: str, channel: str) -> str:
    """
    Build a channel-specific prompt for metadata generation.
    """

    if channel == "shrouded":
        channel_blurb = """
You are generating YouTube metadata for a horror documentary channel called *The Shrouded Ledger*.

TONE:
- Investigative, documentary-style, unsettling but not cheesy.
- Feels like true crime meets paranormal investigation and lost media.
- Avoid clickbait-y ALL CAPS, but you can lean into tension and mystery.

AUDIENCE:
- Viewers who like deep-dive horror stories, urban legends, ARGs, and weird history.
"""
    else:  # aperture
        channel_blurb = """
You are generating YouTube metadata for a horror/liminal-image channel called *Aperture Black*.

TONE:
- Minimal, eerie, suggestive.
- Focus on mood: liminal spaces, analog photos, impossible or unsettling locations.
- Titles can be short and haunting; descriptions should feel like a curator note or recovered artifact.
"""

    return f"""
{channel_blurb}

TASK:
Based on the following video concept, create:

1) A single, strong YouTube TITLE.
   - Aim for ~60 characters or fewer when possible.
   - Must be understandable and intriguing on its own.

2) A 2–4 paragraph DESCRIPTION.
   - First paragraph: hook the viewer emotionally / conceptually.
   - Second/third paragraphs: give context, deepen the mystery, hint at what's explored.
   - Last line: gentle call-to-action (subscribe, like, etc.) that fits the channel tone.

3) A list of 15–25 comma-separated TAGS.
   - Start with narrow, highly relevant tags (specific scenario, themes).
   - Include a mix of niche and broad tags (e.g., horror documentary, analog horror, liminal spaces).
   - No hashtags in this section, just raw tags.

4) A block of 5–10 HASHTAGS.
   - These will be pasted at the bottom of the description.
   - Include channel-relevant tags (e.g., #TheShroudedLedger or #ApertureBlack if appropriate).

VIDEO CONCEPT:
\"\"\"{seed_idea}\"\"\"

OUTPUT FORMAT (IMPORTANT):
Return your answer in this exact structure:

TITLE:
[title text here]

DESCRIPTION:
[one or more paragraphs]

TAGS:
[tag1, tag2, tag3, ...]

HASHTAGS:
#tag1 #tag2 #tag3 ...
"""


def generate_metadata(seed_idea: str, channel: str = "shrouded") -> str:
    """
    Call the OpenAI API to generate metadata text.
    """

    prompt = build_metadata_prompt(seed_idea, channel)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert YouTube metadata strategist for horror channels. "
                    "You balance SEO with atmospheric, emotionally resonant language."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=900,
        temperature=0.7,
    )

    return response.choices[0].message.content


# ---------- CLI WIRES ----------

def main():
    parser = argparse.ArgumentParser(
        description="Creator Assistant: multi-tool CLI for outlines and metadata."
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Outline subcommand
    outline_parser = subparsers.add_parser("outline", help="Generate a story outline.")
    outline_parser.add_argument(
        "seed",
        nargs="+",
        help="Short description or concept for the video/story.",
    )
    outline_parser.add_argument(
        "--beats",
        type=int,
        default=10,
        help="Number of beats in the outline (default: 10).",
    )
    outline_parser.add_argument(
        "--channel",
        choices=["shrouded", "aperture"],
        default="shrouded",
        help="Tone preset for outline (default: shrouded).",
    )

    # Metadata subcommand
    metadata_parser = subparsers.add_parser(
        "metadata", help="Generate YouTube metadata (title, description, tags, hashtags)."
    )
    metadata_parser.add_argument(
        "seed",
        nargs="+",
        help="Short description or concept for the video.",
    )
    metadata_parser.add_argument(
        "--channel",
        choices=["shrouded", "aperture"],
        default="shrouded",
        help="Channel preset (shrouded or aperture). Default: shrouded.",
    )

    args = parser.parse_args()

    if args.command == "outline":
        seed_idea = " ".join(args.seed)
        beats = args.beats
        channel = args.channel

        print(f"\n[Creator Assistant] Generating OUTLINE ({beats} beats, channel='{channel}')...\n")
        outline = generate_outline(seed_idea, beats=beats, channel=channel)
        print("=== OUTLINE ===\n")
        print(outline)

    elif args.command == "metadata":
        seed_idea = " ".join(args.seed)
        channel = args.channel

        print(f"\n[Creator Assistant] Generating METADATA (channel='{channel}')...\n")
        metadata = generate_metadata(seed_idea, channel=channel)
        print("=== METADATA ===\n")
        print(metadata)


if __name__ == "__main__":
    main()
