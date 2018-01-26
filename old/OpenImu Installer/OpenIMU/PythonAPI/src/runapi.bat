cd ..\PythonAPI\src\
tasklist /nh /fi "imagename eq python.exe" | find /i "python.exe" > nul || (start /B "" "C:\Python27\python.exe" "tornado_wsgi.py")
exit