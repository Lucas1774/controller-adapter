@echo off
pyinstaller --onefile --add-data "swarm;swarm" mapper.py
move dist\mapper.exe .
rmdir /s /q dist
rmdir /s /q build
del mapper.spec
