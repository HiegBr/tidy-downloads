# Shaped brief: dry-run report for tidy-downloads

**Problem.** People fear auto-organizers touching Downloads (e.g. Simple-Organizer issue #65). They need to see exactly what would happen before anything moves.

**Rough flow.**
1. User runs `python3 tidy_downloads.py ~/Downloads` (no flags).
2. Tool prints a plan: each file -> destination folder, grouped by folder, plus counts of skipped files with a reason (hidden, partial, recent, lock file).
3. Nothing is written. Exit with a hint on how to apply.
4. Only with `--apply` does it move files and write an undo file; `--undo` restores.

**Cap.** Two days. Remaining work: a per-reason skipped summary and one real-folder test from a volunteer. If not done by Day 20, stop.

**Will not do.** Delete anything. Touch the network. Recurse into subfolders. Run on a schedule. Have a GUI. Guess file contents. Claim it works on Windows or huge folders.

**Done when.** One real person has run step 1 and told me what it got wrong.
