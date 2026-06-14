#!/usr/bin/env python3
"""Test suite for []commit interpreter."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from commit import load_program, run, match_brackets, COMMANDS, VALID

def test_basic_bf():
    """Standard brainfuck programs should work identically pre-commitment."""
    # Print 'A' (65 pluses then dot)
    prog = '+' * 65 + '.'
    program = [c for c in prog if c in VALID]
    committed, narration, meta = run(program, stability=10)  # high K so no commit

    assert committed == 'A', f"Expected 'A', got {repr(committed)}"
    assert not meta['committed'], "Should not commit with 1 output and K=10"
    print("✓ Basic brainfuck: print 'A'")

def test_commitment_boundary():
    """After K identical outputs, the program commits."""
    # Print 'A' 5 times, with K=3, should commit after 3rd identical output
    prog = '+' * 65 + '.' + '.' + '.' + '.' + '.'
    program = [c for c in prog if c in VALID]
    committed, narration, meta = run(program, stability=3)

    assert meta['committed'], "Should have committed"
    # After 3 identical 'A' outputs, it commits. The 4th and 5th go to narration.
    # Wait: output 'A' (stability_counter=0), output 'A' (counter=1), output 'A' (counter=2)...
    # K=3 means 3 consecutive unchanged outputs. After 1st '.', counter=0. After 2nd '.', same value, counter=1.
    # After 3rd '.', same value, counter=2. After 4th '.', same value, counter=3 >= K=3 → committed!
    # So output 1-4 are committed (4th triggers commit but is still written to committed output
    # because it's the one that DETECTS the boundary). Output 5 is epiphenomenal.
    # Actually let me re-read the logic...
    # After each '.', we check: stability_counter >= stability
    # 1st '.': last=None, counter=0. 0 >= 3? No.
    # 2nd '.': same value, counter=1. 1 >= 3? No.
    # 3rd '.': same value, counter=2. 2 >= 3? No.
    # 4th '.': same value, counter=3. 3 >= 3? YES → commit!
    # So 4th output IS committed (it triggers commitment but still goes to committed_output).
    # 5th output is epiphenomenal.
    assert committed == 'AAAA', f"Expected 'AAAA', got {repr(committed)}"
    assert narration == 'A', f"Expected 'A' narration, got {repr(narration)}"
    print(f"✓ Commitment boundary: committed={repr(committed)}, narration={repr(narration)}")

def test_probe_pre_commitment():
    """? should return 0 before commitment."""
    # Set cell to some value, probe, then check if it's 0
    prog = '+' * 5 + '?'     # cell=5, then probe → cell becomes 0
    # Then add 48 to get '0' char and output
    prog += '+' * 48 + '.'
    program = [c for c in prog if c in VALID]
    committed, narration, meta = run(program, stability=10)

    # cell starts 0, +5 = 5, ? → cell = 0 (pre-boundary), +48 = 48, . → '0'
    assert committed == '0', f"Expected '0', got {repr(committed)}"
    assert not meta['committed'], "Should not commit"
    print("✓ Pre-commitment probe returns 0")

def test_probe_post_commitment():
    """? should return 1 after commitment."""
    # Print 'A' enough times to commit, then probe
    # With K=3: need 4 identical outputs (1st sets counter=0, then 3 more identical → commit at 4th)
    # Actually: 1st '.' counter=0, 2nd counter=1, 3rd counter=2, 4th counter=3 → committed after 4th
    # So after 4 'A's, we're committed. Then probe should set cell to 1.
    # But cell is 65 (ASCII A). After commitment, ? sets cell to 1.
    # Then we can output that.
    prog = '+' * 65 + '....'   # Print 'A' 4 times, commit at 4th with K=3
    # Now we're committed. Cell is still 65. Probe makes it 1.
    # Then output: narration stream.
    prog += '?' + '.'           # ? sets cell to 1, . outputs narration char(1)=SOH
    program = [c for c in prog if c in VALID]
    committed, narration, meta = run(program, stability=3)

    assert meta['committed'], "Should have committed"
    assert committed == 'AAAA', f"Expected 'AAAA', got {repr(committed)}"
    # After commitment: ? sets cell to 1, then . outputs chr(1) to narration
    assert len(narration) == 1, f"Expected 1 narration char, got {len(narration)}"
    assert narration == chr(1), f"Expected SOH, got {repr(narration)}"
    print("✓ Post-commitment probe returns 1")

def test_epiphenomenon_marker_pre_commitment():
    """~ reached pre-boundary should halt the program."""
    prog = '~'   # Immediately hit epiphenomenon marker
    program = [c for c in prog if c in VALID]
    committed, narration, meta = run(program, stability=3)

    assert meta['premature_epiphenomenon'], "Should halt on premature ~"
    assert meta['premature_pc'] == 0, f"Expected pc=0, got {meta['premature_pc']}"
    print("✓ Premature epiphenomenon marker halts program")

def test_epiphenomenon_marker_post_commitment():
    """~ reached post-boundary should be a no-op."""
    # Commit first, then hit ~
    prog = '+' * 65 + '....' + '~'   # Commit, then ~ is a no-op
    program = [c for c in prog if c in VALID]
    committed, narration, meta = run(program, stability=3)

    assert meta['committed'], "Should have committed"
    assert not meta['premature_epiphenomenon'], "~ should be no-op post-boundary"
    print("✓ Post-boundary epiphenomenon marker is no-op")

def test_epiphenomenal_output():
    """Post-boundary . should write to narration, not committed output."""
    # Commit on 'A's, then output different chars post-boundary
    prog = '+' * 65 + '....'   # 4 'A's, commit at 4th (K=3)
    # Now output 'B' (66). Should go to narration.
    prog += '+' + '.'           # cell: 65→66, output 'B' to narration
    program = [c for c in prog if c in VALID]
    committed, narration, meta = run(program, stability=3)

    assert committed == 'AAAA', f"Expected 'AAAA', got {repr(committed)}"
    assert narration == 'B', f"Expected 'B' narration, got {repr(narration)}"
    print(f"✓ Post-boundary output goes to narration")

def test_k_equals_1():
    """K=1 should commit on second identical output."""
    # K=1: 1 consecutive identical output triggers commitment
    # 1st '.': new value → counter=0. 0 >= 1? No.
    # 2nd '.': same value → counter=1. 1 >= 1? YES → commit!
    prog = '+' * 65 + '..'   # Two identical 'A' outputs, K=1
    program = [c for c in prog if c in VALID]
    committed, narration, meta = run(program, stability=1)

    assert meta['committed'], "Should commit with K=1"
    assert committed == 'AA', f"Expected 'AA', got {repr(committed)}"
    print(f"✓ K=1 commits on second identical output")

def test_different_outputs_no_commit():
    """Continually changing outputs should never commit."""
    # Print 1, 2, 3, 4, 5 (different each time) — never stabilizes
    prog = ''
    for i in range(5):
        prog += '+' * (48 + i) + '.'
        prog += '-' * (48 + i)  # reset to 0
    # Wait, that doesn't work in bf because cells accumulate
    # Let's use multiple cells
    # Actually simpler: just set different values and output
    # Cell 0 = 49 ('1'), output, then increment to 50 ('2'), output, etc.
    prog = '+' * 49 + '.'    # '1'
    prog += '+' + '.'         # '2'
    prog += '+' + '.'         # '3'
    prog += '+' + '.'         # '4'
    prog += '+' + '.'         # '5'
    program = [c for c in prog if c in VALID]
    committed, narration, meta = run(program, stability=3)

    assert not meta['committed'], "Should not commit with changing output"
    assert committed == '12345', f"Expected '12345', got {repr(committed)}"
    print("✓ Changing outputs never commit")

def test_post_boundary_computation():
    """Data tape operations continue after commitment."""
    # Commit, then modify tape and branch
    prog = '+' * 65 + '....'   # Commit on 'A's (K=3)
    # Now: cell=65. Let's decrement and output different chars to narration
    prog += '-----'             # cell: 65 → 60 ('<')
    prog += '.'                 # narration: '<'
    prog += '+++++++'           # cell: 60 → 67 ('C')
    prog += '.'                 # narration: 'C'
    program = [c for c in prog if c in VALID]
    committed, narration, meta = run(program, stability=3)

    assert committed == 'AAAA', f"Expected 'AAAA', got {repr(committed)}"
    assert narration == '<C', f"Expected '<C' narration, got {repr(narration)}"
    print("✓ Post-boundary computation works on data tape")

def test_probe_branching():
    """Program can branch on ? to behave differently pre/post boundary."""
    # Pre-boundary: compute normally. Post-boundary: switch to narration mode.
    # Set up cell with value 65, output 'A' 4 times to commit (K=3)
    # Then: ? sets cell to 1 (committed). Use that to output chr(1+47)='0' vs chr(0+48)='0'
    # More interesting: use ? to decide what to output
    prog = '+' * 65            # cell = 65 ('A')
    prog += '....'             # output 'A' 4 times → commit at 4th (K=3)
    # Now committed. ? sets cell to 1.
    prog += '?'                # cell = 1
    # Add 47 to get 48 ('0') and output
    prog += '+' * 47 + '.'    # cell = 48, narration: '0'
    program = [c for c in prog if c in VALID]
    committed, narration, meta = run(program, stability=3)

    assert meta['committed'], "Should have committed"
    assert committed == 'AAAA', f"Expected 'AAAA', got {repr(committed)}"
    assert narration == '0', f"Expected '0' narration, got {repr(narration)}"
    print("✓ ? probe enables post-boundary branching")

if __name__ == '__main__':
    test_basic_bf()
    test_commitment_boundary()
    test_probe_pre_commitment()
    test_probe_post_commitment()
    test_epiphenomenon_marker_pre_commitment()
    test_epiphenomenon_marker_post_commitment()
    test_epiphenomenal_output()
    test_k_equals_1()
    test_different_outputs_no_commit()
    test_post_boundary_computation()
    test_probe_branching()
    print("\n✓ All tests passed!")