#!/usr/bin/env python3
"""tidy-downloads: sort a Downloads folder by type. Dry-run by default, undo included."""
import argparse, json, os, sys, time

CATS = {
 "Images": "jpg jpeg png gif webp svg bmp heic tiff ico",
 "Documents": "pdf doc docx txt md rtf odt xls xlsx csv ppt pptx epub",
 "Archives": "zip tar gz tgz bz2 xz 7z rar",
 "Installers": "exe msi dmg pkg deb rpm appimage apk",
 "Audio": "mp3 wav flac ogg m4a aac",
 "Video": "mp4 mkv mov avi webm",
 "Code": "py js ts json html css sh yml yaml",
}
EXT = {e: c for c, s in CATS.items() for e in s.split()}
PARTIAL = {"crdownload", "part", "download", "tmp"}
UNDO = ".tidy-downloads-undo.json"

def free(dest):
    if not os.path.lexists(dest): return dest
    b, e = os.path.splitext(dest); n = 1
    while os.path.lexists(f"{b} ({n}){e}"): n += 1
    return f"{b} ({n}){e}"

def plan(root, min_age):
    out, taken = [], set(); now = time.time()
    for name in sorted(os.listdir(root)):
        p = os.path.join(root, name)
        if name.startswith(".") or os.path.islink(p) or not os.path.isfile(p): continue
        ext = name.rsplit(".", 1)[-1].lower() if "." in name.strip(".") else ""
        if ext in PARTIAL or now - os.path.getmtime(p) < min_age: continue
        d = os.path.join(root, EXT.get(ext, "Other"))
        dest = free(os.path.join(d, name)); k = 1
        while dest in taken:
            b, e = os.path.splitext(os.path.join(d, name)); dest = f"{b} ({k}){e}"; k += 1
        taken.add(dest); out.append((p, dest))
    return out

def main():
    a = argparse.ArgumentParser(prog="tidy-downloads")
    a.add_argument("folder", nargs="?", default=os.path.expanduser("~/Downloads"))
    a.add_argument("--apply", action="store_true")
    a.add_argument("--undo", action="store_true")
    a.add_argument("--min-age", type=int, default=3600, help="skip files newer than N seconds")
    o = a.parse_args(); root = os.path.abspath(o.folder)
    if not os.path.isdir(root): sys.exit(f"not a folder: {root}")
    log = os.path.join(root, UNDO)
    if o.undo:
        if not os.path.exists(log): sys.exit("no undo file found")
        moves = json.load(open(log)); n = 0
        for src, dest in reversed(moves):
            if os.path.exists(dest) and not os.path.exists(src):
                os.rename(dest, src); n += 1
            else: print("skip (changed):", dest)
        for d in {os.path.dirname(m[1]) for m in moves}:
            try: os.rmdir(d)
            except OSError: pass
        os.remove(log); print(f"restored {n} files"); return
    moves = plan(root, o.min_age)
    for s, d in moves: print(f"{os.path.relpath(s, root)}  ->  {os.path.relpath(d, root)}")
    print(f"\n{len(moves)} files would move." if not o.apply else "")
    if not o.apply:
        if moves: print("Dry run. Nothing moved. Add --apply to do it.")
        return
    if os.path.exists(log): sys.exit("an undo file already exists; run --undo first")
    done = []
    for s, d in moves:
        os.makedirs(os.path.dirname(d), exist_ok=True); os.rename(s, d); done.append([s, d])
        json.dump(done, open(log, "w"), indent=1)
    print(f"moved {len(done)} files. Undo: tidy-downloads {o.folder} --undo")

if __name__ == "__main__": main()
