import os
import sys
import argparse

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("ERROR: Missing OPENAI_API_KEY in .env")
    sys.exit(1)

client = OpenAI(api_key=api_key)


def build_prompt(seed_idea: str, channel: str) -> str:
    """
    Build a detailed prompt for generating 5–8 thumbnail concepts.
    """

    if channel == "shrouded":
        style_block = """
You are generating thumbnail CONCEPTS for a documentary-horror YouTube channel called *The Shrouded Ledger*.

TONE:
- Dark academia + investigative journalism + paranormal documentary.
- Thumbnails must feel like recovered evidence, archival frames, or unsettling images caught at the wrong second.
- Avoid cheesy horror tropes or big cartoonish fonts.

VISUAL RULES:
- Cool or neutral color palettes (deep blues, greys, sickly greens, tungsten lamps).
- High contrast, vignette, subtle film grain.
- Light source is usually unclear or off-frame.
- Composition: rule of thirds, negative space, off-center subjects.
- Never overcrowded. One central mystery element.
- Texture: analog film, static, CRT distortion, archival paper, haunted still-frame energy.

TEXT RULES:
- Minimal or none.
- If present: 1–4 words max. Subtle. Lower-left or lower-right.
- No neon colors. No ALL CAPS unless it's diegetic.
"""
    else:
        # Aperture Black
        style_block = """
You are generating thumbnail CONCEPTS for a horror/liminal-image channel called *Aperture Black*.

TONE:
- Analog photos, impossible architecture, megalophobia, underwater ruins, disturbing nostalgia.
- Evokes the feeling of a recovered image from an abandoned camera.

VISUAL RULES:
- Soft but eerie lighting, heavy grain, washed-out color with surreal hues.
- Wide shots, deep vanishing points, impossible geometry, fog, empty spaces.
- One impossible or unsettling detail that rewards a second look.

TEXT RULES:
- Usually none.
- If used, must feel like an artifact: grainy, understated, not “designed.”

"""

    return f"""
{style_block}

TASK:
Based on the following video concept, produce 5–8 THUMBNAIL CONCEPTS.

For each concept, include:

1) TITLE (a very short name for the idea, not the YouTube title)
2) VISUAL DESCRIPTION (camera angle, composition, lighting, main subject)
3) ATMOSPHERE & TEXTURE (grain, distortion, lens, color grade)
4) OPTIONAL TEXT OVERLAY (1–4 words max) that fits the tone
5) NOTES FOR IMAGE GENERATION (Leonardo/MJ-friendly keywords)

VIDEO CONCEPT:
\"\"\"{seed_idea}\"\"\"

OUTPUT FORMAT (IMPORTANT):

CONCEPT 1:
[Title]
Visual:
Atmosphere:
Text Overlay:
Gen Notes:

CONCEPT 2:
...
"""


def generate_thumbnails(seed_idea: str, channel: str) -> str:
    prompt = build_prompt(seed_idea, channel)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional YouTube thumbnail concept artist specializing in horror, liminal imagery, and documentary aesthetics."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=1500,
        temperature=0.75,
    )

    return response.choices[0].message.content


# ---- CLI ----

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate 5–8 thumbnail concepts for Shrouded Ledger or Aperture Black."
    )

    parser.add_argument(
        "seed",
        nargs="+",
        help="Short description or concept for the video.",
    )

    parser.add_argument(
        "--channel",
        choices=["shrouded", "aperture"],
        default="shrouded",
        help="Which channel's tone to use. Default: shrouded.",
    )

    args = parser.parse_args()
    seed_idea = " ".join(args.seed)
    channel = args.channel

    print(f"\n[Creator Assistant] Generating THUMBNAIL CONCEPTS (channel='{channel}')...\n")

    result = generate_thumbnails(seed_idea, channel)
    print("=== THUMBNAIL CONCEPTS ===\n")
    print(result)
