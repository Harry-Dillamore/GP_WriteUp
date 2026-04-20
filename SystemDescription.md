# dealer

this is the actor which is responsible for dealing cards to the players and handling the majority of the game logic, I chose to put the logic in a single authoritative actor to make it easier to manage and debug the game logic.

- the logic is spit up into many custom events to make it easy trigger different parts of the game loop.
- I attempted to migrate the logic to components to make it easier to involve more people working simultainiously, however, this was not so successful because I could not get people to consistantly work like this and since not enough people were activley working on the logic of the game, it was not worth the time investement.

```mermaid
graph TD
    SystemStart["Begin Play / Initialize"] --> Setup["Setup Deck and Narrator"]
    Setup --> StartDeal["Deal 5 Cards to Players"]
    StartDeal --> TurnStart["Evaluate Turn Count"]

    TurnStart --> ShopCheck{"Is it a Shop Turn?"}
    ShopCheck -->|Yes| ShopPhase["Shop Phase"]
    ShopPhase --> NextTurn["Next Player / Increment Turn"]

    ShopCheck -->|No| PlayerTurn["Regular Turn"]
    PlayerTurn --> SelectCards["Poll Input: Player selects 3 cards"]
    SelectCards --> DeclareValue["Player declares a value"]
    DeclareValue --> AuditPhase{"Audit Phase"}

    AuditPhase -->|Audited| AuditLogic{"Did the player lie?"}
    AuditPhase -->|Not Audited| ApplyValues["Apply Declared Score"]

    AuditLogic -->|Yes - Auditor Wins| PlayerLosedVal["Current player loses declared value"]
    AuditLogic -->|No - Player Wins| AuditorLosedVal["Auditor loses declared value"]

    PlayerLosedVal --> Score["Update Scores"]
    AuditorLosedVal --> Score
    ApplyValues --> Score

    Score --> CheckState{"Check Win/Loss Conditions"}
    CheckState -->|Game Continues| NextTurn
    CheckState -->|Game Over| EndGame["End Game"]

    NextTurn --> TurnStart
```

## start game

![alt text](start_game_blueprints.png)

This section manages the setup of the game, taking place across three main execution paths:

**1. Initialization (BeginPlay)**
On `BeginPlay`, the Dealer triggers `GetNarratorBPReference`. This searches the level using `GetAllActorsOfClass` to find the `BP_NarratorManager` and caches a reference to it in `NarratorManagerRef` so it can be easily accessed throughout the game without performance overhead.

**2. Game Reset (StartGame)**
The `StartGame` custom event is executed to initialize a session. It strictly calls `ResetActiveIndex`, which readies a fresh Card Pool for the game.

**3. Dealing Phase (StartingDeal)**
The `StartingDeal` event handles dispensing the initial hands to all players. It runs a `For Loop` five times (indices 0 to 4). During each of the 5 iterations, a nested `For Each Loop` iterates through the `hands` array (containing all active player hands) and executes `DealCard` to give every player one card at a time. Once the outer loop finishes dealing 5 cards to everyone, it fires the `Turn` function to officially begin gameplay.

```mermaid
graph TD
    subgraph Initialization
    BP([Event Begin Play]) --> CallGetNar[Call GetNarratorBPReference]
    EventGetNar([Event GetNarratorBPReference]) --> GetAll[Get All Actors of Class: BP_NarratorManager]
    GetAll --> SetRef[Set NarratorManagerRef]
    end

    subgraph Prepare Deck
    StartG([Event StartGame]) --> Reset[ResetActiveIndex <br/> 'Resets CardPool']
    end

    subgraph Dealing Cards
    Deal([Event StartingDeal]) --> ForLoop[For Loop <br/> First:0, Last:4]
    ForLoop -- Loop Body --> ForEach[For Each Loop <br/> Array: hands]
    ForEach -- Loop Body --> DealCard[DealCard]
    ForLoop -- Completed --> Turn[Call Turn]
    end
```

## turn

![alt text](turn_blueprints.png)

This section manages the individual player progression and handles the input polling at the start of a turn:

**1. Turn & Shop Tracking**
When the `Turn` event fires, the server (via a `Switch Has Authority` check) increments the `TotalTurnCount`. It uses a modulo operation (`TotalTurnCount % 4 == 0`) to determine if it is time for a Shop Phase or a Regular Turn. (As per the design, a shop phase occurs periodically).

