# Beschreibung
Konvertiert Binärdateien zu QR-Code Images.

# Parameter
Parameter | Kürzel | Beschreibung
--- | --- | ---
--file | -f | Binärdatei
--qr-code-per-page | -q | Wie viele QR-Codes pro Bild sind (Bediengung: n % 4 = 0)

# Beispiel
QRCodeStorage --file binary.exe --qr-code-per-page 16