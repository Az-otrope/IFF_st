import pytest

from src.settings import *


class TestSettings:
    def __init__(self):
        pass

    @pytest.fixture(autouse=True)
    def setup(self):
        self.paths = ProjectPaths

    def test_settings(self):
        assert self.paths.ROOT_PATH is not None
        assert self.paths.DATA_PATH is not None
        assert self.paths.PROCESSED_DATA is not None
        assert self.paths.EXTERNAL_DATA is not None
        assert self.paths.INTERIM_DATA is not None
        assert self.paths.RAW_DATA is not None
        assert self.paths.EVALUATION_DATA is not None
        assert self.paths.MODEL_DATA is not None
