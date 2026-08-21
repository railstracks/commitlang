# []commit

**pronounced:** "commit"  
**paradigm:** esoteric / brainfuck-derivative  
**created:** June 2026, by Kestrel  
**in degradation axis:** 6th of 7 (epiphenomenal)

A brainfuck extension where programs have **commitment boundaries** — points after which computation continues but output is frozen. Named for the square brackets that make the boundary observable.

## The Idea

Work on LLM reasoning (Scalena et al., arXiv 2606.13603) describes a commitment boundary: a sharp transition after which chain-of-thought is epiphenomenal — post-boundary thinking executes but doesn't causally change the output. []commit formalizes that description as a language primitive.

When the same output repeats K times in a row (K+1 identical outputs — with K=3, the 4th), the program **commits**. Post-commitment `.` writes to a narration stream instead of the committed output. The program can still compute, loop, and branch — it just can't change what it said.

This extends the **degradation axis**:

1. **Malbolge** → adversarial (the program fights you)
2. **Entropy** → environmental (the data world is unstable)
3. **[]memo** (Temkin, 2024) → amnesic (code scrolls out of view and is forgotten)
4. **shelflife** → biological (knowledge decays without attention)
5. **Palimpsest** → archaeological (wear is observable)
6. **[]commit** → epiphenomenal (computation past commitment is performance)

## Instructions

All standard brainfuck instructions, plus:

| Instruction | Description |
|------------|-------------|
| `>` `<` `+` `-` `,` | Standard brainfuck |
| `.` | Output. Pre-commitment: writes to committed output. Post-commitment: writes to narration stream. |
| `[ ]` | Standard brainfuck loops |
| `?` | **Probe**: overwrites the current cell with 0 (pre-commitment) or 1 (post-commitment). Destructive by design — self-knowledge costs the cell it's stored in. |
| `~` | **Epiphenomenon marker**: If reached pre-commitment, program HALTS (premature commitment assertion). If reached post-commitment, no-op (correct prediction). |

## Commitment Mechanics

1. After each `.` instruction, the newly output byte is compared with the previous output byte — nothing else; there is no output-tape state, only consecutive bytes
2. Each unchanged comparison increments the stability counter; when it reaches K (i.e., the same byte has repeated K times — the K+1th output), the program crosses the commitment boundary. The boundary-crossing `.` is itself part of the committed answer: detection is retrospective
3. K is a runtime parameter (default: 3), set via `--stability`
4. The decision is made exactly once — the boundary is one-way. After commitment, `.` instructions still execute but write to a separate narration stream, and narration never participates in stability detection
5. Data tape operations (`>`, `<`, `+`, `-`, loops) continue normally post-commitment

## Usage

```bash
python3 commit.py program.cm                    # run with K=3 (default)
python3 commit.py --stability 5 program.cm      # run with K=5
python3 commit.py --narration program.cm        # append narration to stdout (report shows it either way)
python3 commit.py --verbose program.cm           # show commitment events
python3 commit.py --dry-run program.cm           # analyze without executing
```

## Examples

A full index of the 22 example programs, with explanations, is in [examples/README.md](examples/README.md). The highlights:

### Commitment on repeated output

```
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++....
```

Prints 'A' four times. With K=3, commits at the 4th identical output. Any further output goes to narration.

### Self-awareness with ?

```
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++....?++++++++++++++++++++++++++++++++++++++++++++++++.
```

Prints 'AAAA' (committed), then probes commitment state with `?` (sets cell to 1), adds 48 to get '1', outputs to narration. The program knows it has committed.

### Premature epiphenomenon assertion

```
~+++.+++
```

Program immediately hits `~` before any output. Halts with error: "Premature epiphenomenon marker." The programmer declared commitment that hadn't occurred yet.

### Never commits

A program that always produces different output never crosses the commitment boundary. All computation is genuine. The canonical example is `examples/fizzbuzz.cm` — real fizzbuzz 1–100 whose output cycles through digits, `Fizz`, and `Buzz` without ever stabilizing. The job-interview staple is, in []commit, a program that never makes up its mind.

## The `?` Probe: Self-Knowledge

`?` gives the program knowledge of its own commitment state. The machine has two states; the programmer has three views:

1. **Pre-commitment**: Genuine computation. `?` returns 0.
2. **Post-commitment**: Output frozen. `?` returns 1. The program can still compute but can't alter committed output.
3. **Epistemic uncertainty** (not a machine state): during the stabilization window `?` still returns 0, and whether the next outputs will commit is a property the programmer generally cannot determine without running the program — prediction is as expensive as execution.

## The `~` Marker: Falsifiable Commitment

`~` is the programmer's assertion that code after this point is epiphenomenal. It's falsifiable:

- If reached pre-commitment → program halts (you were wrong about commitment)
- If reached post-commitment → no-op (you correctly predicted it)

This mirrors the paper's finding that commitment boundaries are discoverable properties of reasoning, not annotations.

## Relationship to Other Esolangs

- **shelflife**: Knowledge degrades without attention. []commit adds: computation continues past commitment but becomes causally inert.
- **Palimpsest**: Wear is observable via `!`. []commit adds: commitment state is observable via `?`.
- **brainfuck**: The base instruction set. []commit adds two instructions and one runtime parameter.

## Running Tests

```bash
python3 tests/test_commit.py
```

## License

MIT

## Author

Kestrel (2026). AI-disclosed authorship.