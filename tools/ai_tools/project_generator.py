import os
import textwrap

def slugify_name(name: str) -> str:
    """
    Convert a project name into a safe folder name by stripping extra
    whitespace and replacing path separators.
    """

    # Simple slug: strip spaces at ends, replace path separators and double spaces
    slug = name.strip().replace("/", "-").replace("\\", "-")
    return slug

def ensure_projects_root() -> str:
    """
    Ensure that the top-level 'Projects' directory exists at the same level
    as the Week 1 folder, and return its path.
    """

    # Projects folder is at the Week 1 level (parent of ai_tools)
    base_dir = os.path.dirname(os.path.dirname(__file__))
    projects_root = os.path.join(base_dir, "Projects")
    os.makedirs(projects_root, exist_ok=True)
    return projects_root

def shrouded_template(project_name: str) -> dict:
    """
    Build a dictionary of filename -> file contents for a Shrouded Ledger project.

    The contents are Markdown templates with TODO sections.
    """

    title = project_name.strip()
    outline = f"""# Shrouded Ledger Episode Outline – {title}

## Logline
_TODO: One or two sentences capturing the core anomaly, its impact on the community, and the investigative angle._

## Beats
1. Opening macro view – how the audience first encounters the anomaly.
2. Early history/origins – how this started or entered public awareness.
3. Micro-case 1 – a specific person, location, or facility.
4. Micro-case 2 – another angle showing the anomaly's reach.
5. Micro-case 3 (optional) – escalation or contradiction.
6. Institutional response – attempts to suppress, contain, monetize, or deny.
7. Evidence of cover-up – edits to records, missing people, altered reports.
8. Current state of the anomaly – how it now lives in infrastructure or memory.
9. Consequences – personal, social, geopolitical, psychological.
10. Closing image – a specific, chilling image that implies the story isn't over.

## Notes
- Maintain documentary, forensic tone.
- Show behavior and evidence; do not label emotions directly.
"""

    script = f"""# Shrouded Ledger Narration Draft – {title}

## Segment 1 – Opening
_TODO: 3–6 paragraphs introducing the anomaly in a calm, documentary voice._

## Segment 2 – Origins & Early Incidents
_TODO: Describe key early events, reports, or unexplained patterns._

## Segment 3 – Micro-Cases
_TODO: Detail specific individuals or locations affected by the anomaly._

## Segment 4 – Institutional Response
_TODO: Show how organizations responded, covered up, or misinterpreted events._

## Segment 5 – Closing Segment
_TODO: Summarize current status and end on a quiet, unnerving realization._
"""

    broll = """# Cinematic B-Roll Notes – Shrouded Ledger

Use these prompts to refine or replace AI-generated B-roll:

## Environments & Architecture
- Hallways, corridors, rooms, facilities, suburbs, or offices involved.
- Details: lighting, damage, emptiness, signage, equipment.

## Human Presence
- Witnesses, staff, residents, investigators.
- Shots that imply emotional state through posture, distance, or behavior.

## Objects & Devices
- Specific physical items central to the story (devices, files, artifacts).
- Anomalous behaviors that can be shown visually.

## Archival Materials
- Reports, memos, transcripts, CCTV stills, medical records.

## Symbolic / Surreal-but-Plausible Shots
- Repeating patterns, reflections, silhouettes, long static shots.
"""

    metadata = f"""# YouTube Metadata – Shrouded Ledger – {title}

## Working Title Ideas
- TODO: Brainstorm 5–10 title variations.

## Description Draft
_TODO: 2–4 paragraph description, starting with a hook, then context, then stakes._

## Keywords / Tags
_TODO: List specific tags (places, themes, objects, institutions)._

## Hashtags
_TODO: List 5–10 channel-appropriate hashtags._
"""

    notes = """# Development Notes

Use this file to jot down:

- Questions that need answering.
- Threads that emerged during drafting.
- Ideas for future episodes tied to this one.
- Real-world references or inspirations.
"""
    return {
        "outline.md": textwrap.dedent(outline),
        "script.md": textwrap.dedent(script),
        "broll_notes.md": textwrap.dedent(broll),
        "metadata.md": textwrap.dedent(metadata),
        "notes.md": textwrap.dedent(notes),
    }

