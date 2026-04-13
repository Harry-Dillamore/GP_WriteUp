# Week 3 - Security, Compliance, and Networking Evaluation

## Tool Selection 1: GameAnalytics SDK Integration

For this evaluation, we are analyzing the **GameAnalytics SDK Integration** proposed in Week 1. This tool is designed to collect in-game telemetry and economy data to aid in player balancing. Because it interfaces directly with external servers to transmit player behaviors and potentially Personally Identifiable Information (PII), it carries substantial networking, security, and compliance risks.

---

## 1. Identification of Potential Risks

**Could the tool transmit data over a network?**
Yes. The SDK continuously captures discrete gameplay events and pushes them over the internet to the GameAnalytics cloud servers at regular intervals.

**Could it expose sensitive project or player data?**
Yes. If misconfigured or intercepted, the transmitted data could expose:
- **Player Data:** IP addresses, platform hardware IDs, geographic locations, and session durations (PII).
- **Project Data:** Unreleased economic balancing metrics, shop transaction volumes, or proprietary game meta-analysis.

**Could it be exploited or manipulated?**
**Telemetry Spoofing** is a major risk. External attackers or malicious players could decompile the game client, intercept the telemetry endpoints, and write scripts to flood the servers with fake data (e.g., repeatedly firing an event that says *Card X* was played and lost). 

**What happens if it is compromised?**
- **Internal Misuse / Misconfiguration:** A developer might accidentally push an update that tracks sensitive details (like chat logs), massively violating privacy laws.
- **External Attackers:** Flooding the system with spoofed data destroys the integrity of the analytics, leading developers to make incorrect game balancing decisions based on corrupted metrics.
- **Data Leakage:** If the transit isn't secured or the API keys are leaked in the source code, attackers could scrape data or weaponize the telemetry pipeline, resulting in severe GDPR non-compliance fines.

---

## 2. Proposed Mitigations

To secure the GameAnalytics pipeline against the threats of eavesdropping, spoofing, and data leakage, the following technical measures must be enforced:

- **Protocol Choice (HTTPS):** All outgoing telemetry must be strictly forced through **HTTPS (TLS 1.2 or higher)**. Unencrypted HTTP is unacceptable, as it leaves player data vulnerable to man-in-the-middle (MitM) attacks.
- **Encryption Required:** Data in transit must be secured via TLS. Additionally, sensitive analytics data stored locally in a device buffer before transmission should be obfuscated so players cannot easily read their memory dumps.
- **Authentication Method (HMAC Signatures):** To prevent telemetry spoofing, the client must use **HMAC (Hash-based Message Authentication Code)** using a private secret key. The server rejects any payload where the cryptographic signature does not match the content, rendering trivial bot-flooding useless.
- **Access Control:** The GameAnalytics web dashboard must enforce **Role-Based Access Control (RBAC)**. Game designers should only have read access to aggregated statistics. Only the Data Protection Officer (DPO) and Lead Admin can access raw user histories to process Data Subject Access Requests (DSARs).
- **Logging and Auditing:** Enable audit logs on the dashboard to track whenever internal team members access sensitive player profiles, preventing internal abuse.
- **Data Minimisation (GDPR principle):** Enable the SDK’s "IP Anonymization" feature. This scrambles the final octets of a player's IP address client-side before processing, aggregating players regionally rather than mathematically pinpointing individual households. 

---

## 3. Networking and Architecture Considerations (Local vs. Networked)

*While the GameAnalytics tool fundamentally operates over a network, we must evaluate if the current implementation (client-directly-to-analytics-server) is the most secure architecture.*

**Would a dedicated authoritative service reduce risk?**
Currently, the Unreal Engine client talks directly to the GameAnalytics REST API. This exposes the GameAnalytics integration keys inside the shipped client. 
- **Centralised Validation:** To improve trust, the architecture could be restructured into a true **Client–Server model** utilizing an authoritative dedicated backend. Instead of the game client talking directly to GameAnalytics, the client would send secure verification packets securely to our own custom backend server.
- **Authoritative Service:** The custom backend would validate the telemetry against the active game session (e.g., "Could the player have legitimately cast this spell 5 times in 10 seconds?"). If the parameters are mathematically impossible, the server drops the malformed packet. Only legitimate, server-validated data is then forwarded from the backend to the data lake, completely hiding the API keys from the public client.

