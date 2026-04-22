import base64
import zlib
import urllib.request

theme_config = """%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#282828', 'primaryTextColor': '#ecc58d', 'primaryBorderColor': '#fc6a60', 'lineColor': '#fc6a60', 'secondaryColor': '#fc6a60', 'tertiaryColor': '#282828'} }}%%\n"""

content = """graph TD
    subgraph Initialization Events
    Init1[<b>GetNarratorBPReference</b><br/>Runs on BeginPlay to securely locate and cache the Narrator Actor]
    Init2[<b>StartGame</b><br/>Wipes existing data and resets the card pool for a fresh session]
    Init3[<b>StartingDeal</b><br/>Iterates through all valid players to dispense their initial 5 cards]
    end

    subgraph Core Game Loop Events
    Core1[<b>Turn</b><br/>Initialises the active player's state and begins polling for their card selection]
    Core2[<b>AuditPhase</b><br/>Evaluates if truth/bluff conditions were met and distributes server-side score penalties]
    Core3[<b>CloseShop</b><br/>Ends the special shop phase and transitions gameplay back to the standard regular queue]
    Core4[<b>EndOfGame</b><br/>Triggers the final win/loss state to conclude the current session]
    end

    subgraph Utility & State Events
    Util1[<b>DealCard</b><br/>Utility triggered to dispense a single specific card to a target hand]
    Util2[<b>AddToHands</b><br/>Safely drops new player references into the hands array]
    Util3[<b>UpdateAllScores</b><br/>Synchronises the latest authoritative score values across all client UIs]
    end
"""

filename = "mm_dealer_events.svg"
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
