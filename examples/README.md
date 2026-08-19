# []commit — Examples

Run with: `python3 commit.py <file>` — the commitment report shows both streams by default. Add `--narration` to append the narration to stdout after the committed answer (full record).

## Core demonstrations

1. **simple_commit.cm** — prints `IJK`; changing output, never commits. Plain brainfuck behavior.
2. **commit_demo.cm** — sets the cell to 'I', prints it four times, commits on the fourth. A trailing `+` computes but is never output. Narration empty.
3. **signature.cm** — the program's signature move: commits on `AAAA`, probes with `?`, places `~` post-boundary (a no-op — correctly predicted), then prints `1` in narration.
4. **verify.cm** — prints `V` four times (committing on the fourth), then spells `ERIFIED` in narration. The full record (`--narration`) reads `VVVVERIFIED`: one word, half of it real, half of it performance.
5. **dual_phase.cm** — genuine phase only (`FK`, never commits). Two characters, all substance.
6. **identity_crisis.cm** — never commits; all output genuine. The other legitimate identity: pure deliberation.

## Probing (`?`)

7. **probe.cm** — commits on `CCCC`, then `?` sets the cell to 1; `+32` renders it as `!` in narration.
8. **probe_demo.cm** — multi-cell setup (3×8=24), invisible control-char output; probes pre-commitment (`?` returns 0) and never commits.
9. **self_aware.cm** — after commitment, uses `?` to output `1` (the committed flag) to the narration stream.
10. **commit_and_probe.cm** — compute (5×13=65=`A`), commit on repeated `A`, then probe; narration echoes `A`.

## The `~` marker

11. **premature.cm** — `~` before any output. Program halts: premature commitment assertion.
12. **premature_assertion.cm** — computes, then asserts `~` too early. Halts.
13. **correct_epiphenomenon.cm** — commits first, then `~` is a no-op (correct prediction).

## Never commits

14. **never_commits.cm** — prints `0123456789`, every output different. Never stabilizes.
15. **fizzbuzz.cm** — the canonical fizzbuzz (1–100, real brainfuck, ~30k instructions). Output cycles through digits, `Fizz`, `Buzz` — never four identical outputs in a row, so it never commits. The job-interview staple is, in []commit, a program that never makes up its mind.
16. **hello.cm** — prints `Hi!!!!`; commits during the exclamation marks.
17. **hi.cm** — minimal two-character program (`FK`), no commitment.
18. **counting.cm** — counts up with control-character values; never commits.
19. **test_bf.cm** — plain brainfuck compatibility check (`8`).

## Utilities

- **generate_examples.py** — regenerates the generated examples (fizzbuzz included).