**2. Turn Initialization**
If it is a Regular Turn, the system sets up the state by resetting the `realScore` to 0. It determines the active player by grabbing the current hand, casting it to the character (`BP_FirstPersonCharacter_HarryTesting`), and caching this as the `player` variable.

**3. Input Polling**
With the player referenced, it prints "select 3 cards" to the screen. It then enters an input polling loop using a 0.2-second `Delay` to repeatedly check if the length of the `player.chosenCards` array is less than 3.

**4. Value Declaration Prep**
Once the player has selected 3 cards, the loop breaks. The sequence moves to prepare for the value declaration: it resets the player's input state (`inputValue = false`), toggles some UI element visibility (`SetVisibility`), and prompts the player to "write a value or type 0 to tell the truth" on the screen.

```mermaid
graph TD
    Turn([Event Turn]) --> Auth{Switch Has Authority}
    Auth -- Authority --> Inc[Increment TotalTurnCount]
    Inc --> ModCheck{TotalTurnCount % 4 == 0?}

    ModCheck -- Yes --> Shop[CloseShop / Trigger Shop Phase]
    ModCheck -- No --> ResetScore[Set realScore = 0]

    ResetScore --> GetPlayer[Get Current Player Hand <br/> Cast to Player Character]
    GetPlayer --> Cache[Set 'player' reference]
    Cache --> Prompt1[Print: 'select 3 cards']

    Prompt1 --> CheckCards{chosenCards.Length < 3?}
    CheckCards -- True --> Delay[Delay 0.2s]
    Delay --> CheckCards

    CheckCards -- False --> PrepInput[Set inputValue = false <br/> Update UI]
    PrepInput --> Prompt2[Print: 'write a value...']
```

## calculate score

This section manages the logic for determining the exact numerical value of the cards a player has chosen to play, as well as safely removing them from their hand:

**1. Initialization**
When `CalculateScore` is called, it receives `_chosenCards` (an array of integer indices the player selected), the player's `_hand` object, and the `_owner`. It immediately clears a temporary local array called `removeFromHand` to prepare for processing.

**2. Card Evaluation & Multipliers (First Loop)**
The system runs a `For Each Loop` over the `_chosenCards` array. For every selected index:
- It retrieves the precise card ID from the player's `hand` array.
- It adds this card ID into the `removeFromHand` array.
- It converts the card ID into a string and retrieves its baseline data from the `DT_Deck` **Data Table** to extract its `Card Value`.
- It then evaluates the selected cards for pairs or triples. 
  - Unique cards are worth 1x.
  - Pairs double the worth of the matching cards (2x).
  - Triples triple the worth of all cards (3x).
- After determining the correct multiplier, the card's value is multiplied by 1,000 to reach its final score.
- It performs an Add operation, accumulating this value into the total `_score`.

**3. Card Safing & Removal (Second Loop)**
After the first loop completes, a second `For Each Loop` iterates over the `removeFromHand` array. It uses the `Array_RemoveItem` node to delete these newly played cards from the active player's `hand`. Separating the scoring and removal into two distinct loops prevents the index-shifting bugs that occur when removing elements from an array while still iterating over its original indices.

**4. Return Result**
Finally, once all selected cards are evaluated and cleanly removed from the hand, the final calculated `_score` is returned to the main game loop so the player can declare their value ahead of the Audit Phase.

```mermaid
graph TD
    Start([CalculateScore]) --> Setup[Initialize Local Variables & <br/> Clear removeFromHand]
    Setup --> Loop1[For Each Loop: _chosenCards]

    Loop1 -- Loop Body --> GetCard[Get Card ID from hand using index]
    GetCard --> AddToRemove[Add Card ID to removeFromHand]
    AddToRemove --> Lookup[Lookup Face Value in DT_Deck]
    
    Lookup --> CheckMultipliers{Check for Pairs/Triples}
    CheckMultipliers -- "Triple (3 of a kind)" --> Mult3[Face Value * 3]
    CheckMultipliers -- "Pair (2 of a kind)" --> Mult2[Face Value * 2]
    CheckMultipliers -- "Unique" --> Mult1[Face Value * 1]
    
    Mult3 --> Apply1000[Value * 1000]
    Mult2 --> Apply1000
    Mult1 --> Apply1000

    Apply1000 --> AddScore[_score += Final Value]
    AddScore --> Loop1

    Loop1 -- Completed --> Loop2[For Each Loop: removeFromHand]

    Loop2 -- Loop Body --> RemoveCard[RemoveItem: Card ID from hand]

    Loop2 -- Completed --> Return([Return _score])
```
