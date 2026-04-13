# Week 1 - Final Tool Ideation Document

This document outlines the proposed tools for the *Greedy Piggies* production pipeline, addressing both custom utility creation and the integration of existing analytics software.

---

## Part 1: Card Creator (Custom Tool)

### 1. Overview & Objective
**Goal:** Develop an Editor Utility Widget (EUW) that centralizes and standardizes the creation and management of special ability cards for *Greedy Piggies*.

### 2. Intended Users & Target Platform
- **Intended Users:** Game Designers and Developers.
- **Target Platform:** Unreal Engine (Editor Utility Widget / EUW).

### 3. Key Data and File Formats
- **.uasset Data Assets:** Generated automatically to store structured card parameters and stats. This separation ensures that people can work with fewer conflicts.
- **Blueprints & Blueprint Interfaces:** Used to attach custom mechanics securely to each card, ensuring standardized execution for all special ability cards.
- **Central Array Asset/Database:** A central asset grouping references to all separate files, allowing organized fetching during gameplay.

### 4. Implementation Steps
1. **Develop the Editor UI Layer:** 
   - Create a standardized EUW interface within the Unreal Editor for designers to input card details.
2. **Automate Asset Generation:**
   - Script the EUW to generate a new `.uasset` (Data Asset) containing the parameters specified in the UI upon creation.
3. **Standardize Card Abilities:** 
   - Integrate Blueprint Interfaces to ensure the logic structure is identical across all special ability cards, guaranteeing that the core gameplay loop can trigger diverse abilities predictably.
4. **Organize and Register:** 
   - Program the tool to save cards as separate, organized files while automatically registering them to a central array.

### 5. Expected Value to Production
- **Standardized Abilities:** By unifying how special ability cards are created and structured, the game manager can trigger complex abilities seamlessly, reducing bugs and engineering overhead.
- **Minimizes Git Conflicts:** Saving individual cards as separate, highly organized data assets allows multiple designers to create and iterate on cards simultaneously without triggering production-blocking git conflicts on monolithic central files.
- **Designer Autonomy:** Designers can quickly generate, organize, and balance cards via a robust utility widget interface.

---

## Part 2: Game Analytics (Existing Tool Integration)

### 1. Overview & Objective
**Goal:** Integrate the existing **GameAnalytics** tool into Unreal Engine to automatically collect datasets on player actions and economy engagement to aid in game balancing.

### 2. Intended Users & Target Platform
- **Intended Users:** Game Designers (for game balancing), Community Managers, and Data Protection Officers (DPOs).
- **Target Platform:** Unreal Engine (via the official GameAnalytics plug-in SDK), with data visualized on the web dashboard.

### 3. Key Data and File Formats
- **Blueprint Nodes / C++ SDK:** The integration tools inside Unreal Engine used to fire events.
- **Player Telemetry (JSON):** Automatically formatted metrics tracking detailed player actions, such as card usage, win rates, and shop currency transactions.
- **Personally Identifiable Information (PII):** Handled securely server-side based on legal compliance (GDPR).

### 4. Implementation Steps
1. **Engine Integration:**
   - Install the official GameAnalytics SDK plugin from the Unreal Engine Marketplace into the *Greedy Piggies* project.
2. **Implement Telemetry Event Hooks:**
   - Drop simple Blueprint nodes at key points within the core game loop to collect data on specific player actions (e.g., `CardPlayed` or `ShopPurchase`).
3. **Configure Built-In GDPR Settings:**
   - Ensure the tool's privacy switches, like IP Anonymization, are enabled.
4. **Establish the DSAR Protocol:**
   - Utilize the GameAnalytics portal to process Data Subject Access Requests (DSARs), allowing the team to easily delete tracked user PII upon request.

### 5. Expected Value to Production
- **Data-Driven Balancing:** By collecting extensive data on player actions (like specific card win rates), game designers have the empirical metrics needed to perform crucial game balancing.
- **Out-of-the-Box Functionality:** Using an existing, robust analytics tool means developers avoid spending weeks building a custom telemetry database, allowing them to focus on the core game.
- **Seamless GDPR Compliance:** Legal liabilities and the technical complexities of data deletion are safely handled by the established tool's backend, preserving critical gameplay telemetry while stripping PII when legally required.
