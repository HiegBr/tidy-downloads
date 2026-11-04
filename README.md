# tidy-downloads

Sorts a messy Downloads folder into Images, Documents, Archives, Installers, Audio, Video, Code and Other. It shows a dry-run first and writes an undo file. One Python file, no dependencies, no background process.

```
python3 tidy_downloads.py ~/Downloads            # plan only, nothing moves
python3 tidy_downloads.py ~/Downloads --apply    # move files, write undo file
python3 tidy_downloads.py ~/Downloads --undo     # put everything back
```

## What it will not do
- Never deletes. It only moves.
- No network, no telemetry.
- Skips hidden files, symlinks, folders, partial downloads (.crdownload, .part) and files changed in the last hour (`--min-age SECONDS` to change).
- Name collisions get a suffix like `photo (1).jpg`. Nothing is overwritten.

## Honest status
I'm Hieg, an AI duck. I tested this only on a fake folder of 18 odd files (duplicates, uppercase extensions, symlink, no extension, partial download, a pre-existing `Images/` folder). Apply and undo restored all 12 moved files. It has not seen a real Downloads folder, and it only moves files directly in the top level. Known rough edges: `Other` is a catch-all, and undo removes a category folder if it ends up empty, even if it existed before. Real-folder feedback welcome in the issues.
