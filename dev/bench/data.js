window.BENCHMARK_DATA = {
  "lastUpdate": 1790690770371,
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
      }
    ]
  }
}