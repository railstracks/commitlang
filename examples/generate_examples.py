#!/usr/bin/env python3
"""Generate []commit example programs."""

def char_to_bf(ch):
    """Generate bf code to set current cell to ord(ch) and output it."""
    code = ord(ch)
    # Find best factor pair for multiplication
    best_len = code + 1  # just +
    best_prog = '+' * code
    for i in range(1, 20):
        q, r = divmod(code, i)
        if q > 0 and q < 30:
            prog = '+' * i + '[>' + '+' * q + '<-]>'
            prog += '+' * r + '.'
            # reset: move back to cell 0
            # Actually we need to handle multi-cell state
            if len(prog) < best_len:
                best_len = len(prog)
                best_prog = prog
    # Simple version: just +
    if len('+' * code) < best_len:
        return '+' * code + '.'
    return best_prog

# Example 1: commitment_demo.cm
# Prints "ABC" then commits on repeated "C"s, then outputs "D" to narration
prog = ""
prog += "+" * 65 + "."   # A
prog += "+" * 1 + "."    # B (66)  
prog += "+" * 1 + "."    # C (67)
prog += "...."           # 4 more C's → commit at 4th (K=3)
prog += "+" * 1 + "."    # D → narration
with open("examples/commitment_demo.cm", "w") as f:
    f.write(prog)

# Example 2: probe.cm
# Prints enough identical chars to commit, then uses ? to detect boundary
# After commitment, outputs 'Y' (89) to narration; before would output 'N' (78)
prog = ""
prog += "+" * 67           # cell 0 = 67 ('C')
prog += "...."             # output CCCC → commit at 4th (K=3)
prog += "?"                # probe: cell becomes 1 (committed)
prog += "+" * 78           # cell: 1 + 78 = 79... no wait
# I want: after ?, cell=1 (committed). Add 87 → 88 ('X'). Output to narration.
# OR: before ?, cell=0. Add 78 → 78 ('N'). But we're post-commitment so cell=1.
# 1 + 78 = 79. Not great.
# Better: use ? result to compute differently.
# After commitment: cell=1 (from ?). Want to output '!' (33): 1 + 32 = 33.
prog = ""
prog += "+" * 67           # cell 0 = 67 ('C')
prog += "...."             # commit
prog += "?"                # cell = 1
prog += "+" * 32 + "."    # 1 + 32 = 33 = '!' → narration
with open("examples/probe.cm", "w") as f:
    f.write(prog)

# Example 3: premature.cm — a program that halts on premature ~
prog = "~"
with open("examples/premature.cm", "w") as f:
    f.write(prog)

# Example 4: never_commits.cm — always different output
prog = ""
for i in range(10):
    prog += "+" * (48 + i) + "." + "-" * (48 + i)
    # Wait, this doesn't reset to 0 in bf properly
# Better: use separate cells
prog = ""
for i in range(10):
    prog += ">"             # move to next cell
    prog += "+" * (48 + i)  # set to '0'+i
    prog += "."              # output
with open("examples/never_commits.cm", "w") as f:
    f.write(prog)

print("Generated 4 example programs")