import re

def clean_ocr_lines_strict(raw_lines):
    # 🗒️ IGNORE listesi: İstenmeyen sabit kelimeler (KURAL 1)
    IGNORED_WORDS = [
        "maç ön izleme", "maç ôn izleme", "genel bakış", "genel bakiş",
        "diziliş", "takım", "takim", "hazırlık", "hazırlik", "hazırlk",
        "rakip", "rakíp", "ligi", "form", "elit lig", "kupa",
        "txt", "dostluk", "300,0-+", "300,0+", "İIk", "İIk tur"
    ]

    cleaned_lines = []
    form_lines = []
    ovr_indices = []

    # 🔤 Türkçe karakterleri normalize eder
    def normalize_tr(text):
        replacements = {
            "Ç": "C", "ç": "c",
            "Ğ": "G", "ğ": "g",
            "İ": "I", "ı": "i",
            "Ö": "O", "ö": "o",
            "Ş": "S", "ş": "s",
            "Ü": "U", "ü": "u"
        }
        for src, target in replacements.items():
            text = text.replace(src, target)
        return text.lower()

    # ✅ KURAL 1: Sabit kelimeleri sil
    def is_ignored_line(line):
        normalized = normalize_tr(line)
        normalized_ignored = [normalize_tr(w) for w in IGNORED_WORDS]
        return any(word in normalized for word in normalized_ignored)

    # ✅ KURAL 2: Tarih-saat satırları (dd.mm hh:mm)
    def is_datetime(line):
        return re.match(r"\d{2}\.\d{2} \d{2}:\d{2}", line.strip()) is not None

    # ✅ KURAL 3: Anlamsız karakter zincirleri (SSS, $$$ vs)
    def is_garbage(line):
        return re.fullmatch(r"[sS\$kK]+", line.strip()) is not None

    # ✅ KURAL 4: Sadece tam sayı
    def is_integer_only(line):
        return line.strip().isdigit()

    # ✅ KURAL 7: Doğal dil yorum cümleleri
    def is_commentary(line):
        words = line.strip().split()
        if any(punc in line for punc in [".", "!", "?"]) and len(words) > 3:
            return True
        return len(words) > 5

    # ✅ KURAL 8: + işareti ve MB içeren yapılar
    def is_useless_number(line):
        return re.search(r"\+.*[MB]", line) is not None

    # ✅ BONUS: Tek harfli satırlar
    def is_one_letter(line):
        return len(line.strip()) == 1

    # ✅ KURAL 6: OVR normalizasyonu
    def normalize_ovr(line):
        match = re.search(r"ovr[:\s]*([\d.,]+)", line, re.IGNORECASE)
        return f"OVR {match.group(1)}" if match else None

    # ✅ KURAL 5: Form verisi kontrolü ve normalize etme
    def is_valid_form(line):
        compact = line.replace(" ", "").strip()
        if not all(c in "GMB-" for c in compact):
            return False, None
        if len(compact) == 5:
            return True, compact
        if len(compact) < 5 and "-" in compact:
            return True, ("-" * (5 - len(compact))) + compact
        return False, None

    # 🧹 Ana temizlik döngüsü
    for line in raw_lines:
        stripped = line.strip()

        if is_ignored_line(stripped): continue
        if is_datetime(stripped): continue
        if is_garbage(stripped): continue
        if is_integer_only(stripped): continue
        if is_commentary(stripped): continue
        if is_useless_number(stripped): continue
        if is_one_letter(stripped): continue

        normalized = normalize_ovr(stripped)
        if normalized:
            cleaned_lines.append(normalized)
            ovr_indices.append(len(cleaned_lines) - 1)
            continue

        is_form, fixed_form = is_valid_form(stripped)
        if is_form:
            cleaned_lines.append(fixed_form)
            form_lines.append(fixed_form)
            continue

        cleaned_lines.append(stripped)

    # ✅ KURAL 5.4: Form hiç yoksa OVR altına ve sona ----- ekle
    if not form_lines and ovr_indices:
        last_ovr_index = ovr_indices[-1]
        cleaned_lines.insert(last_ovr_index + 1, "-----")
        cleaned_lines.append("-----")

    return cleaned_lines
