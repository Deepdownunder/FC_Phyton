# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 18:56:05 2018

@author: planteuadm
"""

from gui7 import FC_GUI_Fun as FcView
from gui7 import FcModel

class FcController:
    _view = FcView()
    _model = FcModel()
    
    def __init__(self):
        _view.title("FC Python")
        _view.geometry("1000x850")
        
    