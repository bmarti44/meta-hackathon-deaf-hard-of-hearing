"""Gen34 asset fetch: extract selected members from the BRUDEX Zenodo archives by HTTP range requests.

BRUDEX (Fejgin, Middelberg, Doclo, University of Oldenburg; MIT licence; doi 10.5281/zenodo.8340195) holds
acoustically recorded speech (4 talkers) and noise (babble, cafeteria, white) at a binaural hearing-aid setup on a
KEMAR dummy head, for 3 reverberation settings of one laboratory. The archives are large (spk_short.zip 18.3 GB), so
only the needed members are read: zipfile reads the central directory and each member through a seekable HTTP
range reader, and zipfile verifies each member's CRC-32 while extracting. Each extracted file's sha256 goes to a
manifest. Downloaded data stay outside the repo (default /tmp/brudex_dl/data) and are treated as untrusted data:
only HDF5 (.mat v7.3) numeric arrays are read from them later, nothing is executed.

Usage:
  python -I research/gen34/fetch_brudex.py --list spk_short.zip
  python -I research/gen34/fetch_brudex.py --archive spk_short.zip --pattern 'SPK?short_*_eMicRun_1_DOA_{-60,-30,30,60}deg.mat'
"""
from __future__ import annotations
import argparse, fnmatch, hashlib, io, json, sys, time, urllib.request, zipfile
from pathlib import Path

BASE = "https://zenodo.org/records/8340195/files/{name}?download=1"
OUT = Path("/tmp/brudex_dl/data")


class HTTPRangeFile(io.RawIOBase):
    """Read-only seekable view of a remote file via HTTP Range requests, with a small block cache."""

    def __init__(self, url, block=1 << 20):
        self.url, self.block, self.pos, self.cache = url, block, 0, {}
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=120) as r:
            self.size = int(r.headers["Content-Length"])
        self.bytes_fetched = 0

    def seekable(self): return True
    def readable(self): return True
    def tell(self): return self.pos

    def seek(self, off, whence=0):
        self.pos = off if whence == 0 else self.pos + off if whence == 1 else self.size + off
        return self.pos

    def _get(self, start, end):  # inclusive
        for attempt in range(5):
            try:
                req = urllib.request.Request(self.url, headers={"Range": f"bytes={start}-{end}"})
                with urllib.request.urlopen(req, timeout=300) as r:
                    data = r.read()
                if len(data) != end - start + 1:
                    raise IOError(f"short read {len(data)} != {end - start + 1}")
                self.bytes_fetched += len(data)
                return data
            except Exception as e:  # transient network errors
                if attempt == 4:
                    raise
                time.sleep(2 ** attempt)

    def read(self, n=-1):
        if n is None or n < 0:
            n = self.size - self.pos
        n = max(0, min(n, self.size - self.pos))
        if n == 0:
            return b""
        if n >= 4 * self.block:  # large member reads: fetch directly
            data = self._get(self.pos, self.pos + n - 1); self.pos += n; return data
        out = bytearray()
        while n > 0:
            b = self.pos // self.block
            if b not in self.cache:
                if len(self.cache) > 64:
                    self.cache.clear()
                s = b * self.block
                self.cache[b] = self._get(s, min(self.size, s + self.block) - 1)
            blk = self.cache[b]; off = self.pos - b * self.block
            chunk = blk[off:off + n]; out += chunk; self.pos += len(chunk); n -= len(chunk)
        return bytes(out)

    def readinto(self, b):
        data = self.read(len(b)); b[:len(data)] = data; return len(data)


def open_zip(name):
    f = HTTPRangeFile(BASE.format(name=name))
    return zipfile.ZipFile(io.BufferedReader(f, buffer_size=1 << 20)), f


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list"); ap.add_argument("--archive"); ap.add_argument("--pattern", action="append", default=[])
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args()
    if a.list:
        z, f = open_zip(a.list)
        for i in z.infolist():
            print(i.filename, i.file_size, f"{i.CRC:08x}")
        print(f"# {len(z.infolist())} members; fetched {f.bytes_fetched} bytes for the listing", file=sys.stderr)
        return
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    z, f = open_zip(a.archive)
    members = [i for i in z.infolist() if any(fnmatch.fnmatch(Path(i.filename).name, p) for p in a.pattern)]
    assert members, "no members matched"
    man_p = out / "manifest.json"
    man = json.loads(man_p.read_text()) if man_p.exists() else {"source": "BRUDEX doi:10.5281/zenodo.8340195 (MIT)", "files": {}}
    t0 = time.time()
    for k, i in enumerate(members):
        dest = out / Path(i.filename).name
        if dest.exists() and man["files"].get(dest.name, {}).get("crc32") == f"{i.CRC:08x}":
            continue
        with z.open(i) as src:  # zipfile checks CRC-32 at end of stream
            data = src.read()
        dest.write_bytes(data)
        man["files"][dest.name] = {"archive": a.archive, "member": i.filename, "bytes": len(data), "crc32": f"{i.CRC:08x}",
                                   "sha256": hashlib.sha256(data).hexdigest()}
        man_p.write_text(json.dumps(man, indent=1, sort_keys=True))
        print(f"[{k+1}/{len(members)}] {dest.name} {len(data)/1e6:.1f} MB {time.time()-t0:.0f}s", flush=True)
    print(f"done: {len(members)} members, {f.bytes_fetched/1e9:.2f} GB fetched, {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
