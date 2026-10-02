"""Unit tests for `Politeness.acquire`/`release` (ROADMAP.md §2d, #174).

The `.feature` scenarios prove genuine thread/timing behavior end to end
through a real server; these pin the concurrency primitive's exact logic
deterministically — semaphore bounds, per-domain independence, and that a
domain's first-ever dispatch never sleeps — using a fake `sleep` and real
`threading.Thread`s (for real blocking/ordering) rather than wall-clock
assertions.
"""

from __future__ import annotations

import threading
import time

import httpx

from spoor.core.config import PolitenessPolicy
from spoor.operational.politeness import Politeness


def _gate(max_concurrent_per_domain: int = 1, delay: float | None = None) -> Politeness:
    policy = PolitenessPolicy(
        delay=delay, max_concurrent_per_domain=max_concurrent_per_domain
    )
    # No real network: every call in these tests stays within the
    # already-known-domain concurrency/delay bookkeeping, never touching
    # robots.txt.
    client = httpx.Client(transport=httpx.MockTransport(lambda r: httpx.Response(404)))
    return Politeness(policy, client, sleep=lambda _s: None)


def test_first_dispatch_never_sleeps() -> None:
    sleeps: list[float] = []
    gate = _gate(delay=5.0)
    gate._sleep = sleeps.append
    gate.acquire("http://x.test/a")
    gate.release("http://x.test/a")
    assert sleeps == []


def test_second_dispatch_to_same_domain_sleeps_the_delay() -> None:
    sleeps: list[float] = []
    gate = _gate(delay=5.0)
    gate._sleep = sleeps.append
    gate.acquire("http://x.test/a")
    gate.release("http://x.test/a")
    gate.acquire("http://x.test/b")
    gate.release("http://x.test/b")
    assert sleeps == [5.0]


def test_different_domains_each_get_their_own_first_free_dispatch() -> None:
    sleeps: list[float] = []
    gate = _gate(delay=5.0)
    gate._sleep = sleeps.append
    gate.acquire("http://one.test/a")
    gate.release("http://one.test/a")
    gate.acquire("http://two.test/a")
    gate.release("http://two.test/a")
    assert sleeps == []


def test_semaphore_bounds_concurrent_acquires_to_the_cap() -> None:
    gate = _gate(max_concurrent_per_domain=2)
    order: list[str] = []
    barrier_lock = threading.Lock()
    held = 0
    max_held = 0

    def worker(name: str) -> None:
        nonlocal held, max_held
        gate.acquire(f"http://x.test/{name}")
        with barrier_lock:
            held += 1
            max_held = max(max_held, held)
        time.sleep(0.05)
        with barrier_lock:
            held -= 1
        order.append(name)
        gate.release(f"http://x.test/{name}")

    threads = [threading.Thread(target=worker, args=(f"p{i}",)) for i in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=5)

    # Not just "never exceeded" -- proves the cap actually permits 2
    # concurrent holders, not that it silently behaves like a cap of 1.
    assert max_held == 2
    assert len(order) == 5


def test_release_frees_the_slot_for_the_next_acquire() -> None:
    # A cap of 1: the second acquire must not block forever waiting on a slot
    # the first acquire's release already freed.
    gate = _gate(max_concurrent_per_domain=1)
    gate.acquire("http://x.test/a")
    gate.release("http://x.test/a")
    acquired = threading.Event()

    def worker() -> None:
        gate.acquire("http://x.test/b")
        acquired.set()
        gate.release("http://x.test/b")

    t = threading.Thread(target=worker)
    t.start()
    t.join(timeout=2)
    assert acquired.is_set()
