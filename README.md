# VS Code Updater Script (tar.gz, universal Linux)

A small Python script that automates updating a **manually installed**
copy of Visual Studio Code on Linux, using the official `tar.gz` build.

It works on **any Linux distribution** — it doesn't rely on a package
manager, AUR, or any distro-specific tooling, only Python 3 and `tar`,
which are available almost everywhere. It was originally created for
**Arch Linux** (to avoid depending on the AUR), but there's nothing
Arch-specific about it.

## What it does

Running the script performs these steps, in order:

1. **Removes the old install** — deletes the `VSCode-linux-x64` folder if it
   already exists in the same directory as the script (skips this step if
   the folder isn't there).
2. **Downloads the latest stable build** — fetches the current `tar.gz`
   archive from VS Code's official download endpoint:
   ```
   https://code.visualstudio.com/sha/download?build=stable&os=linux-x64
   ```
   This URL always redirects to the newest stable release, so you never
   need to update the link.
3. **Extracts the archive** — runs `tar -xvzf archive.tar.gz` in the
   script's folder, which recreates the `VSCode-linux-x64` directory with
   the new version.
4. **Cleans up** — deletes the downloaded `archive.tar.gz` file once
   extraction is complete.

## How the code is organized

| Function | Purpose |
|---|---|
| `remove_existing_folder()` | Deletes `VSCode-linux-x64` if present, using `shutil.rmtree`. |
| `download_archive()` | Downloads the archive with `urllib.request` (sends a browser-like `User-Agent` header, since some CDNs reject the default Python one). |
| `extract_archive()` | Calls `tar -xvzf archive.tar.gz` via `subprocess.run`, executed in the script's own directory. |
| `delete_archive()` | Removes the downloaded `.tar.gz` file after a successful extraction. |
| `main()` | Runs the four steps in sequence and handles errors (extraction failures, network errors, etc.), exiting with a non-zero status code on failure. |

All paths are computed relative to the script's own location
(`os.path.dirname(os.path.abspath(__file__))`), so it works no matter which
directory you run it from.

## Requirements

- Python 3
- `tar` available on your system (preinstalled on virtually all Linux
  distributions)
- No external Python packages — only the standard library is used

These two requirements are present by default on nearly every mainstream
Linux distro (Arch, Debian/Ubuntu, Fedora, openSUSE, etc.), which is what
makes the script portable across distributions.

## Usage

```bash
python3 vscode_simple_updater_for_arch.py
```

The script will print progress messages for each step. After it finishes,
you'll have an updated `VSCode-linux-x64` folder in the same directory,
and no leftover archive file.

To actually launch VS Code, first make the binary executable, then run it
directly from inside the extracted folder:

```bash
cd VSCode-linux-x64/bin
chmod +xrw code
./code
```

You may want to symlink this into your `PATH`, for example:

```bash
ln -sf ~/Binaries/VSCode-linux-x64/bin/code ~/.local/bin/code
```//assumes ~/.local/bin is in your PATH

## Suggested setup: keep it in `~/Binaries`

Since this is a manual install (not managed by any package manager), it's
convenient to keep all your manually managed binaries in one predictable
place, regardless of which distro you're on. A simple approach:

1. Create a `Binaries` folder in your home directory:
   ```bash
   mkdir -p ~/Binaries
   ```
2. Move (or save) this script into that folder:
   ```bash
   mv vscode_simple_updater_for_arch.py ~/Binaries/
   ```
3. Run it from there:
   ```bash
   cd ~/Binaries
   python3 vscode_simple_updater_for_arch.py
   ```

This way, `~/Binaries/VSCode-linux-x64` becomes your VS Code installation,
and running the script again in the future will always clean out the old
version and pull the latest stable build in place, without touching
anything else on your system.

## Notes

- The script does **not** need `sudo` — everything happens inside
  `~/Binaries` (or wherever you place the script), not system directories.
- Re-running the script is safe: it only deletes its own previous
  `VSCode-linux-x64` folder and archive, nothing else.
- If Microsoft changes the download endpoint format, only the
  `DOWNLOAD_URL` constant at the top of the script would need updating.