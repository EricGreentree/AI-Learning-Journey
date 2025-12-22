import os
import sys
import argparse
import re

from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env in the Week 1 folder
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("ERROR: OPENAI_API_KEY not found in .env")
    sys.exit(1)

client = OpenAI(api_key=api_key)

def call_llm(
    *,
    system: str,
    user: str,
    model: str = "gpt-4o-mini",
    max_tokens: int = 3500,
    temperature: float = 0.4,
) -> str:
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return (resp.choices[0].message.content or "").strip()


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

# ---------- TEMP. CONTENT CHECK ----------

def _looks_like_refusal(text: str) -> bool:
    t = (text or "").strip().lower()
    needles = [
        "i'm sorry", "i am sorry",
        "can't assist", "cannot assist",
        "can't help with that", "cannot help with that",
        "can't comply", "cannot comply",
        "can't complete", "cannot complete",
        "unable to help", "not able to help",
        "policy",
    ]
    return any(n in t for n in needles)


def debug_find_refusal_chunk(script_text: str, mode: str = "tighten", chunk_chars: int = 6000) -> None:
    chunks = [script_text[i:i+chunk_chars] for i in range(0, len(script_text), chunk_chars)]
    for idx, ch in enumerate(chunks, start=1):
        out = polish_script_text(ch, mode=mode)
        if _looks_like_refusal(out):
            print(f"[REFUSAL] chunk {idx}/{len(chunks)} triggered refusal.")
            print(ch[:500])
            return
        else:
            print(f"[OK] chunk {idx}/{len(chunks)} polished.")
    print("[OK] No chunk refused (full script refusal may be length/interaction effect).")


# ---------- SCRIPT POLISHER ----------

SCRIPT_POLISH_MODES = { 
    "neutral-tighten": {
    "label": "NEUTRAL_TIGHTEN",
    "notes": "Copyedit for clarity + specificity + concision. Preserve structure. Do not intensify menace.",
    },

    "tighten": {
        "label": "TIGHTEN",
        "notes": "Reduce fluff, tighten phrasing, preserve structure, increase specificity and menace.",
    },
    "menace": {
        "label": "INCREASE_MENACE",
        "notes": "Increase menace and unease via concrete details and implications; no melodrama; preserve structure.",
    },
    "specific": {
        "label": "MORE_SPECIFIC",
        "notes": "Replace vague language with concrete, observable details; preserve structure.",
    },
}

def polish_script_text(script_text: str, mode: str = "tighten", model: str = "gpt-4o-mini") -> str:
    mode = (mode or "tighten").strip().lower()
    if mode not in SCRIPT_POLISH_MODES:
        valid = ", ".join(sorted(SCRIPT_POLISH_MODES.keys()))
        raise ValueError(f"Unknown polish mode: {mode}. Valid: {valid}")

    constraints = [
        "Do NOT add emotion labeling (no 'he feels', 'she is terrified', 'he is scared', etc.).",
        "Emphasize events, artifacts, documents, observable behavior, and concrete actions.",
        ("Increase menace and specificity through implication + detail, not melodrama."
    if mode != "neutral-tighten"
    else "Increase specificity through concrete detail; do not intensify threat, menace, or violence.")
,
        "Reduce vague poetic filler and generic phrasing.",
        "Preserve the existing structure and ordering unless a sentence is clearly redundant.",
        "Keep the same POV and documentary narration style.",
        "Do not add sections that are not present; do not remove major beats.",
        "Keep violence non-graphic; do not linger on harm to minors.",
    ]

    mode_notes = SCRIPT_POLISH_MODES[mode]["notes"]

    if mode == "neutral-tighten":
        system = (
        "You are a professional copy editor. "
        "Rewrite for clarity, specificity, and concision while preserving structure. "
        "This is fictional narration. Do not provide instructions for wrongdoing."
    )
    else:
        system = (
        "You are a professional script polisher for FICTIONAL documentary-style horror narration. "
        "You are not assisting wrongdoing. Do not provide instructions for violence or illegal acts. "
        "If the script contains violence, keep it non-graphic and described at a high level. "
        "If the draft references minors/children, do NOT intensify those parts—generalize or remove those references "
        "while preserving narrative function."
    )




    user = f"""
TASK:
Polish the following Draft 0 script with the mode: {mode.upper()}.

MODE GOAL:
{mode_notes}

HARD CONSTRAINTS:
- """ + "\n- ".join(constraints) + """

OUTPUT RULES:
- Return ONLY the polished script text.
- Do not include headings, analysis, bullet points, or commentary.
- Keep paragraph breaks logical and consistent with the original.

DRAFT 0 SCRIPT:
{script_text}
""".strip()


    polished = call_llm(
    system=system,
    user=user,
    model="gpt-4o-mini",
    max_tokens=3500,
    temperature=0.4,
)

    return polished.strip()

