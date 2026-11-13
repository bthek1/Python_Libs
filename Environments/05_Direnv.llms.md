# Direnv

For auto load and unloading environments

Author

Benedict Thekkel

## Install

``` bash
sudo apt-get install direnv
```

## Configure Your Shell

> Add to bash

``` sh
eval "$(direnv hook bash)"
```

> Reload bash

``` sh
source ~/.bashrc 
```

## Create a .envrc File in Your Project Directory

> Navigate to your project directory and create a .envrc file:

------------------------------------------------------------------------

``` bash
cd /path/to/your/project
echo 'export POETRY_ACTIVE=1' > .envrc
echo 'source "$(poetry env info --path)/bin/activate"' >> .envrc
```

### Example .envrc File

``` bash

# .envrc - Environment configuration for the project

# --- Check if the virtual environment exists ---
if [ ! -d ".venv" ]; then
  echo "❌ Virtual environment .venv does not exist. Creating..."
  uv .venv  # Or any other Python version you prefer
else
  echo "✔️ Using existing virtual environment."
fi

# --- Activate the virtual environment ---
source .venv/bin/activate

# --- Set environment variables ---
export PROJECT_HOME=$(pwd)  # Set the project root directory path

# --- Load environment variables from .env file ---
if [ -f .env ]; then
  echo "✔️ Loading environment variables from .env..."
  export $(grep -v '^#' .env | xargs -d '\n')  # This will load non-comment lines from .env file
else
  echo "⚠️ No .env file found. Skipping environment variable loading."
fi

# --- Custom commands or setup ---
echo "✔️ Environment setup complete. You are now in the project environment."
```

## Allow the .envrc File

``` bash
direnv allow
```

Back to top
