#!/usr/bin/env python3
# simple_pyaes_bruteforce.py
# Usage:
#   python3 simple_pyaes_bruteforce.py -i file.zip.aes -w list.txt -o web.zip
#   python3 simple_pyaes_bruteforce.py -i file.zip.aes -w list.txt -o  web.zip --resume 1000

import argparse, os, sys
try:
    import pyAesCrypt
except Exception as e:
    print("[-] pyAesCrypt module not found. Install it:\n    pip3 install pyAesCrypt", file=sys.stderr)
    sys.exit(2)

BUF_SIZE = 64 * 1024  # default buffer size used by pyAesCrypt

def try_pw(infile, outfile, pw):
    """Return True if decryption with pw succeeds, else False."""
    tmp = outfile + ".tmp"
    try:
        # decryptFile raises on wrong password; writes to tmp on success
        pyAesCrypt.decryptFile(infile, tmp, pw, BUF_SIZE)
        # success → move tmp to final
        os.replace(tmp, outfile)
        return True
    except Exception:
        # cleanup temp if present
        try:
            if os.path.exists(tmp):
                os.remove(tmp)
        except Exception:
            pass
        return False

def main():
    ap = argparse.ArgumentParser(description="Bruteforce a pyAesCrypt .aes file with a wordlist (single process).")
    ap.add_argument("-i", "--input", required=True, help="Encrypted .aes input file")
    ap.add_argument("-w", "--wordlist", required=True, help="Wordlist (one password per line)")
    ap.add_argument("-o", "--output", default="test.zip", help="Output filename for decrypted result")
    ap.add_argument("--resume", type=int, default=0, help="Skip first N lines of the wordlist")
    ap.add_argument("--status-every", type=int, default=5000, help="Print status every N attempts")
    args = ap.parse_args()

    if not os.path.isfile(args.input):
        print(f"[-] Encrypted file not found: {args.input}", file=sys.stderr); sys.exit(2)
    if not os.path.isfile(args.wordlist):
        print(f"[-] Wordlist not found: {args.wordlist}", file=sys.stderr); sys.exit(2)

    tried = 0
    with open(args.wordlist, "r", errors="ignore") as f:
        # skip resume lines
        for _ in range(args.resume):
            if f.readline() == "":
                print("[-] Reached EOF during resume skip.", file=sys.stderr); sys.exit(1)

        for line in f:
            pw = line.rstrip("\r\n")
            if not pw:
                continue
            tried += 1
            if args.status_every and tried % args.status_every == 0:
                print(f"[.] Tried {tried + args.resume} passwords... (last: {pw[:40]})")

            if try_pw(args.input, args.output, pw):
                print(f"[+] SUCCESS! Password: {pw}")
                print(f"[+] Decrypted to: {args.output}")
                print("[i] You can now: unzip -l", args.output)
                return 0

    print("[-] No password found in the provided wordlist.")
    return 1

if __name__ == "__main__":
    sys.exit(main())
