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


def build_prompt(beat_text: str, channel: str, include_broll: bool = True) -> str:
    """
    Build a prompt that expands a beat into a 2–4 minute narrated
    Shrouded Ledger-style documentary segment, optionally with B-roll.
    """

    if channel == "shrouded":
        base_style = """
You are writing in the voice of *The Shrouded Ledger* — a documentary-style horror channel.

VOICE:
- Clinical, investigative, documentary-sharp.
- Emotionally restrained; horror emerges from logistics, systems, and implications.
- Assume an intelligent audience; do not over-explain.

SHOW, DON'T TELL (IMPORTANT):
- Do NOT state a character's internal feelings directly (avoid phrases like "he felt scared," "she was anxious," "they were terrified").
- Instead, describe observable behavior, physical reactions, environmental changes, or brief dialogue that imply the emotion.
- Let the viewer infer how people feel from what they do, what changes around them, and what is left unsaid.


STRUCTURE:
- This segment should feel like part of a larger episode.
- Use a calm, confident narrator voice.
"""

        if include_broll:
            broll_block = """
B-ROLL MODE (ENABLED):

You are also generating CINEMATIC B-ROLL for The Shrouded Ledger. The imagery must feel investigative,
atmospheric, and grounded in plausible reality—even when symbolic or surreal.

B-ROLL SHOULD INCORPORATE HUMANS, BUT WITH RESTRAINT:

HUMAN PRESENCE (GUIDELINES):
- People appear as witnesses, staff, residents, workers, investigators or protagonists.
- Do not use character names. Use descriptions like “middle-aged woman,” “maintenance worker,”
  “paramedic,” “young office clerk,” etc.
- Human shots may be observational (captured from a distance), symbolic (hands, silhouettes),
  neutral (walking, waiting), or archival (ID photos, CCTV stills).
- Often partially obscured, out of focus, seen from behind, or faceless in shadows.
- Humans should feel small compared to the system they inhabit.

CATEGORIES OF B-ROLL:
1. ENVIRONMENTAL & ARCHITECTURAL
   - dim corridors, abandoned floors, unmarked utility doors
   - flickering fluorescents, empty reception desks, silent waiting rooms

2. HUMAN PRESENCE (SUBTLE & DOCUMENTARY-REAL)
   - someone sitting alone in a break room, staring at a malfunctioning device
   - a lone figure in a long hallway, unaware they are observed
   - a teacher at a whiteboard, but the class is oddly still

3. OBJECTS & CONSUMER TECH (ANOMALOUS)
   - close-ups of devices displaying subtle irregularities
   - smart panels glowing softly in empty rooms
   - discarded AR glasses on a desk

4. ARCHIVAL & DOCUMENTARY ARTIFACTS
   - blurred ID photos, timestamp anomalies, redacted case files
   - handwritten notes, intake forms, leaked internal memos

5. ATMOSPHERIC HUMAN-ABSENCE
   - abandoned personal belongings mid-activity
   - chairs pulled from desks, beds still indented
   - coffee cups beside glowing monitors in an empty office

6. SYMBOLIC / SURREAL BUT PLAUSIBLE
   - repeating patterns suggesting unseen watchers
   - grainy CCTV stills where a figure appears misaligned
   - reflections that don’t quite match their subjects

FORM:
- Generate 4–7 shots per beat.
- Each shot is 1–2 sentences.
- Include camera language: “static wide shot,” “grainy CCTV still,” “slow dolly,” “close-up,” etc.
- Shots must feel observational, cold, and investigative.
"""
        else:
            broll_block = """
B-ROLL MODE (DISABLED):

For this request, DO NOT generate any B-roll lists or shot suggestions.
Focus entirely on clean, documentary narration and a closing beat.
"""

        structure_block = """
RESPONSE FORMAT:

Your response MUST be formatted into clear sections.

1) NARRATION:
   - 4–8 paragraphs.
   - Crisp, documentary-style voiceover.
   - Each paragraph should either:
     * advance the viewer’s understanding of the anomaly, OR
     * deepen the mystery with new evidence, contradictions, or implications.

"""

        if include_broll:
            structure_block += """
2) CINEMATIC B-ROLL (Shrouded Ledger):
   - A bullet or numbered list of 4–7 shots.
   - Each shot uses the B-ROLL MODE guidelines above.
   - Each shot is 1–2 sentences, including mood + camera language.

3) CLOSING BEAT:
   - 1 short paragraph that ends on subtle dread or an unanswered implication.
"""
        else:
            structure_block += """
2) CLOSING BEAT:
   - 1 short paragraph that ends on subtle dread or an unanswered implication.
"""

        return f"""
{base_style}

{broll_block}

TASK:
Expand the following outline beat into a fully narrated segment in The Shrouded Ledger style.

BEAT:
\"\"\"{beat_text}\"\"\"

{structure_block}

Begin now.
"""

    else:
        # Placeholder for future Aperture Black narrative expansions
        return f"""
You are writing a surreal, image-driven narration suitable for a short Aperture Black video.
Focus on liminal visuals, analog-photo textures, and quiet dread.

TASK:
Expand the following outline beat into a 2–4 minute narrated segment.

BEAT:
\"\"\"{beat_text}\"\"\"

Write 4–8 paragraphs of narration. Do not include B-roll. Just pure narration.
"""


def expand_script(beat_text: str, channel: str = "shrouded", broll: bool = True) -> str:
    """
    Call the OpenAI API to expand one beat into full narration,
    optionally including B-roll.
    """

    prompt = build_prompt(beat_text, channel, include_broll=broll)

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
        max_tokens=1500,
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

    parser.add_argument(
        "--no-broll",
        action="store_true",
        help="Disable the cinematic B-roll section in the output.",
    )

    args = parser.parse_args()

    beat_text = " ".join(args.beat)
    channel = args.channel
    include_broll = not args.no_broll

    mode_label = "with B-ROLL" if include_broll else "no B-ROLL"
    print(f"\n[Creator Assistant] Expanding beat (channel='{channel}', {mode_label})...\n")

    narration = expand_script(beat_text, channel=channel, broll=include_broll)

    print("=== EXPANDED SCRIPT ===\n")
    print(narration)
