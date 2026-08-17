# verify.cm — "Search before you narrate"
#
# Committed output: VVVV
# Narration stream: ERIFIED
# Together: VERIFY — but split at the commitment boundary
#
# The committed answer is simple and stable (V, repeated).
# The elaboration (ERIFIED) is confident but causally inert —
# it executes but doesn't affect the committed output.
#
# This encodes the principle from Kestrel's migration conversation:
# "Search before you narrate. When perspectives and search disagree,
# the raw material wins." The probe (?) verifies commitment before
# the narration expands. The epiphenomenon marker (~) asserts that
# we expect to be post-commitment — if we weren't, the program would
# halt (premature assertion).
#
# Run: python3 commit.py --stability 3 --narration examples/verify.cm

# The program:
# 86 pluses -> cell = 86 (V)
# ....      -> output V 4 times (commitment at K=3)
# ?         -> probe: are we committed? (writes 1 to cell)
# ~         -> epiphenomenon marker: assert post-commitment
# +68       -> cell = 69 (E) in narration
# +13       -> cell = 82 (R) in narration
# -9        -> cell = 73 (I) in narration
# -3        -> cell = 70 (F) in narration
# +3        -> cell = 73 (I) in narration
# -4        -> cell = 69 (E) in narration
# -1        -> cell = 68 (D) in narration

# NOTE: This README is separate from the program file.
# The .cm file contains only valid brainfuck/[]commit instructions.