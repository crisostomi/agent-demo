import os
from omegaconf import DictConfig
import pytest
from pytest import FixtureRequest, TempPathFactory
from hydra.core.hydra_config import HydraConfig
from typing import Dict, Union
from hydra import compose, initialize
import shutil


#
# Base configurations
#
@pytest.fixture(scope="package")
def cfg(tmp_path_factory: TempPathFactory):
    test_cfg_tmpdir = tmp_path_factory.mktemp("test_train_tmpdir")

    with initialize(config_path="../config"):
        cfg = compose(config_name="default", return_hydra_config=True)
        HydraConfig().set_config(cfg)

        # Force the storage dir to be in the temp folder
        cfg.core.storage_dir = str(test_cfg_tmpdir)

        yield cfg

    shutil.rmtree(test_cfg_tmpdir)
