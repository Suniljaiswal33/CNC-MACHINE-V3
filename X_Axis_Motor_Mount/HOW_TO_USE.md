# How to Use: Repo Reorganiser Scripts

Two scripts — run them in order.

---

## Prerequisites

- Python 3 installed
- All repo folders downloaded and sitting in one parent folder
- Script files placed in the same parent folder

Your folder should look like this before starting:

```
sft-01/
├── repo-1/
├── repo-2/
├── ...
├── source_stls/               ← all source STL files dumped here (flat, no subfolders)
├── reorganise_repos.py
└── copy_source_stls.py
```

---

## Script 1 — `reorganise_repos.py`

**What it does:**
Pairs `.py` files with their output `.stl` files and organises them into named part folders.

Before:
```
repo-1/
├── Python/
│   └── PartName.py
└── stl output/
    └── PartName_output.stl
```

After:
```
repo-1/
└── PartName/
    ├── PartName.py
    └── PartName.stl
```

**Naming rules it handles automatically:**
- Strips `_output` or `_result` suffix from STL filenames before matching
- Matching is case-insensitive (`PartName.py` matches `partname.stl`)
- Final files are always named after the `.py` file stem

**How to run:**

1. Open terminal and `cd` into the parent folder:
```bash
cd /path/to/sft-01
```

2. Do a dry run first (no files will be touched):
```bash
# Open reorganise_repos.py, set DRY_RUN = True, save, then:
python reorganise_repos.py
```

3. Check the output — verify all pairs look correct, no unexpected warnings.

4. Set `DRY_RUN = False`, save, then run for real:
```bash
python reorganise_repos.py
```

**What to watch for in the log:**
- `UNMATCHED .py` — a Python file had no matching STL
- `UNMATCHED .stl` — an STL had no matching Python file
- `SKIP` — a repo folder didn't have the expected `Python/` or `stl output/` folders
- `LEFT '.../' — N unmatched file(s) remain` — old folder wasn't deleted because unmatched files are still in it

> Log is saved to `reorganise_repos.log` in the parent folder.

---

## Script 2 — `copy_source_stls.py`

**What it does:**
Takes all source STL files from the `source_stls/` folder and moves each one into its matching part folder, renaming it with a `source_` prefix.

Before:
```
source_stls/
└── PartName.stl

repo-1/
└── PartName/
    ├── PartName.py
    └── PartName.stl
```

After:
```
source_stls/          ← now empty
repo-1/
└── PartName/
    ├── PartName.py
    ├── PartName.stl
    └── source_PartName.stl
```

**How to run:**

1. Make sure `source_stls/` folder is populated with all source STLs.

2. Do a dry run first:
```bash
# Open copy_source_stls.py, set DRY_RUN = True, save, then:
python copy_source_stls.py
```

3. Check the output — verify matches look correct.

4. Set `DRY_RUN = False`, save, then run for real:
```bash
python copy_source_stls.py
```

**What to watch for in the log:**
- `MISSING` — no source STL found for a part folder (filename mismatch)
- `SKIP (already exists)` — source STL already in the part folder (set `FORCE = True` to overwrite)
- `OVERWRITE (force)` — existing file was replaced

> Log is saved to `copy_source_stls.log` in the parent folder.

---

## Flags Reference

| Script | Flag | Default | What it does |
|---|---|---|---|
| `reorganise_repos.py` | `DRY_RUN` | `False` | Preview only, no files touched |
| `copy_source_stls.py` | `DRY_RUN` | `False` | Preview only, no files touched |
| `copy_source_stls.py` | `FORCE` | `True` | Overwrite existing source STLs |

---

## Troubleshooting

**Script says "No folders found"**
Make sure you're running the script from the parent folder, not from inside a repo.

**Lots of MISSING warnings for source STLs**
The source STL filename doesn't match the part folder name. Check for extra suffixes or typos. Matching is case-insensitive but the stem must otherwise be identical.

**UNMATCHED .py or .stl warnings**
A file in `Python/` or `stl output/` has no pair. Check for typos or missing files. The unmatched file stays in the old folder and is not moved.

**Repo was SKIPPED**
The repo doesn't have folders named exactly `Python/` and `stl output/`. Check the actual folder names inside that repo.

---

## Script 3 — `volumetric_validation.py` (per part folder)

**What it does:**
Downloads both STLs for a part directly from GitHub and computes the volume difference.

**One-time setup — GitHub token:**

The script needs a Personal Access Token (PAT) to access private repos. Set it once on your machine:

Mac/Linux:
```bash
export GITHUB_TOKEN="your_token_here"
```
Windows:
```bash
setx GITHUB_TOKEN "your_token_here"
```

Get a token from: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token → check `repo` scope.

**How to run:**
1. Download the part folder from GitHub (or clone the whole repo)
2. Open terminal, `cd` into the part folder
3. Run:
```bash
python volumetric_validation.py
```

**What it does automatically:**
- Detects the repo and part name from its own location
- Downloads `{stem}.stl` and `source_{stem}.stl` from GitHub
- Computes volume difference (absolute + %)
- Saves results to `volumetric_validation.log` in the same folder

**Log output looks like:**
```
Source volume : 12453.21 mm³
Output volume : 12401.05 mm³
Difference    : 52.16 mm³  (0.42%)
```
