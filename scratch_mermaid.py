import base64
import zlib
import urllib.request

graphs = {
    "mm_ai_logic.svg": """graph LR
    Pick[AI Picks Random Cards] --> Play[Plays Face Down]
    Play --> Random[Randomized Audit Choice]
    Random -- "Audits" --> Check{Evaluate Truth}
    Random -- "Ignores" --> Wait[Next Player]""",
    
    "mm_start_game.svg": """graph TD
    BP([Begin Play]) --> Ref[Cache Narrator Reference]
    Start([StartGame]) --> Reset[Reset CardPool]
    Deal([StartingDeal]) --> L1{Loop 0 to 4}
    L1 --> L2{For Each Player} --> DealCard[Deal 1 Card]
    L1 -- Completed --> Call[Call Turn]""",
    
    "mm_turn_logic.svg": """graph TD
    Turn([Event Turn]) --> Check[Validate Player]
    Check --> Prompt[Print: 'Select 3 Cards']
    Prompt --> Loop{Player.Cards < 3?}
    Loop -- Yes --> Delay[Delay 0.2s] --> Loop
    Loop -- No --> Lock[Lock Inputs & Prompt Truth]""",
    
    "mm_audit_logic.svg": """graph TD
    D{Is the player audited?}
    D -- Not Audited --> T1{Is declaration true?}
    D -- Audited --> T2{Is declaration true?}
    T1 -- True/False --> WinP([Player wins value])
    T2 -- True --> WinA([Auditor loses value])
    T2 -- False --> LoseP([Player loses value])""",
    
    "mm_data_logic.svg": """graph LR
    Draw[Card Drawn ID: 12] --> Lookup{Get DataTableRow}
    Lookup --> DT[(DT_Deck)]
    Lookup --> Data[Returns Value, Suit & Image]
    Data --> Math[Multiply by 1000]""",

    "mm_rpc_logic.svg": """graph LR
    Client1((Client UI)) -- Audit Decision --> RPC[Run-On-Server RPC]
    RPC -- PlayerIndex / Audit? --> Auth[(Server Dealer)]
    Auth -- Calculate Results --> Multi[Multicast RPC]
    Multi -- Push Score Arrays --> ClientAll((All Clients))""",

    "mm_creator_logic.svg": """graph LR
    Form[Designer Input Form] --> Code[Blueprint Script]
    Code --> DA[Creates Data Asset]
    Code --> BP[Generates Empty Actor]
    BP -. inherits .-> Interface((BPI_CardBehaviors))""",
    
    "mm_game_loop_v2.svg": """graph TD
    A([Start Game]) --> B[Deal 5 Cards]
    B --> C[Player Turn: Play 3 Cards & Declare]
    C --> D{"Audited?"}
    
    D -- "No" --> E([Player Wins Value])
    D -- "Yes" --> F{"Did Player Lie?"}
    
    F -- "Yes" --> G([Player Loses Value])
    F -- "No" --> H([Auditor Loses Value])
    
    E --> I[Update Scores]
    G --> I
    H --> I
    
    I --> J{"Score Limits Reached?"}
    J -- "No" --> K[Next Player Turn]
    K --> C
    J -- "Yes" --> L([Game Over])"""
}

# Inject the presentation theme into the diagram logic
theme_config = """%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#282828', 'primaryTextColor': '#ecc58d', 'primaryBorderColor': '#fc6a60', 'lineColor': '#fc6a60', 'secondaryColor': '#fc6a60', 'tertiaryColor': '#282828'} }}%%\n"""


for filename, content in graphs.items():
    diagramSource = theme_config + content
    compressed = zlib.compress(diagramSource.encode('utf-8'))
    b64_encoded = base64.urlsafe_b64encode(compressed).decode('utf-8')
    url = f"https://kroki.io/mermaid/svg/{b64_encoded}"
    
    try:
        # Add User-Agent header
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            svg_data = response.read()
            with open(filename, 'wb') as f:
                f.write(svg_data)
        print(f"Saved {filename}")
    except Exception as e:
        print(f"Failed to generate {filename}: {e}")
