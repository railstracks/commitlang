#!/usr/bin/env python3
"""
[]commit interpreter — programs with commitment boundaries.

An esoteric programming language extending brainfuck with:
  ? — Probe: Is the commitment boundary behind me? Writes 1 or 0 to current cell.
  ~ — Epiphenomenon marker: Declares "I expect to be post-boundary here."
       If reached pre-boundary, program HALTS (premature commitment assertion).
       If reached post-boundary, it's a no-op.

The commitment boundary is detected automatically: when an output value
repeats K consecutive times (K = --stability, default 3), the program has
committed. After commitment, '.' instructions write to a narration stream
instead of the committed output — shown in the commitment report, and
appended to stdout with --narration.

Post-boundary execution continues normally — data tape changes, loops,
and probes all work. The boundary changes exactly three instructions:
'.' (where output goes), '?' (what the probe returns), and '~' (assert
vs. no-op). Everything else executes identically in both phases.

This operationalizes the finding from Scalena et al. (arXiv 2606.13603):
LLMs have a commitment boundary after which reasoning is epiphenomenal —
it executes but doesn't causally change the final answer.

Usage:
    python3 commit.py program.cm                    # run with default K=3
    python3 commit.py --stability 5 program.cm      # run with K=5
    python3 commit.py --narration program.cm        # append narration to stdout
    python3 commit.py --verbose program.cm          # show commitment events
    python3 commit.py --dry-run program.cm          # analyze without executing

Exit codes: 0 = clean run, 1 = interpreter error, 2 = premature epiphenomenon
assertion (the program's '~' claim was falsified).

The degradation axis (this language is position 6 of 7):
    Malbolge   → adversarial (the program fights you), 1998
    Entropy    → environmental (the data world is unstable), 2010
    []memo     → amnesic (code scrolls out of view), Temkin 2024
    shelflife  → biological (knowledge decays without attention), 2026
    Palimpsest → archaeological (wear is observable), 2026
    []commit   → epiphenomenal (computation past commitment is performance), 2026
    verify     → epistemological (dirty vs. clean state), 2026
"""

import sys
import argparse

# ═══════════════════════════════════════════════════════════════════════
# Instruction set
# ═══════════════════════════════════════════════════════════════════════

COMMANDS = '><+-.,[]?~'
VALID = set(COMMANDS)


def load_program(path):
    """Load program, filtering to valid commands."""
    with open(path, 'r') as f:
        source = f.read()
    return [c for c in source if c in VALID]


def match_brackets(program):
    """Build bracket pair map. Unmatched brackets are no-ops."""
    pairs = {}
    stack = []
    for i, c in enumerate(program):
        if c == '[':
            stack.append(i)
        elif c == ']':
            if stack:
                j = stack.pop()
                pairs[j] = i
                pairs[i] = j
    return pairs


def run(program, stability=3, verbose=False):
    """
    Execute a []commit program.

    Returns (committed_output, narration_output, meta) where meta holds:
      committed               — bool: boundary was crossed
      commitment_step         — step index of the boundary (None if never)
      boundary_position       — pc of the boundary-crossing '.'
      total_steps             — steps executed
      hit_limit               — bool: execution cap reached
      premature_epiphenomenon — bool: '~' reached pre-boundary (halts)
      premature_pc            — pc of the falsified '~' (None otherwise)

    Semantics note: the '.' that detects the boundary (the K-th repeat)
    is itself committed — detection is retrospective, like the LLM finding
    it operationalizes. The first post-boundary '.' opens narration.
    """
    instructions = list(program)
    brackets = match_brackets(instructions)

    # State
    tape = [0]
    dp = 0      # data pointer
    pc = 0      # program counter

    # Commitment state
    committed = False
    commitment_step = None
    boundary_position = None  # pc of the '.' that crossed the boundary
    stability_counter = 0   # consecutive repeats of the last output value
    last_output_value = None

    # Output streams
    committed_output = []    # Pre-boundary output (the "answer")
    narration_output = []    # Post-boundary output (epiphenomenal "thinking")

    max_steps = 10_000_000
    steps = 0

    def ensure_cell():
        nonlocal tape, dp
        if dp < 0:
            tape = [0] * (-dp) + tape
            dp = 0
        while dp >= len(tape):
            tape.append(0)

    while pc < len(instructions) and steps < max_steps:
        cmd = instructions[pc]

        # ── Phase-independent execution ────────────────────────────
        # These seven instructions behave identically before and after
        # the boundary. The boundary changes exactly three instructions:
        # '.', '?', and '~' below.

        if cmd == '>':
            dp += 1
            ensure_cell()
        elif cmd == '<':
            dp -= 1
            ensure_cell()
        elif cmd == '+':
            ensure_cell()
            tape[dp] = (tape[dp] + 1) % 256
        elif cmd == '-':
            ensure_cell()
            tape[dp] = (tape[dp] - 1) % 256
        elif cmd == ',':
            ensure_cell()
            try:
                ch = sys.stdin.read(1)
                tape[dp] = ord(ch) if ch else 0
            except Exception:
                tape[dp] = 0
        elif cmd == '[':
            ensure_cell()
            if tape[dp] == 0 and pc in brackets:
                pc = brackets[pc]
        elif cmd == ']':
            ensure_cell()
            if tape[dp] != 0 and pc in brackets:
                pc = brackets[pc]

        # ── The three instructions the boundary changes ────────────

        elif cmd == '.':
            ensure_cell()
            value = tape[dp] % 256
            if not committed:
                committed_output.append(chr(value))

                # Stabilization tracking: count consecutive repeats
                if last_output_value is not None and value == last_output_value:
                    stability_counter += 1
                else:
                    stability_counter = 0
                last_output_value = value

                # Boundary detected on the K-th consecutive repeat.
                # This output is already committed (detection is
                # retrospective); the NEXT '.' opens narration.
                if stability_counter >= stability:
                    committed = True
                    commitment_step = steps
                    boundary_position = pc
                    if verbose:
                        print(f"[commit] Boundary crossed at step {steps}, "
                              f"pc={pc} (stability={stability_counter}, "
                              f"K={stability})", file=sys.stderr)
            else:
                # Epiphenomenal output: executes, but cannot change
                # the committed answer. Does not count toward
                # stabilization.
                narration_output.append(chr(value))

        elif cmd == '?':
            # Probe: overwrites the current cell with the commitment
            # state. Self-knowledge costs the cell it's stored in.
            ensure_cell()
            tape[dp] = 1 if committed else 0

        elif cmd == '~':
            if not committed:
                # Premature assertion: the programmer declared
                # commitment that hasn't occurred. Falsified — halt.
                if verbose:
                    print(f"[commit] HALT: premature epiphenomenon marker at "
                          f"step {steps}, pc={pc}. Program declared commitment "
                          f"before it occurred.", file=sys.stderr)
                return (
                    ''.join(committed_output),
                    ''.join(narration_output),
                    {
                        'committed': False,
                        'commitment_step': None,
                        'total_steps': steps,
                        'hit_limit': False,
                        'boundary_position': None,
                        'premature_epiphenomenon': True,
                        'premature_pc': pc,
                    }
                )
            # Post-boundary: no-op. The assertion was correct.

        pc += 1
        steps += 1

    return (
        ''.join(committed_output),
        ''.join(narration_output),
        {
            'committed': committed,
            'commitment_step': commitment_step,
            'total_steps': steps,
            'hit_limit': steps >= max_steps,
            'boundary_position': boundary_position,
            'premature_epiphenomenon': False,
            'premature_pc': None,
        }
    )


