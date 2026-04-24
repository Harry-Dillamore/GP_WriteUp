# Week 3 – Security & Compliance Evaluation: Card Creator Tool

## Selected Tool

The **Card Creation & Management Editor Utility Widget (EUW)** is a local Unreal Engine tool that generates `.uasset` Data Assets, assigns Blueprint Interfaces, and registers cards to a centralised array. It runs entirely locally; its only network interaction is indirect — generated assets are pushed to a public GitHub repository.

---

## 1. Threat Identification

**Network transmission.** The tool makes no direct network calls, but every `.uasset` it generates is committed to a public repository. Card stats, ability parameters, and balance values are therefore permanently visible by design. Any credentials accidentally committed alongside assets are immediately readable — automated bots scrape public repositories continuously, so exposure should be treated as instant (GitGuardian, 2024).

**Sensitive data exposure.** No player data is processed, so no direct GDPR liability exists. However, card stats and ability parameters represent commercial IP; leakage of pre-launch data could harm the product's competitive novelty.

**Asset manipulation.** `.uasset` files are binary and opaque to standard diff tools, meaning a poisoned asset — one with illegal stat values or a corrupted array reference — can merge undetected. This matches the supply-chain attack pattern where trusted binary artifacts are compromised before integration (Twingate, 2024). Separately, if the EUW's Blueprint graph were tampered with, malicious logic could execute silently during normal designer use.

| Threat                               | Impact                                                     |
| ------------------------------------ | ---------------------------------------------------------- |
| Credentials committed to public repo | Immediately exposed; history rewrite required to remediate |
| Poisoned `.uasset` merged            | Corrupted card data enters production build                |
| Central array overwritten            | All card references lost                                   |
| EUW Blueprint tampered               | Silent malicious execution in editor                       |

---

## 2. Threat Consideration

**Internal misuse** is the most likely vector. A designer could input out-of-range values, delete array entries, or commit a binary-conflicted asset — all without any enforcement layer currently in place.

**External attackers** could gain write access via compromised contributor credentials, allowing them to push poisoned assets or tamper with CI configuration.

**Misconfiguration.** Unreal Engine config files (e.g., `DefaultEngine.ini` overrides, plugin tokens) can be unintentionally tracked by Git and committed alongside card assets. GitGuardian (2024) found that 4.6% of active repositories leaked at least one secret, and over 90% remained valid five days after exposure — a significant risk given the repository is already public.

**Data leakage** can also occur informally; screenshots of the EUW interface may reveal unannounced card names or stats without any repository breach.

---

## 3. Mitigations

**Asset integrity.** The EUW should write a plaintext **`.json` manifest** alongside each generated asset, logging the creator, timestamp, and a hash of key parameters. This provides a text-diffable audit trail that compensates for the binary opacity of `.uasset` files. **Git LFS** should be enabled to prevent partial binary corruption on merge.

**CI validation.** A CI pipeline should run a headless Unreal commandlet on every commit touching a card asset, verifying fields are present and stats are within legal ranges. This enforces card validity at the pipeline level — directly addressing the risk that binary assets bypass human review.

**Credential hygiene.** The `.gitignore` must exclude Unreal config directories (`Saved/`, `Intermediate/`, `.ini` overrides) to prevent tokens being committed alongside card assets. GitHub's **push protection** should be enabled to block credential commits before they reach the public remote.

**Access control.** The **principle of least privilege** (NIST SP 800-53, 2020) should be applied: contributors only receive write access to the directories relevant to their role, limiting the blast radius of both accidental and deliberate asset corruption.

**GDPR.** The tool currently processes no personal data, so the **data minimisation principle** (UK GDPR, Article 5(1)(c); ICO, 2021) does not yet apply — but must be considered if the tool is extended to log activity or connect to an external service.

---

## 4. Networking Consideration

Currently, networking would add unnecessary complexity. The core risks — binary asset opacity, credential leakage, and undetected tampering — are addressable within the existing local-plus-Git workflow.

The **CI validation pipeline** is the one networking enhancement with clear justification. It delivers the primary benefit of a client–server trust model — authoritative enforcement of card validity — using existing infrastructure. A dedicated HTTPS validation endpoint would offer stronger enforcement at scale, but is disproportionate for this team size. The CI pipeline achieves the same outcome at negligible overhead.

---

## References

- GitGuardian (2024) _State of Secrets Sprawl 2024_. Available at: https://www.gitguardian.com/state-of-secrets-sprawl-report-2024 (Accessed: 22 April 2026).
- ICO (2021) _Data minimisation_. Information Commissioner's Office. Available at: https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/the-principles/data-minimisation/ (Accessed: 22 April 2026).
- NIST (2020) _Security and Privacy Controls for Information Systems and Organisations_, SP 800-53 Rev. 5. Available at: https://doi.org/10.6028/NIST.SP.800-53r5 (Accessed: 22 April 2026).
- Twingate (2024) _What is a Supply Chain Attack?_ Available at: https://www.twingate.com/blog/glossary/supply-chain-attack (Accessed: 22 April 2026).

> This documentation was modified with the use of Antigravity (Claude 4.6, Google gemini 3 flash)