def polish_script_notes(script_text: str, mode: str = "tighten", model: str = "gpt-4o-mini") -> str:
    system = (
        "You are a professional copy editor. The user is writing FICTIONAL narration.\n"
        "Do NOT rewrite the entire passage.\n"
        "Instead, provide edit notes and a few optional sentence-level replacements.\n"
        "Do not provide instructions for wrongdoing or violence."
    )

    user = f"""
TASK:
Provide production-focused edit notes for the text below.

MODE: {mode.upper()}

RULES:
- Do NOT produce a full rewritten passage.
- Output in this exact structure:

## Issues to fix (bullet list)
## Specificity upgrades (bullet list: vague phrase -> more specific alternative)
## Emotion-labeling removals (bullet list; if none say 'None')
## Optional sentence swaps (3–6 items)
Each swap should include:
- Original: "..."
- Replacement: "..."

TEXT:
{script_text}
""".strip()

    return call_llm(system=system, user=user, model=model, max_tokens=1200, temperature=0.2).strip()



def _split_script_into_beats(script_text: str) -> list[tuple[str, str]]:
    """
    Returns list of (heading, body) where heading is like '## Beat 1'
    and body is everything until the next beat heading.
    If no beats are found, returns one chunk with empty heading.
    """
    pattern = re.compile(r"(^## Beat\s+\d+\s*$)", re.MULTILINE)
    parts = pattern.split(script_text)

    # If no split happened, return whole script as one chunk
    if len(parts) == 1:
        return [("", script_text)]

    chunks: list[tuple[str, str]] = []
    preamble = parts[0]
    if preamble.strip():
        chunks.append(("", preamble))

    # parts looks like: [preamble, heading1, body1, heading2, body2, ...]
    for i in range(1, len(parts), 2):
        heading = parts[i].strip()
        body = parts[i + 1]
        chunks.append((heading, body))
    return chunks