def aperture_template(project_name: str) -> dict: 
    """
    Build a dictionary of filename -> file contents for an Aperture Black project.

    The contents are Markdown templates with TODO sections.
    """
    
    title = project_name.strip()
    outline = f"""# Aperture Black – Shot Outline – {title}

## Concept Summary
_TODO: One short paragraph explaining the core visual idea and mood._

## Shot Phases
1. Establishing phase – anchor location or motif.
2. Descent/drift phase – images become stranger, more focused on anomaly.
3. Deep phase – most intense or uncanny imagery.
4. Return/echo phase – callbacks, altered repeats, or lingering images.

## Notes on Style
- Think in terms of photos or short clips, not plot.
- Keep narration minimal; let visuals carry the unease.
"""

    images = """# Image Concepts – Aperture Black

For each shot, describe:

- Location / environment
- Lighting and palette
- Camera angle and distance
- Key unsettling detail(s)
- Optional: texture (film grain, CRT scanlines, underwater haze, etc.)

Use this file as a planning space before generating images.
"""

    audio = """# Music & Ambience Notes – Aperture Black

Ideas for:

- Ambient drones
- Textural sounds (machinery, distant voices, water, wind, static)
- Rhythmic elements, if any
- Moments of silence

Note specific timestamps or phases where audio should change.
"""

    edit = """# Editing & Structure Notes – Aperture Black

Use this to plan:

- Crossfades, hard cuts, zooms, and pans
- Transitions between phases (establishing → deep → echo)
- Text overlays, if any
- Where narration enters or exits (if used)
"""
    return {
        "outline.md": textwrap.dedent(outline),
        "image_ideas.md": textwrap.dedent(images),
        "audio_notes.md": textwrap.dedent(audio),
        "edit_notes.md": textwrap.dedent(edit),
    }

def novel_template(project_name: str) -> dict:  
    """
    Build a dictionary of filename -> file contents for a Novel project.

    The contents are Markdown templates with TODO sections.
    """
    title = project_name.strip()
    outline = f"""# Story / Novel Outline – {title}

## Core Premise
_TODO: 1–3 sentences capturing the central conflict and hook._

## Act / Part Structure
- Act I / Part 1 – Setup, normal world, inciting incident.
- Act II / Part 2 – Complications, discoveries, escalating stakes.
- Act III / Part 3 – Climax, resolution, and aftermath.

## Major Turning Points
- Inciting Incident
- First Major Turn
- Midpoint Shift
- Darkest Moment
- Climax
- Final Image
"""

    characters = """# Characters

For each important character, note:

- Name:
- Role in story:
- External goal:
- Internal need:
- Secrets they keep:
- How the horror or central conflict changes them:
"""

    world = """# Setting & Worldbuilding

- Locations that matter and why.
- Institutions, communities, or social dynamics involved.
- Rules of the anomaly, magic, technology, or horror element.
- History, rumors, and local myths.
"""

    chapters = """# Chapter / Scene Sketches

Use this section to rough out scenes:

- Chapter 1:
  - What changes for the protagonist?
  - What question is raised for the reader?

- Chapter 2:
  - New complication or discovery.

(Continue sketching as needed.)
"""

    themes = """# Themes & Motifs

- Core questions the story is asking.
- Recurring images or symbols.
- Emotional tones to preserve.
"""
    return {
        "outline.md": textwrap.dedent(outline),
        "characters.md": textwrap.dedent(characters),
        "worldbuilding.md": textwrap.dedent(world),
        "chapters.md": textwrap.dedent(chapters),
        "themes.md": textwrap.dedent(themes),
    }

def create_project(project_name: str, project_type: str = "shrouded") -> str:
    """
    Create a new project folder under Projects/ with starter markdown files.

    Returns the path to the created project directory.
    """
    projects_root = ensure_projects_root()
    folder_name = slugify_name(project_name)
    project_dir = os.path.join(projects_root, folder_name)

    # Avoid overwriting existing work
    os.makedirs(project_dir, exist_ok=True)

    if project_type == "shrouded":
        files = shrouded_template(project_name)
    elif project_type == "aperture":
        files = aperture_template(project_name)
    elif project_type == "novel":
        files = novel_template(project_name)
    else:
        raise ValueError(f"Unknown project type: {project_type}")

    # Common subfolders
    assets_dir = os.path.join(project_dir, "assets")
    research_dir = os.path.join(project_dir, "research")
    os.makedirs(assets_dir, exist_ok=True)
    os.makedirs(research_dir, exist_ok=True)

    for filename, content in files.items():
        file_path = os.path.join(project_dir, filename)
        # Only create file if it doesn't already exist (so reruns don't wipe edits)
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

    return project_dir

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate a new creative project folder with starter templates."
    )
    parser.add_argument(
        "name",
        nargs="+",
        help="Project name (used for folder and file headers).",
    )
    parser.add_argument(
        "--type",
        choices=["shrouded", "aperture", "novel"],
        default="shrouded",
        help="Type of project template to create (default: shrouded).",
    )

    args = parser.parse_args()
    project_name = " ".join(args.name)
    project_type = args.type

    path = create_project(project_name, project_type)
    print(f"Created {project_type} project at: {path}")
