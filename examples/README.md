[]commit — Signature Examples
================================

These examples demonstrate the language's key features.
Run with: python3 commit.py <file> --narration --verbose

1. commit_and_probe.cm — Commit on repeated output, then probe state
   The program prints 'A' until commitment, then uses ? to verify.
   
2. premature.cm — Premature epiphenomenon assertion
   The ~ marker is reached before any output. Program halts.
   
3. never_commits.cm — Always-changing output never commits
   Produces different values each time. All computation is genuine.
   
4. self_aware.cm — Program that knows it committed
   After commitment, uses ? to output '1' (the committed flag)
   to the narration stream.