**Explain whether networking adds value or unnecessary complexity?**
Introducing an intermediary authoritative server **adds immense security value** for competitive, high-stakes games where data integrity must be 100% accurate. However, for a smaller production relying on out-of-the-box Unreal plugins, building and maintaining a custom validating telemetry firewall introduces **unnecessary complexity**. For *Greedy Piggies*, utilizing the built-in plugin with strict HMAC authentication, HTTPS, and diligent data minimisation policies is the optimal balance of security and engineering effort.

---

## Tool Selection 2: Card Creator (Editor Utility Widget)

While our analytics tool operates primarily over a network, the **Card Creator EUW** is built to operate locally on developers' machines. Evaluating this tool highlights the internal security and risk considerations for a local production pipeline.

### 1. Identification of Potential Risks

**Could the tool transmit data over a network?**
By default, the tool only saves `.uasset` files locally to the user's disk. Data is only transmitted over the network when a developer commits and pushes those new files to the shared version control repository.

**Could it expose sensitive project or player data?**
It does not expose PII or player data. However, it handles **Project Data**, specifically unreleased game mechanics, character abilities, and upcoming cards. A leak reveals the unreleased project roadmap.

**Could it be exploited or manipulated?**
**Internal Misuse / Misconfiguration:** A designer could accidentally bypass intended balancing parameters (e.g., giving a card 9999 attack damage) because the local tool lacks authoritative limits.
**Data Leakage:** If the repository access is compromised externally via stolen credentials, the local `.uasset` parameter arrays are exposed to attackers.

**What happens if it is compromised?**
A compromised or misconfigured card pushed to the main branch could crash the game loop for the whole team, break the automatic build pipeline, or lead to accidentally shipping severely unbalanced elements to players.

### 2. Proposed Mitigations

- **Access Control:** Enforce strict **Role-Based Access Control (RBAC)** on the version control repository. Developers can only push to individual feature branches.
- **Protocol Choice:** All version control network traffic (pushing/pulling) must use the **SSH** protocol or **HTTPS** secured with TLS. 
- **Encryption Required:** Dev machines must utilize Full Disk Encryption (e.g., BitLocker) to secure local assets in the event hardware is stolen.
- **Authentication Method:** Require **Multi-Factor Authentication (MFA)** for all GitHub/Perforce accounts on the team to prevent credential scraping.
- **Logging and Auditing:** Rely on the Git commit history and pull request logs to audit exactly who authored and modified specific special ability cards.
- **Data Minimisation:** Ensure the EUW script only writes necessary card parameters into the `.uasset` and strips out any underlying workstation metadata (like local Windows usernames or explicit IP configurations).

### 3. Networking Additions (Improving a Local Tool)

*The Card Creator currently operates locally as a standalone widget. How could networking improve it?*

**How could networking improve it?**
- **Centralised Validation:** Moving from a purely local script to a **Client–Server model** would significantly improve trust in the data. When a designer hits "Create Card" in the EUW, the widget could send an HTTP payload to an internal, authoritative service. This internal server cross-references the requested card stats against current algorithmic balance margins and approves or rejects the creation.
- **Version Control Integration:** Networking could automate the deployment process. Upon creating a valid card, an API call could trigger a continuous integration bot to automatically draft a pull request and notify the team on a shared dashboard.

**Does networking add value or unnecessary complexity?**
For a small indie team, building a dedicated authoritative validation server for an internal tool adds **unnecessary complexity**. Standard Git hooks and manual pull request approvals are sufficient to evaluate local `.uasset` data. However, for a massive live-service studio where hundreds of cards are made weekly, offloading validation to a centralised network dashboard adds tremendous value by programmatically ensuring build stability and preventing overpowered parameters from entering the final pipeline.
