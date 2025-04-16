#!/usr/bin/env bash
AGENT_USER=maintenance-agent
AGENT_SOURCE_DIR=/home/${AGENT_USER}/.agent-source
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
CURRENT_USER=$(whoami)
PYTHON_EXECUTABLE=/usr/bin/python3

echo "Running as ${CURRENT_USER}"

if [ ${AGENT_USER} = "${CURRENT_USER}" ]; then
  echo "Is agent user"
  if [ ! -d "${AGENT_SOURCE_DIR}/venv" ]; then
    echo "Create venv"
    "${PYTHON_EXECUTABLE}" -m venv "${AGENT_SOURCE_DIR}/venv"
  fi
  echo "Activate venv"
  . "${AGENT_SOURCE_DIR}/venv/bin/activate"
  echo "Upgrade pip"
  python -m pip install --upgrade pip
  echo "Install requirements"
  pip install --quiet -r "${AGENT_SOURCE_DIR}/requirements.txt"
  echo "Launch agent script"
  python "${AGENT_SOURCE_DIR}/main.py"
  exit $?
fi
  
echo "Not agent user - prepare agent env"
echo "Create agent source code dir ${AGENT_SOURCE_DIR}"
sudo mkdir -p "${AGENT_SOURCE_DIR}"

echo "Copy source code"
sudo rsync -r --delete "${SCRIPT_DIR}/" "${AGENT_SOURCE_DIR}/" \
       --exclude venv/ \
       --exclude .venv/ \
       --exclude .git/ \
       --exclude .idea/ \
       --exclude __pycache__/ \
       --exclude logs/ \
       --exclude work_dir/

echo "Set owner to ${AGENT_USER}:${AGENT_USER}"
sudo chown -R "${AGENT_USER}:${AGENT_USER}" "${AGENT_SOURCE_DIR}"

echo "Give group write rights"
sudo chmod -R g+rw "${AGENT_SOURCE_DIR}"

echo "Run launch script as agent user"
sudo -H -u ${AGENT_USER} "${AGENT_SOURCE_DIR}/run.sh"
