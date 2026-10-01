window.BENCHMARK_DATA = {
  "lastUpdate": 1790874430121,
  "repoUrl": "https://github.com/HiddenTrail/ht-spoor",
  "entries": {
    "Spoor exploration perf (small)": [
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "f64325f4bd2ce96812377e9408bf3f077892495b",
          "message": "Merge pull request #87 from pekka-hiddentrail/perf-bench\n\nAdd a deterministic exploration performance bench (§5.5)",
          "timestamp": "2026-09-15T21:59:12+03:00",
          "tree_id": "7aeb6c4cb6a7843e02e1b4a7615050e043c87487",
          "url": "https://github.com/pekka-hiddentrail/ht-spoor/commit/f64325f4bd2ce96812377e9408bf3f077892495b"
        },
        "date": 1789499931181,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 118.047,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.03977,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 1.8068,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.13815,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 3.3013,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.06841,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 11.6332,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.10586,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 19.061,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.0426,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.2569,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.5626,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 29.1555,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.05676,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 14.0874,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 0.88007,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 29.7004,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.08784,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.531,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.01072,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.6465,
            "unit": "s"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "1db9da3722a326b31efec985d5623216fa45bf7f",
          "message": "Merge pull request #88 from pekka-hiddentrail/perf-seed-baseline\n\nAdd a baseline-seeding mode to the perf workflow (§5.5)",
          "timestamp": "2026-09-15T22:48:36+03:00",
          "tree_id": "a8589b32d11bda2ea59d57c522a33be9acc57e03",
          "url": "https://github.com/pekka-hiddentrail/ht-spoor/commit/1db9da3722a326b31efec985d5623216fa45bf7f"
        },
        "date": 1789501875402,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 89.113,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.03569,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 0.962,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.132,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 2.8929,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.06171,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 11.228,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.1065,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 18.2021,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.05127,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.2711,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.55483,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 17.8881,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.05225,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 5.4511,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 0.87726,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 23.3036,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.09212,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.568,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.01073,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.4985,
            "unit": "s"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "249903e7b9911e67a7ea529291508300b6514049",
          "message": "Gate only reproducible perf counters + seed the baseline (§5.5) (#89)\n\n* Gate only reproducible perf counters; demote call counts to advisory (§5.5)\n\nA CI seeding run showed the assumption that per-operation call counts are\ndeterministic is false: the walk's replay/recovery loop reacts to the live\ntarget's runtime nondeterminism (Juice Shop is an SPA whose reset does not\nalways land identically), so reset/state_html/ax_nodes/probe/perform counts —\nand which replay-failure message a skip carries — vary run to run even for the\nidentical map. Two CI runs agreed on the structural and dedup counts but\ndisagreed on those.\n\nSo check_drift now gates only the reproducible counters (states, transitions,\nskipped, discovered, image_files, image_refs); the committed baseline holds only\nthose. Per-operation call counts and the skip-reason histogram are still\nreported (advisory lines in the run output, useful for triage) but never fail\nthe build. Corrects the §5.5 note accordingly.\n\nCo-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>\n\n* Seed the committed juice-shop-small perf baseline (§5.5)\n\nCaptured on the CI runner via a workflow_dispatch update_baseline run and\ninspected: the six gated structural/dedup counters, matching both prior CI\nruns. With this committed the small-set drift gate is now live (fails on any\nchange to the crawl shape or dedup counts).\n\nCo-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>\n\n* Narrow perf gate to the pure graph shape; demote dedup counts to advisory (§5.5)\n\nA check-mode CI run proved image_refs wobbles run to run (151->152) while the\ngraph shape (states/transitions/skips/discovered) stays identical — the walk's\nreplay/recovery loop reacts to Juice Shop's SPA nondeterminism (an extra element\ncapture), which moves the capture counts without changing the map. So the dedup\ncounts join the per-op call counts and skip histogram as advisory-only signals;\nonly the four reproducible graph-shape counters gate against the committed\nbaseline. Re-seed the baseline to those four fields and reconcile the docstrings,\nROADMAP §5.5 and the workflow comment.\n\nCo-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>\n\n---------\n\nCo-authored-by: Claude Opus 4.8 <noreply@anthropic.com>",
          "timestamp": "2026-09-16T07:57:38+03:00",
          "tree_id": "af07c406d2e6fedc9f74e2e39f2ee8896c02dd4e",
          "url": "https://github.com/pekka-hiddentrail/ht-spoor/commit/249903e7b9911e67a7ea529291508300b6514049"
        },
        "date": 1789534825831,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 85.133,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.03976,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 0.9862,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.12789,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 2.7799,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.06505,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 11.8579,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.10948,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 18.1959,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.04446,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.266,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.55624,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 17.9589,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.04382,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 4.4647,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 0.85249,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 19.8956,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.08533,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.5369,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.01076,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.4278,
            "unit": "s"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "0224f05041b6474a34e0b3a8f42f6ab4d61ea821",
          "message": "Add an event-anchored resource trace to the perf bench (§5.5) (#90)\n\nEvery timed transaction now also carries its start offset on the run's time axis\nand the resident memory (this process + children, via psutil, so Chromium counts)\nsampled just before and after the call — bracketing each browser round-trip so a\nmemory step attributes to the operation that caused it. RSS is read outside the\nperf_counter window, so sampling never inflates the reported per-op duration.\n\nThe trace is a within-run diagnostic: like the walk-dependent call counts it is\nnondeterministic run to run, so it is never gated. It is emitted as a per-run\nJSON timeline artifact (ordered t_start/duration/op/detail/rss_before/rss_after\nrows, ready to stretch onto a timeline), and its one scalar reduction — peak RSS —\nrides the advisory dashboard as a smaller-is-better trend line beside the timing\nrows. psutil is a dev/bench-only dependency; when it is absent the readings are 0\nand the trace degrades to timing-only (no flatline row is charted).\n\nRendering the trace to a matplotlib timeline PNG on gh-pages is the next slice;\nthis lands the collection and the artifact it will consume.\n\nCo-authored-by: Claude Opus 4.8 <noreply@anthropic.com>",
          "timestamp": "2026-09-16T09:08:27+03:00",
          "tree_id": "f26f71a9f828b0f87d09b22b283c2a16789e1a58",
          "url": "https://github.com/pekka-hiddentrail/ht-spoor/commit/0224f05041b6474a34e0b3a8f42f6ab4d61ea821"
        },
        "date": 1789539077175,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 92.301,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.04408,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 1.1248,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.13171,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 3.0153,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.06197,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 11.9996,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.1076,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 18.1608,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.06239,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.2933,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.55647,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 17.9791,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.05369,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 5.3832,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 0.87312,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 20.0864,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.09411,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.5655,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.01073,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.4303,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 3735.9,
            "unit": "MB"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "871b317972393d45574057b769c59e4d585486ba",
          "message": "Merge pull request #92 from pekka-hiddentrail/exploration-settling-announcements\n\nSettle also waits out urgent live-region announcements (§2e, 7f)",
          "timestamp": "2026-09-16T11:35:29+03:00",
          "tree_id": "cdeb6253c877353e4b8be65cc43bb8c8ff095c06",
          "url": "https://github.com/pekka-hiddentrail/ht-spoor/commit/871b317972393d45574057b769c59e4d585486ba"
        },
        "date": 1789548003898,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 200.365,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.0284,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 1.33,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.09519,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 2.3739,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.05233,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 8.4694,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.08139,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 13.3241,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.03077,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.1668,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.55956,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 29.212,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.0332,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 8.8058,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 5.92434,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 124.574,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.07231,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.4359,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.00789,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.3488,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 4969.7,
            "unit": "MB"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "2fa95b80accbed9c77666f13eb9f4fc71a14c866",
          "message": "Merge pull request #91 from pekka-hiddentrail/perf-trace-report\n\nRender the perf resource trace as an interactive HTML report (§5.5)",
          "timestamp": "2026-09-16T11:54:28+03:00",
          "tree_id": "c3738d8d168cc5f61f9fe39bef4d8fde9010935a",
          "url": "https://github.com/pekka-hiddentrail/ht-spoor/commit/2fa95b80accbed9c77666f13eb9f4fc71a14c866"
        },
        "date": 1789549164219,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 214.82,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.04013,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 1.9325,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.11437,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 2.7196,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.06396,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 10.7082,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.11826,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 17.0089,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.04364,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.2488,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.57922,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 32.2825,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.04711,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 11.9888,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 5.986,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 126.2121,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.0844,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.5475,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.00968,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.4336,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 5299.7,
            "unit": "MB"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "18800c0ce3feebda7fab238fde6edd626f016676",
          "message": "Merge pull request #93 from pekka-hiddentrail/roadmap-second-round-exploration\n\nDesign notes: §2e v2 exploration — interactive second round + anchored resume",
          "timestamp": "2026-09-16T13:48:26+03:00",
          "tree_id": "b8b3b9f07bd65d73a6f80b8c5c92b8d8bc35a865",
          "url": "https://github.com/pekka-hiddentrail/ht-spoor/commit/18800c0ce3feebda7fab238fde6edd626f016676"
        },
        "date": 1789555986393,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 206.23,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.03034,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 1.5978,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.10139,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 2.4305,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.05642,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 9.2217,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.08644,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 14.3451,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.03356,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.2091,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.56073,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 31.6298,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.03548,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 9.8691,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 5.92567,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 124.6125,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.0746,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.4728,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.00862,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.3761,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 5284.3,
            "unit": "MB"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "7c752d79e30d38bd6fed0fac808ac045574c7c23",
          "message": "Merge pull request #94 from pekka-hiddentrail/exploration-anchor-selector\n\nResolve a state-selector to one anchor state (§2e resume, slice 1)",
          "timestamp": "2026-09-16T14:04:40+03:00",
          "tree_id": "4cbf898060e1c7ca9b0b0d68887c3c24deb79b4e",
          "url": "https://github.com/pekka-hiddentrail/ht-spoor/commit/7c752d79e30d38bd6fed0fac808ac045574c7c23"
        },
        "date": 1789556974632,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 209.85,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.03167,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 1.5331,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.1009,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 2.4174,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.05643,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 10.3625,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.09238,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 15.5385,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.03406,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.2441,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.55945,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 31.6086,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.0401,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 10.4965,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 5.92142,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 124.7036,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.07857,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.4748,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.0088,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.3945,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 5345.2,
            "unit": "MB"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "bfc9e37b3c58c59f701f91ebb573b47e7384e1b5",
          "message": "Merge pull request #95 from pekka-hiddentrail/exploration-graph-candidates\n\nBuild anchor candidates from an exploration graph (§2e resume, slice 2)",
          "timestamp": "2026-09-16T15:59:55+03:00",
          "tree_id": "146ca5ef68b12c8610bb320e93800a11b8a4743f",
          "url": "https://github.com/pekka-hiddentrail/ht-spoor/commit/bfc9e37b3c58c59f701f91ebb573b47e7384e1b5"
        },
        "date": 1789563891268,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 218.82,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.0369,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 1.9789,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.11371,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 2.7561,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.06697,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 11.2967,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.11808,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 18.1896,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.04723,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.2725,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.58455,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 32.4762,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.05029,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 12.6618,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 5.98763,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 126.2053,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.09534,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.5625,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.00969,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.4178,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 5348.9,
            "unit": "MB"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "ba5401d9a067718e76cdd2a2e1e5e47aa3b4d4e8",
          "message": "Merge pull request #97 from pekka-hiddentrail/exploration-persisted-map\n\nLoad a persisted exploration map back into a graph (§2e resume, slice 3)",
          "timestamp": "2026-09-16T16:16:04+03:00",
          "tree_id": "08c739e28fa0b56c5bd9378a5a3e25978790e65b",
          "url": "https://github.com/pekka-hiddentrail/ht-spoor/commit/ba5401d9a067718e76cdd2a2e1e5e47aa3b4d4e8"
        },
        "date": 1789564849072,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 220.857,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.03804,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 1.9183,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.12317,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 2.9479,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.06406,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 11.1736,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.11102,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 17.59,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.04248,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.2658,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.57286,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 32.044,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.05042,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 12.3875,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 5.98367,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 126.3981,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.08204,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.5139,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.01048,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.4658,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 5370.6,
            "unit": "MB"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "483b13f8ca544b3195c3004dda4cac154f547523",
          "message": "Merge pull request #98 from pekka-hiddentrail/exploration-resume-traversal\n\nResume exploration from a mapped anchor (§2e resume, slice 4)",
          "timestamp": "2026-09-17T00:05:01+03:00",
          "tree_id": "622cfca9ec19e18f988b5cdadea057f9ca60bf59",
          "url": "https://github.com/pekka-hiddentrail/ht-spoor/commit/483b13f8ca544b3195c3004dda4cac154f547523"
        },
        "date": 1789592995268,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 228.353,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.03928,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 2.1749,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.12229,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 2.9029,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.06504,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 10.7294,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.1093,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 17.9056,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.04092,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.2605,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.57303,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 32.1794,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.04992,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 12.4757,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 5.99841,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 132.4488,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.0845,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.5152,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.01039,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.4639,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 5299.2,
            "unit": "MB"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "ec34fc81a64ef345deaf5b8a75960d1cd3040504",
          "message": "Merge pull request #99 from pekka-hiddentrail/testgen-writer-live-run\n\nWrite the generated regression suite to disk and run it (§2g, slice 2g-ii)",
          "timestamp": "2026-09-17T01:03:52+03:00",
          "tree_id": "d76978d5c051d2c0acda24500b3254ea35ba01cc",
          "url": "https://github.com/pekka-hiddentrail/ht-spoor/commit/ec34fc81a64ef345deaf5b8a75960d1cd3040504"
        },
        "date": 1789596516831,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 220.977,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.03938,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 2.0485,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.12438,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 2.9917,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.06184,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 11.1122,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.10957,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 17.756,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.04966,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.2656,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.57234,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 32.0672,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.05081,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 12.4023,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 5.97663,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 126.1336,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.0902,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.5559,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.01035,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.4473,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 5244.5,
            "unit": "MB"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "73afd4496fcf45c63e4f9ee73e871c49d222f026",
          "message": "Merge pull request #100 from pekka-hiddentrail/wiki-subfolder-layout\n\nGroup wiki state and transition pages into subfolders (§2e, slice 6g)",
          "timestamp": "2026-09-17T08:52:10+03:00",
          "tree_id": "0a70da5819d9c72411db8b11d1d060e3ef4d706f",
          "url": "https://github.com/pekka-hiddentrail/ht-spoor/commit/73afd4496fcf45c63e4f9ee73e871c49d222f026"
        },
        "date": 1789624618781,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 205.363,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.02721,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 1.4212,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.10023,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 2.3903,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.05451,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 9.2113,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.09188,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 14.282,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.04521,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.2315,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.56391,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 31.2441,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.03499,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 9.5669,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 5.9359,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 125.1622,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.07759,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.4514,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.00843,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.3601,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 5385.8,
            "unit": "MB"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "e16445ccb4827f746e97445f0baa3365a65091a4",
          "message": "Add presentation overview; keep demo/ output untracked (#127)\n\ndemo/ holds regenerable demo wikis and generated regression suites,\nnot source of truth, so it's kept out of git and listed in\n.gitignore instead of committed.\n\nCo-authored-by: Claude Sonnet 5 <noreply@anthropic.com>",
          "timestamp": "2026-09-21T22:18:35+03:00",
          "tree_id": "8c9f5fa4d98409d0ef0f8cc9edaa9068bf1e4891",
          "url": "https://github.com/pekka-hiddentrail/ht-spoor/commit/e16445ccb4827f746e97445f0baa3365a65091a4"
        },
        "date": 1790018636336,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 210.901,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.03478,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 1.8238,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.10163,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 2.4953,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.05963,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 10.1851,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.09944,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 15.4977,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.04704,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.2814,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.56685,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 31.8759,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.03828,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 10.2259,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 5.94883,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 125.0592,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.06944,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.4427,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.00897,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.3929,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 5226.3,
            "unit": "MB"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "ae3d0d4437f608d4aa79188f4d302291dcb479a6",
          "message": "Backlog: generated regression tests don't flag new/unexpected signals (§9, §2g) (#129)\n\nThe generated suite only re-asserts the specific console/storage/network values\nrecorded as added during the original crawl. Since state identity is DOM-based,\nnot signal-based, a redesign that keeps the same markup but starts firing extra\nnetwork requests or logging new console warnings produces the identical graph\nand a green suite. Recorded as a known, non-blocking gap for a future design\npass, not built now.\n\nCo-authored-by: Claude Sonnet 5 <noreply@anthropic.com>",
          "timestamp": "2026-09-23T12:07:50+03:00",
          "tree_id": "de8de056762f0d52d67bc0def65bf001f572eefe",
          "url": "https://github.com/HiddenTrail/ht-spoor/commit/ae3d0d4437f608d4aa79188f4d302291dcb479a6"
        },
        "date": 1790154752790,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 202.949,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.02755,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 1.4718,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.09901,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 2.3814,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.05118,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 8.7774,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.08688,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 13.9808,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.03173,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.2158,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.56379,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 31.4532,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.03405,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 9.153,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 5.94141,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 125.3201,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.07289,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.4311,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.00841,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.3708,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 5384.2,
            "unit": "MB"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "33dde30c67f600d6713b1f7c3eca6d0ab74e37ea",
          "message": "Scaffold an interactive-round config from an exploration graph (#131) (#132)\n\n* Record freshness-by-re-observation design note (§2f, #107)\n\nAgreed design for detecting \"ghost calls\" on mapped transitions: a\nre-observation run replays recorded transitions (same safety gate),\nrecords per transition what changed since the saved map, and marks\nsignals volatile when two in-run replays disagree (Diffy-style, no\naccumulated history). Records the observe-vs-judge boundary so Spoor\nstays a map, not a testing tool. Cross-links the §9 freshness and\n#128 backlog items; three decisions remain open before the feature file.\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\n\n* Scaffold an interactive-round config from an exploration graph (issue #131)\n\nAdds spoor explore --scaffold <file>: from a completed read-only crawl, writes\na human-editable YAML file listing discovered fields (with a best-guess\ngenerator and a blank value to fill in), discovered login points, and\ndiscovered actions the safety gate skipped for being destructive. Scaffold\n*generation* only — consuming a filled-in scaffold to run an actual\ninteractive round is separate, later work.\n\n- ActionableElement gains input_type (spoor/exploration/discovery.py), read\n  by the driver the same way destination was added for links (slice 9b): one\n  batched DOM read, additive, no behavior change for existing consumers. This\n  is the only signal that tells a password field apart from any other text\n  box, since the accessibility tree alone reports both as role=\"textbox\".\n- spoor/scaffold/interactive_config.py: build_scaffold (pure) / render_scaffold\n  (thin writer), mirroring pytest_gen.py's split. A password field becomes a\n  login_points entry pointing at the existing session: mechanism, never a\n  fillable credential (§2h, bring-your-own-session). destructive_actions\n  entries are matched against the safety gate's own recorded skip reason\n  (new DESTRUCTIVE_SKIP_REASON constant in safety.py) rather than re-derived\n  from the action's label, so an action skipped for an unrelated reason (e.g.\n  an overlay) is never misreported as having been skipped for being\n  destructive.\n- spoor explore --scaffold <file> wired beside --wiki/--gen-tests.\n\nBDD-first: features/interactive_scaffold.feature (6 fast-tier scenarios + one\n@browser live scenario against a new dedicated fixture, explore_login.html,\nkept separate from the shared two-page traversal fixture so it doesn't\nperturb exploration_browser.feature's hardcoded state/transition counts).\n\nFull local gate green: ruff, mypy (155 files), pytest (714 passed / 8\n@browser scenarios), scripts/check_genericity.py.\n\nCo-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>\n\n* Clarify re-observation baseline compatibility and sampling uncertainty\n\n---------\n\nCo-authored-by: Claude Opus 5.5 <noreply@anthropic.com>",
          "timestamp": "2026-09-29T11:28:28+03:00",
          "tree_id": "3eb34a11d9ad1a1e70d75a061f2629f6405c9a72",
          "url": "https://github.com/HiddenTrail/ht-spoor/commit/33dde30c67f600d6713b1f7c3eca6d0ab74e37ea"
        },
        "date": 1790670810810,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 226.661,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.03949,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 2.0782,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.12692,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 3.0978,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.07642,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 12.5622,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.12031,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 19.4185,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.04471,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.2855,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.57981,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 32.5578,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.05492,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 13.4131,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 6.01108,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 126.5995,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.09966,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.5917,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.01087,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.4823,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 5291.5,
            "unit": "MB"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "f0efbefb30308c79865395e31fc27b5de90913b4",
          "message": "Backlog: how a filled scaffold field gets applied (§2e) (#133)\n\n* Backlog: how a filled scaffold field gets applied, not just typed (§2e)\n\nRecords the open question round-two consumption will need to answer (a value\nto pin isn't enough on its own -- most fields need Enter or a submit click),\nand the recommended technique: Scrapy's FormRequest.from_response() /\nSelenium's element.submit() (walk to the nearest ancestor form, use its\ndeclared submit control), reimplemented small rather than vendored as a\ndependency or punted to a model call the way the LLM-driven browser agents\ndo. Not designed in detail yet -- recorded so the technique choice isn't\nrelitigated later.\n\nCo-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>\n\n* docs: distinguish form discovery from submission execution\n\n---------\n\nCo-authored-by: Claude Sonnet 5 <noreply@anthropic.com>",
          "timestamp": "2026-09-29T13:53:48+03:00",
          "tree_id": "e52c0f88f806779037a00eccaa944698843e1006",
          "url": "https://github.com/HiddenTrail/ht-spoor/commit/f0efbefb30308c79865395e31fc27b5de90913b4"
        },
        "date": 1790679519272,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 224.724,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.03996,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 2.1799,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.124,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 2.9458,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0002,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.07015,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 11.6618,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.10781,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 18.4403,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.04331,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.2584,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.57558,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 32.3129,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.05033,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 12.8341,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 5.99485,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 126.5826,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.08564,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.5261,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.01057,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.4625,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 5380.8,
            "unit": "MB"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "5ac5aa87655117aa8fa0416f3e7c21d622d53694",
          "message": "Decision: sandbox-only typing round two may proceed ahead of #101 (#134)\n\n* Decision: typing-only round two may proceed ahead of #101 (§2e)\n\nMaintainer-approved, narrow exception to the read-only-mode-exit gate: a\nround that only types a scaffold's pinned values into their fields -- never\nsubmits, never clicks, never applies a value -- may proceed ahead of the\nkeyword-list localization prerequisite. Filling a field isn't a match\nagainst DESTRUCTIVE_KEYWORDS (that list matches action labels, not typed\ncontent), and every fired action still goes through the same unconditional,\nlocale-independent evaluate_action gate. Applying a value remains fully\nblocked on #101 until it's resolved.\n\nCo-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>\n\n* docs: restrict typing-only exception to sandbox targets\n\n---------\n\nCo-authored-by: Claude Sonnet 5 <noreply@anthropic.com>",
          "timestamp": "2026-09-29T13:59:07+03:00",
          "tree_id": "57ad9f3a16d38c5a384c802111986942f3b696da",
          "url": "https://github.com/HiddenTrail/ht-spoor/commit/5ac5aa87655117aa8fa0416f3e7c21d622d53694"
        },
        "date": 1790679855201,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 202.229,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.02731,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 1.4318,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.09298,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 2.2778,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.0508,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 8.6581,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.08541,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 13.6352,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.03176,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.1949,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.56281,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 31.6415,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.03561,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 9.4305,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 5.92711,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 124.505,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.0718,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.4557,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.00776,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.3386,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 5443.5,
            "unit": "MB"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "99ec3e337e9afe37738f4994114afd5d40c4b636",
          "message": "Type a filled-in interactive-round scaffold's values into their fields (#135)\n\n* Type a filled-in interactive-round scaffold's values into their fields\n\nAdds spoor apply-scaffold <url> <file>: the first, deliberately narrow slice\nof consuming a filled-in interactive-round scaffold (issue #131 shipped\ngeneration only). Navigates to each field's recorded state and types its\npinned value in -- never presses Enter, never clicks a submit control, never\napplies the value. This is the maintainer-approved, explicitly narrow\nexception to the read-only-mode-exit gate ahead of keyword-list localization\n(#101): typing isn't a DESTRUCTIVE_KEYWORDS match, and applying a value\nstays fully blocked on #101.\n\n- PlaywrightDriver.fill(action, value): shares perform()'s exact\n  relocate-and-verify path (_actuation -- the same find_target re-lookup,\n  the same verified click point) rather than Playwright's own locator API,\n  consistent with the relocation-bug precedent (7a) that first ruled that\n  out. Clicks to focus, selects existing content, types with real trusted\n  keystrokes (page.keyboard.type), never a synthetic DOM write.\n- spoor/scaffold/apply.py: apply_scaffold navigates via paths_from_root +\n  driver.perform replay -- the same reset-and-replay pattern the generated\n  test suite already proves, so no new crawl primitive was needed. One\n  field's failure (unresolved state prefix, field no longer present,\n  vanished/covered element) is recorded and the rest still run, mirroring\n  the explorer's own skip-and-continue posture.\n- FIELD_ROLES promoted to public in interactive_config.py so apply.py\n  matches the same role set scaffold generation used, by construction.\n\nBDD-first: features/interactive_scaffold_apply.feature, 5 fast-tier\nscenarios + one @browser scenario that types into a real field and reads\nthe DOM value back. New field added to the existing dedicated\nexplore_login.html fixture (not the shared two-page traversal fixture, per\nthe lesson from issue #131's own PR).\n\nFull local gate green: ruff, mypy (157 files), pytest (719 passed / 6\n@browser scenarios for this feature), scripts/check_genericity.py. Also\nverified against the real EcoEstate demo target with a human-filled\nscaffold -- 5 fields applied live, 0 failures.\n\nCo-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>\n\n* Fix 5 safety/correctness gaps in scaffold apply (§2e, #131 review)\n\napply_scaffold now checks is_sandbox before touching the driver at all,\nmatching the §2e destructive-action non-negotiable (the previous cut\nfired fill() unconditionally). Fields on the same resolved state share\none reset+visit instead of reloading the page per field, which was\noverwriting earlier fields' typed values. A reset/replay failure now\nfails only that state's fields instead of aborting the whole run. A\nnon-string YAML value (an unquoted number) is now reported as a failed\nfield instead of silently dropped. And apply is restricted to the root\nstate only: a field reachable solely by replaying navigation clicks is\nrefused (\"navigation replay is outside the typing-only scope\") rather\nthan attempted, since a click that only exists to reach a field is\nstill a click this module's contract forbids.\n\nSeparately, PlaywrightDriver.fill() now verifies a field's live value\nactually changed to what was typed before reporting success, so a\nread-only/disabled field can't be reported as filled. Raises the new\nElementNotEditable.\n\nAdded --sandbox to `spoor apply-scaffold`, a @browser scenario proving\nthe read-only-field case end to end (fixtures/static/explore_login.html\ngained a read-only \"Account ID\" field), and reconciled README.md,\ndocs/ROADMAP.md's decision note (which previously claimed a safety\ngate the shipped code didn't actually apply), and features/README.md.\n\nCo-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>\n\n---------\n\nCo-authored-by: Claude Sonnet 5 <noreply@anthropic.com>",
          "timestamp": "2026-09-29T14:51:19+03:00",
          "tree_id": "a6eabd57508d65bd2c42003364735083e13bbf84",
          "url": "https://github.com/HiddenTrail/ht-spoor/commit/99ec3e337e9afe37738f4994114afd5d40c4b636"
        },
        "date": 1790683005551,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 225.494,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.04486,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 2.1698,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.1266,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 3.1211,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.07267,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 11.8111,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.12515,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 18.8337,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.04415,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.261,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.57632,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 32.3289,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.05265,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 13.5291,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 6.02332,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 126.9786,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.09005,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.5561,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.01069,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.4825,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 5305.4,
            "unit": "MB"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "98112bacfbff5bc94f801e779bab87f13d9bb6c9",
          "message": "Design: apply-scaffold observes and persists the fill-revealed state (§2e) (#136)\n\nRecords a design (not yet built) for closing a gap a user found while\nrunning spoor apply-scaffold against the EcoEstate demo: typing a\nscaffold's pinned values in currently updates nothing but the live\npage -- the saved map and wiki still describe the pre-fill crawl, even\nwhen the typed value visibly changed what's on screen.\n\nProposes reusing the same read-only discover_actions + capture_signals\nobservation the crawl loop already runs after every click, now run\nafter a fill instead, with the result merged additively into the map\nand the wiki re-rendered through the existing render_wiki pipeline --\nno new mechanism invented. Explicitly excludes continuing to crawl\npast the fill-revealed state (that's the \"interactive form-driven\nexploration\" mode the round-two design already gates behind #101, and\ndecision #134's typing-only carve-out only covers typing). Flags two\nopen design questions -- how a fill is represented as a graph edge,\nand whether a fill-revealed state is resume/testgen-reachable -- for a\nmaintainer decision before any implementation, rather than deciding\nthem here.\n\nCo-authored-by: Claude Sonnet 5 <noreply@anthropic.com>",
          "timestamp": "2026-09-29T15:30:13+03:00",
          "tree_id": "86bc5de72b5fa24b39c6889993b245ad73548acc",
          "url": "https://github.com/HiddenTrail/ht-spoor/commit/98112bacfbff5bc94f801e779bab87f13d9bb6c9"
        },
        "date": 1790685319881,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 225.478,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.04262,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 2.0157,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.13614,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 3.2257,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0002,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.08319,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 12.5151,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.13442,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 20.3165,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.04932,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.3057,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.58416,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 32.8283,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.04711,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 11.5629,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 5.99098,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 126.0203,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.09414,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.5786,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.01183,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.5191,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 3550.8,
            "unit": "MB"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "cb0e5824a47c89c11140de2d689b3d58d5b48617",
          "message": "apply-scaffold observes and persists the state a fill reveals (§2e, #137) (#138)\n\nCloses the gap where filling in a scaffold and re-running spoor apply-scaffold\nupdated nothing but the live page: the saved map and wiki still described the\noriginal read-only crawl even when the typed value visibly changed the screen.\n\nActionableElement gains an optional fill_value field. A transition whose action\ncarries one is a typed edge, not a clicked one -- no new transition kind, every\nexisting consumer unaffected since the field defaults to None everywhere but here.\nAfter a successful fill, apply_scaffold observes the resulting page the same\nread-only way exploration observes after any click (discover_actions +\ncapture_signals, reused via a widened ApplyDriver protocol) and, if the page\nactually changed, adds a real state and transition to the graph -- idempotent, so\nre-running an unchanged scaffold against an unchanged target adds nothing twice.\nThe CLI persists the enriched graph back to MapStore (preserving the entry's\nexisting records/tier/api_surface/config) and refreshes the wiki via --wiki.\n\nPer explicit maintainer direction, these states/transitions are real and\nreplayable, not excluded from replay as this feature's own design note first\nproposed: pytest_gen.py's generated tests and _PATH replay now carry a role/name/\nfill_value triple per step and dispatch to a new fill() helper instead of fire()\nwhen appropriate. Both the wiki's state and transition pages clearly flag a\nconfig-derived entry so it's never mistaken for one the site itself linked to.\nfill_value stays raw in the local persisted map (like name already does) and is\nredacted only at the wiki/testgen/serving boundary -- verified the MCP/API\nredaction gate (redact_value) is structural, so the new field is covered by the\nexisting mechanism with no special-casing needed.\n\nVerified end-to-end against the live EcoEstate demo target: filling \"Search\npostcodes\" revealed a new state with a real signal diff (new network request,\naccessibility-node delta), correctly persisted under its URL and shown on the\nrefreshed wiki with both badges; a second run against the same target added\nnothing further, confirming idempotency empirically.\n\nCo-authored-by: Claude Sonnet 5 <noreply@anthropic.com>",
          "timestamp": "2026-09-29T16:41:04+03:00",
          "tree_id": "24485b61f5bb35befac4c8e4d5957b17ecc62608",
          "url": "https://github.com/HiddenTrail/ht-spoor/commit/cb0e5824a47c89c11140de2d689b3d58d5b48617"
        },
        "date": 1790689534669,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 197.468,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.02593,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 1.3296,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.08505,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 2.0843,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.06361,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 8.5832,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.08876,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 12.8865,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.03296,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.1929,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.54198,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 30.549,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.02804,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 8.0561,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 5.89682,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 124.0592,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.06133,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.3734,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.00672,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.2993,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 5341.5,
            "unit": "MB"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "bdc22dea02d10c0788e60ca8b5fd1a9e0f31aac0",
          "message": "Move the live-docker-archetype integration tier off the PR gate to nightly (#139)\n\ndocker compose -f fixtures/docker-compose.yml up -d in ci.yml was unscoped, so\nit booted the whole archetype bench (Juice Shop, Sauce Demo -- built from\nsource on every run, no prebuilt image -- and PrestaShop, which has no\nintegration test consuming it yet) on every PR. That made the mandatory gate\n\"terribly long\" for a check that only needs to catch a genericity regression\nwithin a day, not synchronously with every push.\n\nci.yml now runs `pytest -m \"not integration\"` (fast tier + browser tier, no\nDocker at all) and no longer touches the archetype bench. The `integration`\nmarker moved to a new job in nightly.yml, on the existing daily schedule plus\nworkflow_dispatch for an on-demand run; it boots the full bench and runs\n`pytest -m integration`, same steps ci.yml used to run. Also dropped the\n\"Upload extraction output\" step from ci.yml -- test-output/ is only ever\nwritten by integration-marked tests, so it could never fire there anymore.\n\nRecorded as a decision in docs/ROADMAP.md (§5.1) rather than a silent config\ntweak, since it changes what a PR-blocking gate actually covers; CLAUDE.md's\nown description of the split is updated to match. This narrows *when* the\nlive-archetype proof runs, never *whether* it runs or what it's allowed to\nfind.\n\nVerified locally: `pytest -m \"not integration\"` passes in full (765 passed, 11\ndeselected -- exactly the integration-marked tests), matching what the new\nci.yml gate will run.\n\nCo-authored-by: Claude Sonnet 5 <noreply@anthropic.com>",
          "timestamp": "2026-09-29T17:00:51+03:00",
          "tree_id": "e695ef160be4a14e24a394b7f0c5e93d5469ff0e",
          "url": "https://github.com/HiddenTrail/ht-spoor/commit/bdc22dea02d10c0788e60ca8b5fd1a9e0f31aac0"
        },
        "date": 1790690769442,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 235.987,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.04421,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 2.2842,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.13226,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 3.1369,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0002,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.06968,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 12.1392,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.12972,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 20.6394,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.04413,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.2959,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.58143,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 32.5659,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.05578,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 14.1785,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 6.0352,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 133.2303,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.1044,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.6466,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.01162,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.5215,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 5316.3,
            "unit": "MB"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "ba4f8a3fdfedf2f315af6de8c91b4a8a5542de0e",
          "message": "CLI: add an interactive wizard for building commands (#141)\n\nReplaces the earlier --dry-run + shell-completion approach (PR #140, closed\nunmerged per maintainer decision) with what was actually wanted: `spoor wizard`\nwalks through picking a command (explore/apply-scaffold/run/serve/serve-mcp)\nand answering one prompt per flag -- optional ones skip on a blank answer, a\nbad number just re-asks instead of crashing -- then prints the exact resolved\ncommand line before anything runs. Confirming runs that exact line as a\nsubprocess; declining just leaves it to copy. The wizard never reimplements a\ncommand's logic: it only assembles the same argv --help documents, so it can\nnever drift from what the real command actually does.\n\nCovers the \"mixing up commands and flags\" problem the --dry-run approach was\nalso aimed at, but front-loads the guidance (a prompt per flag, in order)\ninstead of only catching a mistake after it's already been typed.\n\nVerified manually (all five command types, the numeric-retry path, and the\n\"run it now\" path actually invoking python -m spoor.cli as a subprocess) and\nwith 4 new tests following the existing test_cli.py pattern -- CliRunner's\ninput= drives the prompts, subprocess.run is monkeypatched to assert it's\ncalled with the exact resolved argv (or not called at all when declined).\n\nCo-authored-by: Claude Sonnet 5 <noreply@anthropic.com>",
          "timestamp": "2026-09-29T21:47:21+03:00",
          "tree_id": "0c9f58f12676b9f79499717bd429f2fcae104150",
          "url": "https://github.com/HiddenTrail/ht-spoor/commit/ba4f8a3fdfedf2f315af6de8c91b4a8a5542de0e"
        },
        "date": 1790707931543,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 223.577,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.04332,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 2.0604,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.12374,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 2.9437,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.06658,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 11.2982,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.11416,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 18.6041,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.04597,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.2677,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.57945,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 32.2688,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.05439,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 13.2303,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 5.99515,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 126.6275,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.09408,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.5755,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.01051,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.4713,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 5306,
            "unit": "MB"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "416e3f32a73e03c990c8a95314e9a0300c8836ae",
          "message": "spoor explore: show a live progress spinner/bar while crawling (#142)\n\nA long crawl printed nothing until it finished, giving no sense of whether it\nwas working or stuck. Adds a dependency-free live indicator: a [####------] NN%\ngauge against --max-states/--max-requests when either is set, or a spinner\n(|, /, -, \\) when the run is unbounded, alongside live states/requests/elapsed\ncounts.\n\nPlaywright's sync API is not safe to use from any thread but the one that\ncreated it, which rules out running the crawl in a background thread and\npolling it from the main thread -- the natural-looking approach, and wrong.\nInstead explorer.explore() (and resume_exploration, which delegates to it)\ngains an optional, no-argument progress callback, fired synchronously on the\nsame thread right after controller.record_state/record_request -- the same\n\"opt-in sink, None by default, zero cost unless asked for\" shape the\nscreenshot sinks already use. RunController gained public states/requests/\nbudget read accessors (previously private-only) for a caller to read from\ninside that callback.\n\nThe CLI's _CliProgress ticks off that callback: throttled to ~10 redraws/sec,\nand silently inactive when stdout isn't a real terminal (piped, redirected, or\nunder a test runner), so non-interactive output is never polluted with\ncarriage-return control characters.\n\nCovered by a new BDD scenario in exploration_loop.feature (the callback fires\nat least once per state and per action, using the existing fake-driver\nharness) and verified live against the real EcoEstate demo target: the bar\ncorrectly advanced 33% -> 66% -> 100% against --max-states 3, with request\ncounts and elapsed time ticking up between state discoveries, and cleared\nitself on completion.\n\nCo-authored-by: Claude Sonnet 5 <noreply@anthropic.com>",
          "timestamp": "2026-09-29T22:14:23+03:00",
          "tree_id": "350e7b35b0eafb7d52fa05719be14003d0bc1238",
          "url": "https://github.com/HiddenTrail/ht-spoor/commit/416e3f32a73e03c990c8a95314e9a0300c8836ae"
        },
        "date": 1790709548430,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 218.732,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.03911,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 1.7059,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.12297,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 2.9879,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.06431,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 11.4919,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.11066,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 17.7677,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.05182,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.2702,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.57553,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 29.6876,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.05254,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 12.5256,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 5.99497,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 126.3317,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.09128,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.5608,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.01046,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.4561,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 4871,
            "unit": "MB"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "091967e3ac30bbcefa43e118c1df06b088540311",
          "message": "CLI: reject colliding --wiki/--gen-tests/--scaffold output paths upfront (#143)\n\nReal incident: spoor wizard was used to build `spoor explore ... --wiki\ndemo/wizard-eco --scaffold demo/wizard-eco` -- the same path handed to both\nflags. --wiki writes a directory of files; --scaffold writes one YAML file.\nThe crawl ran to completion (states/transitions/skips printed successfully),\nthen crashed writing the scaffold with a bare PermissionError, because that\npath already existed as the wiki's directory.\n\nAdds _check_explore_output_paths, run before any browser is launched: refuses\nwith a clear message when two of --wiki/--gen-tests/--scaffold share a path,\nor when one already exists on disk as the wrong kind of thing (a file where a\ndirectory-writing flag expects one, or vice versa). Verified against the\nexact reported command -- now fails in under a second instead of after a full\ncrawl.\n\nAlso hardens the wizard itself, since this is precisely the class of mistake\nit exists to prevent: _wizard_optional_output_path rejects and re-prompts\nwhen a later output-path answer (--gen-tests, --scaffold) repeats an earlier\none (--wiki, --gen-tests) in the same session, catching it before the command\nis even built -- belt-and-suspenders with the CLI-level check, not a\nreplacement for it (a directly-typed `spoor explore` command bypasses the\nwizard entirely and still needs its own guard).\n\nCovered by 3 new tests in test_cli.py: the exact colliding-paths case, a path\nthat already exists as the wrong kind of thing, and the wizard's reprompt\npath -- all following the existing \"assert PlaywrightDriver is never\nconstructed\" pattern to prove nothing runs before the check.\n\nCo-authored-by: Claude Sonnet 5 <noreply@anthropic.com>",
          "timestamp": "2026-09-29T22:25:31+03:00",
          "tree_id": "b1b120710df9f3458a82922e71f4e76bfa3c4d2a",
          "url": "https://github.com/HiddenTrail/ht-spoor/commit/091967e3ac30bbcefa43e118c1df06b088540311"
        },
        "date": 1790710232895,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 222.827,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.03824,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 1.9535,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.1288,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 3.0947,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.06866,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 11.6343,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.11559,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 18.3855,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.07934,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.3659,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.57499,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 32.0711,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.05241,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 13.2017,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 5.98129,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 125.9622,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.09317,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.577,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.01119,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.4875,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 5342.5,
            "unit": "MB"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "c25659d9aa121e0b29d0460f57280c3f6a511d52",
          "message": "--scaffold now writes into a directory, like --wiki/--gen-tests (#144)\n\nFollowed up on a maintainer question after the --wiki/--scaffold collision fix\n(PR #143): why does --scaffold take a file path at all, when --wiki and\n--gen-tests both take a directory? There was no real reason -- it was designed\nto mirror `run`'s -o/--output (a single-file flag), but --wiki/--gen-tests\nmirror each other instead (both write many files into a directory), so\nspoor explore ended up with two incompatible \"give me a path\" conventions on\nthe same command. That's exactly what let --wiki and --scaffold collide on\nthe same path in the first place.\n\nrender_scaffold now takes out_dir and writes a fixed SCAFFOLD_FILENAME\n(\"interactive.yaml\") inside it, the same directory-writer shape render_wiki\nand render_suite already use. --scaffold's CLI help/docstrings updated to\nmatch, and the collision guard from #143 is simplified: since none of\n--wiki/--gen-tests/--scaffold's filenames can ever collide with each other\nnow, giving them the same directory is a legitimate, even convenient way to\nkeep one run's output together, so it's no longer rejected -- only a path\nthat already exists as something other than a directory still is. Removed\nthe now-unnecessary same-path reprompt from spoor wizard for the same reason.\n\nspoor apply-scaffold's own positional scaffold argument is unchanged: it\nstill reads a single file (interactive.yaml, now nested inside the directory\n--scaffold wrote), since that's something the user reads/hand-edits, not\nsomething Spoor's output-flag conventions apply to.\n\nVerified live against the real EcoEstate demo target: --wiki and --scaffold\npointed at the same directory now both write happily -- the exact scenario\nthat crashed before PR #143 and would have been needlessly rejected by #143's\nown collision guard.\n\nCo-authored-by: Claude Sonnet 5 <noreply@anthropic.com>",
          "timestamp": "2026-09-29T23:23:07+03:00",
          "tree_id": "bb39f7b2c0d1c074a82d57f53cb2d76b7b8159e3",
          "url": "https://github.com/HiddenTrail/ht-spoor/commit/c25659d9aa121e0b29d0460f57280c3f6a511d52"
        },
        "date": 1790713673775,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 208.636,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.03138,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 1.6333,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.10299,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 2.5067,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.05822,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 9.6039,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.09169,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 15.1598,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.03576,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.2175,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.56501,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 31.9117,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.0435,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 10.6397,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 5.9578,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 125.4355,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.0753,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.4456,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.00859,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.3791,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 5395.5,
            "unit": "MB"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "af257a1506ceecef61ee9d0086e8b6cbb3b8a32b",
          "message": "Docs: fix Phase column regressions in features/README.md, fill a README.md gap (#145)\n\nAudited every README against the current main (post PR #144) to answer \"is\nevery README up to date\": ran spoor --help for every command and compared\nagainst README.md's documented flags/examples, and cross-checked every\nfeatures/README.md row's last column against its .feature file.\n\nFound a real mistake made across three earlier PRs this session: the table's\nlast column is \"Phase\" (the project phase number), not a scenario count --\nevery other §2e row already correctly reads 5. Three rows I edited this\nsession (exploration_loop.feature, interactive_scaffold.feature,\ninteractive_scaffold_apply.feature) had that 5 overwritten with a scenario\ncount (8, 8, 14) by mistake. Reverted all three to 5, matching every sibling\n§2e row.\n\nAlso found a real gap, not a regression: README.md's \"Available now\" capability\nlist never mentioned the scaffold-generation/apply-scaffold feature at all,\ndespite the detailed walkthrough earlier in the same file -- added a bullet,\nand a short mention of the live progress indicator in the exploration bullet.\n\nNoted, not fixed (pre-existing, unrelated to this session's work): features/\nREADME.md still lists `interaction.feature` under Phase 2, but that file was\nnever created under features/ -- a stale forward-reference from before this\nsession, left for a maintainer to triage rather than guessed at here.\n\nCo-authored-by: Claude Sonnet 5 <noreply@anthropic.com>",
          "timestamp": "2026-09-30T09:35:17+03:00",
          "tree_id": "95a1780ac7f789ff3658cf51b6e3b0781a564f8a",
          "url": "https://github.com/HiddenTrail/ht-spoor/commit/af257a1506ceecef61ee9d0086e8b6cbb3b8a32b"
        },
        "date": 1790750414120,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 227.444,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.041,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 2.1061,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.13041,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 3.0613,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.07464,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 12.6033,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.11997,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 19.5635,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.04582,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.2874,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.58215,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 32.6139,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.05263,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 13.5583,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 6.02009,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 126.8962,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.09263,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.5774,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.01061,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.4675,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 5303.7,
            "unit": "MB"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "1e881383ae2e5469d598aba137c26af4ece0a0d4",
          "message": "Add competitive plan: what Spoor takes from the landscape (#157)\n\nWorking draft, maintainer-editable, not a decision record -- nothing here\nis decided until recorded in docs/ROADMAP.md, which wins on any conflict.\nSurveys Crawlee/Scrapy, Scrapling, Crawljax, browser-use/Skyvern/Stagehand,\nCrawl4AI/Firecrawl, OWASP ZAP/Katana, and Healenium/Testim, and proposes\nwhich ideas to depend on, adapt, build, or deliberately skip, to reach\nroughly 90% of table-stakes parity without becoming a feature grab bag.\n\nConverted into GitHub issues #146-#156 and prioritized in the Spoor Roadmap\nproject (https://github.com/orgs/HiddenTrail/projects/4).\n\nCo-authored-by: Claude Sonnet 5 <noreply@anthropic.com>",
          "timestamp": "2026-09-30T10:10:49+03:00",
          "tree_id": "1161bc7771ea01092d2383b9fde690dac31a3c8c",
          "url": "https://github.com/HiddenTrail/ht-spoor/commit/1e881383ae2e5469d598aba137c26af4ece0a0d4"
        },
        "date": 1790752555415,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 227.965,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.04296,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 2.0635,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.13269,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 3.1317,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.07363,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 12.8349,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.12097,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 19.8057,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.04689,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.2924,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.57651,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 32.619,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.05339,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 13.4345,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 6.0145,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 126.7983,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.10016,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.5995,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.01097,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.5009,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 5334.9,
            "unit": "MB"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "3d3438075cb6684b3a800675223234a8e10e036c",
          "message": "Record D2: the optional LLM tier's shape is \"LLM once, replay forever\" (#159)\n\nCloses #147. Records the decision in docs/ROADMAP.md §9 per\ndocs/COMPETITIVE_PLAN.md's own rule -- nothing there is decided until it's\nrecorded here. Doesn't start building the LLM tier itself (#156); only\nsettles the replay model whichever facet of it gets built first, and\nreaffirms it doesn't relax §1 (still optional, never the default loop, no\nautonomous agents) or the §2e sandbox-only rule.\n\nCo-authored-by: Claude Sonnet 5 <noreply@anthropic.com>",
          "timestamp": "2026-09-30T10:37:33+03:00",
          "tree_id": "6f26bcab8c9ce10d1bcd4e69e4b2fad68fe1026c",
          "url": "https://github.com/HiddenTrail/ht-spoor/commit/3d3438075cb6684b3a800675223234a8e10e036c"
        },
        "date": 1790754152211,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 225.171,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.04273,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 2.0442,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.12762,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 3.0773,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.07183,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 12.3142,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.11699,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 19.1599,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.04749,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.2955,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.58129,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 32.4633,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.05122,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 13.5111,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 5.99326,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 126.5173,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.08477,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.5192,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.01123,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.5192,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 5358.8,
            "unit": "MB"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "48e1e9800184aaa3dc0fab0a4c29102f32c4b3a6",
          "message": "§2a/§2d: add a Markdown table output sink (#158)\n\nCloses #155. docs/COMPETITIVE_PLAN.md flagged Crawl4AI/Firecrawl's page-to-\nmarkdown output as cheap parity with a highly visible competitor feature.\nSpoor's version is a direct table rendering of the config's own field\nschema (the config already names the fields and their order), not clean-\nprose content extraction.\n\nAdded as a fourth OutputFormat (\"md\", inferred from a .md extension or\n--format md) alongside the existing JSON/JSON Lines/CSV sinks, sharing the\nsame schema-validate-then-redact pipeline write_records already runs before\nany sink writes a byte. A cell's pipe/backslash/newline characters are\nescaped so a captured value can never break a table row into extra columns\nor lines -- the same \"never let a value corrupt the format\" guarantee CSV's\nquoting already gives it via the stdlib csv module.\n\nCovered by two new BDD scenarios in output.feature (a normal table render,\nand a value containing a pipe and a newline), following the existing\nfake-config-and-records pattern in test_output_steps.py -- no browser, no\nnetwork. Full gate green (736 passed); manually verified the rendered\noutput against a config with an embedded pipe and newline.\n\nCo-authored-by: Claude Sonnet 5 <noreply@anthropic.com>",
          "timestamp": "2026-09-30T11:28:58+03:00",
          "tree_id": "a61ec2197610977fb9ec739b48dcd4d498282260",
          "url": "https://github.com/HiddenTrail/ht-spoor/commit/48e1e9800184aaa3dc0fab0a4c29102f32c4b3a6"
        },
        "date": 1790757227804,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 218.068,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.03569,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 1.7883,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.12016,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 2.8873,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.05943,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 10.9339,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.10731,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 17.0853,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.04712,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.27,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.56948,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 31.9182,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.04455,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 11.778,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 5.97325,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 125.8591,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.08679,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.5429,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.01002,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.4392,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 5329.4,
            "unit": "MB"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "c895af4ba19ba483c19c1028708ac658d04c7e7c",
          "message": "§5.1: add streaming-clone, the fourth fixture archetype (#160)\n\nThe planned \"self-hosted Netflix-clone\" archetype had no clean adopt-as-is\ncandidate. Every third-party project vetted (devopsinsiders/netflix-clone,\nApestein/nextflix, zoriya/Kyoo, an aiworklabs clone, ridhwaans/homehost, the\nLocalFlix/netflix-local family) was either a production media server needing\nreal video files and a transcoding pipeline, or a thin frontend hard-wired to\na mandatory external SaaS (Clerk/Stripe/Neon/TMDB/Spotify in various\ncombinations) -- neither matches the bench's pattern of a self-contained app\nwith its own data and no external accounts.\n\nSo this one is purpose-built: a small Express app (fixtures/streaming-clone/)\nwith a same-origin JSON API, a server-set-session login gate (a second,\ndifferently-shaped bring-your-own-session proof point alongside Sauce Demo's\nSPA-token pattern), and a per-title detail view with a <video> element -- the\nfirst fixture to exercise the media/streaming-capture signal ROADMAP.md §2c\nnames but none of the others trigger. No database, built from our own\nchecked-in source (no upstream commit to pin, unlike Sauce Demo). Catalog and\nposters are checked in; seed video clips are deliberately not (see\nseed/videos/README.md) -- the app degrades gracefully to \"Preview\nunavailable\" until real short clips are dropped in.\n\nJoins docker-compose.yml on port 3002 (STREAMING_CLONE_PORT), same\nspoor.sandbox label as the rest of the bench. tests/test_integration_\nstreaming_clone.py proves the fixture's own contract (login, gated catalog,\nunauthenticated rejection) against the live container, the same\nstand-it-up-first step PrestaShop's own decision note took before wiring it\ninto Spoor's exploration/extraction bench. No .feature file: this is fixture\ninfrastructure (§5.1), not a Spoor capability with runtime behavior to spec --\nsame precedent as the existing Sauce Demo/PrestaShop compose additions.\n\nVerified: image builds, container boots, login/catalog/gate/missing-video-404\nall checked live over HTTP, pytest -m integration -k streaming_clone (3\npassed), fast tier unchanged (734 passed), ruff/mypy/check_genericity.py all\nclean. fixtures/README.md and docs/ROADMAP.md §5.1 updated to describe four\nlive archetypes.\n\nCo-authored-by: Claude Sonnet 5 <noreply@anthropic.com>",
          "timestamp": "2026-09-30T11:36:38+03:00",
          "tree_id": "7d1eb122b201dd0bdb888819fe9f14ef4b257c61",
          "url": "https://github.com/HiddenTrail/ht-spoor/commit/c895af4ba19ba483c19c1028708ac658d04c7e7c"
        },
        "date": 1790757696961,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 222.485,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.03937,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 2.0889,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.12278,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 2.9616,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.06366,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 11.424,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.10905,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 17.8345,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.04126,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.2566,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.57234,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 32.0204,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.05116,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 12.9084,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 5.9939,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 126.5909,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.08295,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.5056,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.0105,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.4648,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 5271.9,
            "unit": "MB"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "bbeeef5a5101976395ca47fd77b9fc62bfaebf5c",
          "message": "fixtures/streaming-clone: add the seed video clips (#161)\n\n* fixtures/streaming-clone: add the seed video clips\n\nseed/videos/README.md (added in #160) documented the filename contract but\nshipped no video bytes -- generating a real, valid mp4 needed an encoder that\nenvironment didn't have. Six short, low-bitrate clips (one per catalog title,\nmatching the filenames in seed/catalog.json) are added here, so the fixture's\nwhole point -- exercising the <video> playback-state signal ROADMAP.md §2c\nnames -- actually works out of the box rather than only degrading gracefully.\n\nfixtures/README.md and the ROADMAP.md §5.1 decision note updated to say the\nclips are checked in, not pending. tests/test_integration_streaming_clone.py\ngained a fourth test asserting every seeded title's video is actually\nfetchable as video/mp4, not just that the catalog/login wiring works.\n\nVerified: rebuilt the image, booted the container, confirmed all six clips\nserve 200 video/mp4 over HTTP and pass an mp4 header sanity check (ftyp isom),\npytest -m integration -k streaming_clone (4 passed), fast tier unaffected\n(736 passed), ruff/mypy/check_genericity.py all clean.\n\nCo-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>\n\n* fixtures/streaming-clone: swap in the final seed video clips\n\nSame six filenames as before (matching seed/catalog.json) -- only the video\nbytes changed. Rebuilt the image, booted the container, and reran the\nstreaming-clone integration tests against the new clips (4 passed, including\nthe per-title playable-video check) to confirm the swap didn't break\nanything.\n\nCo-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>\n\n---------\n\nCo-authored-by: Claude Sonnet 5 <noreply@anthropic.com>",
          "timestamp": "2026-09-30T12:22:19+03:00",
          "tree_id": "4874cd93fb2f05f296e5e809c9ee95edfa3299ba",
          "url": "https://github.com/HiddenTrail/ht-spoor/commit/bbeeef5a5101976395ca47fd77b9fc62bfaebf5c"
        },
        "date": 1790760433914,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 226.115,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.04142,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 2.2326,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.12828,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 3.1108,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.0719,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 11.779,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.11232,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 18.7682,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.04678,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.2839,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.584,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 32.4601,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.05093,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 13.1346,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 6.01402,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 126.5131,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.09296,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.5446,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.01068,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.4735,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 5328,
            "unit": "MB"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "553fa042aa406c057aa1411918a34f417e6283e7",
          "message": "§2h/§5.1: wire streaming-clone into Spoor's extraction pipeline (#162)\n\nFollow-on to #160/#161, deferred there the same way PrestaShop's own landing\ndeferred it: stand the archetype up and prove its own contract first, wire it\ninto the real pipeline after. This is that wiring.\n\nfixtures/configs/streaming-clone-catalog.yaml extracts the title catalog via\na new item-mode config (item: \".tile\", fields for title/category/poster).\npublic/app.js gained a hidden per-tile .tile-category span, since a field\nselector resolves *within* its matched element (a descendant query), not\nagainst the element itself -- a category attribute on the tile div wouldn't\nhave been reachable.\n\ntests/test_integration_streaming_clone_extraction.py mirrors Sauce Demo's\ntest shape and gives streaming-clone its own end-to-end bring-your-own-\nsession (§2h) proof, structurally different from Sauce Demo's: a session-less\nrun escalates to the browser tier but extracts nothing (no .tile ever attaches\nwithout the fetch a login gates); an authenticated run (session captured by\ndriving a real Chromium through the login form -- Spoor performs no login\nitself, §2h/§0) extracts the catalog and matches a committed golden master\n(§5.4) -- an exact match fits here, unlike PrestaShop's deferred golden\nmaster, since the catalog is static checked-in seed data. No core code\nchanged (§0): both the config and the frontend tweak are fixture-side.\n\nVerified: pytest -m integration -k streaming_clone (6 passed, ~4min --\ntier 2's real Chromium overhead, not a hang: bisected a spurious \"hang\"\nduring development down to impatient test timeouts, confirmed with a\ntimed direct call to Tier2Resolver.run() before settling this in). Fast\ntier unaffected (736 passed). ruff/mypy/check_genericity.py all clean.\ndocs/ROADMAP.md §5.1 gained a decision note recording this wiring.\n\nCo-authored-by: Claude Sonnet 5 <noreply@anthropic.com>",
          "timestamp": "2026-09-30T13:11:14+03:00",
          "tree_id": "6bbe097db1226223346a982b3c131a09271fc7ec",
          "url": "https://github.com/HiddenTrail/ht-spoor/commit/553fa042aa406c057aa1411918a34f417e6283e7"
        },
        "date": 1790763367183,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 222.447,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.0416,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 1.9404,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.12475,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 2.9273,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.06836,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 11.4142,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.11239,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 18.0553,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.04952,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.2858,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.57484,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 32.2559,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.0526,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 12.8516,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 5.9883,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 126.4571,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.08316,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.527,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.01055,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.4576,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 5333.1,
            "unit": "MB"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "354b13cd1366d60abe06d7db4dcc357f9cef3b5b",
          "message": "Backlog: wiki network grouping should use browser resource type (§9, §2e) (#163)\n\nThe state page groups requests by a URL-extension heuristic\n(wiki._request_category) because the live driver records only request.url.\nPlaywright's request.resource_type is derived from how the page initiated the\nrequest, is equally generic (§0), and needs no response capture. Recorded as a\nnon-blocking follow-on to slice 6d with a sketch of the backward-compatible\nshape, not built now.\n\nCo-authored-by: Claude Opus 5.5 <noreply@anthropic.com>",
          "timestamp": "2026-09-30T14:18:50+03:00",
          "tree_id": "0e750537c3c64fb66c45bb7b01fbd2c3e8beb0a5",
          "url": "https://github.com/HiddenTrail/ht-spoor/commit/354b13cd1366d60abe06d7db4dcc357f9cef3b5b"
        },
        "date": 1790767395176,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 195.157,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.02239,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 1.2363,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.08231,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 2.0167,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.05368,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 7.9809,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.08002,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 12.3864,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.0269,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.1755,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.54592,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 30.3143,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.02695,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 7.8456,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 5.87518,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 123.6473,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.05987,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.3766,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.00635,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.2875,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 5373.5,
            "unit": "MB"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "4577bbd1bcba681dfbdaa493690825f51184843d",
          "message": "§2e/§2h: bring-your-own-session for spoor explore/apply-scaffold (#165)\n\nCloses #164. spoor run had session: from the start; exploration mode never\ndid -- PlaywrightDriver(url) was always constructed anonymously, a\ndeliberate scope narrowing (the \"Sauce Demo dropped from the exploration\nbench\" decision), not an oversight, but one that left streaming-clone's\nwhole reason for existing (a rich, login-gated catalog/detail surface)\nunreachable: spoor explore against it mapped exactly one state, the login\nscreen.\n\nThe real fork wasn't \"add a flag\": PlaywrightDriver.reset() deliberately\nclears cookies and web storage before every navigation so a reset is\nalways a true first visit. Loading a session only at context creation\nwould get silently wiped by the very first reset(). Resolution: a\nsupplied session redefines \"true first visit\" as \"as this session, not\nanonymous\" -- cookies are re-added via context.add_cookies() right after\nevery clear_cookies() in reset(); localStorage is restored by one\ncontext.add_init_script() registered once at __enter__ that runs before\nany page script on every document the context ever loads, so it needs no\nper-reset action. Proven together live: an anonymous crawl against a\nloopback fixture whose second page is cookie-gated and third is\nlocalStorage-gated maps 1 state, a cookie-only session reaches 2, a full\nsession reaches all 3 -- across the crawl's several reset() calls, not\njust the first.\n\nspoor/security/session.py:LoadedSession gained a raw field (the parsed\nstorage-state object itself) so the driver re-applies Playwright's own\ncookie/origin shapes exactly, rather than round-tripping through\nSessionCookie (built only for the static tier's httpx jar). --session\nlands on both explore and apply-scaffold, validated up front via\nload_session so a bad file fails before any browser launches; composes\nfreely with --resume-from (orthogonal). Spoor still performs no login\nitself (§2h/§0). No change to the BrowserDriver Protocol, so every\nexisting fake driver is untouched.\n\nManually verifying this against the fixture that motivated it surfaced a\nsecond, real gap in the same session: streaming-clone's tiles were <div>s\nwith a JS click handler and no ARIA role, invisible to the accessibility\ntree Spoor's discovery reads from -- an authenticated crawl reached the\nreal catalog (confirmed by screenshot) but still mapped only 1 state.\nConverted each tile to a real <button> (restyled to look identical); the\nsame session then reaches all 6 detail screens -- 7 states, 15\ntransitions, real screenshots including the seeded <video> preview.\n\nVerified: pytest -m browser (44 passed, no regressions), fast tier (742\npassed, +6 new), ruff/mypy/check_genericity.py clean, all 6 streaming-clone\nintegration tests still pass against the button-based tiles. Manual run:\nspoor explore http://127.0.0.1:3002/ --session <captured> --wiki --screenshots\nagainst the live fixture produced a real 7-state wiki with screenshots of\nthe catalog and every detail modal (video preview included) -- not just\nthe login screen. docs/ROADMAP.md, README.md, and fixtures/README.md\nupdated.\n\nCo-authored-by: Claude Sonnet 5 <noreply@anthropic.com>",
          "timestamp": "2026-09-30T14:26:29+03:00",
          "tree_id": "dd048661f320263dad58e258d1677c0a1577ed36",
          "url": "https://github.com/HiddenTrail/ht-spoor/commit/4577bbd1bcba681dfbdaa493690825f51184843d"
        },
        "date": 1790767882629,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 211.536,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.03244,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 1.9332,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.10945,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 2.5862,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.06321,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 9.8485,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.10074,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 16.5999,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.03589,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.241,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.56716,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 32.0251,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.03868,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 10.7609,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 5.92804,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 124.8082,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.06921,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.4211,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.00899,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.392,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 5379.9,
            "unit": "MB"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "b012c98b26f93866f0620638be2e447913edecfd",
          "message": "CLI: don't blame every explore skip on the sandbox gate (#167)\n\nFound while manually inspecting a real crawl's skip reasons (streaming-\nclone, #160-#165): spoor explore's run summary printed \"(destructive\nactions were skipped -- this target is not a declared sandbox)\" whenever\ngraph.skipped was non-empty, regardless of why each action was actually\nskipped. In that crawl, all 36 skips were \"could not be performed: ...\nnot located after replay\" (native <video> control elements, an\nactuation/relocation failure, see #166) -- none were destructive-gate\nskips -- so the summary was telling the operator the wrong reason for\nevery single one.\n\nspoor/exploration/safety.py already names DESTRUCTIVE_SKIP_REASON as the\none exact string a destructive-gate skip carries, specifically so a\ndownstream consumer can tell it apart from any other kind rather than\nmisreporting one as the other -- the CLI just never checked it. Now it\ncounts each kind separately and only claims the sandbox gate for skips\nthat actually came from it, and surfaces the other kind honestly instead\nof hiding it behind a wrong explanation.\n\nVerified: 3 new CLI tests (actuation-only skips report no \"destructive\"\nclaim, destructive-only skips still report correctly, a mix reports\nboth correctly). Fast tier 745 passed (+3), ruff/mypy/check_genericity.py\nclean.\n\nCo-authored-by: Claude Sonnet 5 <noreply@anthropic.com>",
          "timestamp": "2026-10-01T07:56:30+03:00",
          "tree_id": "4c651cd34a6729de6bf043f3707ab6e8452fb961",
          "url": "https://github.com/HiddenTrail/ht-spoor/commit/b012c98b26f93866f0620638be2e447913edecfd"
        },
        "date": 1790830899781,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 215.643,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.03267,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 1.8341,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.10681,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 2.5996,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.07269,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 10.8988,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.11298,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 17.003,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.0343,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.2472,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.56542,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 31.7403,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.04343,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 11.4119,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 5.95643,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 125.3118,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.0731,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.4594,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.00903,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.3917,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 5307.1,
            "unit": "MB"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "a9dd33acf98ebe0130f2fb37c2f04500baf7881f",
          "message": "§2e: exclude native <video>/<audio> control children from discovery (#168)\n\nCloses #166. Exploring streaming-clone with a session supplied reached\nevery detail screen correctly but still logged 36 skips every run, all\n\"could not be performed: ... not located after replay\" on the same six\nelements: the native <video controls> play/mute/volume/scrubber/\nfullscreen/overflow-menu buttons.\n\nInvestigated against a real Chromium build rather than guessed at. My\noriginal hypothesis in #166 (controls auto-hide without a mouse hover)\nwas wrong -- these elements resolve and box-model fine over CDP every\ntime, hover or not, first visit or after a full reset-and-replay. The\nactual cause: document.elementFromPoint -- what the live click-\nverification every discovered element passes through (§2e 7a) checks\nthe click lands on -- always retargets a hit anywhere inside a\n<video>/<audio> element's *closed* user-agent shadow DOM back to the\nhost element itself. Confirmed directly: elementFromPoint at a play\nbutton's coordinates returns the <video> tag, every time. A structural\nfact of the browser's shadow-DOM boundary, true on every site with a\nplain HTML5 media element (§0), not a fixture quirk -- so no amount of\nretrying would ever make the existing verification succeed for one.\n\ndiscover_actions now excludes these at the source: _has_media_ancestor\nwalks a candidate node's parentId chain in the same\nAccessibility.getFullAXTree snapshot discovery already has (confirmed\nlive the ancestor chain does carry a role: \"Video\"/\"Audio\" node -- no\nextra CDP round-trip). Cycle-guarded; tolerant of a node missing\nparentId/nodeId (every existing fake driver), which simply never\nmatches -- the same \"include it\" default the rest of discovery already\ntakes for any other missing field.\n\nfeatures/exploration_discovery.feature gained three scenarios: a native\nmedia-control child excluded, an ordinary wrapped element still\ndiscovered (the exclusion doesn't over-fire on non-media ancestors),\nand a cyclic ancestor chain not hanging discovery.\n\nVerified: all existing discovery/exploration tests pass unaffected\n(fast tier 748 passed, +3 new), ruff/mypy/check_genericity.py clean.\nLive re-run of the exact crawl that motivated this: the same streaming-\nclone crawl that logged 36 skips before now logs 0, discovering the\nsame 7 states. docs/ROADMAP.md records the finding and the fix.\n\nCo-authored-by: Claude Sonnet 5 <noreply@anthropic.com>",
          "timestamp": "2026-10-01T10:13:30+03:00",
          "tree_id": "d671474fadb974baea9de5cc1e2ef0d03482070b",
          "url": "https://github.com/HiddenTrail/ht-spoor/commit/a9dd33acf98ebe0130f2fb37c2f04500baf7881f"
        },
        "date": 1790839137769,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 239.284,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.04762,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 2.4527,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.13576,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 3.2816,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0002,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.09563,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 14.5305,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.14306,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 22.9427,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.05417,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.3282,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.60463,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 32.7391,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.0605,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 15.8983,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 6.04326,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 127.5328,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.09518,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.5699,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.01215,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.5282,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 5294.1,
            "unit": "MB"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "02a4bd4ae3791e48b6b443941835e22e6458ac2e",
          "message": "§2d: link following with scope rules (closes #169) (#172)\n\ndocs/COMPETITIVE_PLAN.md names this Spoor's single biggest concrete gap\nagainst Scrapy/Crawlee: pagination.next follows exactly one declared\nlink in a straight chain; there was no way to discover and follow\nmultiple links per page. Split out of the bigger crawl-engine issue\n(#148), which is blocked on the still-open D1 Crawlee decision (#146)\n-- this piece isn't, since link discovery and scope filtering are\nSpoor-side generic logic no matter what (if anything) eventually sits\nunderneath as a request-queue/concurrency layer.\n\nNew CrawlScope config (spoor/core/config.py): include/exclude glob\npatterns (fnmatch.fnmatchcase against the URL path, case-sensitive),\nmax_depth, same_origin (default true). Both tiers' page-following loops\nwere structurally identical -- a single url variable, a seen set, the\nexisting _MAX_PAGES cycle guard, url = _next_url(...) at the bottom --\nso this generalizes that single-URL chain into a deque[tuple[str, int]]\nfrontier rather than inventing a parallel mechanism. Every other\nper-page behavior (politeness, retry, change detection, challenge\ndetection, signal capture, the _MAX_PAGES ceiling) is unchanged -- these\nare just more frontier items flowing through the identical loop body.\n\nTwo non-obvious design points, both pinned by scenarios: a\npagination.next hop never counts against max_depth (continues the same\nlisting rather than branching, so the two compose without surprise);\nand break became continue on a blocked/dead-lettered frontier item in\nboth loops (unobservable with a single chain, but necessary so one\nfailed branch doesn't abort sibling branches still waiting their turn\n-- a regression scenario confirms the no-crawl-at-all case is still\nbyte-for-byte unchanged).\n\nfeatures/extraction.feature gained the fast-tier scope-rule matrix\n(include, exclude-wins-over-include, max_depth, same-origin default and\nopt-out, the pagination-composition case, the regression guard) plus\none @browser scenario for tier parity. A live multi-page proof against\nPrestaShop is a natural immediate follow-on, deferred the same way\nPrestaShop's own onboarding deferred its integration test.\n\nVerified: pytest -m browser (45 passed, +1, no regressions), fast tier\n(752 passed, +7), ruff/mypy/check_genericity.py clean. Manually\nconfirmed the one edge case worth double-checking rather than assuming:\nan empty `crawl: {}` block follows every same-origin link and excludes\nnothing, never the opposite. docs/ROADMAP.md and README.md updated.\n\nCo-authored-by: Claude Sonnet 5 <noreply@anthropic.com>",
          "timestamp": "2026-10-01T10:14:56+03:00",
          "tree_id": "9e43615a227a0fe0da030c4a30c42cd45852d63d",
          "url": "https://github.com/HiddenTrail/ht-spoor/commit/02a4bd4ae3791e48b6b443941835e22e6458ac2e"
        },
        "date": 1790839202684,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 227.907,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.04241,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 2.2105,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.12666,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 3.0128,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.07054,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 12.2957,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.12572,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 20.2609,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.05625,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.3101,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.5769,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 32.3444,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.05418,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 14.0683,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 6.00467,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 126.5529,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.09136,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.5588,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.01081,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.4705,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 5354.6,
            "unit": "MB"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "e1d31069d9394f011390cb75a989bfb18be99750",
          "message": "Record D1: do not adopt Crawlee (closes #146) (#176)\n\nThe hands-on spike found Crawlee's base package lean and its\nRequestQueue/SitemapRequestLoader/AutoscaledPool usable standalone --\nthe adoption case looked real. It didn't hold up against what actually\ngot built next: #169 (link following with scope rules) and #170\n(sitemap/robots.txt seeding) -- the two biggest items the competitive\nplan marked Depend or Depend-or-Adapt -- both shipped with zero Crawlee\ndependency, at no higher cost than adopting would have been.\n\nThat leaves autoscaling concurrency and resumable persisted crawl\nstate -- and the second was never simply free from Crawlee either,\nsince reconciling its storage model with Spoor's existing local-cache\nconventions and the already-shipped exploration resume story is real\ndesign work regardless. The deciding cost against the narrowed\nremainder: Crawlee is asyncio-native throughout, Spoor is synchronous\nthroughout, and adopting even just AutoscaledPool means bridging sync\nand async for one feature -- an ongoing structural cost, not a\none-time task. A plain stdlib ThreadPoolExecutor with per-domain\nsemaphores covers Spoor's actual bottleneck (politeness-gated HTTP\nfetches, not CPU-bound work) without ever leaving its synchronous\nworld.\n\nCorrects the real ROADMAP/code mismatch the competitive plan flagged:\nsection 2.1's \"Crawlee's autoscaling pool already handles per-domain\nconcurrency\" was asserted as current fact while crawlee was never a\ndependency. Fixed in both the §2d prose and the §7 tech-stack\nreference table. #148 (the crawl-engine mega-issue) is closed,\nreplaced by #174 (concurrency) and #175 (resumable state), each scoped\nand in-house.\n\nCo-authored-by: Claude Sonnet 5 <noreply@anthropic.com>",
          "timestamp": "2026-10-01T11:54:14+03:00",
          "tree_id": "565db1a4603201236e910ea5ce96c78088572c09",
          "url": "https://github.com/HiddenTrail/ht-spoor/commit/e1d31069d9394f011390cb75a989bfb18be99750"
        },
        "date": 1790845152852,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 222.34,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.03693,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 1.8956,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.12502,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 2.9968,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.06469,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 10.8514,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.11258,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 18.3365,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.05447,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.2819,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.57234,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 32.219,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.0517,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 12.9389,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 5.99693,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 126.5387,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.08261,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.4948,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.01037,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.4732,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 5424.3,
            "unit": "MB"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "43e367c703273ca423c6a3cee4c8c591d425aec1",
          "message": "§2d: sitemap.xml and robots.txt as crawl seed sources (closes #170) (#173)\n\nThe second of the two D1-independent pieces split out of #148 alongside\n#169, for the same reason: no dependency needed -- a sitemap is plain\nXML and robots.txt is already fetched and parsed by Politeness.\n\nurllib.robotparser.RobotFileParser -- the parser Politeness._parser\nalready builds and caches per origin -- turned out to already expose\nsite_maps(), reading a robots.txt's Sitemap: directive(s) for free; no\nnew robots.txt fetch or parsing needed, just a new public\nPoliteness.sitemap_seed_urls(target) that fetches and parses whatever\nit names. A <urlset> yields its page URLs directly; a <sitemapindex>'s\nentries are child sitemaps, fetched the same way breadth-first, bounded\nby a fetched-sitemaps cap and a total-URL cap against a cyclic or\nunbounded index. xml.etree.ElementTree (stdlib) parses tolerantly of a\nmissing/non-sitemaps.org namespace by comparing tag local names, not\nfull namespaced tags. A fetch failure, non-200, or unparseable/\nunrecognized-root XML yields nothing from that source -- the same\ntolerant degrade the rest of this module already takes for a missing\nrobots.txt.\n\nOpt-in (crawl.sitemap: true, default false): pulling in a whole site's\nsitemap in one step is a bigger behavior change than crawl: being set\nalone implies, the same reasoning change_detection and every capture.*\nflag already follow. Seeded URLs are filtered through the same\n_in_scope check #169 already built, and added to the frontier at depth\n0 -- a sitemap names known entry points, not links discovered from a\npage.\n\nfeatures/operational.feature gained the scenario matrix (seeds the\ncrawl, seeds still scope-filtered, no Sitemap: yields nothing extra, a\nsitemap index follows to its children, malformed XML degrades rather\nthan crashes, off-by-default regression guard) -- reusing that file's\nexisting per-scenario dynamic-routing-table pattern rather than a\nshared static fixture, since a shared fixtures/static/robots.txt would\nhave silently changed every other test on localhost:8000.\n\nVerified: 6 new scenarios pass, fast tier 761 passed (no regressions),\nthe two browser-tier extraction scenarios touched by the Tier2Resolver\nchange still pass, ruff/mypy/check_genericity.py clean. docs/ROADMAP.md\nand README.md updated.\n\nCo-authored-by: Claude Sonnet 5 <noreply@anthropic.com>",
          "timestamp": "2026-10-01T12:04:54+03:00",
          "tree_id": "d70e1336cd903f14098dee6e34bf30e7a07048eb",
          "url": "https://github.com/HiddenTrail/ht-spoor/commit/43e367c703273ca423c6a3cee4c8c591d425aec1"
        },
        "date": 1790845822403,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 232.667,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.04612,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 2.3339,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.13701,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 3.2868,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0002,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.08507,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 13.4593,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.13196,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 21.5718,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.05822,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.3608,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.59827,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 32.5657,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.05989,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 14.7902,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 6.01444,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 127.1652,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.09518,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.569,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.01149,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.5261,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 5334.6,
            "unit": "MB"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "103989476+pekka-hiddentrail@users.noreply.github.com",
            "name": "pekka-hiddentrail",
            "username": "pekka-hiddentrail"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "e602d4ebe477ccbbd713b0cc827bd459d03593d6",
          "message": "Add bring-your-own-proxy support (closes #149) (#177)\n\nOperator-supplied proxy routes a run's traffic through it — the same\nbring-your-own posture as session: for authenticated targets. A new\nproxy: config block (server, username, password, bypass) wires into\nboth resolvers' httpx clients and the browser tier's Chromium launch;\nsince Politeness and sitemap seeding reuse whichever client they're\ngiven, robots.txt/sitemap fetches route through it automatically too.\n\nCo-authored-by: Claude Sonnet 5 <noreply@anthropic.com>",
          "timestamp": "2026-10-01T20:01:53+03:00",
          "tree_id": "16ae62d484976b7c1e07cce18172d210b95de325",
          "url": "https://github.com/HiddenTrail/ht-spoor/commit/e602d4ebe477ccbbd713b0cc827bd459d03593d6"
        },
        "date": 1790874429614,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "juice-shop-small / total elapsed",
            "value": 225.163,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes median",
            "value": 0.04042,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / ax_nodes total",
            "value": 2.1359,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals median",
            "value": 0.1296,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / capture_signals total",
            "value": 3.089,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url median",
            "value": 0.00001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / current_url total",
            "value": 0.0001,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box median",
            "value": 0.07606,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_box total",
            "value": 11.9727,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot median",
            "value": 0.11614,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / element_screenshot total",
            "value": 19.9865,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot median",
            "value": 0.06326,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / opened_screenshot total",
            "value": 0.312,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform median",
            "value": 0.58188,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / perform total",
            "value": 32.1657,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe median",
            "value": 0.0541,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / probe total",
            "value": 13.5026,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset median",
            "value": 5.97838,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / reset total",
            "value": 126.081,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot median",
            "value": 0.09114,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / screenshot total",
            "value": 0.5454,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html median",
            "value": 0.01115,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / state_html total",
            "value": 0.4866,
            "unit": "s"
          },
          {
            "name": "juice-shop-small / peak RSS",
            "value": 5330.1,
            "unit": "MB"
          }
        ]
      }
    ]
  }
}