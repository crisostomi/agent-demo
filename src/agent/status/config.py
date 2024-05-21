# config_singleton.py
from omegaconf import OmegaConf, DictConfig
import hydra
import os


class Config:
    _instance = None

    @staticmethod
    def get_instance():
        assert Config._instance is not None

        return Config._instance

    @staticmethod
    def set_instance(cfg: DictConfig):
        Config._instance = cfg
