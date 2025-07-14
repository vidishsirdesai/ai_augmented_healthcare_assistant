# Setup
1. `brew install pyenv`.
2. `pyenv --version`.
3. `pyenv install --list`.
4. `pyenv versions`.
5. `brew install pyenv-virtualenv`.
6. `eval "$(pyenv virtualenv-init -)"`.
7. `source ~/.zshrc`.
8. `cd <project_directory>`.
9. `pyenv global 3.11.9`.
10. `pyenv virtualenv 3.11.9 venv`.
11. `pyenv activate venv`.
12. `pip3 install -r requirements.txt`.
13. `uvicorn src.main:app --port 8000`.
