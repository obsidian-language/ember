@echo off
setlocal enabledelayedexpansion

set "REPO=obsidian-language/obsidian"
set "INSTALL_DIR=%USERPROFILE%\.obsidian"
set "BIN_DIR=%USERPROFILE%\.local\bin"
set "OBSIDIAN_BINARY=obsidian.exe"
set "OS=windows"
set "ARCH=x86_64"

if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
if not exist "%BIN_DIR%" mkdir "%BIN_DIR%"

where curl >nul 2>&1
if errorlevel 1 (
    echo [ERROR] 'curl' is required but not found. Please install it and try again.
    exit /b 1
)

echo [INFO] Fetching release information for %REPO%...
curl -s -o "%INSTALL_DIR%\release.json" "https://api.github.com/repos/%REPO%/releases/latest"

for /f "tokens=2 delims=:" %%i in ('findstr /i "tag_name" "%INSTALL_DIR%\release.json"') do set "TAG_NAME=%%i"
set "TAG_NAME=%TAG_NAME:~2,-1%"
if "%TAG_NAME%"=="" (
    echo [ERROR] Could not retrieve release information. Aborting.
    exit /b 1
)

echo [INFO] Latest release: %TAG_NAME%
set "EXPECTED_TARBALL_NAME=obsidian-%OS%-%ARCH%.tar.gz"
set "EXPECTED_CHECKSUM_NAME=%OS%-%ARCH%.sha256"

for /f "tokens=*" %%i in ('type "%INSTALL_DIR%\release.json" ^| findstr /i /c:"%EXPECTED_TARBALL_NAME%"') do (
    set "TARBALL_URL=%%i"
)
set "TARBALL_URL=%TARBALL_URL:*\https=https%"
for /f "tokens=*" %%i in ('type "%INSTALL_DIR%\release.json" ^| findstr /i /c:"%EXPECTED_CHECKSUM_NAME%"') do (
    set "CHECKSUM_URL=%%i"
)
set "CHECKSUM_URL=%CHECKSUM_URL:*\https=https%"

if "%TARBALL_URL%"=="" (
    echo [ERROR] Tarball URL not found. Aborting.
    exit /b 1
)

echo [INFO] Downloading release assets...
curl -L -o "%INSTALL_DIR%\%EXPECTED_TARBALL_NAME%" "%TARBALL_URL%"
curl -L -o "%INSTALL_DIR%\%EXPECTED_CHECKSUM_NAME%" "%CHECKSUM_URL%"

echo [INFO] Verifying checksum...
cd /d "%INSTALL_DIR%"
for /f %%i in ('certutil -hashfile "%EXPECTED_TARBALL_NAME%" SHA256 ^| findstr /v "SHA256 hash"') do set "DOWNLOADED_CHECKSUM=%%i"
for /f %%i in ('type "%EXPECTED_CHECKSUM_NAME%"') do set "EXPECTED_CHECKSUM=%%i"

if /i "!DOWNLOADED_CHECKSUM!" neq "!EXPECTED_CHECKSUM!" (
    echo [ERROR] Checksum verification failed. Aborting.
    del "%EXPECTED_TARBALL_NAME%"
    del "%EXPECTED_CHECKSUM_NAME%"
    exit /b 1
)

echo [INFO] Extracting files...
tar -xvf "%INSTALL_DIR%\%EXPECTED_TARBALL_NAME%" -C "%INSTALL_DIR%"
move "%INSTALL_DIR%\obsidian.exe" "%BIN_DIR%\%OBSIDIAN_BINARY%"
del "%EXPECTED_TARBALL_NAME%"
del "%EXPECTED_CHECKSUM_NAME%"

echo [INFO] Adding %BIN_DIR% to PATH...
setx PATH "%BIN_DIR%;%PATH%" >nul

echo [INFO] Installation complete! Run 'obsidian --version' to confirm.
exit /b 0
