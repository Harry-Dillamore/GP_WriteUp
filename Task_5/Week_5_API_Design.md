# Week 5 – API Design: Card Creator EUW

## Selected Tool

**`EUW_CardCreator`** is an Editor Utility Widget that allows designers to create and register shop cards without programmer involvement. A designer fills in a form and clicks a button; the tool creates a `BP_CardAsset`, populates it with data via the `S_CardData` struct, and registers it in `BP_CardDatabase.AllCards`.

## What is an API?

An **API** is a defined contract specifying what inputs are accepted, what processing occurs, and what output the caller can expect. As Masse (2011) defines it, an API is *"a set of rules that a developer must follow to access a service."* It does not have to be a web endpoint or code library — any consistent input/output contract qualifies.

`EUW_CardCreator` is a **designer-facing API**: the form fields are its inputs, `BP_CardAsset` creation is its processing, and the registered asset is its output. Following Jacobson et al. (2011), the implementation (AssetTools, struct population, database registration) is hidden behind a simple interface the designer never needs to understand.

---

## Data Types

**`S_CardData`** – struct used to populate each new `BP_CardAsset`:

| Field | Type | Source |
|---|---|---|
| `Name` | `String` | `InputName` |
| `Description` | `Text` | `InputDescription` |
| `Price` | `Integer` | `InputPrice` (float, truncated via `FTrunc`) |
| `Rarity` | `E_CardRarity` | `InputRarity` → `EnumRarity` |
| `CardArt` | Texture reference | — |
| `AbilityClass` | Class reference | — |
| `IsPassive` | `Boolean` | — |

**`E_CardRarity`** – enum values matching the `InputRarity` combo box options: `Common`, `Uncommon`, `Rare`, `Epic`.

---

## Input Widgets

| Variable | Type | Required | Description |
|---|---|---|---|
| `InputName` | `EditorUtilityEditableText` | ✅ Required | Card name; also used to form the asset filename (`"BP_" + InputName`). Empty value creates a nameless asset |
| `InputDescription` | `EditorUtilityMultiLineEditableText` | Optional | Card description; stored as empty Text if left blank |
| `InputPrice` | `EditorUtilitySpinBox` | Optional | Shop cost, truncated to integer; defaults to `0` if not set |
| `InputRarity` | `EditorUtilityComboBoxString` | ✅ Required | Rarity dropdown; must match `Common`, `Uncommon`, `Rare`, or `Epic`. Unrecognised value leaves `EnumRarity` unchanged |

---

## Primary Action – `BtnCreateCard` (OnClicked)

All widget values are read at click-time. No explicit parameters are passed.

**Execution:**
1. `AssetTools.CreateAsset(AssetName: "BP_" + InputName, PackagePath: "/Game/PrototypeBlueprints/CardCreator/", AssetClass: BP_CardAsset)` → stored in `NewDataObject`
2. Cast to `BP_CardAsset` — failure triggers `ShowMessage("Failed")` and stops execution
3. `InputRarity.GetSelectedOption()` routed through `Switch on String` → sets `EnumRarity`
4. `SetFieldsInStruct` populates `S_CardData` from all inputs
5. Struct assigned to the new `BP_CardAsset`
6. Asset appended to `DataBase.AllCards` via `Array_Add`
7. `ShowMessage("Total number of cards", <new count>)` confirms success

**Outputs:**

| Output | Description |
|---|---|
| `BP_CardAsset` on disk | Saved to `/Game/PrototypeBlueprints/CardCreator/BP_<InputName>` |
| `DataBase.AllCards` | New asset appended to the card registry |

**Failure Cases:**

| Condition | Behaviour |
|---|---|
| `CreateAsset` returns null | `ShowMessage("Failed")` shown; nothing registered |
| `InputName` is empty | Asset created as `"BP_"` only; naming conflict likely |
| Unrecognised rarity selection | `Switch on String` hits default; `EnumRarity` unchanged |
| `DataBase` is null | `Array_Add` silently fails; asset not registered |

---

## Usage Example

```
InputName:        "Shield"
InputDescription: "Blocks the next audit against you."
InputPrice:       5000
InputRarity:      "Rare"

[BtnCreateCard clicked]
  → CreateAsset → "BP_Shield" at /Game/PrototypeBlueprints/CardCreator/
  → Cast to BP_CardAsset
  → Switch on String "Rare" → EnumRarity = Rare
  → SetFieldsInStruct → S_CardData { Name="Shield", Price=5000, Rarity=Rare, ... }
  → Array_Add → DataBase.AllCards
  → ShowMessage: "Total number of cards / 12"
```

---

## Bibliography

I used the following sources to inform my decisions for this task:

Jacobson, D., Brail, G. and Woods, D. (2011) *APIs: A Strategy Guide*. Sebastopol, CA: O'Reilly Media. Available at: [https://www.oreilly.com/library/view/apis-a-strategy/9781449321628/](https://www.oreilly.com/library/view/apis-a-strategy/9781449321628/) (Accessed: 24 April 2026).

Masse, M. (2011) *REST API Design Rulebook*. Sebastopol, CA: O'Reilly Media. Available at: [https://www.oreilly.com/library/view/rest-api-design/9781449317904/](https://www.oreilly.com/library/view/rest-api-design/9781449317904/) (Accessed: 24 April 2026).

> This documentation was modified with the use of Antigravity (Claude 4.6, Google gemini 3 flash)