def run_script_polish(
    project_dir: Path,
    mode: str,
    output: str | None,
    append: bool,
    model: str,
    output_format: str = "rewrite",   # "rewrite" or "notes"
    narration_only: bool = True,      # <<< NEW: only polish narration sections
    debug: bool = False,              # <<< OPTIONAL: print chunk previews
) -> Path:
    """
    Reads script.md, generates either:
      - rewritten narration (rewrite mode), or
      - narration polish notes (notes mode),
    and writes an artifact in the project folder.

    narration_only=True:
      - Extracts only the ### NARRATION: section (or ### 1) NARRATION:) from each beat.
      - Leaves Source beat / B-roll / TODO scaffolding untouched.
    """

    def extract_narration_only(text: str) -> str | None:
        """
        Extract only narration body from a chunk. Returns None if not found.
        Matches headers like:
          ### NARRATION:
          ### 1) NARRATION:
        Stops at the next ### header or end of chunk.
        """
        pat = re.compile(
            r"(?:^|\n)###\s*(?:\d+\)\s*)?NARRATION:\s*(.*?)(?=\n###|\Z)",
            re.IGNORECASE | re.DOTALL,
        )
        m = pat.search(text)
        if not m:
            return None
        narration = (m.group(1) or "").strip()
        return narration if narration else None

    script_path = project_dir / "script.md"
    if not script_path.exists():
        raise FileNotFoundError(f"Missing script.md at: {script_path}")

    draft0 = script_path.read_text(encoding="utf-8").strip()
    if not draft0:
        raise ValueError(f"script.md is empty: {script_path}")

    chunks = _split_script_into_beats(draft0)

    polished_parts: list[str] = []
    refusal_hits: list[str] = []

    for heading, body in chunks:
        original_chunk = (heading + "\n\n" + body).strip() if heading else body.strip()
        if not original_chunk:
            continue

        if debug:
            print("=" * 60)
            print("[DEBUG] Processing:", heading or "PREAMBLE")
            print("[DEBUG] Chunk length:", len(original_chunk))
            print("[DEBUG] Chunk preview:", repr(original_chunk[:220]))
            print("=" * 60)

        # If we only want narration, extract it; otherwise operate on full chunk.
        target_text = original_chunk
        narration_text = None
        if narration_only:
            narration_text = extract_narration_only(original_chunk)
            if not narration_text:
                # No narration section found — keep chunk unchanged.
                polished_parts.append(original_chunk)
                continue
            target_text = narration_text

        # Choose output behavior
        if output_format == "notes":
            out = polish_script_notes(target_text, mode=mode, model=model)
        else:
            out = polish_script_text(target_text, mode=mode, model=model)

        # Refusal handling (keep original content, log which section refused)
        if _looks_like_refusal(out):
            label = heading or "[PREAMBLE/NO BEAT HEADING]"
            refusal_hits.append(label)

            # In narration_only mode, we keep the whole original chunk untouched
            polished_parts.append(original_chunk)
            continue

        # Stitch output back into the chunk (narration-only handling)
        if narration_only:
            if output_format == "notes":
                # Keep original chunk, append a notes block under it.
                notes_block = (
                    "\n\n### NARRATION POLISH NOTES (AUTO)\n\n"
                    + out.strip()
                    + "\n"
                )
                polished_parts.append(original_chunk + notes_block)
            else:
                # Replace only the narration body in the original chunk.
                # We preserve the "### NARRATION:" header and surrounding structure.
                def _replace(match: re.Match) -> str:
                    return match.group(0).split(":", 1)[0] + ":\n\n" + out.strip() + "\n"

                narration_pat = re.compile(
                    r"(###\s*(?:\d+\)\s*)?NARRATION:)\s*(.*?)(?=\n###|\Z)",
                    re.IGNORECASE | re.DOTALL,
                )
                replaced = narration_pat.sub(lambda m: m.group(1) + "\n\n" + out.strip() + "\n", original_chunk, count=1)
                polished_parts.append(replaced.strip())
        else:
            # Not narration_only: output replaces the whole chunk
            polished_parts.append(out.strip())

    polished = "\n\n".join(polished_parts).strip()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = (
        f"\n\n---\n"
        f"# AUTO-GENERATED POLISH PASS\n"
        f"- Mode: {mode}\n"
        f"- Format: {output_format}\n"
        f"- Narration-only: {narration_only}\n"
        f"- Model: {model}\n"
        f"- Generated: {timestamp}\n"
        f"---\n\n"
    )

    # If anything refused, write a debug file next to the output
    if refusal_hits:
        debug_path = project_dir / "script_polish_refusals.txt"
        debug_path.write_text(
            "Refusal detected in these sections:\n"
            + "\n".join(f"- {h}" for h in refusal_hits)
            + "\n",
            encoding="utf-8",
        )
        print(f"[WARN] Refusals detected. See: {debug_path}")

    # Choose default output filename by format
    default_out = "script_polish_notes.md" if output_format == "notes" else "script_polished.md"

    if append:
        script_path.write_text(draft0 + header + polished + "\n", encoding="utf-8")
        return script_path

    out_name = output.strip() if output else default_out
    out_path = project_dir / out_name
    out_path.write_text(header.strip() + "\n\n" + polished + "\n", encoding="utf-8")
    return out_path





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


