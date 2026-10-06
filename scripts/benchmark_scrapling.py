"""Benchmark: Scrapling's adaptive relocation vs. Spoor's tier-3 self-healing,
on the identical §5.3 mutation corpus (closes #151).

Not a shipped capability — a one-off, reproducible measurement, filed as a
question per issue #151: "Scrapling scores better" is something concrete to
learn from and adapt into tier 3; "Scrapling scores worse" is a measured,
defensible competitive claim instead of an assumed one. Either way the result
goes into a docs/ROADMAP.md decision note, not new product code.

Reuses the *exact* page, target element, and mutation-op implementations
`tests/test_healing_mutation.py` defines (same import, not a reimplementation)
so both tools are judged on literally the same markup under literally the same
mutations — only the plan-generation source differs: the real test draws its
300-plan batch from `hypothesis` under `derandomize=True`, which is
reproducible across runs of the *same* Hypothesis version but not guaranteed
stable across Hypothesis versions and not meant to be called from outside a
`@given`-wrapped test. This script instead drives `_APPLY`'s mutation
functions directly with a plain, explicitly-seeded `random.Random`, so the
plan batch — and therefore the generated mutated HTML — is reproducible from
one fixed constant, independent of either tool's own internals.

For each of N plans, two *separate* fresh parses of the same `_PAGE` string
are mutated in place with the same op sequence (same seed, so the sequences of
random choices each `_APPLY` function consumes are identical) — one for each
tool — so each tool's success check can use plain lxml object identity against
its own tree's pre-mutation target, with no cross-tool interference from
mutating a shared tree.

Run: python scripts/benchmark_scrapling.py
"""

from __future__ import annotations

import random
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tests"))

from lxml import html as lxml_html  # noqa: E402
from lxml.html import HtmlElement  # noqa: E402
from parsel import Selector as ParselSelector  # noqa: E402
from scrapling import Selector as ScraplingSelector  # noqa: E402
from test_healing_mutation import (  # noqa: E402
    _APPLY,
    _MUTATIONS,
    _PAGE,
    _TARGET_ID,
    _elements,
)

from spoor.core.healing import fingerprint, heal  # noqa: E402

_CORPUS_SIZE = 300
# Fixed, explicit, version-independent — unlike the real test's Hypothesis
# derandomize, this seed is a plain constant anyone can reproduce by reading
# this file, with no dependency on Hypothesis's internal choice sequence.
_MASTER_SEED = 0xC0FFEE


@dataclass(frozen=True)
class Plan:
    ops: tuple[str, ...]
    seed: int


def _generate_plans(count: int, master_seed: int) -> list[Plan]:
    """The same shape `_plans()` draws from hypothesis — 1-5 unique mutation
    ops plus a per-plan seed — generated with a plain, explicitly-seeded RNG
    instead, so the batch is reproducible independent of Hypothesis itself."""
    rng = random.Random(master_seed)
    plans = []
    for _ in range(count):
        k = rng.randint(1, 5)
        ops = tuple(rng.sample(_MUTATIONS, k))
        plans.append(Plan(ops=ops, seed=rng.randrange(2**31 - 1)))
    return plans


def _mutated_tree(plan: Plan) -> tuple[HtmlElement, HtmlElement]:
    """A fresh parse of `_PAGE`, mutated in place by `plan`. Returns the tree
    root and the target element, captured *before* mutation so the identity
    check holds regardless of what the mutation does to the target's own
    attributes/text."""
    tree = lxml_html.fromstring(_PAGE)
    target = tree.get_element_by_id(_TARGET_ID)
    rng = random.Random(plan.seed)
    for op in plan.ops:
        _APPLY[op](tree, rng)
    return tree, target


def _tier3_heals(plan: Plan) -> bool:
    clean = lxml_html.fromstring(_PAGE)
    stored = fingerprint(ParselSelector(root=clean.get_element_by_id(_TARGET_ID)))
    mutated, target = _mutated_tree(plan)
    candidates = [ParselSelector(root=el) for el in _elements(mutated)]
    result = heal(stored, candidates)
    return result is not None and result.element.root is target


def _scrapling_heals(plan: Plan) -> bool:
    # Calls `.relocate()` directly rather than going through `.css(adaptive=
    # True)`: the latter takes a shortcut when the literal selector still
    # happens to match post-mutation (a plan that never touches the id, say)
    # and returns that direct hit *without ever exercising its scorer* — an
    # "easy win" heal() has no equivalent of, since heal() is always called
    # unconditionally in the real corpus. Calling relocate() directly forces
    # Scrapling's scorer to run on every plan, the same way heal()'s is,
    # for a true scorer-vs-scorer comparison rather than one that credits
    # Scrapling for cases its literal selector got right by accident.
    clean = lxml_html.fromstring(_PAGE)
    clean_target = clean.get_element_by_id(_TARGET_ID)
    mutated, target = _mutated_tree(plan)
    # percentage=0: always take Scrapling's best guess, the same "no refusal,
    # always a ranked answer" shape heal() has — a fair best-guess-accuracy
    # comparison, not "did it also clear Scrapling's own default threshold".
    matches = ScraplingSelector(root=mutated, adaptive=True).relocate(
        clean_target, percentage=0
    )
    return bool(matches) and matches[0] is target


def main() -> None:
    plans = _generate_plans(_CORPUS_SIZE, _MASTER_SEED)

    tier3_hits = 0
    scrapling_hits = 0
    per_op: dict[str, list[int]] = {}  # op -> [n, tier3_hits, scrapling_hits]

    for plan in plans:
        t3 = _tier3_heals(plan)
        scr = _scrapling_heals(plan)
        tier3_hits += t3
        scrapling_hits += scr
        for op in plan.ops:
            row = per_op.setdefault(op, [0, 0, 0])
            row[0] += 1
            row[1] += t3
            row[2] += scr

    n = len(plans)
    print(f"Mutation corpus: {n} plans, seed=0x{_MASTER_SEED:X}\n")
    print(f"{'tool':<12} {'hits':>6} {'rate':>8}")
    print(f"{'tier-3':<12} {tier3_hits:>6} {tier3_hits / n:>8.1%}")
    print(f"{'scrapling':<12} {scrapling_hits:>6} {scrapling_hits / n:>8.1%}")
    print(
        "\nPer-mutation-class breakdown (a plan may use several ops; counted in each):"
    )
    print(f"{'op':<18} {'n':>5} {'tier-3':>10} {'scrapling':>10}")
    for op in sorted(per_op):
        n_op, t3_op, scr_op = per_op[op]
        print(f"{op:<18} {n_op:>5} {t3_op / n_op:>9.1%} {scr_op / n_op:>10.1%}")


if __name__ == "__main__":
    main()
