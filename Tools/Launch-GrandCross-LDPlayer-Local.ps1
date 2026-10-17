$ErrorActionPreference = 'Stop'

$adb = 'C:\Program Files (x86)\Android\android-sdk\platform-tools\adb.exe'
$frida = 'C:\Users\conno\AppData\Local\Python\pythoncore-3.14-64\Scripts\frida.exe'
$script = 'E:\7DS-Offline\Tools\Frida\grand-cross-native-network.js'
$device = 'emulator-5554'
$root = 'E:\7DS-Offline'
$python = 'C:\Users\conno\AppData\Local\Python\pythoncore-3.14-64\python.exe'

if (-not (Get-Process GrandCrossLocalServer -ErrorAction SilentlyContinue)) {
    Start-Process -FilePath "$root\Server\GrandCrossLocalServer.exe" -WorkingDirectory "$root\Server" -WindowStyle Hidden `
        -RedirectStandardOutput "$root\Research\local-server-launch.log" -RedirectStandardError "$root\Research\local-server-launch-error.log"
}
if (-not (Get-NetTCPConnection -LocalPort 5100 -State Listen -ErrorAction SilentlyContinue)) {
    Start-Process -FilePath $python -ArgumentList "$root\Tools\LocalHttps\serve_local_content.py" -WorkingDirectory $root -WindowStyle Hidden `
        -RedirectStandardOutput "$root\Research\local-content-launch.log" -RedirectStandardError "$root\Research\local-content-launch-error.log"
}

& $adb -s $device root | Out-Host
& $adb -s $device reverse tcp:5001 tcp:5001 | Out-Host
& $adb -s $device reverse tcp:5100 tcp:5100 | Out-Host
& $adb -s $device shell 'am force-stop com.netmarble.nanagb' | Out-Host
# Resolve the current installation instead of assuming Android's randomized path.
$packagePath = & $adb -s $device shell pm path com.netmarble.nanagb |
    Where-Object { $_.Trim().EndsWith('/base.apk') } | Select-Object -First 1
if (-not $packagePath) { throw 'Grand Cross is not installed in LDPlayer.' }
$packagePath = $packagePath.Trim().Replace('package:', '')
$nativePath = $packagePath.Substring(0, $packagePath.Length - '/base.apk'.Length) + '/lib/arm64/libil2cpp.so'
& $adb -s $device push "$root\Original-APK\libil2cpp.cloud-local-r21.so" /data/local/tmp/gc-local-r21.so | Out-Host
if ($LASTEXITCODE -ne 0) { throw 'Could not stage the tested local client library.' }
& $adb -s $device shell "cp /data/local/tmp/gc-local-r21.so $nativePath" | Out-Host
if ($LASTEXITCODE -ne 0) { throw 'Could not install the local client library.' }
$uidLine = (& $adb -s $device shell dumpsys package com.netmarble.nanagb | Select-String 'userId=(\d+)' | Select-Object -First 1).ToString()
$appUid = [regex]::Match($uidLine, 'userId=(\d+)').Groups[1].Value
if (-not $appUid) { throw 'Could not identify the local game UID.' }
& $adb -s $device shell "iptables -C OUTPUT -m owner --uid-owner $appUid ! -d 127.0.0.0/8 -j REJECT || iptables -I OUTPUT 1 -m owner --uid-owner $appUid ! -d 127.0.0.0/8 -j REJECT" | Out-Host
& $adb -s $device shell "ip6tables -C OUTPUT -m owner --uid-owner $appUid ! -d ::1/128 -j REJECT || ip6tables -I OUTPUT 1 -m owner --uid-owner $appUid ! -d ::1/128 -j REJECT" | Out-Host
& $adb -s $device shell 'pidof gc-frida' | Out-Null
if ($LASTEXITCODE -ne 0) {
    Start-Process -FilePath $adb -ArgumentList @('-s', $device, 'shell', '/data/local/tmp/gc-frida', '-D') -WindowStyle Hidden
    Start-Sleep -Seconds 2
}

Write-Host '[Grand Cross Local] Local login and hero draw testing. Two billion diamonds; draws do not debit the balance.' -ForegroundColor Green
Write-Host '[Grand Cross Local] Keep this window open while testing.' -ForegroundColor Yellow
& $frida -D $device --realm native -f com.netmarble.nanagb -l $script
