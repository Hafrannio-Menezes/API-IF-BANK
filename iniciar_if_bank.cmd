@echo off
cd /d "%~dp0"
powershell -ExecutionPolicy Bypass -File "%~dp0iniciar_if_bank.ps1"
