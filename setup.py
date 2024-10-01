from cx_Freeze import setup, Executable

setup(
    name="YourAppName",
    version="0.1",
    description="Your application description",
    executables=[Executable("your_script.py")]
)