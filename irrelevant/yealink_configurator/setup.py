from cx_Freeze import setup, Executable

setup(
    name = "yealink_configurator",
    version = "0.1",
    description = "Yealink's configurator",
    executables = [Executable("main.py")]
)
