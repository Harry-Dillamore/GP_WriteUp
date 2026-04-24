---
marp: true
backgroundColor: "#282828"
color: "#ecc58d"
---

<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400..700;1,400..700&display=swap');

/* Override default Marp theme colors */
h1, h2, h3, h4, h5, h6,
h1 strong, h2 strong, h3 strong, h4 strong, h5 strong, h6 strong {
  color: #fc6a60 !important;
  font-family: 'Lora', serif !important;
}
li::marker {
  color: #fc6a60 !important;
}
strong {
  color: #fce3b8 !important;
}
</style>

# **Client Brief: Project Contributions**

**By Harry Dillamore**
Gameplay Programmer & Technical Architect

---

# **Overview of Contributions**

- **Role**: Gameplay Programmer
- **Core Focus**: Translating paper design into a structurally sound digital architecture.
- **Key Deliverables**:
  - Complete authoritative Game Loop (Dealer Actor)
  - Networked Multiplayer Foundation
  - Data-driven Systems (Card Lookup, Scoring)
  - Tooling (Card Creator Editor Utility Widget)

![bg right:40% 100%](https://pub-9c6c59cb1e3f474f938dca895e9f576d.r2.dev/GreedyPiggies/raci_chart.png)

---

# **Rapid Prototyping & AI**

- I created the **initial prototype** for the game, which included the **core gameplay loop** and **AI opponents**.
- This meant that we could test the game loop before multiplayer was ready and find any issues with it early on.
- The prototype I made was then taken forward and used as the **foundation** for the rest of the game.

![bg right:30% 100% height:100%](https://pub-9c6c59cb1e3f474f938dca895e9f576d.r2.dev/GreedyPiggies/mm_game_loop_v2.svg)

---

![bg fit](https://pub-9c6c59cb1e3f474f938dca895e9f576d.r2.dev/GreedyPiggies/bp_turn_logic.png)

---

# **System Architecture**

- I created one **authoritative Dealer actor** where the flow of the game is defined and executed.
- Manages the **absolute flow** of the game, including safely transitioning between Regular turns and Shop phases over the network.
- The Dealer is organized using **custom events** for each phase of the game.
- This means that the Dealer is highly **modular** and can be easily modified to add new phases to the game.

<!-- _footer: "*Reference: Gambetta, G. (2016) Fast-Paced Multiplayer*" -->

![bg right:30% 100% height:100%](https://pub-9c6c59cb1e3f474f938dca895e9f576d.r2.dev/GreedyPiggies/mm_start_game.svg)

---

![bg fit](https://pub-9c6c59cb1e3f474f938dca895e9f576d.r2.dev/GreedyPiggies/image-2.png)

---

![bg fit](https://pub-9c6c59cb1e3f474f938dca895e9f576d.r2.dev/GreedyPiggies/mm_dealer_events.svg)

---

# **Data-Driven Architecture**

- Segregated hard data from logic frameworks to ensure stability and **stop Git-merge conflicts**.
- Utilized static **Unreal Data Tables** to store card indexes, values, and image paths.
- Logic retrieves structured data cleanly using `Get Data Table Row` and `Break Struct` nodes rather than relying on messy variable clusters.

<!-- _footer: "*Reference: Gregory, J. (2018) Game Engine Architecture*" -->

<br>

<div align="center">
  <img src="https://pub-9c6c59cb1e3f474f938dca895e9f576d.r2.dev/GreedyPiggies/mm_data_logic.svg" width="900px" />
</div>

---

![bg fit](https://pub-9c6c59cb1e3f474f938dca895e9f576d.r2.dev/GreedyPiggies/dt_card_data_table.png)

---

# **Multiplayer Integration**

- This was something very new to me and the rest of the team.
- We adopted a **pair / group programming** approach to help us get to grips with the concepts of **replication** and **remote procedure calls**.
- **Server Authority:** Secured core logic to only execute on the server using `Switch Has Authority` nodes.
- **Remote Procedure Calls (RPCs):** Established clear event boundaries for client-to-server communication.

<!-- _footer: "*Reference: Fowler, M. (2007) On Pair Programming*" -->

<br>

<div align="center">
  <img src="https://pub-9c6c59cb1e3f474f938dca895e9f576d.r2.dev/GreedyPiggies/mm_rpc_logic.svg" width="900px" />
</div>

---

# **Auditing Mechanics**

- Executed the game's core **"bluffing" conflict** using conditional `Branch` and `Sequence` nodes.
- Evaluates **truth tables** (Did they lie? Were they audited?) to apply **scoring penalties** safely on the server.
- Replaced rudimentary **recursive polling** with a simultaneous, **timed decision widget** for all players.

![bg right:40% 100% height:100%](https://pub-9c6c59cb1e3f474f938dca895e9f576d.r2.dev/GreedyPiggies/mm_audit_simple.svg)

---

![bg fit](https://pub-9c6c59cb1e3f474f938dca895e9f576d.r2.dev/GreedyPiggies/bp_audit_decision_logic.png)

---

# **Card Creator Tool**

- Created an **Editor Utility Widget** to provide designers with a simple, **automated asset production pipeline**.
- Input fields programmatically trigger `Construct Object from Class` nodes to generate matching **Data Assets** automatically.
- Standardized action events inherently via **Blueprint Interfaces**.

<br>

<div align="center">
  <img src="https://pub-9c6c59cb1e3f474f938dca895e9f576d.r2.dev/GreedyPiggies/mm_creator_logic.svg" width="900px" />
</div>

---

![bg vertical fit](https://pub-9c6c59cb1e3f474f938dca895e9f576d.r2.dev/GreedyPiggies/image-3.png)
![bg fit](https://pub-9c6c59cb1e3f474f938dca895e9f576d.r2.dev/GreedyPiggies/image-4.png)

---

# **Successes**

- The **Card Creator pipeline** completely prevented **Git friction**.
- Overcame steep learning curves to validate complex **networked RPCs** and **Server-Authority workflows**.
- Overall, my work created a **solid foundation** for the game as I was able to build most of the data and logic systems for all of the **core mechanics**, meaning that the rest of the team could build on this to add polish and better user experience.

---

# **Areas for Improvement**

- Should have **decentralized logic** from the **monolithic Dealer Actor** to prevent late-stage **manageability issues** and **workflow bottlenecks**.
- Needed **better communication** on system functionality to **encourage team contributions** and improve final features.

---

# **Thank you**

---

# **Bibliography**

- Fowler, M. (2007) _On Pair Programming_. Available at: https://martinfowler.com/articles/on-pair-programming.html (Accessed: 21 April 2026).
- Gambetta, G. (2016) _Fast-Paced Multiplayer_. Available at: https://www.gabrielgambetta.com/client-server-game-architecture.html (Accessed: 21 April 2026).
- Gregory, J. (2018) _Game Engine Architecture_. 3rd edn. Boca Raton: CRC Press.
