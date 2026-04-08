# GDPR & Data Handling Tool Proposal

## Proposed Tool: GameAnalytics (Unreal Engine SDK Integration)

### 1. Overview & Objective
**Goal:** Integrate **GameAnalytics** into Unreal Engine to automatically collect player engagement telemetry, economy data, and performance metrics for *Greedy Piggies*, while efficiently offloading the legal and backend complexity of GDPR compliance.

### 2. Intended Users & Target Platform
- **Intended Users:** Game Designers (for game balancing), Community Managers, and Data Protection Officers (DPOs).
- **Target Platform:** Unreal Engine (via the official GameAnalytics plug-in), with data viewed on the GameAnalytics web dashboard.

### 3. Key Data and File Formats
- **Blueprint Nodes / C++ SDK:** Tool used inside Unreal Engine to capture discrete in-game events.
- **Player Telemetry (JSON):** Automatically formatted data packages tracking session length, win/loss rates, specific card usage, and shop currency transactions.
- **Personally Identifiable Information (PII):** IP addresses, location data, and platform identifiers which are tracked and obscured server-side.

### 4. Implementation Steps
1. **Engine Integration:**
   - Download and install the official GameAnalytics SDK plugin from the Unreal Engine Marketplace into the *Greedy Piggies* project.
2. **Implement Telemetry Event Hooks:**
   - Drop simple Blueprint nodes at key points within the core game loop to capture specific design data (e.g., `DesignEvent:CardPlayed` or `EconomyEvent:ShopPurchase_250k`).
3. **Configure Built-In GDPR Settings:**
   - Leverage GameAnalytics' out-of-the-box privacy switches. Ensure that tools like "IP Anonymization" are enabled so that player locations are grouped broadly rather than tracked individually to individual households.
4. **Establish the DSAR Protocol:**
   - Adopt the GameAnalytics dashboard to process direct Data Subject Access Requests (DSARs). If a user requests their data be deleted under the GDPR "Right to be Forgotten", Community Managers can simply input the user's ID into the GameAnalytics portal to permanently wipe the tracked PII without needing engineers to write custom database SQL scripts.

### 5. Expected Value to Production & Compliance
Adopting GameAnalytics bridges the gap between the design need for massive amounts of telemetry data and the legal requirement for strict user privacy.
- **Legal Compliance Out of the Box:** Building a custom backend to process GDPR deletions accurately within the mandated 30-day window is legally risky and time-consuming. Using an established tool offloads this massive liability to a compliant third party.
- **Preserves Critical Telemetry:** When a user requests data deletion, GameAnalytics can sever the personal identity from the data while maintaining the raw statistical metrics. This ensures game designers don't lose precious economic balancing data (like determining if a specific card has an 80% un-audited win rate) when an account is deleted.
- **Zero Backend Maintenance:** By using the official Unreal Engine SDK, developers don't have to spend weeks building custom scalable databases, allowing them to focus entirely on building core gameplay features.