# ---------- NARRATION FINALIZER ----------

def extract_all_narration(script_text: str) -> list[tuple[str, str]]:
    """
    Returns a list of (beat_heading, narration_text).
    """
    beats = _split_script_into_beats(script_text)
    results = []

    narration_pat = re.compile(
        r"###\s*(?:\d+\)\s*)?NARRATION:\s*(.*?)(?=\n###|\Z)",
        re.IGNORECASE | re.DOTALL,
    )

    for heading, body in beats:
        m = narration_pat.search(body)
        if not m:
            continue
        narration = m.group(1).strip()
        if narration:
            results.append((heading or "PREAMBLE", narration))

    return results

def extract_sentence_swaps(notes_text: str) -> list[tuple[str, str]]:
    swaps = []
    pat = re.compile(
        r"- Original:\s*\"(.*?)\"\s*\n\s*- Replacement:\s*\"(.*?)\"",
        re.DOTALL,
    )

    for m in pat.finditer(notes_text):
        orig = m.group(1).strip()
        repl = m.group(2).strip()
        if orig and repl:
            swaps.append((orig, repl))

    return swaps

def finalize_narration(
    script_text: str,
    notes_text: str,
    apply_all: bool = True,
) -> str:
    narrations = extract_all_narration(script_text)
    swaps = extract_sentence_swaps(notes_text)

    finalized_blocks = []

    for heading, narration in narrations:
        updated = narration
        for orig, repl in swaps:
            if orig in updated:
                updated = updated.replace(orig, repl)

        block = f"{heading}\n\n{updated.strip()}"
        finalized_blocks.append(block)

    return "\n\n---\n\n".join(finalized_blocks)

def run_narration_finalize(project_dir: Path, apply: str, dry_run: bool = False) -> Path:
    script_path = project_dir / "script.md"
    notes_path = project_dir / "script_polish_notes.md"

    if not script_path.exists():
        raise FileNotFoundError("Missing script.md")
    if not notes_path.exists():
        raise FileNotFoundError("Missing script_polish_notes.md")

    script_text = script_path.read_text(encoding="utf-8")
    notes_text = notes_path.read_text(encoding="utf-8")

    finalized = finalize_narration(script_text, notes_text, apply_all=True)

    header = (
        "# FINALIZED NARRATION (VOICEOVER READY)\n"
        "# Auto-generated from script.md + script_polish_notes.md\n\n"
    )

    if dry_run:
        print(header + finalized)
        return project_dir

    out_path = project_dir / "script_narration_final.md"
    out_path.write_text(header + finalized + "\n", encoding="utf-8")
    return out_path




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


# ---------- PUBLISH PACK TOOL ----------

def build_publish_pack_prompt(
    narration_text: str,
    *,
    channel: str = "shrouded",
    title_count: int = 10,
    description_count: int = 3,
    thumbnail_count: int = 8,
) -> str:
    """Build a prompt that turns finalized narration into an upload-ready publish pack."""
    # Keep narration bounded; we want metadata, not a rewrite.
    narration_text = narration_text.strip()

    style_hint = (
        "Documentary-horror tone: clinical, investigative, ominous, restrained."
        if channel == "shrouded"
        else "Atmospheric sci-fi/liminal tone: evocative, mysterious, minimal, image-forward."
    )

    return f"""You are given FINALIZED narration for a YouTube video.

GOAL
Create an upload-ready PUBLISH PACK derived ONLY from the narration. Do not rewrite the narration.

STYLE
{style_hint}

HARD RULES
- Do NOT invent plot points, locations, organizations, dates, or claims that are not clearly supported by the narration.
- You MAY generalize into SEO-friendly phrasing (e.g., "classified", "leaked", "archival"), but keep it plausible.
- No spoilers that reveal the ending if the narration is structured as a reveal; keep descriptions hook-forward.
- Output must be in markdown and follow the exact template below.

OUTPUT TEMPLATE (markdown)
# Publish Pack

## Titles ({title_count})
1. ...
2. ...
...

## Descriptions ({description_count})
### Description 1
<150–220 words. Hook in first 2 lines. 1 short paragraph break. End with a single-line call-to-action. No bullet lists.>

### Description 2
...

### Description 3
...

## Tags (comma-separated, <= 500 characters)
tag1, tag2, tag3, ...

## Hashtags (10–15)
#tag
#tag
...

## Thumbnail Concepts ({thumbnail_count})
For each concept, provide:
- Concept: <1 sentence>
- Overlay Text: <2–5 words>
- Visual Notes: <short notes on composition, focal point, contrast, mood>

NARRATION (source)
""" + narration_text + """"""


