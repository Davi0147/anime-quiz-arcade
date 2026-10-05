@echo off
chcp 65001 >nul
title Servidor Local - Anime Opening Blind Test
cd /d "%~dp0"
python server.py
pause
