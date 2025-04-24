from line_classifier import classify_cleaned_lines

# Örnek cleaned_lines verisi
cleaned_lines = [
    "4-4-2",
    "Anti Tartar S.K.",
    "OVR 84,8",
    "3-5-2",
    "82,7",
    "84,1",
    "91,2",
    "Fc Delft",
    "----G",
    "OVR 53,6",
    "Savunma",
    "Orta saha",
    "Hücum",
    "51,6",
    "51,1",
    "56,1",
    "---MB"
]

# Testi çalıştır
result = classify_cleaned_lines(cleaned_lines)

# Sonuçları yazdır
print("✅ Formlar:", result["form_values"])
print("🎯 OVR'ler:", result["ovr_values"])
print("💪 Güç Değerleri:", result["power_values"])
print("📐 Dizilişler:", result["formations"])
print("🧾 Takım Adları:", result["team_names"])
