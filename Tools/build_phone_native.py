"""Build the phone server with its C++ runtime linked into the library."""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
LLVM = Path('E:/MyAI/android-sdk/ndk/27.2.12479018/toolchains/llvm/prebuilt/windows-x86_64/bin')
subprocess.run([
    str(LLVM/'clang++.exe'), '--target=aarch64-linux-android26',
    '-shared', '-fPIC', '-static-libstdc++', '-std=c++17', '-O2',
    '-IAndroidHub/native', 'AndroidHub/native/GameHandlers.cpp',
    'AndroidHub/native/PhoneTransport.cpp', '-llog',
    '-o', 'AndroidHub/native/libgcserver.so',
], cwd=ROOT, check=True)
print('Built phone server with a self-contained C++ runtime')
