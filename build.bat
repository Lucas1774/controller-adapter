@echo off
pyinstaller --onefile src\joy_to_mouse.py
move dist\joy_to_mouse.exe .
rmdir /s /q dist
rmdir /s /q build
del joy_to_mouse.spec
