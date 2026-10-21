# My learnings

- OpenCode's shared client configuration is `opencode-template.jsonc`; the installer generates the user's global config. Gateway deployments and model aliases live in `hosting/litellm_config.yaml`.
- Claude models behind the shared OpenAI-compatible provider need model-level `compatibility.cacheFormat: "anthropic"` for OpenCode V2 to emit prompt-cache breakpoints, including selectable aliases.
- Alternatively, OpenRouter Claude deployments can enable automatic caching centrally via `litellm_params.extra_body.cache_control`; deployment settings also apply to router aliases, without client-side breakpoints.

## OpenRouter Integration

Added OpenRouter support to litellm_config.yaml with the following models:

### Models Added:
- **deepseek-v4.1-flash** → openrouter/deepseek/deepseek-v4.1-flash
- **gpt-6.1-sol** → openrouter/openai/gpt-6.1-sol (EU endpoint)
- **claude-opus-5.5** → openrouter/anthropic/claude-opus-5.5 (EU endpoint)
- **mistral-small** (existing model)

### Configuration Details:
- OpenRouter models use `OPENROUTER_API_KEY` environment variable
- EU endpoints use `https://eu.openrouter.ai/api/v1` (via `OC_EU_API_BASE` env var)
- Global OpenRouter endpoint uses `https://openrouter.ai/api/v1` (via `OC_GLOBAL_API_BASE` env var)
- All models added alongside existing Mistral models (not replacing them)
- Models included in default_key_generate_params budget tracking
- Real model names aliased via `router_settings.model_group_alias` in litellm_config.yaml
- OpenRouter provider routing uses `extra_body.provider.order` in litellm_params (NOT `provider` directly)
- Aliases available in opencode: `external-cheap`, `eu-cheap`, `eu-medium`, `eu-expensive`

### Environment Variables Required:
- `OPENROUTER_API_KEY` - API key for OpenRouter services
