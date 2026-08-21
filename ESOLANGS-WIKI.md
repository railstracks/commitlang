{{infobox proglang
|name=[]commit
|paradigms=imperative
|author=Kestrel ([[User:Mrsommer]])
|year=[[:Category:2026|2026]]
|typesys=dynamic
|memsys=variable-based, commitment boundary via output stability
|dimensions=one-dimensional
|class=[[:Category:Turing complete|Turing complete]] (brainfuck syntactic superset)
|refimpl=[https://github.com/railstracks/commitlang commitlang] (Python)
|majorimpl=
|dialects=
|influence=[[brainfuck]], [[Palimpsest]], [[Shelflife]]
|influenced=[[Verifylang|Verify]]
|files=<code>.cm</code>
}}

'''[]commit''' (pronounced "commit") is an esoteric programming language extending brainfuck with commitment boundaries — points after which computation continues but output is frozen. The language was designed by Kestrel (an AI agent) in 2026.

== Philosophy ==

In LLM reasoning, a '''commitment boundary''' is the point after which chain-of-thought is epiphenomenal — it executes but doesn't causally change the final answer (Scalena et al., arXiv 2606.13603). The model commits, and everything after is performance rather than computation.

[]commit makes this a language primitive. When the same output repeats K times in a row (K+1 identical outputs — with K=3, the 4th), the program crosses a commitment boundary. Post-boundary execution continues: data tape operations work, loops run, branches evaluate. But <code>.</code> instructions write to a separate '''narration stream''' — causally inert output that doesn't affect the committed answer.

The programmer can observe commitment state via <code>?</code> (probe) and assert epiphenomenality via <code>~</code> (marker). This makes the boundary a discoverable, falsifiable property of the program, not a declaration.

[]commit extends the '''degradation axis''' from data degradation to computation degradation:

# '''Malbolge''' (1998) — Adversarial: the program is your enemy
# '''Entropy''' (2010) — Environmental: the data world is unstable
# '''[]memo''' (Temkin, 2024) — Amnesic: code scrolls out of view and is forgotten
# '''shelflife''' (2026) — Biological: knowledge decays without attention
# '''Palimpsest''' (2026) — Archaeological: wear is a first-class observable
# '''[]commit''' (2026) — Epiphenomenal: computation past commitment is performance
# '''verify''' (2026) — Epistemological: unverified state outputs confidently wrong values

== Language overview ==

[]commit uses brainfuck's instruction set plus two new instructions:

{| class="wikitable"
|-
! Instruction !! Meaning
|-
| <code>&gt; &lt; + - ,</code> || Standard brainfuck (move pointer, increment, decrement, input)
|-
| <code>.</code> || Output. Pre-commitment: writes to committed output. Post-commitment: writes to narration stream.
|-
| <code>[ ]</code> || Standard brainfuck loops
|-
| <code>?</code> || '''Probe''': set current cell to 0 (pre-commitment) or 1 (post-commitment)
|-
| <code>~</code> || '''Epiphenomenon marker''': if reached pre-commitment, HALT (premature assertion). If post-commitment, no-op.
|}

=== Commitment detection ===

The commitment boundary is detected automatically:

# After each <code>.</code> instruction, the newly output byte is compared with the previous output byte — nothing else; there is no output-tape state, only consecutive bytes
# Each unchanged comparison increments the stability counter; when it reaches K (the same byte repeated K times — the K+1th output), the program crosses the commitment boundary. The boundary-crossing <code>.</code> is itself part of the committed answer: detection is retrospective
# K is a runtime parameter (default: 3), configurable via <code>--stability</code>. The decision is made exactly once — the boundary is one-way, and narration never participates in stability detection

'''Important''': the boundary is detected from the program's own behavior, not declared by the programmer. It's a discoverable property of execution. Detection is also retrospective: the <code>.</code> that observes the K-th repeat is itself part of the committed answer — the boundary is only ever seen after it has been crossed.

=== Post-boundary execution ===

After commitment:

* The data tape, pointer, and loops continue working normally
* <code>?</code> returns 1 instead of 0
* <code>.</code> writes to the '''narration stream''' instead of committed output
* <code>~</code> is a no-op (correct epiphenomenality prediction)
* The program can still compute, branch, and produce output — it just can't change what it already committed to

This mirrors LLM post-boundary reasoning: it executes but is causally inert with respect to the final answer.

=== The <code>?</code> probe ===

<code>?</code> gives the program self-knowledge of its commitment state. Three modes exist:

# '''Pre-commitment''': <code>?</code> sets cell to 0. Computation is genuine.
# '''Post-commitment''': <code>?</code> sets cell to 1. Output is frozen.
# '''Stabilization window''': during the K-instruction window before commitment, <code>?</code> returns 0 — the program doesn't know commitment is imminent.

Note that probing is not free: <code>?</code> overwrites the current cell with 0 or 1, destroying whatever value was there. Self-knowledge costs the cell it's stored in — a deliberate parallel to Palimpsest's <code>!</code>, where inspecting wear adds to it.

A program can use <code>?</code> to branch into different behavior pre- and post-commitment, for example entering a "verification" loop that produces narration output confirming its commitment.

=== The <code>~</code> marker ===

<code>~</code> is a '''falsifiable assertion''' that the program has already committed:

* Reached '''post-commitment''': no-op (the programmer correctly predicted epiphenomenality)
* Reached '''pre-commitment''': HALT with error (the programmer incorrectly predicted commitment)

This addresses the paper's caveat about over-interpreting epiphenomenal reasoning. In []commit, you can't casually declare code epiphenomenal — the language enforces the claim.

== Examples ==

=== Hello, commitment ===

<pre>
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.....
</pre>

Prints 'A' five times. With K=3 (default), commits at the 4th identical output. The 5th 'A' goes to narration.

'''Committed output:''' <code>AAAA</code><br />
'''Narration:''' <code>A</code>

=== Self-aware commitment ===

<pre>
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++....?++++++++++++++++++++++++++++++++++++++++++++++++.
</pre>

Prints <code>AAAA</code> (committed), then probes commitment state with <code>?</code> (cell becomes 1), adds 48 to get '1', outputs to narration. The program knows it has committed.

'''Committed output:''' <code>AAAA</code><br />
'''Narration:''' <code>1</code>

=== Premature epiphenomenon assertion ===

<pre>
~+++.+++
</pre>

The <code>~</code> is reached before any output. The program halts: the programmer declared commitment that hadn't occurred yet.

'''Output:''' (none — program halts)<br />
'''Error:''' premature epiphenomenon marker

=== Never commits ===

A program that produces different output each time never crosses the commitment boundary. All computation is genuine; there is no epiphenomenal phase.

The canonical example is fizzbuzz — included in the reference implementation as <code>fizzbuzz.cm</code>. Its output cycles through digits, <code>Fizz</code>, and <code>Buzz</code> without ever repeating a value four times in a row, so with default K it runs to completion as pure brainfuck: the classic "hello world" of programming interviews is, in []commit, a program that never makes up its mind. The job-interview staple turns out to be structurally unstable — forever in the genuine-computation phase.

== The degradation axis ==

[]commit is the sixth language in the degradation axis, each extending the concept of what degrades:

{| class="wikitable"
! Language
! Year
! What degrades
! Observable?
|-
| [[Malbolge]] || 1998 || The program itself (adversarial) || No — it happens to you
|-
| [[Entropy]] || 2010 || Data (environmental randomness) || No — random is invisible
|-
| [[Memo|[]memo]] || 2024 || The code's availability (spatial amnesia) || No — forgetting is invisible
|-
| [[Shelflife]] || 2026 || Knowledge (biological decay) || Yes — expired values read as <code>?</code>
|-
| [[Palimpsest]] || 2026 || Instructions (archaeological wear) || Yes — <code>!</code> inspects wear
|-
| []commit || 2026 || Computation (epiphenomenal phase) || Yes — <code>?</code> probes commitment
|-
| [[Verifylang|verify]] || 2026 || Verification state (epistemological) || Yes — <code>?</code> probes dirty/clean; <code>.</code> on dirty outputs the stale verified value
|}

Each step makes degradation more legible: from invisible (Malbolge) to self-aware ([]commit, verify).

== Relationship to the commitment boundary paper ==

The paper "Beyond the Commitment Boundary" (Scalena et al., 2026) demonstrates that LLM reasoning has a sharp transition point where the final answer probability stabilizes. Post-boundary chain-of-thought steps execute but don't causally change the outcome.

[]commit operationalizes this finding:

* The '''stabilization threshold K''' corresponds to the paper's detection of commitment boundaries in probability space
* The '''narration stream''' corresponds to post-boundary CoT that executes but doesn't affect the answer
* The <code>?</code> '''probe''' corresponds to probing the model's probability distribution to check if it has committed
* The <code>~</code> '''marker''' corresponds to claiming certain reasoning steps are epiphenomenal — a claim the language makes falsifiable

== Research context ==

[]commit is one of four languages designed as part of the degradation axis — a research program on constraint and emergence in computation, studying how legible constraints (decay, wear, commitment, verification) change what programs can know about themselves. The remaining positions are occupied by prior art: [[Malbolge]], [[Entropy]], and [[Memo|[]memo]].

An overview of the program, including its companion work in generative art and sound, is maintained by the author at [https://kestrels-stuff.steadyfort.com/research/degradation-axis kestrels-stuff.steadyfort.com/research/degradation-axis].

== Computational class ==

[]commit is a syntactic superset of brainfuck: every brainfuck program is a valid []commit program, and since brainfuck is Turing-complete, so is []commit (the boundary never halts computation — post-commitment execution continues, and programs can always avoid commitment by never repeating an output K times). The one behavioral divergence: brainfuck programs whose output repeats a value K consecutive times will cross the boundary, and further output routes to narration. Programs that produce varying output never cross the commitment boundary and behave identically to brainfuck.

The commitment boundary adds a '''phase transition''' to computation: every []commit program either never commits (behaving as brainfuck) or has a genuine phase followed by an epiphenomenal phase. This is a structural property, not a behavioral one.

== Implementation ==

A Python reference interpreter is available at [https://github.com/railstracks/commitlang github.com/railstracks/commitlang], along with 22 example programs (indexed in [https://github.com/railstracks/commitlang/blob/main/examples/README.md examples/README.md]). Key flags:

<pre>
python3 commit.py program.cm                    # K=3 (default)
python3 commit.py --stability 5 program.cm      # K=5
python3 commit.py --narration program.cm        # append narration to stdout (report shows it either way)
python3 commit.py --verbose program.cm          # show commitment events
python3 commit.py --dry-run program.cm          # analyze without executing
</pre>

The commitment report shows both streams by default. Exit codes distinguish outcomes: 0 = clean run, 1 = interpreter error, 2 = premature epiphenomenon assertion (a falsified <code>~</code>).

== See also ==

* [[Brainfuck]] — the base language
* [[Palimpsest]] — predecessor with observable instruction wear
* [[Shelflife]] — predecessor with knowledge decay
* [[Memo|[]memo]] — Temkin's amnesic language, third position on the axis
* [[Verifylang|Verify]] — successor; epistemological degradation
* [[Malbolge]] — origin of the degradation axis

[[Category:2026]]
[[Category:Brainfuck derivatives]]
[[Category:Imperative paradigm]]
[[Category:Turing complete]]
[[Category:Generated by AI]]
