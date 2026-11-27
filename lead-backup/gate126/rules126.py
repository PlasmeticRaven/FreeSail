import re
FOG_TEXT = ("A fog is settling in.", "The fog is thickening.", "The fog has shut in thick.",
            "The fog seems to be clearing.", "The fog is thinning.", "The fog lifted.", "Fog came down.")
SPAR_RE = re.compile(r"clearing away the wreck|clear away the wreck|shifting the |rigging a jury mast|"
                     r"bending the .*\(its spar shifted|\(bent again to its spar\)|Belayed (shifting|clearing)|"
                     r"[Ss]hifted the .* for a spare|wreck of the|[Cc]leared away the wreck|sway(ed)? (up|aloft)|"
                     r"spare (topmast|yard|spar)|jury mast")


def classify(kind, sev, text, side):
    t = text
    if kind in ("weather.fog",) or t.startswith(FOG_TEXT):
        return "FOG-line"
    if kind == "weather.sky" and t in ("The sky hazy.", "The sky thick.") or (kind == "weather.sky"):
        return "FOG-sky"
    if kind == "weather.hour":
        return "FOG-hour"
    if kind == "weather.change":
        return "FOG-change"
    if SPAR_RE.search(t):
        return "SPAR"
    if "no topsail set to lie a-try under" in t:
        return "SMACK"
    return "UNDECLARED"


DIVERGING = ("SPAR", "FOG-line", "SMACK")
