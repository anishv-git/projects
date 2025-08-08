from hn_pulse import __version__
from hn_pulse.config import DATA_DIR, MODELS_DIR

def test_version():
    assert isinstance(__version__, str) and len(__version__) > 0

def test_paths_exist():
    assert DATA_DIR.exists()
    assert MODELS_DIR.exists()
