# Week 5 - Public-Facing API Design

## Selected Feature: GameAnalytics Telemetry Validation Service (REST API)

As explored in the Week 3 Security Evaluation, allowing the Unreal Engine client to send unverified telemetry directly to GameAnalytics exposes our metrics to spoofing. To resolve this, I implemented a **Custom Authoritative Telemetry Proxy** as an external **RESTful Web Service**. The Unreal Engine client sends data to this API, which validates the mathematical possibility of the events before securely forwarding them to the official GameAnalytics dashboard.

---

## 1. API Surface & Endpoints

### Endpoint: `POST /api/v1/telemetry/design-event`
**Description:** Captures standard gameplay events (like a specific card being played or a match ending) and validates them to prevent spam/spoofing.
**Parameters (JSON Body):**
- `player_id` (String, Required) - The unique UUID of the reporting player.
- `event_id` (String, Required) - The hierarchical GameAnalytics event string (e.g., `CardPlayed:Fireball:Win`).
- `match_id` (String, Required) - The active match session ID used to verify the event is occurring within an actual server instance.
- `value` (Float, Optional) - An optional numerical value attached to the event (e.g., damage dealt).

**Return Data / Outputs (JSON):**
- `status` (String) - Returns `"success"` or `"error"`.
- `forwarded` (Boolean) - `true` if the server deemed the event mathematically legitimate and securely forwarded it to GameAnalytics.

**Errors / Failure Cases:**
- `400 Bad Request` - Missing required parameters or an invalid JSON structure.
- `403 Forbidden` - The `match_id` does not correlate to an active, registered server instance.
- `429 Too Many Requests` - The client is attempting to fire events faster than mathematically possible in the normal game loop (Rate Limit / Anti-Cheat triggered).

---

### Endpoint: `POST /api/v1/telemetry/economy-event`
**Description:** Tracks virtual currency (VC) fluctuations. This node validates that currency added or subtracted strictly matches verified server-side match outcomes.
**Parameters (JSON Body):**
- `player_id` (String, Required) - The unique UUID of the player.
- `currency_type` (String, Required) - The string identifier of the currency (e.g., `GoldCoins`).
- `transaction_type` (Enum: `Source` | `Sink`, Required) - Whether the currency was earned (`Source`) or spent (`Sink`).
- `amount` (Integer, Required) - The exact amount of currency exchanged.
- `item_id` (String, Required) - What the currency was physically spent on or earned from (e.g., `MatchWin_Bonus` or `Shop_EpicCard`).

**Return Data / Outputs (JSON):**
- `status` (String) - Returns `"success"` or `"error"`.
- `validated_balance` (Integer) - The authoritative balance tracked internally by the server cache after the event.

**Errors / Failure Cases:**
- `400 Bad Request` - Missing parameters.
- `409 Conflict` - The client claims to have earned an `amount` that is impossible for the specified `item_id` (e.g., claiming 1,000,000 coins from a standard match).

---

## 2. Usage Example: REST Call Flow

Below is a minimal HTTP example demonstrating how the Unreal Engine client natively communicates with our REST validation proxy when a player legitimately spends in-game currency on a shop card.

**Request (from Unreal Engine Client):**
```http
POST /api/v1/telemetry/economy-event HTTP/1.1
Host: telemetry.greedypiggies.io
Authorization: Bearer <session_auth_token>
Content-Type: application/json

{
  "player_id": "usr_8f92j1k1",
  "currency_type": "GoldCoins",
  "transaction_type": "Sink",
  "amount": 25000,
  "item_id": "Shop_Purchase_Card_Peek"
}
```

**Response (from Validation Server):**
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "success",
  "message": "Economy event validated and safely forwarded to GameAnalytics.",
  "data": {
    "forwarded": true,
    "validated_balance": 180000
  }
}
```

By placing this robust REST API logically between the game client and the third-party GameAnalytics service, we effectively sanitize our data lake, preventing malicious users from ruining the critical economic balancing metrics of *Greedy Piggies*.
