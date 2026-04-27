import sys
import os

# Add the repository root to sys.path so pytest can import
# core/, models/, api/, and dashboard/ as packages from any
# working directory and any Python version.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
