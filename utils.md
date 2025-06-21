# Add Env variable via cmd
set Path=C:\Users\Maheswaran\.local\bin;%Path%

# Add Env variable via PS
$env:Path = "C:\Users\Maheswaran\.local\bin;$env:Path"

# Install UV in windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
