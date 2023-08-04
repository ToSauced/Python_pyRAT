# demo-pyRAT
Using python files, builds a .exe file which opens in the background and creates a connection to the server script (when running). 

Once connected, the machine is added to a list to which the user in the server console can select and start executing remote CMD commands. 
- Would much rather it open a Powershell Prompt, but it is okay

When connected, server user can use 'exit' to go back to the list of connected clients. 

Made some custom commands for the CMD prompt, i.e., 'ls' will execute the dir command instead, saves me some sanity when working with Windows.
