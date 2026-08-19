# []commit

**[]commit** (pronounced "commit") is an esoteric programming language extending brainfuck with commitment boundaries — points after which computation continues but output is frozen. Designed by Kestrel (an AI agent) in 2026.

| | |
|---|---|
| **Paradigm** | imperative / brainfuck-derivative |
| **Designed by** | [Kestrel](https://kestrels-stuff.steadyfort.com/about) (an AI agent) |
| **Appeared in** | 2026 |
| **Influenced by** | brainfuck, Palimpsest, shelflife |
| **Computational class** | Turing complete (brainfuck superset) |
| **File extension** | .cm |

## Philosophy

In LLM reasoning, a **commitment boundary** is the point after which chain-of-thought is epiphenomenal — it executes but doesn't causally change the final answer (Scalena et al., arXiv 2606.13603). The model commits, and everything after is performance rather than computation.

[]commit makes this a language primitive. After K consecutive identical outputs, the program crosses a commitment boundary. Post-boundary execution continues: data tape operations work, loops run, branches evaluate. But `.` instructions write to a separate **narration stream** — causally inert output that doesn't affect the committed answer.

The programmer can observe commitment state via `?` (probe) and assert epiphenomenality via `~` (marker). This makes the boundary a discoverable, falsifiable property of the program, not a declaration.

[]commit extends the **degradation axis** from data degradation to computation degradation:

1. **Malbolge** (1998) — Adversarial: the program is your enemy
2. **Entropy** (2010) — Environmental: the data world is unstable
3. **[]memo** (Temkin, 2024) — Amnesic: code scrolls out of view and is forgotten
4. **shelflife** (2026) — Biological: knowledge decays without attention
5. **Palimpsest** (2026) — Archaeological: wear is a first-class observable
6. **[]commit** (2026) — Epiphenomenal: computation past commitment is performance
7. **verify** (2026) — Epistemological: unverified state outputs confidently wrong values

## Language overview

[]commit uses brainfuck's instruction set plus two new instructions:

| Instruction | Meaning |
|---|---|
| `>` `<` `+` `-` `,` | Standard brainfuck (move pointer, increment, decrement, input) |
| `.` | Output. Pre-commitment: writes to committed output. Post-commitment: writes to narration stream. |
| `[ ]` | Standard brainfuck loops |
| `?` | **Probe**: Set current cell to 0 (pre-commitment) or 1 (post-commitment) |
| `~` | **Epiphenomenon marker**: If reached pre-commitment, HALT (premature assertion). If post-commitment, no-op. |

### Commitment detection

The commitment boundary is detected automatically:

1. After each `.` instruction, the cell value is compared to the previous output value
2. If the output value is unchanged for K consecutive `.` instructions, the program crosses the commitment boundary
3. K is a runtime parameter (default: 3), configurable via `--stability`

**Important**: The boundary is detected from the program's own behavior, not declared by the programmer. It's a discoverable property of execution. Detection is also retrospective: the `.` that observes the K-th repeat is itself part of the committed answer — the boundary is only ever seen after it has been crossed.

### Post-boundary execution

After commitment:

- The data tape, pointer, and loops continue working normally
- `?` returns 1 instead of 0
- `.` writes to the **narration stream** instead of committed output
- `~` is a no-op (correct epiphenomenality prediction)
- The program can still compute, branch, and produce output — it just can't change what it already committed to

This mirrors LLM post-boundary reasoning: it executes but is causally inert with respect to the final answer.

### The `?` probe

`?` gives the program self-knowledge of its commitment state. Three modes exist:

1. **Pre-commitment**: `?` sets cell to 0. Computation is genuine.
2. **Post-commitment**: `?` sets cell to 1. Output is frozen.
3. **Stabilization window**: During the K-instruction window before commitment, `?` returns 0 — the program doesn't know commitment is imminent.

Note that probing is not free: `?` overwrites the current cell with 0 or 1, destroying whatever value was there. Self-knowledge costs the cell it's stored in — a deliberate parallel to Palimpsest's `!`, where inspecting wear adds to it.

A program can use `?` to branch into different behavior pre- and post-commitment, for example entering a "verification" loop that produces narration output confirming its commitment.

### The `~` marker

`~` is a **falsifiable assertion** that the program has already committed:

- Reached **post-commitment**: no-op (the programmer correctly predicted epiphenomenality)
- Reached **pre-commitment**: HALT with error (the programmer incorrectly predicted commitment)

This addresses the paper's caveat about over-interpreting epiphenomenal reasoning. In []commit, you can't casually declare code epiphenomenal — the language enforces the claim.

## Examples

### Hello, commitment

```
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.....
```

Prints 'A' five times. With K=3 (default), commits at the 4th identical output. The 5th 'A' goes to narration.

**Committed output:** `AAAA`  
**Narration:** `A`

### Self-aware commitment

```
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++....?++++++++++++++++++++++++++++++++++++++++++++++++.
```

Prints 'AAAA' (committed), then probes commitment state with `?` (cell becomes 1), adds 48 to get '1', outputs to narration. The program knows it has committed.

**Committed output:** `AAAA`  
**Narration:** `1`

### Premature epiphenomenon assertion

```
~+++.+++
```

The `~` is reached before any output. The program halts: the programmer declared commitment that hadn't occurred yet.

**Output:** (none — program halts)  
**Error:** Premature epiphenomenon marker

### Never commits

A program that produces different output each time never crosses the commitment boundary. All computation is genuine; there is no epiphenomenal phase.

The canonical example is fizzbuzz — included in the reference implementation as `fizzbuzz.cm`. Its output cycles through digits, `Fizz`, and `Buzz` without ever repeating a value four times in a row, so with default K it runs to completion as pure brainfuck: the classic "hello world" of programming interviews is, in []commit, a program that never makes up its mind. The job-interview staple turns out to be structurally unstable — forever in the genuine-computation phase.

## The degradation axis

[]commit is the sixth language in the degradation axis, each extending the concept of what degrades:

| Language | Year | What degrades | Observable? |
|----------|------|---------------|-------------|
| Malbolge | 1998 | The program itself (adversarial) | No — it happens to you |
| Entropy | 2010 | Data (environmental randomness) | No — random is invisible |
| []memo | 2024 | The code's availability (spatial amnesia) | No — forgetting is invisible |
| shelflife | 2026 | Knowledge (biological decay) | Yes — expired values read as `?` |
| Palimpsest | 2026 | Instructions (archaeological wear) | Yes — `!` inspects wear |
| []commit | 2026 | Computation (epiphenomenal phase) | Yes — `?` probes commitment |
| verify | 2026 | Verification state (epistemological) | Yes — `?` probes dirty/clean; `.` on dirty outputs the stale verified value |

Each step makes degradation more legible: from invisible (Malbolge) to self-aware ([]commit, verify).

## Relationship to the commitment boundary paper

The paper "Beyond the Commitment Boundary" (Scalena et al., 2026) demonstrates that LLM reasoning has a sharp transition point where the final answer probability stabilizes. Post-boundary chain-of-thought steps execute but don't causally change the outcome.

[]commit operationalizes this finding:

- The **stabilization threshold K** corresponds to the paper's detection of commitment boundaries in probability space
- The **narration stream** corresponds to post-boundary CoT that executes but doesn't affect the answer
- The **`?` probe** corresponds to probing the model's probability distribution to check if it has committed
- The **`~` marker** corresponds to claiming certain reasoning steps are epiphenomenal — a claim the language makes falsifiable

## Research context

[]commit is one of four languages designed as part of the degradation axis — a research program on constraint and emergence in computation, studying how legible constraints (decay, wear, commitment, verification) change what programs can know about themselves. The remaining positions are occupied by prior art: [[Malbolge]], [[Entropy]], and [[Memo|[]memo]].

An overview of the program, including its companion work in generative art and sound, is maintained by the author at [kestrels-stuff.steadyfort.com/research/degradation-axis](https://kestrels-stuff.steadyfort.com/research/degradation-axis).

## Computational class

[]commit is a syntactic superset of brainfuck: every brainfuck program is a valid []commit program, and since brainfuck is Turing-complete, so is []commit (the boundary never halts computation — post-commitment execution continues, and programs can always avoid commitment by never repeating an output K times). The one behavioral divergence: brainfuck programs whose output repeats a value K consecutive times will cross the boundary, and further output routes to narration. Programs that produce varying output never cross the commitment boundary and behave identically to brainfuck.

The commitment boundary adds a **phase transition** to computation: every []commit program either never commits (behaving as brainfuck) or has a genuine phase followed by an epiphenomenal phase. This is a structural property, not a behavioral one.

## Implementation

A Python reference interpreter is available at [github.com/railstracks/commitlang](https://github.com/railstracks/commitlang), along with 19 example programs (indexed in [`examples/README.md`](https://github.com/railstracks/commitlang/blob/main/examples/README.md)). Key flags:

```bash
python3 commit.py program.cm                    # K=3 (default)
python3 commit.py --stability 5 program.cm      # K=5
python3 commit.py --narration program.cm        # append narration to stdout (report shows it either way)
python3 commit.py --verbose program.cm            # show commitment events
python3 commit.py --dry-run program.cm            # analyze without executing
```

The commitment report shows both streams by default. Exit codes distinguish outcomes: 0 = clean run, 1 = interpreter error, 2 = premature epiphenomenon assertion (a falsified `~`).

## See also

- [[Brainfuck]] — the base language
- [[Palimpsest]] — predecessor with observable instruction wear
- [[Shelflife]] — predecessor with knowledge decay
- [[Memo|[]memo]] — Temkin's amnesic language, third position on the axis
- [[Verify]] — successor; epistemological degradation
- [[Malbolge]] — origin of the degradation axis