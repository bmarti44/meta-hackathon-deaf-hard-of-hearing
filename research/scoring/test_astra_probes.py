"""Astra-review contract probes for gate_table v2 (run from research/scoring)."""
import sys
sys.path.insert(0, "research/scoring")
from gate_table import Row, build_gate_matrix, effective_verdict

def r(gate, window, verdict, tier="T4", grade="Moderate", cand="X"):
    return Row(cand, "P", gate, window, "", tier, grade, None, None, None, None, verdict)

# Probe 1: G2 W3 PASS + G2 W0 INSUFFICIENT -> G2 PASS (mechanism excluded)
m = build_gate_matrix([r("G2", "W3", "PASS"), r("G2", "W0", "INSUFFICIENT")])
assert m["X"]["G2"] == "PASS", m
# Probe 2: T0/VeryLow PASS -> INSUFFICIENT
v, w = effective_verdict(r("G1", "W3", "PASS", tier="T0", grade="VeryLow"))
assert v == "INSUFFICIENT" and w
v, w = effective_verdict(r("G1", "W3", "PASS", tier="T2", grade="UNASSESSED"))
assert v == "INSUFFICIENT" and w
# Probe 3: legitimate PASS survives
v, w = effective_verdict(r("G2", "W3", "PASS", tier="T4", grade="High"))
assert v == "PASS" and w is None
print("ASTRA PROBES PASS")
