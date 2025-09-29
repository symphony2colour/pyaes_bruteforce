# pyaes_bruteforce
A tiny, single-process pyAesCrypt password bruteforcer for .aes files.

Features:

Works with standard pyAesCrypt AES files (*.zip.aes, *.tar.gz.aes, etc.)

Safe temp file handling (writes to output.tmp then atomically renames on success)

Progress heartbeat (--status-every N)

Resume from a wordlist offset (--resume N)

Requirements:

`pip3 install pyAesCrypt`

Basic Usage:

`python3 simple_pyaes_bruteforce.py -i web_20250806_120723.zip.aes -w rockyou.txt -o web.zip`


Notes

Buffer size defaults to 64 KiB (pyAesCrypt default).
On success: prints the password, writes the decrypted archive to -o/--output.
On failure: exits with non-zero status and prints a short message.

Disclaimer

For educational and legitimate recovery/testing purposes only. Do not use on files you don’t have permission to access.
