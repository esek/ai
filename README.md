This is a repo for all AI-related config files for members we use at the guild.

To get started, you need to:
- get a token & account to access our AI infrastructure (ask Informationschefen)
- [install OpenCode](https://opencode.ai/) (preferably using your system's package manager if you're on Linux or macOS)
- [install the config files](#installation)
- for using the web UI (like ChatGPT), log into <https://chat.esek.se> with the account credentials you received from Informationschefen
- _optional: install the VSCode extension for OpenCode_

# AI tips

## What costs money?

> Everybody gets a quota of money / month. Therefore, reducing cost is the same as getting "more" out of the AI.

At the fundamental level, tokens cost money. Output tokens (what the AI writes (files, to you, asking to read files etc)) is often more expensive (~5x) than input tokens (what it reads). We have optimized the system prompt to limit how much it reads by searching instead of reading a whole file.

A single request to the AI API is made between each tool call (tool call: reading file, searching, web, writing file, running script). In every request, it sends the whole context (conversation / session) to the AI API. The conversation has been cached by the AI API but still costs a bit of money. With long contexts (>128K), most money is spent on these "cached tokens". For my codex usage, I had 3x more cost in cached tokens than input/output tokens. Therefore, it's important to create new sessions when you no longer need the context. Compacting the context is also a really useful tool. Models with shorter context is available to get auto-compaction sooner. Keeping the context short is also useful (which we try to achieve in the system prompt as mentioned above).

## Prompt "engineering"

Look in the system prompt of the `esek.md` file for inspiration, but we try to keep all the "prompt engineering" in that so we don't have to retype it each session:)

In general though, it's very useful to create a plan with the AI (just write a markdown document and ask it to ask questions about the implementation specifics) before letting it go on on it's own.

## Reasoning effort / thinking

You can change the reasoning effort of the model. That just changes how much it thinks before giving an answer. Try increasing it before selecting a bigger model (it's still way cheaper!).

# Installation

To install the opencode configuration files from this repository:

```bash
python3 install_opencode_config.py
```

This will copy the files to your user's opencode config directory and prompt for your API key, which will be written to the config file.

## Manual Installation

### Linux/macOS

```bash
# Copy the files to your opencode config directory
cp opencode.jsonc ~/.config/opencode/
mkdir -p ~/.config/opencode/agents
cp agents/esek.md ~/.config/opencode/agents/
```

### Windows (PowerShell)

```powershell
# Copy the files to your opencode config directory
Copy-Item opencode.jsonc $env:APPDATA\opencode\
New-Item -ItemType Directory -Force -Path $env:APPDATA\opencode\agents
Copy-Item agents\esek.md $env:APPDATA\opencode\agents\
```

# API Key Setup

The API key is automatically configured during installation. If you need to update it later, simply run the install script again:

```bash
python3 install_opencode_config.py
```

It will prompt you for your API key and update the configuration file.

## Updating

After installation:
- Edit files in this repository:
  - `opencode.jsonc`
  - `agents/esek.md`
- Run the install script again to copy the updated files:
  ```bash
  python3 install_opencode_config.py
  ```
