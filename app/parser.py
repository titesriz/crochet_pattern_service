import re
from typing import List
from app.models import Pattern, Part, Round


TOUR_REGEX = re.compile(
    r"^\s*(?:Tour|Rang|Rg)\s*(\d+)\s*[:\-]?\s*(.+)$",
    re.IGNORECASE
)

STITCH_COUNT_REGEX = re.compile(r"\((\d+)\)")


def parse_text_to_pattern(
    text: str,
    pattern_id: str = "amigurumi_001",
    part_id: str = "head_body",
    part_name: str = "Head / Body",
) -> Pattern:
    """
    MVP : parse un texte où chaque ligne décrit un tour.
    Exemple attendu :
        Tour 1 : 6 m.s. dans un cercle magique (6)
        Tour 2 : 6 augm. m.s. (12)
    """

    rounds: List[Round] = []

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue  # ignore lignes vides

        m = TOUR_REGEX.match(line)
        if not m:
            continue  # pour l'MVP, on ignore ce qu'on ne comprend pas

        round_number_str, raw_text = m.groups()
        round_number = int(round_number_str)

        # Essayer d'extraire le nombre total de mailles entre parenthèses
        total_stitches = None
        m_stitches = STITCH_COUNT_REGEX.search(raw_text)
        if m_stitches:
            total_stitches = int(m_stitches.group(1))

        rounds.append(
            Round(
                round=round_number,
                raw_text=raw_text.strip(),
                total_stitches=total_stitches,
            )
        )

    part = Part(
        part_id=part_id,
        name=part_name,
        work_type="rounds",
        rounds=sorted(rounds, key=lambda r: r.round),
    )

    pattern = Pattern(
        pattern_id=pattern_id,
        part=part,
    )

    return pattern