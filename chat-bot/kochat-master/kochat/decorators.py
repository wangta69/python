import os

import torch
from torch import Tensor, nn
import kochat_config as config


def backend(cls):
    for key, val in config.BASE.items():
        setattr(cls, key, val)
    return cls


def data(cls):
    cls = backend(cls)
    for key, val in config.DATA.items():
        setattr(cls, key, val)
    return cls


def proc(cls):
    cls = backend(cls)
    for key, val in config.PROC.items():
        setattr(cls, key, val)

    return cls


def loss(cls):
    cls = backend(cls)
    for key, val in config.LOSS.items():
        setattr(cls, key, val)
    return cls


def gensim(cls):
    cls = backend(cls)
    for key, val in config.GENSIM.items():
        setattr(cls, key, val)

    return cls


def intent(cls):
    cls = backend(cls)
    for key, val in config.INTENT.items():
        setattr(cls, key, val)
    return cls


def entity(cls):
    cls = backend(cls)
    for key, val in config.ENTITY.items():
        setattr(cls, key, val)
    return cls


def api(cls):
    cls = backend(cls)
    for key, val in config.API.items():
        setattr(cls, key, val)
    return cls
