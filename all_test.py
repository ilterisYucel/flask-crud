import os
from utils import calculate_max, calculate_std
from model import books
from app import update_book_handler, search

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def test_calculate_max():
	assert calculate_max(os.path.join(SCRIPT_DIR, "test_items", radar.jpeg)) == 5

def test_calculate_std():
	assert calculate_std(os.path.join(SCRIPT_DIR, "test_items", radar.jpeg)) == 0

def test_model():
	assert books("python-flask", None, "any", None, 5, 5, 5, 5) == None

def test_update_book_handler():
	assert update_book_handler(2) == None

def test_search():
	assert search() == None
	