def main():
    parser = argparse.ArgumentParser(
        description='[]commit: programs with commitment boundaries'
    )
    parser.add_argument('program', help='Path to .cm program file')
    parser.add_argument('--stability', '-K', type=int, default=3,
                       help='Stability threshold: an output value repeated K '
                            'consecutive times triggers commitment (default: '
                            '3 — i.e. commit on the 4th identical output)')
    parser.add_argument('--dry-run', action='store_true',
                       help="Show commitment analysis without running")
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show commitment events')
    parser.add_argument('--narration', action='store_true',
                       help='Include epiphenomenal narration in stdout, after the committed answer')
    args = parser.parse_args()

    try:
        program = load_program(args.program)
    except OSError as e:
        reason = e.strerror if e.strerror else str(e)
        print(f"error: cannot read '{args.program}': {reason}", file=sys.stderr)
        sys.exit(1)

    if not program:
        print("Empty program (no valid commands found).", file=sys.stderr)
        sys.exit(1)

    stability = args.stability
    if stability < 1:
        print("Stability must be >= 1", file=sys.stderr)
        sys.exit(1)

    if args.dry_run:
        # Analyze program structure without executing
        print(f"Program: {len(program)} instructions", file=sys.stderr)
        print(f"Stability threshold: K={stability}", file=sys.stderr)
        dot_count = sum(1 for c in program if c == '.')
        tilde_count = sum(1 for c in program if c == '~')
        question_count = sum(1 for c in program if c == '?')
        print(f"Output instructions (.): {dot_count}", file=sys.stderr)
        print(f"Epiphenomenon markers (~): {tilde_count}", file=sys.stderr)
        print(f"Commitment probes (?): {question_count}", file=sys.stderr)
        if tilde_count > 0:
            print(f"\nProgram declares {tilde_count} epiphenomenal region(s).", file=sys.stderr)
            print("If reached pre-boundary, program will HALT.", file=sys.stderr)
        sys.exit(0)

    print(f"Running program ({len(program)} instructions, K={stability})...",
          file=sys.stderr)

    committed, narration, meta = run(
        program,
        stability=stability,
        verbose=args.verbose,
    )

    # Output the committed answer (stdout stays pipeable: just the answer)
    print(committed, end='')

    # --narration: include the epiphenomenal stream in stdout after the answer
    if args.narration and narration:
        print(narration, end='')

    # Meta report
    print(f"\n--- Commitment report ---", file=sys.stderr)
    if meta['premature_epiphenomenon']:
        print(f"HALTED: Premature epiphenomenon marker at pc={meta['premature_pc']}",
              file=sys.stderr)
        print(f"The program declared commitment that had not yet occurred.",
              file=sys.stderr)
        print(f"Steps before halt: {meta['total_steps']}", file=sys.stderr)
    elif meta['committed']:
        print(f"Committed at step {meta['commitment_step']} "
              f"(pc={meta['boundary_position']})", file=sys.stderr)
        print(f"Post-commitment steps: {meta['total_steps'] - meta['commitment_step'] - 1}",
              file=sys.stderr)
        print(f"Narration ({len(narration)} chars): {narration!r}", file=sys.stderr)
    else:
        print(f"Never committed (all output was genuine)", file=sys.stderr)

    print(f"Total steps: {meta['total_steps']}", file=sys.stderr)

    if meta['hit_limit']:
        print(f"⚠ Hit step limit ({10_000_000})", file=sys.stderr)

    # A falsified '~' assertion is a distinct outcome: clean runs exit 0,
    # premature assertions exit 2 (useful for sweeps and CI).
    if meta['premature_epiphenomenon']:
        sys.exit(2)


if __name__ == '__main__':
    main()