def generate_publish_pack_from_narration(
    narration_text: str,
    *,
    channel: str = "shrouded",
    model: str = "gpt-4o-mini",
    title_count: int = 10,
    description_count: int = 3,
    thumbnail_count: int = 8,
) -> str:
    """Generate a full publish pack from finalized narration text."""
    system = (
        "You are an expert YouTube packaging strategist. "
        "You create titles, descriptions, tags, hashtags, and thumbnail concepts "
        "that match the source narration and improve click-through and search discovery."
    )
    user = build_publish_pack_prompt(
        narration_text,
        channel=channel,
        title_count=title_count,
        description_count=description_count,
        thumbnail_count=thumbnail_count,
    )
    return call_llm(
        system=system,
        user=user,
        model=model,
        max_tokens=1600,
        temperature=0.6,
    )


def run_publish_pack(
    *,
    project_dir: Path,
    script_filename: str = "script_narration_final.md",
    output_filename: str = "publish_pack.md",
    channel: str = "shrouded",
    model: str = "gpt-4o-mini",
    title_count: int = 10,
    description_count: int = 3,
    thumbnail_count: int = 8,
) -> Path:
    """Read finalized narration and write publish_pack.md to the project folder."""
    in_path = project_dir / script_filename
    if not in_path.exists():
        raise FileNotFoundError(
            f"Final narration not found: {in_path}\n"
            "Run 'narration-finalize' first (or pass --script to point at a different file)."
        )

    narration_text = in_path.read_text(encoding="utf-8")

    pack_md = generate_publish_pack_from_narration(
        narration_text,
        channel=channel,
        model=model,
        title_count=title_count,
        description_count=description_count,
        thumbnail_count=thumbnail_count,
    )

    out_path = project_dir / output_filename
    out_path.write_text(pack_md.strip() + "\n", encoding="utf-8")
    return out_path

