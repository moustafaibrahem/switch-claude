@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
where python >nul 2>nul
if %ERRORLEVEL%==0 (
  python "%SCRIPT_DIR%claude_switch.py" %*
) else (
  python3 "%SCRIPT_DIR%claude_switch.py" %*
)
endlocal
