@echo off
title Eliminando Servicio Zebra Agent
agent\nssm.exe remove ZebraZPLAgent confirm
pause
