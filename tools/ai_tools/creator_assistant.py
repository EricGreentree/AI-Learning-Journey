import os
import sys
import argparse
import re

from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env in the Week 1 folder
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("ERROR: OPENAI_API_KEY not found in .env")
    sys.exit(1)

client = OpenAI(api_key=api_key)

from project_generator import slugify_name  # add near top, where other imports from project_generator are


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


# ---------- ALTERNATIVES TOOL ----------

def generate_ideas_from_assistant(
    seed_idea: str,
    count: int = 5,
    channel: str = "shrouded",
) -> str:
    """
    Generate multiple alternative story treatments for a Shrouded Ledger or Aperture Black episode.

    Parameters:
        seed_idea: A short description or premise (e.g., 'classified social experiment in a suburb').
        count:     Number of alternative treatments to generate.
        channel:   'shrouded' for documentary horror (The Shrouded Ledger),
                   'aperture' for image-driven liminal horror (Aperture Black).

    Returns:
        A formatted string containing numbered story treatments.
    """
    if channel == "shrouded":
        style_description = (
            "documentary-style horror in the tone of The Shrouded Ledger: "
            "investigative, calm, ominous, grounded in leaks, documents, and interviews. "
            "No jump scares, no gore, but deep unease."
        )
    else:
        style_description = (
            "image-driven, liminal horror in the tone of Aperture Black: "
            "disturbing photographs, analog textures, uncanny spaces, and subtle cosmic dread. "
            "Narration is sparse and atmospheric, focusing on visual investigation rather than character psychology."
        )

    prompt = f"""
You are designing episode concepts for a YouTube horror channel.

CHANNEL STYLE:
- Work in {style_description}
- Focus on a CENTRAL ANOMALY or SYSTEM (device, program, corporation, experiment, location).
- Show how it intersects with normal life: suburbs, offices, infrastructure, digital platforms.
- Each concept should be self-contained, distinct from the others, and scalable to a 20–40 minute episode.

IMPORTANT RULES:
- Do NOT just describe vague feelings. Show concrete events, artifacts, footage, leaked memos, witness behavior.
- Avoid generic 'lost tapes' or 'we don't know what happened' endings.
- Make each idea specific enough that it feels like a real casefile, not a loose vibe.

SEED IDEA:
\"\"\"{seed_idea}\"\"\"


TASK:
Generate {count} different story treatments.

For EACH treatment, include:

1. A TITLE (evocative, like a Shrouded Ledger episode or Aperture Black video).
2. A 2–3 sentence CORE PREMISE.
3. The CENTRAL ANOMALY (what is actually going on? device / entity / program / experiment / infrastructure / pattern).
4. The PRIMARY EVIDENCE that would appear in the episode:
   - e.g., leaked internal documents, product manuals, error logs, urban legends, CCTV footage, photos, reviews, building plans.
5. ESCALATION: 3 short bullet points that show how the situation worsens over time.
6. PRESENT DAY STATUS: 1–2 sentences about what the world looks like after the events (cover-up? quiet integration? unexplained disappearances?).

FORMAT IT LIKE THIS:

1) TITLE: ...
   PREMISE: ...
   CENTRAL ANOMALY: ...
   EVIDENCE:
   - ...
   - ...
   ESCALATION:
   - ...
   - ...
   - ...
   PRESENT DAY STATUS: ...

2) TITLE: ...
   ...

Make sure each treatment is clearly separated and numbered.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You generate structured horror story treatments with concrete investigative details. "
                    "You do not describe internal emotions directly; you show events, documents, and observable behavior."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=2000,
        temperature=0.9,
    )

    return response.choices[0].message.content

# ---------- IDEA LOCKER TOOL ----------

def run_idea_locker(args: argparse.Namespace) -> None:
    """
    Save ideas text into a project's concepts.md file.

    Usage patterns:

      # Save from a file
      creator_assistant.py idea-locker --project "Hush Pulse Initiative" \
          --source /tmp/ideas_batch1.txt --label "Twin Flame Portal variants" --favorite

      # Save directly from stdin (pipe from ideas command)
      creator_assistant.py ideas "some seed idea" ... \
          | creator_assistant.py idea-locker --project "Hush Pulse Initiative"

      # List the current concepts.md
      creator_assistant.py idea-locker --project "Hush Pulse Initiative" --list
    """
    project_name = args.project

    # Match the same Projects root logic used by fill-outline / fill-script
    base_dir = os.path.dirname(os.path.dirname(__file__))  # ai_tools -> tools
    projects_root = os.path.join(base_dir, "Projects")

    # Prefer the slugified folder name, but fall back to raw name if needed
    slug_folder = slugify_name(project_name)
    slug_dir = os.path.join(projects_root, slug_folder)
    raw_dir = os.path.join(projects_root, project_name)

    if os.path.isdir(slug_dir):
        project_dir = slug_dir
    elif os.path.isdir(raw_dir):
        project_dir = raw_dir
    else:
        raise SystemExit(
            "Project folder not found.\n"
            f"Tried:\n  {slug_dir}\n  {raw_dir}\n"
            "Make sure you've created the project with 'new-project'."
        )

    concepts_path = os.path.join(project_dir, "concepts.md")

    # If user just wants to list existing concepts, do that and exit
    if getattr(args, "list", False):
        if not os.path.exists(concepts_path):
            print(f"No concepts.md found for project: {project_name}")
            return
        with open(concepts_path, "r", encoding="utf-8") as f:
            print(f.read())
        return

    # --- determine ideas text source ---
    if args.source:
        # Read from a file
        if not os.path.exists(args.source):
            raise SystemExit(f"Source file not found: {args.source}")
        with open(args.source, "r", encoding="utf-8") as f:
            ideas_text = f.read().strip()
    else:
        # Read from stdin (for piping)
        if sys.stdin.isatty():
            raise SystemExit(
                "No --source provided and no stdin detected.\n"
                "Either pass --source /path/to/file or pipe text into this command."
            )
        ideas_text = sys.stdin.read().strip()

    if not ideas_text:
        raise SystemExit("No ideas text to save (input was empty).")

    # --- ensure concepts.md exists and has a header ---
    is_new_file = not os.path.exists(concepts_path)
    if is_new_file:
        with open(concepts_path, "w", encoding="utf-8") as f:
            f.write("# Idea Locker\n\n")
            f.write(f"_Project:_ **{project_name}**\n\n")

    # --- append a new batch section ---
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    label = args.label or ""
    favorite_flag = "yes" if args.favorite else "no"

    batch_header_parts = [f"### Batch – {timestamp}"]
    if label:
        batch_header_parts.append(f"({label})")
    batch_header = " ".join(batch_header_parts)

    with open(concepts_path, "a", encoding="utf-8") as f:
        f.write("\n---\n\n")
        f.write(f"{batch_header}\n\n")
        f.write(f"- Favorite batch: **{favorite_flag}**\n")
        f.write(f"- Source: `idea-locker`\n\n")
        f.write("```text\n")
        f.write(ideas_text)
        f.write("\n```\n")

    print(f"Ideas batch saved to {concepts_path}")


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

 
 # ------------- OUTLINE FILLER ----------
    
def fill_project_outline_from_assistant(
    project_name: str,
    seed_idea: str,
    beats: int = 10,
    channel: str = "shrouded",
) -> str:
    """
    Generate an outline for a given project and append it to that project's outline.md.

    Parameters:
        project_name: The human-readable name of the project (same as used in new-project).
        seed_idea:    The seed concept for the outline.
        beats:        Number of outline beats.
        channel:      'shrouded' or 'aperture'.

    Returns:
        The path to the outline.md file that was written to.
    """
    # Locate Projects root (same logic as project_generator.ensure_projects_root)
    base_dir = os.path.dirname(os.path.dirname(__file__))  # ai_tools -> tools -> Week 1
    projects_root = os.path.join(base_dir, "Projects")

    folder_name = slugify_name(project_name)
    project_dir = os.path.join(projects_root, folder_name)

    if not os.path.isdir(project_dir):
        raise FileNotFoundError(
            f"Project folder not found: {project_dir}\n"
            "Make sure you've created it with the 'new-project' command."
        )

    outline_path = os.path.join(project_dir, "outline.md")

    # Generate the outline text using your existing outline generator
    outline_text = generate_outline(seed_idea, beats=beats, channel=channel)

    # Append to outline.md with a separator and header
    header = f"\n\n---\n\n# AUTO-GENERATED OUTLINE ({channel}, {beats} beats)\n\n"
    content_to_write = header + outline_text.strip() + "\n"

    with open(outline_path, "a", encoding="utf-8") as f:
        f.write(content_to_write)

    return outline_path


# ---------- BEAT EXPANDER ----------

def append_expanded_beat_to_script(
    project_name: str,
    beat_text: str,
    channel: str = "shrouded",
    include_broll: bool = True,
) -> str:
    """
    Expand a single outline beat and append it to a project's script.md file.

    Parameters:
        project_name: Human-readable project name (same as used with new-project).
        beat_text:    The outline beat or descriptive sentence to expand.
        channel:      'shrouded' or 'aperture' tone preset.
        include_broll: If True, include the B-roll section in the expansion.

    Returns:
        The filesystem path of the script.md file that was written to.
    """
    # Locate Projects root (parent of ai_tools is tools/)
    base_dir = os.path.dirname(os.path.dirname(__file__))  # ai_tools -> tools
    projects_root = os.path.join(base_dir, "Projects")

    folder_name = slugify_name(project_name)
    project_dir = os.path.join(projects_root, folder_name)

    if not os.path.isdir(project_dir):
        raise FileNotFoundError(
            f"Project folder not found: {project_dir}\n"
            "Make sure you've created it with the 'new-project' command."
        )

    script_path = os.path.join(project_dir, "script.md")

    # Generate expanded narration using your existing expander
    expanded = expand_from_assistant(beat_text, channel=channel, broll=include_broll)

    # Short header so you know what this segment came from
    short_beat = beat_text.strip().replace("\n", " ")
    if len(short_beat) > 120:
        short_beat = short_beat[:117] + "..."

    header = (
        f"\n\n---\n\n"
        f"## AUTO-GENERATED SEGMENT ({channel})\n\n"
        f"**Source beat:** {short_beat}\n\n"
    )

    content_to_write = header + expanded.strip() + "\n"

    with open(script_path, "a", encoding="utf-8") as f:
        f.write(content_to_write)

    return script_path

# ----------SCRIPT DRAFT BUILDER ----------

def run_script_draft_builder(args: argparse.Namespace) -> None:
    """
    Build a full Draft 0 script from a project's curated beats file.

    - Reads numbered beats from beats_final.md (or custom beats file)
    - Expands each beat using expand_from_assistant()
    - Appends a Draft 0 section to script.md in order
    """
    project_name = args.project
    channel = args.channel
    include_broll = not args.no_broll
    beats_filename = args.beats_file or "beats_final.md"

    try:
        project_dir = _get_project_dir(project_name)
    except FileNotFoundError as e:
        raise SystemExit(str(e))

    beats_path = os.path.join(project_dir, beats_filename)
    script_path = os.path.join(project_dir, "script.md")

    if not os.path.exists(beats_path):
        raise SystemExit(
            f"Beats file not found for project '{project_name}': {beats_path}\n"
            "Run beat-manager first to create a final beat list."
        )

    with open(beats_path, "r", encoding="utf-8") as f:
        beats_text = f.read()

    beats = _parse_numbered_beats(beats_text)

    if not beats:
        raise SystemExit(
            f"No numbered beats found in {beats_filename}.\n"
            "Make sure it contains lines like '1. First beat...'"
        )

    total = len(beats)
    mode_label = "with B-ROLL" if include_broll else "no B-ROLL"

    print(
        f"\n[Creator Assistant] Script Draft Builder\n"
        f"Project: {project_name}\n"
        f"Beats file: {beats_path}\n"
        f"Output script: {script_path}\n"
        f"Channel: {channel}, Mode: {mode_label}\n"
        f"Beats to expand: {total}\n"
    )

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Open script.md in append mode and write one Draft 0 section header
    with open(script_path, "a", encoding="utf-8") as f:
        f.write("\n\n---\n\n")
        f.write(
            f"# AUTO-GENERATED DRAFT 0 ({channel}, {mode_label})\n\n"
            f"_Project:_ **{project_name}**\n"
            f"_Generated:_ {timestamp}\n"
            f"_Source beats file:_ `{os.path.basename(beats_path)}`\n\n"
        )

        for idx, (num, beat_text) in enumerate(beats, start=1):
            print(f"[Creator Assistant] Expanding beat {idx}/{total} (original #{num})...")
            expanded = expand_from_assistant(
                beat_text,
                channel=channel,
                broll=include_broll,
            )

            # Short beat preview for the header
            short_beat = beat_text.strip().replace("\n", " ")
            if len(short_beat) > 160:
                short_beat = short_beat[:157] + "..."

            f.write(f"## Beat {idx}\n\n")
            f.write(f"**Source beat:** {short_beat}\n\n")
            f.write(expanded.strip())
            f.write("\n\n")

    print(f"\n[Creator Assistant] Draft 0 complete.")
    print(f"Expanded {total} beats into: {script_path}")

# ---------- BEAT MANAGER TOOL ----------

def _get_project_dir(project_name: str) -> str:
    """
    Resolve a project directory using the same slug logic as fill-outline/fill-script.
    """
    base_dir = os.path.dirname(os.path.dirname(__file__))  # ai_tools -> tools
    projects_root = os.path.join(base_dir, "Projects")

    folder_name = slugify_name(project_name)
    slug_dir = os.path.join(projects_root, folder_name)
    raw_dir = os.path.join(projects_root, project_name)

    if os.path.isdir(slug_dir):
        return slug_dir
    if os.path.isdir(raw_dir):
        return raw_dir

    raise FileNotFoundError(
        "Project folder not found.\n"
        f"Tried:\n  {slug_dir}\n  {raw_dir}\n"
        "Make sure you've created it with 'new-project'."
    )


def _extract_latest_outline_section(outline_text: str) -> str:
    """
    Return the text from the last 'AUTO-GENERATED OUTLINE' header to the end.
    If not found, return the entire outline_text.
    """
    marker = "AUTO-GENERATED OUTLINE"
    last_index = outline_text.rfind(marker)
    if last_index == -1:
        return outline_text
    # Back up to the start of the line for cleaner parsing
    start_of_line = outline_text.rfind("\n", 0, last_index)
    if start_of_line == -1:
        start_of_line = 0
    return outline_text[start_of_line:]


def _parse_numbered_beats(section_text: str) -> list[tuple[int, str]]:
    """
    Parse beats like:
      1. First beat...
      2. Second beat...

    Multi-line beats are supported; any lines until the next 'N.' line
    are attached to the current beat.
    Returns a list of (beat_number, beat_text).
    """
    lines = section_text.splitlines()
    beats: list[tuple[int, str]] = []
    current_num: int | None = None
    current_lines: list[str] = []

    beat_header_re = re.compile(r"^\s*(\d+)\.\s+(.*)")

    for line in lines:
        m = beat_header_re.match(line)
        if m:
            # flush previous beat
            if current_num is not None and current_lines:
                beats.append((current_num, "\n".join(current_lines).strip()))

            current_num = int(m.group(1))
            current_lines = [m.group(2)]
        else:
            # continuation of current beat
            if current_num is not None:
                current_lines.append(line)

    # flush last beat
    if current_num is not None and current_lines:
        beats.append((current_num, "\n".join(current_lines).strip()))

    return beats

def run_beat_manager(args: argparse.Namespace) -> None:
    """
    Interactively curate beats from a project's outline.md into beats_final.md.

    - Reads the last AUTO-GENERATED OUTLINE section from outline.md
    - Lets you accept/reject/edit each beat
    - Writes a curated, numbered beat list to beats_final.md (or custom output)
    """
    project_name = args.project
    output_filename = args.output or "beats_final.md"

    try:
        project_dir = _get_project_dir(project_name)
    except FileNotFoundError as e:
        raise SystemExit(str(e))

    outline_path = os.path.join(project_dir, "outline.md")
    beats_path = os.path.join(project_dir, output_filename)

    # If user only wants to list current beats_final, do that and exit
    if args.list:
        if not os.path.exists(beats_path):
            print(f"No {output_filename} found for project '{project_name}'.")
            return
        with open(beats_path, "r", encoding="utf-8") as f:
            print(f.read())
        return

    if not os.path.exists(outline_path):
        raise SystemExit(f"outline.md not found for project: {project_dir}")

    with open(outline_path, "r", encoding="utf-8") as f:
        outline_text = f.read()

    latest_section = _extract_latest_outline_section(outline_text)
    beats = _parse_numbered_beats(latest_section)

    if not beats:
        raise SystemExit(
            "No numbered beats found in the latest outline section.\n"
            "Make sure your outline has lines like '1. First beat...'"
        )

    print(
        f"\n[Creator Assistant] Beat Manager for project '{project_name}'\n"
        f"Source: {outline_path}\n"
        f"Output: {beats_path}\n"
    )
    print("You will now review each beat.")
    print("Commands: [a]ccept (default), [r]eject, [e]dit, [q]uit\n")

    curated_beats: list[str] = []

    for idx, (num, text) in enumerate(beats, start=1):
        print("──────────────────────────────────────────")
        print(f"Beat {num} (#{idx} in this session):\n")
        print(text)
        print("\n[a]ccept / [r]eject / [e]dit / [q]uit > ", end="", flush=True)

        choice = input().strip().lower() or "a"

        if choice == "q":
            print("\nStopping early. Saving accepted beats so far...\n")
            break

        elif choice == "r":
            # Generate a replacement beat in place of the rejected one
            print("\n→ Generating replacement beat via OpenAI...\n")
            replacement_text = generate_replacement_beat(text, channel=args.channel)

            print("Replacement proposal:\n")
            print(replacement_text)
            print("\n[a]ccept / [e]dit / [s]kip > ", end="", flush=True)

            sub_choice = input().strip().lower() or "a"

            if sub_choice == "a":
                curated_beats.append(replacement_text.strip())
                print("→ Replacement accepted.\n")
            elif sub_choice == "e":
                print("\nEnter new text for this replacement beat.")
                print("Finish by entering a blank line on its own.\n")
                new_lines: list[str] = []
                while True:
                    line = input()
                    if line == "":
                        break
                    new_lines.append(line)
                new_text = "\n".join(new_lines).strip()
                if not new_text:
                    print("No new text entered; replacement skipped.\n")
                else:
                    curated_beats.append(new_text)
                    print("→ Replacement edited and accepted.\n")
            else:
                print("→ Replacement skipped; original beat rejected with no substitute.\n")

            continue  # move on to the next original beat

        elif choice == "e":
            print("\nEnter new text for this beat.")
            print("Finish by entering a blank line on its own.\n")
            new_lines: list[str] = []
            while True:
                line = input()
                if line == "":
                    break
                new_lines.append(line)
            new_text = "\n".join(new_lines).strip()
            if not new_text:
                print("No new text entered; skipping this beat.\n")
                continue
            curated_beats.append(new_text)
            print("→ Edited and accepted.\n")

        else:  # default accept
            curated_beats.append(text)
            print("→ Accepted.\n")


    if not curated_beats:
        print("No beats were accepted. Nothing written.")
        return

    # Write beats_final.md
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(beats_path, "w", encoding="utf-8") as f:
        f.write("# Final Beat List\n\n")
        f.write(f"_Project:_ **{project_name}**\n")
        f.write(f"_Generated:_ {timestamp}\n\n")
        f.write("---\n\n")
        for i, beat_text in enumerate(curated_beats, start=1):
            # Keep simple numbered format for Script Draft Builder
            f.write(f"{i}. {beat_text}\n\n")

    print(f"Curated {len(curated_beats)} beats.")
    print(f"Final beat list written to: {beats_path}")



# ----------BEAT REPLACEMENT TOOL ----------

def generate_replacement_beat(original_beat: str, channel: str = "shrouded") -> str:
    """
    Use the OpenAI API to generate an alternative beat that could replace the original one.

    - Keeps the same general story role/context.
    - Changes the specific event, evidence, or imagery.
    - Returns 2–5 sentences, no numbering.
    """
    if channel == "shrouded":
        system_msg = (
            "You are an expert documentary-horror story crafter for The Shrouded Ledger. "
            "You revise outline beats so they stay structurally consistent but use different "
            "events, evidence, or imagery. You do not describe emotions directly; you show "
            "observable behavior, documents, and anomalies."
        )
    else:  # aperture
        system_msg = (
            "You are an expert in image-driven liminal horror outlines for Aperture Black. "
            "You revise outline beats so they stay structurally consistent but use different "
            "visual environments and unsettling details."
        )

    user_prompt = f"""
