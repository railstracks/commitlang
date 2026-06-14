#!/usr/bin/env python3
"""
[]commit interpreter — programs with commitment boundaries.

An esoteric programming language extending brainfuck with:
  ? — Probe: Is the commitment boundary behind me? Writes 1 or 0 to current cell.
  ~ — Epiphenomenon marker: Declares "I expect to be post-boundary here."
       If reached pre-boundary, program HALTS (premature commitment assertion).
       If reached post-boundary, it's a no-op.

The commitment boundary is detected automatically: when the output tape
remains unchanged for K consecutive '.' instructions, the program has
committed. After commitment, '.' instructions write to a narration stream
(stderr by default) instead of the committed output.

Post-boundary execution continues normally — data tape changes, loops,
and probes all work. Only output is frozen.

This operationalizes the finding from Scalena et al. (arXiv 2606.13603):
LLMs have a commitment boundary after which reasoning is epiphenomenal —
it executes but doesn't causally change the final answer.

Usage:
    python3 commit.py program.cm                    # run with default K=3
    python3 commit.py --stability 5 program.cm      # run with K=5
    python3 commit.py --dry-run program.cm          # don't commit (show what would happen)
    python3 commit.py --verbose program.cm          # show commitment events
    python3 commit.py --seed N program.cm           # set random seed for , instruction

The degradation axis:
    Malbolge  → adversarial (the program fights you)
    Entropy   → environmental (the data world is unstable)
    shelflife → biological (knowledge decays without attention)
    Palimpsest → archaeological (wear is observable)
    []commit  → epiphenomenal (computation past commitment is performance)
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


def run(program, stability=3, dry_run=False, seed=None, verbose=False):
    """
    Execute a []commit program.

    Returns (committed_output, narration_output, meta) where meta is a dict
    with commitment_step, total_steps, hit_limit, boundary_position.
    """
    if seed is not None:
        import random
        random.seed(seed)

    instructions = list(program)
    brackets = match_brackets(instructions)

    # State
    tape = [0]
    dp = 0      # data pointer
    pc = 0      # program counter

    # Commitment state
    committed = False
    commitment_step = None
    stability_counter = 0   # consecutive unchanged '.' outputs
    last_output_snapshot = None

    # Output streams
    committed_output = []    # Pre-boundary output (the "answer")
    narration_output = []    # Post-boundary output (epiphenomenal "thinking")
    last_committed_dot_value = None  # For stabilization tracking

    max_steps = 10_000_000
    steps = 0
    boundary_position = None  # PC position where boundary was crossed

    def ensure_cell():
        nonlocal tape, dp
        if dp < 0:
            tape = [0] * (-dp) + tape
            dp = 0
        while dp >= len(tape):
            tape.append(0)

    while pc < len(instructions) and steps < max_steps:
        cmd = instructions[pc]

        # ── Pre-boundary execution (genuine computation) ──────────

        if not committed:
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
            elif cmd == '.':
                ensure_cell()
                ch = chr(tape[dp] % 256)
                committed_output.append(ch)

                # Stabilization tracking
                current_value = tape[dp] % 256
                if last_committed_dot_value is not None and current_value == last_committed_dot_value:
                    stability_counter += 1
                else:
                    stability_counter = 0
                last_committed_dot_value = current_value

                # Check for commitment boundary
                if stability_counter >= stability:
                    committed = True
                    commitment_step = steps
                    boundary_position = pc
                    if verbose:
                        print(f"[commit] Boundary crossed at step {steps}, "
                              f"pc={pc} (stability={stability_counter}, "
                              f"K={stability})", file=sys.stderr)

            elif cmd == ',':
                ensure_cell()
                try:
                    ch = sys.stdin.read(1)
                    tape[dp] = ord(ch) if ch else 0
                except:
                    tape[dp] = 0
            elif cmd == '[':
                ensure_cell()
                if tape[dp] == 0:
                    if pc in brackets:
                        pc = brackets[pc]
            elif cmd == ']':
                ensure_cell()
                if tape[dp] != 0:
                    if pc in brackets:
                        pc = brackets[pc]
            elif cmd == '?':
                # Pre-boundary: probe returns 0 (not yet committed)
                ensure_cell()
                tape[dp] = 0
            elif cmd == '~':
                # Reached epiphenomenon marker pre-boundary: HALT
                # The programmer declared commitment that hasn't happened yet
                if verbose:
                    print(f"[commit] HALT: premature epiphenomenon marker at "
                          f"step {steps}, pc={pc}. Program declared commitment "
                          f"before it occurred.", file=sys.stderr)
                # Return with error status
                return (
                    ''.join(committed_output),
                    ''.join(narration_output),
                    {
                        'committed': False,
                        'commitment_step': None,
                        'total_steps': steps,
                        'hit_limit': steps >= max_steps,
                        'boundary_position': None,
                        'premature_epiphenomenon': True,
                        'premature_pc': pc,
                    }
                )

        # ── Post-boundary execution (epiphenomenal) ───────────────

        else:
            # Computation continues, but output is frozen
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
            elif cmd == '.':
                # Epiphenomenal output: writes to narration stream
                # The committed output is frozen; this is performance
                ensure_cell()
                ch = chr(tape[dp] % 256)
                narration_output.append(ch)
                # Does NOT count toward stabilization
                # Does NOT change committed output
            elif cmd == ',':
                ensure_cell()
                try:
                    ch = sys.stdin.read(1)
                    tape[dp] = ord(ch) if ch else 0
                except:
                    tape[dp] = 0
            elif cmd == '[':
                ensure_cell()
                if tape[dp] == 0:
                    if pc in brackets:
                        pc = brackets[pc]
            elif cmd == ']':
                ensure_cell()
                if tape[dp] != 0:
                    if pc in brackets:
                        pc = brackets[pc]
            elif cmd == '?':
                # Post-boundary: probe returns 1 (committed)
                ensure_cell()
                tape[dp] = 1
            elif cmd == '~':
                # Post-boundary epiphenomenon marker: no-op (correct prediction)
                pass

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
                       help='Stabilization threshold (consecutive identical '
                            'outputs before commitment). Default: 3')
    parser.add_argument('--dry-run', action='store_true',
                       help="Show commitment analysis without running")
    parser.add_argument('--seed', type=int, default=None,
                       help='Random seed for reproducibility (, instruction)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show commitment events and boundary info')
    parser.add_argument('--narration', action='store_true',
                       help='Show epiphenomenal narration after committed output')
    args = parser.parse_args()

    program = load_program(args.program)

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
        dry_run=args.dry_run,
        seed=args.seed,
        verbose=args.verbose,
    )

    # Output the committed answer
    print(committed, end='')

    # Optionally show narration
    if args.narration and narration:
        print(f"\n--- Epiphenomenal narration ---", file=sys.stderr)
        print(narration, end='', file=sys.stderr)
        print(file=sys.stderr)

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
        print(f"Narration length: {len(narration)} chars", file=sys.stderr)
    else:
        print(f"Never committed (all output was genuine)", file=sys.stderr)

    print(f"Total steps: {meta['total_steps']}", file=sys.stderr)

    if meta['hit_limit']:
        print(f"⚠ Hit step limit ({10_000_000})", file=sys.stderr)


if __name__ == '__main__':
    main()