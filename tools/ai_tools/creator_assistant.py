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
    Generate a structured story outline using the OpenAI API.

    Parameters:
        seed_idea: Short description or concept for the episode/video.
        beats: Number of outline beats to generate.
        channel: 'shrouded' for The Shrouded Ledger tone,
                 'aperture' for Aperture Black (image-driven) tone.

    Returns:
        A numbered outline as a single formatted string.
    """
    ...


    if channel == "shrouded":
        system_tone = (
            "You are an expert documentary-horror story crafter for a channel "
            "called The Shrouded Ledger. Your tonal benchmark is the episode "
            "about Viridia Vector Systems (VVS): investigative, systemic, "
            "forensic, and unnervingly plausible."
        )

        tone_block = f"""
You are writing an outline for an episode of *The Shrouded Ledger*, a documentary-style horror YouTube channel.

TONE & STYLE (SHROUDED LEDGER / VVS-LEVEL):
- Clinical, investigative, documentary-sharp.
- Emotionally restrained; horror emerges from systems, logistics, patterns, and implications.
- Feels like a blend of true-crime, leaked intelligence reports, and infrastructural horror.
- Assume an intelligent audience; do not over-explain.

SHOW, DON'T LABEL EMOTION (IMPORTANT):
- Do NOT write beats like: "The subject is terrified," "The investigator feels uneasy," or "They are horrified."
- Instead, describe observable behavior, physical reactions, choices, and environmental changes that imply emotion.
  Example (bad): "The engineer is scared of the panel."
  Example (good): "The engineer begins sleeping in his car rather than in the apartment with the panel installed."

STRUCTURAL MOVEMENT:
Design the {beats}-beat outline so it feels like it could sit next to the VVS episode in tone and quality.

Use this rough movement (you can adapt as needed to fit the concept):

1. OPENING MACRO VIEW:
   - Introduce the anomaly, case, object, phenomenon, or entity.
   - Explain how it appears in the world (infrastructure, culture, tech, places, lives).
   - Hint that its influence is larger and more systemic than anyone understands.

2. EARLY HISTORY / ORIGINS:
   - How it began, was discovered, or entered public awareness.
   - Early uses, innocent context, or initial misinterpretation.

3–6. ESCALATION & MICRO-CASES:
   - Show how the anomaly spreads, intensifies, or reveals its nature.
   - Include 1–3 specific micro-cases (individuals, facilities, towns, organizations).
   - Use supporting materials: leaked memos, reviews, CCTV stills, building reports, medical notes, etc.
   - Each beat should contain something *visual* the viewer could imagine seeing on screen.

7–9. INSTITUTIONAL RESPONSE & CONSEQUENCES:
   - How governments, companies, experts, or communities respond.
   - Attempts at suppression, containment, denial, or weaponization.
   - Show failures, cover-ups, and unintended consequences.

10. CLOSING IMAGE / ONGOING THREAT:
   - End on a chilling, specific image or insight that makes it clear:
     *the story is not over.*
   - It may suggest a fragile chance at human response, but avoid neat resolution.

OUTLINE REQUIREMENTS:
- Number the beats clearly from 1 to {beats}.
- Each beat should be 2–5 sentences.
- Each beat must contain at least ONE detail that could translate directly into B-roll:
  a place, document, object, action, or visual anomaly.
- Avoid generic phrasing like "things got worse," "they were terrified," "it was very disturbing."
- Be concrete and specific. Think like a documentarian and an editor.
"""
    else:
        # Aperture Black: image-driven, liminal horror outlines
        system_tone = (
            "You are an expert at crafting eerie, image-driven narrative outlines "
            "for a surreal horror channel called Aperture Black."
        )

        tone_block = f"""
You are writing an outline for a video on *Aperture Black*, a horror/liminal-image channel.

