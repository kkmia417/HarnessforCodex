from __future__ import annotations

import re
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RESOURCE_NAMES = {"references", "scripts", "assets"}

OFFICIAL_SKILLS_DIR = Path(".agents") / "skills"
LEGACY_SKILLS_DIR = Path("skills")
DEFAULT_USER_SKILLS_DIR = Path.home() / ".agents" / "skills"
SKILL_LAYOUTS = {
    "official": (OFFICIAL_SKILLS_DIR,),
    "legacy": (LEGACY_SKILLS_DIR,),
    "both": (OFFICIAL_SKILLS_DIR, LEGACY_SKILLS_DIR),
}
