# pyaes_bruteforce

> A small, **lab‑safe** utility that attempts to recover the password for files encrypted with the **pyAesCrypt** format (`*.aes`). Built for your **own data** recovery, training, and research.

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/scope-personal%20recovery%20%2F%20education-blue">
  <img alt="license" src="https://img.shields.io/badge/license-MIT-green">
  <img alt="python" src="https://img.shields.io/badge/python-3.9%2B-orange">
</p>

---

## ✨ Features

- **Wordlist brute force** against pyAesCrypt (`*.aes`) files
- **Resume** capability via `--resume <N>` to skip the first *N* candidates
- **Streaming decryption** using pyAesCrypt’s buffered API (default 64 KiB blocks)
- **Safe output handling**: writes to a temporary file first, then atomically moves on success
- Minimal dependencies and a straightforward CLI

> This tool targets the **pyAesCrypt container format** specifically. It does not attack general ZIP/7z/GPG containers.

---

## 🧩 How it works (at a glance)

For each candidate password in the wordlist:
1. Attempt decryption via `pyAesCrypt.decryptFile(infile, tmp_out, password, BUF_SIZE)`.
2. On success, move the temporary file to the requested output path.
3. On failure, catch the exception and continue with the next candidate.

No plaintext is kept if a password is incorrect; temporary files are cleaned up.

---

## 🚀 Quick start

### 1) Install requirements

```bash
python -m venv .venv && source .venv/bin/activate
pip install pyAesCrypt
```

> If you prefer pinned versions, add `pyAesCrypt` to your `requirements.txt` and pin a specific release.

### 2) Usage

The script name below reflects your file: `simple_pyaes_bruteforce.py`.

```bash
# Basic usage
python simple_pyaes_bruteforce.py \
  -i encrypted_file.aes \
  -w /path/to/wordlist.txt \
  -o recovered.bin
```

```bash
# Resume from a specific wordlist index (e.g., 123456th candidate)
python simple_pyaes_bruteforce.py \
  -i web_20250806_120723.zip.aes \
  -w rockyou.txt \
  -o web.zip \
  --resume 10000
```

Command‑line options (as implemented in this repository):

| Flag | Description |
|---|---|
| `-i, --infile` | Path to the `*.aes` file (pyAesCrypt format) |
| `-w, --wordlist` | Path to the candidate password list (one per line) |
| `-o, --outfile` | Where to write the decrypted output on success |
| `--resume` | (Optional) Integer offset in the wordlist to skip candidates |

> Run `python simple_pyaes_bruteforce.py -h` for the authoritative help, in case you’ve modified flags.

---

## ⚙️ Notes & limitations

- **Format**: Supports files created with **pyAesCrypt**. (This is not a generic AES file cracker.)  
- **Buffer size**: Defaults to `BUF_SIZE = 64 * 1024` (64 KiB), matching pyAesCrypt defaults.  
- **Performance**: CPU‑bound + I/O‑bound; for large wordlists, prefer an SSD and avoid verbose logging.  
- **Stability**: On successful decryption, the temporary file is **atomically** moved to the final path. On failure, the temp file is removed.  
- **Integrity**: pyAesCrypt performs integrity checks; wrong passwords raise an exception which this tool treats as “try next”.

---

## 🛡️ Ethics & legal

This tool is intended for:
- recovering **your own** lost passwords,
- **research/education** in a lawful, authorized context.

Do **not** use it on data you do not own or lack explicit permission to test. You are solely responsible for complying with applicable laws and agreements.

---

## 🧪 Tips

- Make sure your terminal encoding can handle passwords with non‑ASCII characters.  
- Consider **splitting** large wordlists and using the `--resume` flag to chunk progress.  
- Keep backups of `.aes` files before experiments to avoid accidental overwrites.

---

## 📦 Project layout

```
.
├── simple_pyaes_bruteforce.py
└── README.md  (this file)
```

---

## 📝 License

MIT — see `LICENSE`.

---

## 🙌 Acknowledgements

- pyAesCrypt for the encryption container and reference implementation.
