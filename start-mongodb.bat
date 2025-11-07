@echo off
echo Starting MongoDB...
echo.

REM Try to find MongoDB installation
set MONGO_PATH="C:\Program Files\MongoDB\Server\7.0\bin\mongod.exe"
if not exist %MONGO_PATH% set MONGO_PATH="C:\Program Files\MongoDB\Server\6.0\bin\mongod.exe"
if not exist %MONGO_PATH% set MONGO_PATH="C:\Program Files\MongoDB\Server\5.0\bin\mongod.exe"

REM Create data directory if it doesn't exist
if not exist "C:\data\db" mkdir "C:\data\db"

echo MongoDB path: %MONGO_PATH%
echo Data directory: C:\data\db
echo.
echo Starting MongoDB server...
echo Press Ctrl+C to stop MongoDB
echo.

REM Start MongoDB
%MONGO_PATH% --dbpath "C:\data\db"

pause
