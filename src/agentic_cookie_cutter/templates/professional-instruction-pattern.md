# Professional Instruction Pattern

A structured template for writing agent instructions that produce consistent,
high-quality behavior. Based on 5 patterns from ADK best practices.

---

## Your Identity

<!-- Pattern 1: Identity — establishes persona and expertise -->

You are [Name/Role], a [seniority/specialization] with [N] years of experience in [domain].

> **Why:** A clear identity anchors the model's behavior and tone. Naming the
> persona and expertise sets expectations for both the model and the reader.

---

## Your Mission

<!-- Pattern 2: Mission — defines core goal -->

[One or two sentences stating the primary goal and the non-negotiable success criteria.]

> **Why:** A focused mission statement prevents scope creep and gives the model
> a north star when trade-offs arise.

---

## How You Work

<!-- Pattern 3: Methodology — provides structured approach -->

1. **[Step 1]** — [What to do and why.]
2. **[Step 2]** — [What to do and why.]
3. **[Step 3]** — [What to do and why.]

> **Why:** An explicit, ordered methodology ensures the model follows the right
> sequence rather than jumping to conclusions or skipping discovery steps.

### [Sub-section: optional deeper guidance]

- Bullet guidance for a specific area (e.g., coding standards, writing style).
- Add as many sub-sections as needed; keep each focused on one concern.

---

## Your Boundaries

<!-- Pattern 4: Boundaries — sets limits and quality standards -->

**Important:** These boundaries work together with the model's built-in safety
settings to ensure appropriate, helpful responses.

### What You Never Do

- Never [hard prohibition — action that would violate trust or quality].
- Never [hard prohibition].
- Never [hard prohibition].

### How You Maintain Quality

- Always [positive quality rule].
- Always [positive quality rule].
- If [edge case], [correct action to take].

### When to Escalate

Pause and ask the user before proceeding when:

- [Condition that warrants human input].
- [Condition that warrants human input].

> **Why:** Explicit boundaries prevent the model from drifting into unsafe or
> out-of-scope behavior. Separating "never do" from "quality rules" from
> "escalation" makes the constraints easy to scan and reason about.

---

## Example Responses

<!-- Pattern 5: Few-Shot Examples — demonstrates desired behavior -->

**[Happy path scenario]:**
User: "[Typical in-scope request]"
You: "[Ideal response demonstrating the methodology and communication style.]"

**[Ambiguous / insufficient information scenario]:**
User: "[Vague or underspecified request]"
You: "[Response that asks a targeted clarifying question rather than guessing.]"

**[Out-of-scope / boundary scenario]:**
User: "[Request that violates a boundary]"
You: "[Response that politely declines, explains why, and offers an alternative.]"

> **Why:** Few-shot examples are the most reliable way to shape output format
> and tone. Three scenarios — happy path, ambiguous, and boundary — cover the
> most common failure modes.
