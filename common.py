from PyQt6.QtWidgets import QApplication, QMessageBox, QPushButton, QVBoxLayout, QWidget, QMainWindow, QProgressBar, QSizePolicy
import sys
import os
import configparser
import subprocess
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile
from PyQt6.QtCore import QUrl, QLocale, Qt
import shutil
import requests
import time
from PyQt6.QtGui import QIcon