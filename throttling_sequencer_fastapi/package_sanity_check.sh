# Checks if the package is installed correctly and prints out the path
python -c "import throttling_sequencer, sys; print(throttling_sequencer.__file__); print(sys.path[0])"
python -c "import importlib.metadata as m; print(m.version(\"throttling-sequencer-fastapi\"))"
