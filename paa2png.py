#!/usr/bin/env python3
"""
PAA to PNG. Decodes ArmA's DXT5 .paa textures so they can be used as figures in the guide.

    python3 paa2png.py <paa-dir> <out-dir> [name ...]

Every .paa in this addon is type 0xFF05 (DXT5), so that is the only codec implemented. If a file with a
different magic turns up the script says so and skips it rather than writing a corrupt image.
"""
import sys, os, struct
from PIL import Image

DXT5 = 0xFF05


def _lzo1x_decompress(src, out_len):
    """PAA mipmaps above 128px are LZO1X packed. Uses python-lzo rather than a hand rolled decoder,
    because getting LZO1X exactly right by hand produces images that look decoded but are silently blank."""
    import lzo
    return lzo.decompress(src, False, out_len)


def decode_dxt5(data, w, h):
    """DXT5: per 4x4 block, 8 bytes alpha then 8 bytes DXT1 colour."""
    img = bytearray(w * h * 4)
    bx, by = (w + 3) // 4, (h + 3) // 4
    p = 0
    for byi in range(by):
        for bxi in range(bx):
            if p + 16 > len(data):
                break
            a0, a1 = data[p], data[p + 1]
            abits = int.from_bytes(data[p + 2:p + 8], "little")
            c0, c1 = struct.unpack_from("<HH", data, p + 8)
            cbits = struct.unpack_from("<I", data, p + 12)[0]
            p += 16

            def rgb(c):
                return (((c >> 11) & 31) * 255 // 31,
                        ((c >> 5) & 63) * 255 // 63,
                        (c & 31) * 255 // 31)

            r0, g0, b0 = rgb(c0)
            r1, g1, b1 = rgb(c1)
            cols = [(r0, g0, b0), (r1, g1, b1),
                    ((2 * r0 + r1) // 3, (2 * g0 + g1) // 3, (2 * b0 + b1) // 3),
                    ((r0 + 2 * r1) // 3, (g0 + 2 * g1) // 3, (b0 + 2 * b1) // 3)]
            if a0 > a1:
                al = [a0, a1] + [((6 - i) * a0 + (i + 1) * a1) // 7 for i in range(6)]
            else:
                al = [a0, a1] + [((4 - i) * a0 + (i + 1) * a1) // 5 for i in range(4)] + [0, 255]

            for py in range(4):
                for px in range(4):
                    x, y = bxi * 4 + px, byi * 4 + py
                    if x >= w or y >= h:
                        continue
                    i = py * 4 + px
                    r, g, b = cols[(cbits >> (2 * i)) & 3]
                    a = al[(abits >> (3 * i)) & 7]
                    o = (y * w + x) * 4
                    img[o:o + 4] = bytes((r, g, b, a))
    return bytes(img)


def read_paa(path):
    d = open(path, "rb").read()
    magic = struct.unpack_from("<H", d, 0)[0]
    if magic != DXT5:
        raise ValueError(f"unsupported PAA type {hex(magic)} (only DXT5 0xFF05 handled)")
    p = 2
    # skip TAGG blocks: "GGAT" + 4 char name + 4 byte length + payload
    while d[p:p + 4] == b"GGAT":
        ln = struct.unpack_from("<I", d, p + 8)[0]
        p += 12 + ln
    npal = struct.unpack_from("<H", d, p)[0]
    p += 2 + npal * 3
    # first (largest) mipmap
    w, h = struct.unpack_from("<HH", d, p)
    p += 4
    size = int.from_bytes(d[p:p + 3], "little")
    p += 3
    raw = d[p:p + size]
    if w & 0x8000:
        w &= 0x7FFF
        raw = _lzo1x_decompress(raw, ((w + 3) // 4) * ((h + 3) // 4) * 16)
    return w, h, decode_dxt5(raw, w, h)


def convert(src, dst):
    w, h, px = read_paa(src)
    Image.frombytes("RGBA", (w, h), px).save(dst)
    return w, h


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    srcdir, outdir = sys.argv[1], sys.argv[2]
    names = sys.argv[3:]
    os.makedirs(outdir, exist_ok=True)
    ok = fail = 0
    for root, _, files in os.walk(srcdir):
        for fn in sorted(files):
            if not fn.endswith(".paa"):
                continue
            if names and not any(n in fn for n in names):
                continue
            src = os.path.join(root, fn)
            dst = os.path.join(outdir, fn[:-4] + ".png")
            try:
                w, h = convert(src, dst)
                print(f"  {fn:44s} {w}x{h}")
                ok += 1
            except Exception as e:
                print(f"  {fn:44s} FAILED: {e}")
                fail += 1
    print(f"{ok} converted, {fail} failed")
