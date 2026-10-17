$ErrorActionPreference = 'Stop'

$source = 'E:\7DS-Offline\Original-APK\libil2cpp.original.so'
$output = 'E:\7DS-Offline\Original-APK\libil2cpp.cloud-local.so'
$offset = 0x4FBEA94

# Replacement for PageLogin.NextProcess on ARM64. It preserves the client's
# normal SetExecuteProcess transition (including its coroutine/UI work). Once
# the required local configuration/session bootstrap reaches stage 7, it maps
# the retired public account, live patch download, and tutorial stages 8-25
# directly to NextScene (26). The installed client data is used as-is.
$patch = [byte[]](
    0x08,0x44,0x40,0xB9, # ldr w8, [x0,#0x44]
    0x1F,0x1D,0x00,0x71, # cmp w8,#7
    0xAB,0x00,0x00,0x54, # b.lt increment
    0x1F,0x69,0x00,0x71, # cmp w8,#26
    0x6A,0x00,0x00,0x54, # b.ge increment
    0x41,0x03,0x80,0x52, # mov w1,#26
    0x6F,0xF8,0xFF,0x17, # b PageLogin.SetExecuteProcess
    0x01,0x05,0x00,0x11, # increment: add w1,w8,#1
    0x6D,0xF8,0xFF,0x17  # b PageLogin.SetExecuteProcess
)

Copy-Item -LiteralPath $source -Destination $output -Force
$stream = [IO.File]::Open($output, [IO.FileMode]::Open, [IO.FileAccess]::ReadWrite, [IO.FileShare]::None)
try {
    $stream.Position = $offset
    $stream.Write($patch, 0, $patch.Length)
} finally {
    $stream.Dispose()
}

$hash = (Get-FileHash -LiteralPath $output -Algorithm SHA256).Hash
Write-Host "Patched PageLogin.NextProcess at 0x$($offset.ToString('X')); SHA256=$hash"