# ---------- OUTLINE FILL ----------

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

       # Script Polish subcommand
    polish_p = subparsers.add_parser(
    "script-polish",
    help="Polish Draft 0 in script.md into a production-ready pass (no emotion labeling)."
)

    polish_p.add_argument("--project", required=True, help="Project folder name inside tools/Projects/")
    polish_p.add_argument(
    "--mode",
    default="tighten",
    choices=sorted(SCRIPT_POLISH_MODES.keys()),
    help="Polish mode (default: tighten)"
)
    polish_p.add_argument(
    "--model",
    default="gpt-4o-mini",
    help="Model to use for polishing (default: gpt-4o-mini). Try gpt-4o or gpt-4.1-mini if refusals persist."
)

    polish_p.add_argument(
    "--smoke-test",
    action="store_true",
    help="Run a tiny rewrite test to verify the model can do basic copyediting before polishing."
)

    polish_p.add_argument(
    "--output",
    default=None,
    help="Output filename written in the project folder (default: script_polished.md)"
)

    polish_p.add_argument(
    "--append",
    action="store_true",
    help="Append the polished pass to script.md instead of writing a separate file."
)
    polish_p.add_argument(
    "--format",
    default="rewrite",
    choices=["rewrite", "notes"],
    help="rewrite = produce rewritten text, notes = produce edit notes + sentence swaps (more reliable)."
)

       # Finalize Narration subcommand
    final_p = subparsers.add_parser(
    "narration-finalize",
    help="Apply narration polish notes to produce a VO-ready narration script."
)

    final_p.add_argument("--project", required=True)
    final_p.add_argument("--apply", choices=["all"], default="all")
    final_p.add_argument("--dry-run", action="store_true")


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

    # Publish pack subcommand
    publish_p = subparsers.add_parser(
        "publish-pack",
        help="Generate an upload-ready publish_pack.md from script_narration_final.md (titles, descriptions, tags, hashtags, thumbnails).",
    )
    publish_p.add_argument("--project", required=True, help="Project folder name inside tools/Projects/")
    publish_p.add_argument(
        "--script",
        default="script_narration_final.md",
        help="Input narration file in the project folder (default: script_narration_final.md).",
    )
    publish_p.add_argument(
        "--output",
        default="publish_pack.md",
        help="Output filename to write in the project folder (default: publish_pack.md).",
    )
    publish_p.add_argument(
        "--channel",
        choices=["shrouded", "aperture"],
        default="shrouded",
        help="Tone preset (default: shrouded).",
    )
    publish_p.add_argument(
        "--model",
        default="gpt-4o-mini",
        help="Model to use (default: gpt-4o-mini).",
    )
    publish_p.add_argument(
        "--title-count",
        type=int,
        default=10,
        help="Number of title options (default: 10).",
    )
    publish_p.add_argument(
        "--description-count",
        type=int,
        default=3,
        help="Number of descriptions (default: 3).",
    )
    publish_p.add_argument(
        "--thumbnail-count",
        type=int,
        default=8,
        help="Number of thumbnail concept options (default: 8).",
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

    elif args.command == "script-polish":
        project_dir = Path(_get_project_dir(args.project))

        if getattr(args, "smoke_test", False):
            test_system = "You are a professional copy editor. Rewrite for clarity and concision."
            test_user = "Rewrite this sentence more clearly: The folder was empty."
            test_out = call_llm(system=test_system, user=test_user, model=args.model, max_tokens=200, temperature=0.2)
            print("[SMOKE TEST OUTPUT]")
            print(test_out)
            print("----")

        out_path = run_script_polish(
            project_dir=project_dir,
            mode=args.mode,
            output=args.output,
            append=args.append,
            model=args.model,
            output_format=args.format
)

        print(f"[OK] Script polish complete: {out_path}")

    elif args.command == "narration-finalize":
        project_dir = Path(_get_project_dir(args.project))
        out_path = run_narration_finalize(
            project_dir=project_dir,
            apply=args.apply,
            dry_run=args.dry_run,
    )
        print(f"[OK] Narration finalized: {out_path}")
        


    elif args.command == "thumbnail":
        seed_idea = " ".join(args.seed)
        channel = args.channel

        print(f"\n[Creator Assistant] Generating THUMBNAIL CONCEPTS (channel='{channel}')...\n")
        thumbs = generate_thumbnails_from_assistant(seed_idea, channel=channel)
        print("=== THUMBNAIL CONCEPTS ===\n")
        print(thumbs)

    elif args.command == "publish-pack":
        project_dir = Path(_get_project_dir(args.project))
        print(
            f"\n[Creator Assistant] Generating PUBLISH PACK "
            f"(project='{args.project}', channel='{args.channel}', model='{args.model}')...\n"
        )
        out_path = run_publish_pack(
            project_dir=project_dir,
            script_filename=args.script,
            output_filename=args.output,
            channel=args.channel,
            model=args.model,
            title_count=args.title_count,
            description_count=args.description_count,
            thumbnail_count=args.thumbnail_count,
        )
        print(f"[OK] Publish pack written: {out_path}")


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
