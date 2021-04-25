# shortcuts

Creates arbitrary shell scripts from a configuration file; shortcuts

The scripts are described as a [`toml`](https://github.com/toml-lang/toml) file, see [`sample-config.toml`](./sample-config.toml) for an example. You can specify the interpreter, and any links (just copies of the script) you'd want to create, and the command itself. Running `shortcuts create` creates individual shell scripts at `~/.shortcuts`.

A similar functionality could be created with aliases, but those aren't on your \$PATH; aren't visible to other scripts or accessible by system utilities like [`rofi`](https://github.com/davatorium/rofi) (the major inspiration for writing this). You should add the shortcut directory to your path, by adding `export PATH=$PATH:$HOME/.shortcuts` to your shell profile. If you want to use the scripts generated with system utilities, I'd recommend setting your path in `~/.profile` in a `#!/bin/sh` script, and then running `source ~/.profile` in your corresponding `bash`/`zsh` startup files.

This allows me to create/change short/one liner shell scripts in one place, instead of creating/deleting/linking/copying files around in some bin directory manually.

For a more extensive example, see [my `shortcuts.toml` file](https://sean.fish/d/shortcuts.toml?dark)

If you edit this in vim, you can put the following line in your configuration, so that `shortcuts create` runs whenever you save the file:

```
autocmd BufWritePost shortcuts.toml !shortcuts create
```

### Install

Requires python 3.7+

`python3 -m pip install git+https://github.com/seanbreckenridge/shortcuts`

Should be accessible as `shortcuts` or `python3 -m shortcuts`

### Usage

```
Usage: shortcuts create [OPTIONS]

  Create the shell scripts!

Options:
  --debug / --quiet     Log shortcut files being created
  --conf PATH           specify a configuration file
  --shortcuts-dir PATH  specify a shortcuts directory
  --help                Show this message and exit.
```

You can also set the environment variables `SHORTCUTS_CONFIG` and `SHORTCUTS_DIR`, instead of passing `--conf` and `--shortcuts-dir`.
