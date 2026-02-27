---
date: 2026-02-27
title: DiskSpaceTracker
excerpt: Where did my disk space go? A quiet background process that watches your Mac's directories over time, so when your disk fills up you actually know why.
Tags: tech, softwareweneed, Mac
image: hero.svg
---

My MacBook's disk fills up over time. It always does. And every time I hit that "Your disk is almost full" notification, I have no idea what happened. Did I download something huge? Did a cache balloon? Did some app silently dump gigabytes into Library? I open Disk Utility, stare at a colored bar, and start guessing.

That's not how it should work. I want a process that quietly tracks my disk usage over time — directory by directory — so when things get tight, I can look at a timeline and see: _this is what grew, this is when it happened, this is where to look._

## What DiskSpaceTracker would do

A lightweight background daemon that runs only when two conditions are met:

1. **The Mac is idle** — no active user input for N minutes
2. **The Mac is on power** — no draining the battery for bookkeeping

When both conditions are true, it wakes up and takes a snapshot.

## The snapshot

A snapshot walks the directory tree top-down and records, for each directory:

- **Path** — the directory
- **Size** — total size including subdirectories
- **Content hash** — a hash of the `ls` output (filenames, sizes, modification dates)
- **Timestamp** — when the snapshot was taken

The content hash is the key idea. If a directory's hash hasn't changed since the last snapshot, nothing inside it changed — skip the subdirectories. This makes the scan fast even on large disks. You only drill deeper where something actually moved.

```text
/Users/till           2026-02-27T03:12  148.2 GB  a3f8c1...
/Users/till/Downloads 2026-02-27T03:12   23.1 GB  9e2b44...  ← changed
/Users/till/Library   2026-02-27T03:12   41.7 GB  7d1f09...  ← changed
/Users/till/Documents 2026-02-27T03:12   62.3 GB  a3f8c1...  ← unchanged, skip children
```

## Storage format

A simple local database (SQLite would be fine) with one table:

| dir                        | date       | size_bytes  | content_hash |
| -------------------------- | ---------- | ----------- | ------------ |
| /Users/till/Downloads      | 2026-02-27 | 24851390464 | 9e2b44...    |
| /Users/till/Downloads      | 2026-02-20 | 19327352832 | f1a3c7...    |
| /Users/till/Library/Caches | 2026-02-27 | 8741281792  | 3bf812...    |

Every row is a snapshot of one directory at one point in time. Query it however you like — growth per week, biggest movers, directories that appeared out of nowhere.

Important: the database should also record when a directory was _confirmed unchanged_. If I scan `/Users/till/Documents` and the hash is the same as last week, that's a data point — "verified, no change." That's fundamentally different from a directory I simply haven't looked at in months. Without this distinction, you can't tell "stable" from "unknown."

## What I'd want to see

A simple CLI or menu bar view that answers:

- **What grew the most** in the last week / month?
- **What's new** — directories or files that didn't exist before?
- **Timeline** — how did `/Users/till/Library/Caches` change over the last 6 months?
- **Alerts** — notify me when any single directory grows by more than X GB in a week

Nothing fancy. A few sorted tables and maybe a sparkline. The data is the product — the UI is just a way to ask questions.

## Why this doesn't exist (or why existing tools miss the point)

There are disk space analyzers — DaisyDisk, GrandPerspective, ncdu. They show you what's big _right now_. That's useful for a one-time cleanup, but it doesn't tell you what changed. If `/Library/Developer/CoreSimulator` is 30 GB, was it always 30 GB? Or was it 5 GB last month? Without history, you can't tell.

There are also monitoring tools, but they track _total_ free space as one number. "Your disk went from 40 GB free to 12 GB free in three weeks." Great — but _where_?

DiskSpaceTracker sits in between: it tracks space per directory over time. That's the missing piece.

## Technical thoughts

- **macOS-native** — uses `NSProcessInfo` for idle detection, IOKit for power state
- **Runs as a LaunchDaemon** — standard macOS way to schedule background work
- **SQLite storage** — single file, no server, easy to query, easy to back up
- **Exclude list** — skip `/System`, Time Machine snapshots, and other paths that aren't actionable
- **Minimal footprint** — the hash-based skip means most of the tree is never touched on quiet days
- **Smart scan priority** — the scanner can't check everything every time, so it needs to decide what to look at next. A simple algorithm that weighs three factors: biggest directories first (that's where the space is), least-recently-scanned directories next (don't leave blind spots), and directories whose parent hash changed (something moved). This way the most valuable snapshots get taken first, and over time coverage stays even.

The whole thing could be a single Swift binary with no dependencies. Or a Python script with `osascript` hooks. Doesn't matter — the idea is simple enough that the implementation is almost trivial. What matters is that it runs consistently and builds up history.

That's the software I want. Not another "what's big right now" tool — a quiet observer that builds a timeline of where my disk space goes, so when things get tight, the answer is already there.
