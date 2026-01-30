# Copilot Instructions for Ansible Lab

## Project Overview
This repository is an Ansible automation lab for managing infrastructure and AWX (Ansible Tower) via Python scripts and playbooks. It includes AWX integration, inventory management, and a variety of playbooks for Linux and Windows automation.

## Key Components
- **Python AWX Management**: Scripts like `AwxPyDataClass.py`, `AwxPyScript.py`, and `awx_conn.py` provide AWX API integration for managing projects, templates, and job execution. They use the `awxkit` library and environment variables for credentials.
- **Playbooks**: The `playbooks/` directory contains YAML playbooks for common automation tasks (installing packages, user management, updates) for both Linux and Windows hosts.
- **Inventory**: The `inventory/hosts.ini` file defines host groups (webservers, databases, devservers, securitysrv, winservers) and connection variables for Windows.
- **Secrets**: Sensitive variables are stored in `playbooks/variables/vault.yml` (encrypted with Ansible Vault).

## Developer Workflows
- **Run Playbooks**: Use the `ansible-playbook` command with the appropriate inventory and playbook, e.g.:
  ```sh
  ansible-playbook -i inventory/hosts.ini playbooks/install_nginx.yml
  ```
- **AWX Integration**: Python scripts connect to AWX using environment variables (`AWX_URL`, `AWX_USER`, `AWX_PASSWORD`). See `AwxPyDataClass.py` and `AwxPyScript.py` for usage patterns.
- **Credentials**: Store credentials in environment variables or use Ansible Vault for secrets.
- **Extending Playbooks**: Follow the structure in `playbooks/` for new automation tasks. Use group names from `inventory/hosts.ini`.

## Project-Specific Patterns
- **AWX API Usage**: All AWX API interactions are wrapped in helper classes/functions. Prefer using `AWXManager` (see `AwxPyDataClass.py`) for new automation.
- **Error Handling**: Custom exceptions (`AWXConnectionError`, `AWXResourceError`, etc.) are used for robust error reporting in AWX scripts.
- **Job/Template Execution**: Use the `gest_templates.py` and `AWXExecutionManager` patterns for launching and monitoring jobs.
- **Organization/Project Management**: Scripts support both default and custom organizations for AWX projects (see `AwxPyScript.py`).

## Integration Points
- **awxkit**: All AWX automation relies on the `awxkit` Python library.
- **Ansible Vault**: Used for secret management in playbooks.
- **Windows Integration**: Playbooks use `winrm` for Windows hosts (see `inventory/hosts.ini`).

## Examples
- Add a new AWX project via Python:
  ```python
  from AwxPyDataClass import AWXManager, AWXCredentials
  creds = AWXCredentials.from_env()
  awx = AWXManager(creds)
  awx.connect()
  awx.create_project(name="MyProject", url_git="https://repo.git")
  ```
- Run a playbook for all webservers:
  ```sh
  ansible-playbook -i inventory/hosts.ini playbooks/playbook1.yml
  ```

## References
- See `AwxPyDataClass.py` for AWX API patterns
- See `playbooks/` for automation examples
- See `inventory/hosts.ini` for host group definitions

---
For more details, review the Python scripts and playbooks for concrete usage patterns. If unclear, ask for clarification or examples from the codebase.
