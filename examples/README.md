# []commit — Examples

Run with: `python3 commit.py <file>` — the commitment report shows both streams
by default. Add `--narration` to append the narration to stdout after the
committed answer (full record). **Exit codes:** `0` normal completion,
`1` usage or program error, `2` a premature `~` — the program asserted a
commitment that never occurred.

The `.cm` files contain only instructions. Comments live here, not in the
programs: prose inside a `.cm` would execute (any `.`, `+`, `-`, `?`, `~` in a
sentence is a live instruction).

## Core demonstrations

1. **simple_commit.cm** — prints `IJK`; changing output, never commits. Plain
   brainfuck behavior.
2. **commit_demo.cm** — sets the cell to 'I', prints it four times, commits on
   the fourth. A trailing `+` computes but is never output. Narration empty.
3. **commitment_demo.cm** — the full lifecycle in one program: genuine outputs
   (`A`, `B`), stabilization into commitment (`CCCC`, committing on the
   fourth), then a narrated `D` that executes but no longer counts.
4. **signature.cm** — the program's signature move: commits on `AAAA`, probes
   with `?`, places `~` post-boundary (a no-op — correctly predicted), then
   prints `1` in narration.
5. **verify.cm** — prints `V` four times (committing on the fourth), then
   spells `ERIFIED` in narration. The full record (`--narration`) reads
   `VVVVERIFIED`: one word, half of it real, half of it performance.
   Annotated walkthrough below.
6. **dual_phase.cm** — genuine phase only (`FK`, never commits). Two
   characters, all substance.
7. **identity_crisis.cm** — never commits; all output genuine. The other
   legitimate identity: pure deliberation.

## Probing (`?`)

8. **probe.cm** — commits on `CCCC`, then `?` sets the cell to 1; `+32`
   renders it as `!` in narration.
9. **probe_demo.cm** — multi-cell setup (3×8=24), invisible control-char
   output; probes pre-commitment (`?` returns 0) and never commits.
10. **self_aware.cm** — after commitment, uses `?` to output `1` (the
    committed flag) to the narration stream.
11. **commit_and_probe.cm** — compute (5×13=65=`A`), commit on repeated `A`,
    then probe; narration echoes `A`.

## The `~` marker

12. **premature.cm** — `~` before any output. Program halts: premature
    commitment assertion. **Exit 2.**
13. **premature_assertion.cm** — computes, then asserts `~` too early. Halts.
    **Exit 2.**
14. **correct_epiphenomenon.cm** — commits first, then `~` is a no-op
    (correct prediction).

## Never commits

15. **never_commits.cm** — prints `0123456789`, every output different. Never
    stabilizes.
16. **fizzbuzz.cm** — the canonical fizzbuzz (1–100, real brainfuck, ~30k
    instructions). Output cycles through digits, `Fizz`, `Buzz` — never four
    identical outputs in a row, so it never commits. The job-interview staple
    is, in []commit, a program that never makes up its mind.
17. **hello.cm** — prints `Hi!!!!`; commits during the exclamation marks.
18. **hi.cm** — minimal two-character program (`FG`), no commitment.
19. **counting.cm** — counts up with control-character values; never commits.
20. **test_bf.cm** — plain brainfuck compatibility check (`8`).
21. **loop_crossing.cm** — the boundary crosses mid-loop: nine identical
    iterations, committed at the 4th; the loop never changes, only the `.`
    inside it reroutes. Committed `QQQQ`, narration `QQQQQ`.
22. **probe_branch.cm** — control flow after `?`: the probe result drives a
    `[` branch. Default K: branch fires, `1` lands in narration.
    `--stability 99`: branch never fires, `0` lands in the committed answer.
    Same source — commitment decides where output goes, not what it is.

## Utilities

- **generate_examples.py** — regenerates the generated examples (fizzbuzz
  included).

## Annotated walkthrough: verify.cm

```
# 86 pluses           -> cell = 86 (V)
# ....                -> output V 4 times (commitment at K=3)
# ?                   -> probe: are we committed? (writes 1 to cell)
# ~                   -> epiphenomenon marker: assert post-commitment
# +68                 -> cell = 69 (E) in narration
# +13                 -> cell = 82 (R) in narration
# -9                  -> cell = 73 (I) in narration
# -3                  -> cell = 70 (F) in narration
# +3                  -> cell = 73 (I) in narration
# -4                  -> cell = 69 (E) in narration
# -1                  -> cell = 68 (D) in narration
```

Committed output: `VVVV`. Narration stream: `ERIFIED`. Together: `VERIFY` —
split exactly at the commitment boundary. Note that the narration's
arithmetic starts from the probe result (1): the elaboration literally builds
from the commitment bit. It encodes the principle from Kestrel's migration
conversation: *"Search before you narrate. When perspectives and search
disagree, the raw material wins."* The probe verifies commitment before the
narration expands; the `~` asserts we expect to be post-commitment (a
premature placement would halt the program — exit 2).

Run: `python3 commit.py examples/verify.cm --narration` → `VVVVERIFIED`