TONE & STYLE (APERTURE BLACK):
- Minimal narration, heavy on visuals and implied narrative.
- Liminal spaces, analog photos, impossible architecture, underwater or subterranean vistas.
- Feels like a curated sequence of recovered images rather than a traditional story.

OUTLINE STYLE:
- Number the beats from 1 to {beats}.
- Each beat should describe:
  - a primary visual environment,
  - the key unsettling detail(s),
  - and the implied narrative progression.
- Lean into megalophobia, claustrophobia, strange scale, and quiet dread.
- Avoid explaining how characters feel; instead show setting, posture, distance, and anomalies.
"""

    prompt = f"""
{tone_block}

TASK:
Using the following story seed, create a {beats}-beat outline for a {channel}-style video.

STORY SEED:
\"\"\"{seed_idea}\"\"\"

REQUIREMENTS:
- Number the beats 1 through {beats}.
- Each beat should be 2–5 sentences.
- For Shrouded Ledger: maintain investigative, systemic tone with concrete, filmable details.
- For Aperture Black: focus on distinct, visually striking scenes that build mood and implied story.

Begin now.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_tone},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1400,
        temperature=0.7,
    )

    return response.choices[0].message.content



# ---------- METADATA TOOL ----------

def generate_metadata_from_assistant(seed_text: str) -> str:
    """
    Generate YouTube metadata for a video concept.

    Parameters:
        seed_text: Short summary or hook for the video.

    Returns:
        Metadata text including title, description, tags, and hashtags.
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
    Generate YouTube metadata for a video concept.

    Parameters:
        seed_text: Short summary or hook for the video.

    Returns:
        Metadata text including title, description, tags, and hashtags.
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


# ---------- SCRIPT EXPANDER WRAPPER ----------

def expand_from_assistant(beat_text: str, channel: str = "shrouded", broll: bool = True) -> str:
    """
    Expand a single outline beat into a full narrated script segment.

    Uses script_expander.py under the hood.

    Parameters:
        beat_text: One outline beat or descriptive sentence.
        channel: 'shrouded' or 'aperture' tone preset.
        broll: If True, include a B-roll shotlist section in the output.

    Returns:
        Expanded narration text as a string.
    """

    from script_expander import expand_script  # local import
    return expand_script(beat_text, channel=channel, broll=broll)



# ---------- PROJECT GENERATOR WRAPPER ----------

def create_project_from_assistant(project_name: str, project_type: str = "shrouded") -> str:
    """
    Create a new creative project folder using project_generator.py.

    Parameters:
        project_name: Human-readable project title.
        project_type: 'shrouded', 'aperture', or 'novel'.

    Returns:
        The filesystem path of the created project directory.
    """

    from project_generator import create_project  # local import
    return create_project(project_name, project_type)



# ---------- THUMBNAIL GENERATOR WRAPPER ----------

def generate_thumbnails_from_assistant(seed_text: str, channel: str = "shrouded") -> str:
    """
    Generate thumbnail concept ideas and image prompts.

    Parameters:
        seed_text: Description or hook that should be reflected in the thumbnail.
        channel:   'shrouded' for The Shrouded Ledger tone,
                   'aperture' for Aperture Black tone.

    Returns:
        A formatted list of thumbnail concepts and prompt suggestions.
    """

    if channel == "shrouded":
        tone = (
            "the documentary horror aesthetic of The Shrouded Ledger: ominous but grounded, "
            "with realistic lighting, subtle surreal details, and a sense of leaked evidence."
        )
    else:
        tone = (
            "the liminal, analog, haunted-digital aesthetic of Aperture Black: eerie empty spaces, "
            "film grain, CRT bleed, underwater or subterranean textures, odd scale and perspective."
        )

    prompt = f"""
You are a thumbnail concept designer for a horror YouTube channel.

CHANNEL TONE:
- Work in {tone}
- Focus on concrete visual cues: composition, subject, environment, lighting, and perspective.
- Do NOT describe character emotions directly. Show posture, distance, gesture, or surroundings instead.

