#!/usr/bin/env python3
"""
Install opencode.jsonc and agents/esek.md from this repo to user's config via copying.

This script copies the files from this repository to the user's opencode config directory,
and prompts for the API key which is written to the opencode.jsonc config file.
"""

import sys
from pathlib import Path


def get_user_config_dir() -> Path:
    """Get the user's opencode config directory."""
    # Try to get from opencode command first
    try:
        import subprocess
        result = subprocess.run(
            ["opencode", "config-dir"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            config_dir = Path(result.stdout.strip())
            if config_dir.exists():
                return config_dir
    except (subprocess.SubprocessError, FileNotFoundError):
        pass
    
    # Fallback to default locations
    default_dirs = [
        Path.home() / ".config" / "opencode",
        Path("/etc/opencode"),
    ]
    
    for config_dir in default_dirs:
        if config_dir.exists():
            return config_dir
    
    print("Error: Could not find opencode config directory")
    sys.exit(1)


def get_repo_files() -> tuple[Path, Path]:
    """Get paths to repo's opencode.jsonc and agents/esek.md files."""
    repo_root = Path(__file__).parent
    
    opencode_jsonc = repo_root / "opencode.jsonc"
    esek_md = repo_root / "agents" / "esek.md"
    
    if not opencode_jsonc.exists():
        print(f"Error: {opencode_jsonc} does not exist")
        sys.exit(1)
    
    if not esek_md.exists():
        print(f"Error: {esek_md} does not exist")
        sys.exit(1)
    
    return opencode_jsonc, esek_md


def install_files(user_config_dir: Path, repo_opencode_jsonc: Path, repo_esek_md: Path) -> None:
    """Install files by copying to user config directory."""
    print(f"User config directory: {user_config_dir}")
    print(f"Repo opencode.jsonc: {repo_opencode_jsonc}")
    print(f"Repo agents/esek.md: {repo_esek_md}")
    
    # Create agents directory if it doesn't exist
    agents_dir = user_config_dir / "agents"
    agents_dir.mkdir(exist_ok=True)
    
    # Install opencode.jsonc
    user_opencode = user_config_dir / "opencode.jsonc"
    if user_opencode.exists():
        print(f"\n⚠️  {user_opencode} already exists!")
        try:
            confirm = input("Do you want to overwrite it? (y/N): ").strip().lower()
            if confirm != 'y':
                print("Skipping opencode.jsonc installation")
                return
        except EOFError:
            # Non-interactive mode, assume yes
            print("Overwriting existing file (non-interactive mode)")
        else:
            print(f"Overwriting existing {user_opencode}")
    else:
        print(f"\nCopying opencode.jsonc to {user_opencode}")
    
    # Copy the file
    import shutil
    shutil.copy2(repo_opencode_jsonc, user_opencode)
    
    # Prompt for API key and update the config
    print("\n" + "─"*70)
    print("API Key Setup")
    print("─"*70)
    api_key = input("Enter your OPENCODE_API_KEY: ").strip()
    if api_key:
        # Read the JSON file, update the API key, and write back
        import json
        with open(user_opencode, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        if 'providers' in config and 'esek' in config['providers']:
            config['providers']['esek']['settings']['apiKey'] = api_key
            with open(user_opencode, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            print(f"✅ Updated API key in {user_opencode}")
    
    # Install agents/esek.md
    user_esek = agents_dir / "esek.md"
    if user_esek.exists():
        print(f"\n⚠️  {user_esek} already exists!")
        try:
            confirm = input("Do you want to overwrite it? (y/N): ").strip().lower()
            if confirm != 'y':
                print("Skipping agents/esek.md installation")
                return
        except EOFError:
            # Non-interactive mode, assume yes
            print("Overwriting existing file (non-interactive mode)")
        else:
            print(f"Overwriting existing {user_esek}")
            shutil.copy2(repo_esek_md, user_esek)
    else:
        print(f"Copying agents/esek.md to {user_esek}")
        shutil.copy2(repo_esek_md, user_esek)
    
    print("\n✅ Successfully installed opencode configuration files")


def print_install_instructions() -> None:
    """Print installation instructions for different platforms."""
    print("\n" + "="*70)
    print("Installation Instructions")
    print("="*70)
    
    print("\nThe configuration files have been copied to your opencode config directory.")
    print("To update them, edit the files in this repository and run the install script again:")
    print(f"  {Path(__file__).parent / 'opencode.jsonc'}")
    print(f"  {Path(__file__).parent / 'agents' / 'esek.md'}")
    print("\nThen run:")
    print(f"  python3 {__file__}")
    print("\nThis will copy the updated files to your config directory.")
    
    print("\n" + "─"*70)
    print("Updating Configuration")
    print("─"*70)
    print("\nTo update your API key or other settings, simply run the install script again.")
    print("It will prompt you to overwrite the existing configuration files.")
    

def main() -> None:
    """Main entry point."""
    print("opencode Configuration Installer")
    print("="*70)
    
    # Get paths
    user_config_dir = get_user_config_dir()
    repo_opencode_jsonc, repo_esek_md = get_repo_files()
    
    # Install files
    install_files(user_config_dir, repo_opencode_jsonc, repo_esek_md)
    
    # Print instructions
    print_install_instructions()



if __name__ == "__main__":
    main()
