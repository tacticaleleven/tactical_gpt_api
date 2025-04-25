import re

def is_float(line):
    try:
        float(line.replace(",", "."))
        return True
    except:
        return False

def is_ovr(line):
    return line.strip().lower().startswith("ovr")

def is_form_string(line):
    compact = line.replace(" ", "").strip()
    return len(compact) == 5 and all(c in "GMB-" for c in compact)

def classify_cleaned_lines(cleaned_lines):
    powers = []
    ovr_values = []
    form_values = []
    text_comments = []
    formations = []
    team_names = []

    for line in cleaned_lines:
        stripped = line.strip()

        if is_ovr(stripped):
            ovr_values.append(stripped)

        elif is_form_string(stripped):
            form_values.append(stripped)

        elif is_float(stripped):
            powers.append(stripped)

        elif re.match(r"^\d{1,2}-\d{1,2}-\d{1,2}(-\d{1,2})?$", stripped):
            formations.append(stripped)

        elif len(stripped) > 2:
            team_names.append(stripped)

    return {
        "ovr_values": ovr_values,
        "form_values": form_values,
        "power_values": powers,
        "formations": formations,
        "team_names": team_names,
        "all": cleaned_lines
    }