# Week 1 - Tool Ideation Exercise

## Implementation Plan: Card Creation & Management Editor Utility Widget

### 1. Overview & Objective
**Goal:** Develop an Editor Utility Widget (EUW) that centralizes and standardizes the creation and management of shop cards and character abilities for *Greedy Piggies*.

### 2. Intended Users & Target Platform
- **Intended Users:** Game Designers and Developers.
- **Target Platform:** Unreal Engine (Editor Utility Widget / EUW).

### 3. Key Data and File Formats
- **.uasset Data Assets:** Generated automatically to store structured card parameters and stats.
- **Blueprints & Blueprint Interfaces:** Used to attach custom mechanics securely to each card, ensuring standardized ability execution.
- **Central Array Asset/Database:** A centralized array that stores references to all generated cards for easy runtime fetching.

### 4. Implementation Steps
1. **Develop the Editor UI Layer:** 
   - Create a standardized EUW interface within the Unreal Editor for designers to input card details.
2. **Automate Asset Generation:**
   - Script the EUW to generate a new `.uasset` (Data Asset) containing the parameters specified in the UI upon creation.
3. **Implement Blueprint Interfaces:** 
   - Ensure the logic structure mandates a specific Blueprint Interface for the custom logic assigned to each newly created card. This guarantees that the core gameplay loop can trigger diverse abilities predictably.
4. **Register to Central Data Array:** 
   - Program the tool to automatically push the new card asset reference to a centralized array, guaranteeing all cards can be found in a single location and called uniformly across the codebase.

### 5. Expected Value to Production
Implementing this plan yields massive value to the development pipeline:
- **Centralized Data & Uniform Execution:** Adding cards to a central array allows the core game manager to easily find and iterate over them. By enforcing the use of our Blueprint Interface, the core loop can trigger complex card abilities in the exact same way without bespoke hardcoding.
- **Designer Autonomy:** Designers can use the tool to instantly generate, configure, and balance cards via a visual interface without taking away an engineer's time.
- **Minimizes Git Conflicts:** Safely separating individual card data assets across the team allows multiple designers to work simultaneously without encountering production-blocking git conflicts on monolithic central files.

---

> This documentation was modified with the use of Antigravity (Claude 4.6, Google Gemini 3 Flash).