TASK:
Based on the following seed idea, propose 3–5 thumbnail concepts.
For each concept, include:

1) A short TITLE for the concept (e.g., "The Vanishing Street", "Her Final Broadcast").
2) A concrete COMPOSITION description:
   - camera angle (e.g., wide shot, close-up, over-the-shoulder, CCTV frame)
   - what is in the foreground, midground, and background
   - key visual anomaly or unsettling detail
3) A LEONARDO-STYLE PROMPT:
   - single line, comma-separated visual descriptors ready to paste into an image generator
   - include style cues appropriate to the channel (analog, film grain, CCTV, etc.)

SEED IDEA:
\"\"\"{seed_text}\"\"\"

FORMAT:
- Number each concept.
- For each, clearly label:
  - CONCEPT TITLE
  - COMPOSITION
  - LEONARDO PROMPT
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You generate horror thumbnail concepts and concrete image prompts.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=900,
        temperature=0.8,
    )

    return response.choices[0].message.content



# ---------- CLI WIRES ----------

def main():
    parser = argparse.ArgumentParser(
        description="Creator Assistant: multi-tool CLI for outlines, metadata, script expansion, and thumbnails."
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

       # Script expansion subcommand
    expand_parser = subparsers.add_parser(
        "expand", help="Expand an outline beat into full narration."
    )
    expand_parser.add_argument(
        "beat",
        nargs="+",
        help="The outline beat text to expand.",
    )
    expand_parser.add_argument(
        "--channel",
        choices=["shrouded", "aperture"],
        default="shrouded",
        help="Tone preset for script expansion (default: shrouded).",
    )
    expand_parser.add_argument(
        "--no-broll",
        action="store_true",
        help="Disable the cinematic B-roll section in the expanded script.",
    )

       # Thumbnail subcommand
    thumb_parser = subparsers.add_parser(
        "thumbnail",
        help="Generate thumbnail concepts and prompts.",
    )
    thumb_parser.add_argument(
        "seed",
        nargs="+",
        help="Short description of the video or core image idea.",
    )
    thumb_parser.add_argument(
        "--channel",
        choices=["shrouded", "aperture"],
        default="shrouded",
        help="Tone preset for thumbnail concepts (default: shrouded).",
    )

        # New project subcommand
    project_parser = subparsers.add_parser(
        "new-project",
        help="Create a new creative project folder with starter templates.",
    )
    project_parser.add_argument(
        "name",
        nargs="+",
        help="Name of the project (used for the folder).",
    )
    project_parser.add_argument(
        "--type",
        choices=["shrouded", "aperture", "novel"],
        default="shrouded",
        help="Type of project template to create (default: shrouded).",
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

    elif args.command == "expand":
        beat_text = " ".join(args.beat)
        channel = args.channel
        include_broll = not args.no_broll

        mode_label = "with B-ROLL" if include_broll else "no B-ROLL"
        print(f"\n[Creator Assistant] Expanding SCRIPT (channel='{channel}', {mode_label})...\n")
        narration = expand_from_assistant(beat_text, channel=channel, broll=include_broll)
        print("=== EXPANDED SCRIPT ===\n")
        print(narration)


    elif args.command == "thumbnail":
        seed_idea = " ".join(args.seed)
        channel = args.channel

        print(f"\n[Creator Assistant] Generating THUMBNAIL CONCEPTS (channel='{channel}')...\n")
        thumbs = generate_thumbnails_from_assistant(seed_idea, channel=channel)
        print("=== THUMBNAIL CONCEPTS ===\n")
        print(thumbs)


    elif args.command == "new-project":
        project_name = " ".join(args.name)
        project_type = args.type

        print(f"\n[Creator Assistant] Creating new project '{project_name}' (type='{project_type}')...\n")
        result_path = create_project_from_assistant(project_name, project_type)
        print(f"Project created at: {result_path}")



if __name__ == "__main__":
    main()
