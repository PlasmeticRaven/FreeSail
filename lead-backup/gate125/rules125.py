import re
def classify(kind, sev, text, side):
    t = text
    if t.startswith("Missed stays: she came through the wind and fell back") or t.startswith("Missed stays: she lies in irons"):
        return "C-miss"
    if "is left on her: she gripes" in t or "are left on her: she gripes" in t:
        return "D-kept"
    if "Mainsail haul" in t or "ainsail haul" in t or "opsail haul" in t:
        return "A-haul?"
    return "UNDECLARED"
DIVERGING = ("C-miss", "D-kept", "A-haul?")
