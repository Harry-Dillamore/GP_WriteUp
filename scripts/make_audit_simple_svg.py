import base64
import zlib
import urllib.request

theme_config = """%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#282828', 'primaryTextColor': '#ecc58d', 'primaryBorderColor': '#fc6a60', 'lineColor': '#fc6a60', 'secondaryColor': '#fc6a60', 'tertiaryColor': '#282828'} }}%%\n"""

content = """flowchart TD
    A([Play 3 Cards]) --> B([Declare Total Value])
    B --> C([Server Secretly Evaluates])
    C --> Loop{Poll Players for Audit}
    
    Loop -- "Audit Triggered" --> Calc[Run Audit Payouts]
    Loop -- "No Audit" --> Win[Player Wins Declared Value]
    
    Calc --> Truth{Did player lie?}
    Truth -- "Told Truth" --> ALose[Auditor Loses Value]
    Truth -- "Lied" --> PLose[Player Loses Value]
"""

filename = "mm_audit_simple.svg"
diagramSource = theme_config + content
compressed = zlib.compress(diagramSource.encode('utf-8'))
b64_encoded = base64.urlsafe_b64encode(compressed).decode('utf-8')
url = f"https://kroki.io/mermaid/svg/{b64_encoded}"

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        with open(filename, 'wb') as f:
            f.write(response.read())
    print(f"Saved {filename}")
except Exception as e:
    print(f"Failed to generate {filename}: {e}")
