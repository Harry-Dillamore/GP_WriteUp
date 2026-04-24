import base64
import zlib
import urllib.request

theme_config = """%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#282828', 'primaryTextColor': '#ecc58d', 'primaryBorderColor': '#fc6a60', 'lineColor': '#fc6a60', 'secondaryColor': '#fc6a60', 'tertiaryColor': '#282828'} }}%%\n"""

content = """flowchart TD
    subgraph Input Phase
        Start([Begin Audit Phase]) --> CheckP{More players to ask?}
        CheckP -- "Yes" --> IsAI{Is player AI?}
        IsAI -- "Yes" --> AIChoice[AI random decision]
        IsAI -- "No" --> HumanChoice[Wait for 'y'/'n' input]
        AIChoice --> DidAudit
        HumanChoice --> DidAudit
        DidAudit{Did they audit?}
        DidAudit -- "No" --> NextP[Recursive Call: Next Player]
        NextP --> CheckP
    end

    subgraph Resolution Phase
        DidAudit -- "Yes" --> Stop[Stop taking inputs]
        CheckP -- "No" --> NoAudit([No one audited])
        Stop --> RunCalc([Run Audit Calculations])
        
        NoAudit --> NoAuditPayout[Active Player wins declared value]
        RunCalc --> TruthCheck{Did the active player lie?}
        
        TruthCheck -- "No (Told Truth)" --> TruthPayout[Auditor loses declared value]
        TruthCheck -- "Yes (Lied)" --> LiePayout[Active Player loses declared value]
    end
"""

filename = "mm_audit_sequence.svg"
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
