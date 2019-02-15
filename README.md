# vim-yaml

YAML syntax highlighting for Neovim. Unlike most YAML highlighting plugins, it's
implemented as remote plugin using `ruamel.yaml` module to produce highlights
based on tokens.

## Usage

Add this to `vim-plug`:

```
Plug 'jakski/vim-yaml', {
  \ 'do': ':UpdateRemotePlugins',
  \}
```

Install required Python modules in your Neovim venv:

```
$ pip install -r requirements.txt
```

## Options

- `g:yaml#error_signs` - should error signs be displayed
- `g:yaml#patterns` - YAML files extensions for autocommands

## Commands

- `YamlError` - display error description

## TODO

- integration tests including Neovim's RPC interactions
