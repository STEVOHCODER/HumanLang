@echo off
setlocal
cd /d "%~dp0"
python -m pip install -e . --no-build-isolation
echo.
echo HumanLang installed.
echo Try: humanlang run examples\hello.hl
echo If Windows cannot find humanlang, add this folder to PATH:
python -c "import site; import os; print(os.path.join(site.USER_BASE, 'Scripts'))"
