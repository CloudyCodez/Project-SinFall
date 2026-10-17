"""Replace only libil2cpp in LDPlayer's already-installed ARM64 split."""
from pathlib import Path
import hashlib
import zipfile

ROOT = Path(r"E:\7DS-Offline")
SOURCE = ROOT / "Research/LDPlayer-current-arm64.apk"
LIBRARY = ROOT / "Original-APK/libil2cpp.cloud-local-r2.so"
OUTPUT = ROOT / "Research/LDPlayer-grandcross-local-arm64.apk"
ENTRY = "lib/arm64-v8a/libil2cpp.so"

library = LIBRARY.read_bytes()
with zipfile.ZipFile(SOURCE) as source, zipfile.ZipFile(OUTPUT, "w") as target:
    for info in source.infolist():
        target.writestr(info, library if info.filename == ENTRY else source.read(info))

with zipfile.ZipFile(OUTPUT) as check:
    embedded = check.read(ENTRY)
    assert embedded == library
print({
    "output": str(OUTPUT),
    "apk_sha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
    "library_sha256": hashlib.sha256(embedded).hexdigest(),
})