You are revising ONE outline beat for a {channel}-style horror project.

ORIGINAL BEAT:
\"\"\"{original_beat}\"\"\"

TASK:
Write a different beat that could replace it in the same outline.

Requirements:
- Keep roughly the same structural role (scope, focus, where it comes in the story).
- Change the specifics of the event, evidence, or visual imagery.
- Write 2–5 sentences total.
- Do NOT number the beat or add labels; return only the beat text.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=400,
        temperature=0.8,
    )

    return response.choices[0].message.content.strip()


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

        # Ideas subcommand
    ideas_parser = subparsers.add_parser(
        "ideas",
        help="Generate multiple alternative story treatments from a single seed idea.",
    )
    ideas_parser.add_argument(
        "seed",
        nargs="+",
        help="Short description or premise (e.g., 'classified social experiment in a suburb').",
    )
    ideas_parser.add_argument(
        "--count",
        type=int,
        default=5,
        help="Number of different treatments to generate (default: 5).",
    )
    ideas_parser.add_argument(
        "--channel",
        choices=["shrouded", "aperture"],
        default="shrouded",
        help="Tone preset for ideas (default: shrouded).",
    )

    # Idea locker subcommand
    idea_locker_parser = subparsers.add_parser(
        "idea-locker",
        help="Save ideas output into a project's concepts.md 'Idea Locker' file",
)

    idea_locker_parser.add_argument(
        "--project",
        required=True,
        help="Project name (must match a folder under tools/Projects/)",
)

    idea_locker_parser.add_argument(
        "--source",
        help="Path to a text file containing ideas (if omitted, reads from stdin)",
)

    idea_locker_parser.add_argument(
        "--label",
        help="Optional label for this batch (e.g. 'Season 1 variants', 'Twin Flame Portal set')",
)

    idea_locker_parser.add_argument(
        "--favorite",
        action="store_true",
        help="Mark this entire batch as a favorite",
)

    idea_locker_parser.add_argument(
        "--list",
        action="store_true",
        help="Print the project's concepts.md instead of saving a new batch",
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

    # Fill-outline subcommand
    fill_outline_parser = subparsers.add_parser(
        "fill-outline",
        help="Generate an outline for an existing project and append it to its outline.md.",
    )
    fill_outline_parser.add_argument(
        "project",
        nargs="+",
        help="Name of the project (must match the name used with new-project).",
    )
    fill_outline_parser.add_argument(
        "--seed",
        nargs="+",
        required=True,
        help="Seed idea or summary for the episode/story.",
    )
    fill_outline_parser.add_argument(
        "--beats",
        type=int,
        default=10,
        help="Number of beats in the outline (default: 10).",
    )
    fill_outline_parser.add_argument(
        "--channel",
        choices=["shrouded", "aperture"],
        default="shrouded",
        help="Tone preset for outline (default: shrouded).",
    )

        # Fill-script subcommand
    fill_script_parser = subparsers.add_parser(
        "fill-script",
        help="Expand a beat and append it to a project's script.md.",
    )
    fill_script_parser.add_argument(
        "project",
        nargs="+",
        help="Name of the project (must match the name used with new-project).",
    )
    fill_script_parser.add_argument(
        "--beat",
        nargs="+",
        required=True,
        help="Outline beat or description to expand into narration.",
    )
    fill_script_parser.add_argument(
        "--channel",
        choices=["shrouded", "aperture"],
        default="shrouded",
        help="Tone preset for expansion (default: shrouded).",
    )
    fill_script_parser.add_argument(
        "--no-broll",
        action="store_true",
        help="Disable the CINEMATIC B-ROLL section in the appended segment.",
    )

         # Beat manager subcommand
    beat_manager_parser = subparsers.add_parser(
        "beat-manager",
        help="Curate beats from outline.md into a final beat list.",
    )
    beat_manager_parser.add_argument(
        "--project",
        required=True,
        help="Name of the project (same as used with new-project).",
    )
    beat_manager_parser.add_argument(
        "--output",
        help="Name of the output beats file (default: beats_final.md).",
    )
    beat_manager_parser.add_argument(
        "--list",
        action="store_true",
        help="Print the current final beats file instead of running interactive curation.",
    )
    beat_manager_parser.add_argument(
        "--channel",
        choices=["shrouded", "aperture"],
        default="shrouded",
        help="Tone preset used when generating replacement beats (default: shrouded).",
    )

    # Script draft builder subcommand
    script_draft_parser = subparsers.add_parser(
        "script-draft",
        help="Generate a full Draft 0 script from a project's final beats file.",
    )
    script_draft_parser.add_argument(
        "--project",
        required=True,
        help="Name of the project (same as used with new-project).",
    )
    script_draft_parser.add_argument(
        "--beats-file",
        help="Beats file to read (default: beats_final.md).",
    )
    script_draft_parser.add_argument(
        "--channel",
        choices=["shrouded", "aperture"],
        default="shrouded",
        help="Tone preset for expansion (default: shrouded).",
    )
    script_draft_parser.add_argument(
        "--no-broll",
        action="store_true",
        help="Disable the CINEMATIC B-ROLL sections in the generated script.",
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

    elif args.command == "ideas":
        seed_idea = " ".join(args.seed)
        count = args.count
        channel = args.channel

        print(
            f"\n[Creator Assistant] Generating {count} alternative story treatments "
            f"(channel='{channel}')...\n"
        )

        ideas_text = generate_ideas_from_assistant(
            seed_idea=seed_idea,
            count=count,
            channel=channel,
        )

        print("=== STORY TREATMENTS ===\n")
        print(ideas_text)    

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

    elif args.command == "idea-locker":
        run_idea_locker(args)
    
    
    elif args.command == "fill-outline":
        project_name = " ".join(args.project)
        seed_idea = " ".join(args.seed)
        beats = args.beats
        channel = args.channel

        print(
            f"\n[Creator Assistant] Filling outline for project '{project_name}' "
            f"({channel}, {beats} beats)...\n"
        )

        try:
            outline_path = fill_project_outline_from_assistant(
                project_name=project_name,
                seed_idea=seed_idea,
                beats=beats,
                channel=channel,
            )
            print(f"Outline appended to: {outline_path}")
        except FileNotFoundError as e:
            print(f"Error: {e}")

    elif args.command == "fill-script":
        project_name = " ".join(args.project)
        beat_text = " ".join(args.beat)
        channel = args.channel
        include_broll = not args.no_broll

        print(
            f"\n[Creator Assistant] Expanding beat into script for project "
            f"'{project_name}' (channel='{channel}', broll={'on' if include_broll else 'off'})...\n"
        )

        try:
            script_path = append_expanded_beat_to_script(
                project_name=project_name,
                beat_text=beat_text,
                channel=channel,
                include_broll=include_broll,
            )
            print(f"Segment appended to: {script_path}")
        except FileNotFoundError as e:
            print(f"Error: {e}")

    elif args.command == "beat-manager":
        run_beat_manager(args)

    elif args.command == "script-draft":
        run_script_draft_builder(args)

if __name__ == "__main__":
    main()
