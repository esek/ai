#!/usr/bin/env python3
"""
Install opencode-template.jsonc, commands/analyze.md, and agents/esek.md from this repo to user's config via copying.

This script copies the files from this repository to the user's opencode config directory,
and prompts for the API key which is written to the opencode.jsonc config file.
"""

import sys
import os
from pathlib import Path


def get_user_config_dir() -> Path:
    """Get the user's opencode config directory."""
    # Try to get from opencode command first
    try:
        import subprocess

        result = subprocess.run(
            ["opencode", "config-dir"], capture_output=True, text=True, timeout=5
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


def get_repo_files() -> tuple[Path, Path, Path]:
    """Get paths to repo's opencode.jsonc, commands/analyze.md, and agents/esek.md files."""
    repo_root = Path(__file__).parent

    opencode_jsonc = repo_root / "opencode-template.jsonc"
    esek_md = repo_root / "agents" / "esek.md"
    analyze_md = repo_root / "commands" / "analyze.md"

    if not opencode_jsonc.exists():
        print(f"Error: {opencode_jsonc} does not exist")
        sys.exit(1)

    if not esek_md.exists():
        print(f"Error: {esek_md} does not exist")
        sys.exit(1)

    if not analyze_md.exists():
        print(f"Error: {analyze_md} does not exist")
        sys.exit(1)

    return opencode_jsonc, esek_md, analyze_md


def install_files(
    user_config_dir: Path,
    repo_opencode_jsonc: Path,
    repo_esek_md: Path,
    repo_analyze_md: Path,
) -> None:
    """Install files by copying to user config directory."""
    print(f"User config directory: {user_config_dir}")
    print(f"Repo opencode.jsonc: {repo_opencode_jsonc}")
    print(f"Repo agents/esek.md: {repo_esek_md}")
    print(f"Repo commands/analyze.md: {repo_analyze_md}")

    # Create agents directory if it doesn't exist
    agents_dir = user_config_dir / "agents"
    agents_dir.mkdir(exist_ok=True)

    # Create commands directory if it doesn't exist
    commands_dir = user_config_dir / "commands"
    commands_dir.mkdir(exist_ok=True)

    # Ask once at the start if files should be overwritten
    user_opencode = user_config_dir / "opencode.jsonc"
    user_esek = agents_dir / "esek.md"
    user_analyze = commands_dir / "analyze.md"

    override = True
    if user_opencode.exists() or user_esek.exists():
        override = input(
            "Some files already exist. Overwrite? (y/N): "
        ).strip().lower() in ("y", "yes")

    if not override:
        print("Skipping file installation")
        return

    # Install opencode.jsonc
    if user_opencode.exists():
        print(f"\nOverwriting existing {user_opencode}")
    else:
        print(f"\nCopying opencode.jsonc to {user_opencode}")

    # Copy the file
    import shutil

    shutil.copy2(repo_opencode_jsonc, user_opencode)

    # Prompt for API key and update the config
    print("\n" + "─" * 70)
    print("API Key Setup")
    print("─" * 70)
    # Check if .env file exists and read OPENCODE_API_KEY from it
    api_key = None
    env_path = os.path.join(os.path.dirname(user_opencode), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("OPENCODE_API_KEY="):
                    api_key = line.strip().split("=", 1)[1]
                    break

    # If not found in .env or .env doesn't exist, prompt user
    if not api_key:
        api_key = input("Enter your OPENCODE_API_KEY: ").strip()
        if api_key:
            # Append to .env file
            with open(env_path, "a", encoding="utf-8") as f:
                f.write(f"OPENCODE_API_KEY={api_key}\n")
            print(f"✅ Saved API key to {env_path}")

    if api_key:
        config = user_opencode.read_text()

        config = config.replace("<token goes here>", api_key)
        user_opencode.write_text(config)
        print(f"✅ Updated API key in {user_opencode}")

    # Install agents/esek.md
    if user_esek.exists():
        print(f"\nOverwriting existing {user_esek}")
    else:
        print(f"Copying agents/esek.md to {user_esek}")
    shutil.copy2(repo_esek_md, user_esek)

    # Install commands/analyze.md
    if user_analyze.exists():
        print(f"\nOverwriting existing {user_analyze}")
    else:
        print(f"Copying commands/analyze.md to {user_analyze}")
    shutil.copy2(repo_analyze_md, user_analyze)

    print("\n✅ Successfully installed opencode configuration files")


def print_install_instructions() -> None:
    """Print installation instructions for different platforms."""
    print("\n" + "=" * 70)
    print("Installation Instructions")
    print("=" * 70)

    print(
        "\nThe configuration files have been copied to your opencode config directory."
    )
    print(
        "To update them, edit the files in this repository and run the install script again:"
    )
    print(f"  {Path(__file__).parent / 'opencode.jsonc'}")
    print(f"  {Path(__file__).parent / 'agents' / 'esek.md'}")
    print("\nThen run:")
    print(f"  python3 {__file__}")
    print("\nThis will copy the updated files to your config directory.")

    print("\n" + "─" * 70)
    print("Updating Configuration")
    print("─" * 70)
    print(
        "\nTo update your API key or other settings, simply run the install script again."
    )
    print("It will prompt you to overwrite the existing configuration files.")


def main() -> None:
    """Main entry point."""
    print("opencode Configuration Installer")
    print("=" * 70)

    # Get paths
    user_config_dir = get_user_config_dir()
    repo_opencode_jsonc, repo_esek_md, repo_analyze_md = get_repo_files()

    # Install files
    install_files(user_config_dir, repo_opencode_jsonc, repo_esek_md, repo_analyze_md)

    # Print instructions
    print_install_instructions()


if __name__ == "__main__":
    main()
