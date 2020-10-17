# shortcuts

[![Build Status](https://travis-ci.org/seanbreckenridge/shortcuts.svg?branch=master)](https://travis-ci.org/seanbreckenridge/shortcuts) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

Some ruby to create arbitrary shell scripts - shortcuts.

The scripts are described as a [`toml`](https://github.com/toml-lang/toml) file, see [`sample-config.toml`](./sample-config.toml) for an example. You can specify the interpreter, file mode, and any links you'd want to create, and the command itself. Running `shortcuts create` creates individual shell scripts at `~/.shortcuts`.

A similar functionality could be created with aliases, but those aren't on your \$PATH; aren't visible to other scripts or accessible by system utilities like [`rofi`](https://github.com/davatorium/rofi) (the major inspiration for writing this). You should add the shortcut directory to your path, by adding `export PATH=$PATH:$HOME/.shortcuts` to your shell profile. If you want to use the scripts generated with system utilities, I'd recommend setting your path in `~/.profile` in a `#!/bin/sh` script, and then running `source ~/.profile` in your corresponding `bash`/`zsh` startup files.

This allows me to create/change short/one liner shell scripts in one place, instead of creating/deleting/linking/copying files around in some bin directory manually.

For a more extensive example, see [my `shortcuts.toml` file](https://sean.fish/d/shortcuts.toml?dark)

---

```
shortcuts 0.1.1

Creates shortcut shell scripts from a configuration file.

Usage:
  shortcuts create
  shortcuts create [--conf=<FILE>] [--shortcuts-dir=<DIR>]
  shortcuts create [--debug]
  shortcuts -h | --help

Options:
  -h --help               Print the help message
  -d --debug              Print debug information
  --conf=<FILE>           Specify a configuration file
                          [default ~/.config/shortcuts.toml]
  --shortcuts-dir=<DIR>   Specify a shortcuts directory
                          [default ~/.shortcuts/]
```

You can also set the environment variables `SHORTCUTS_CONFIG` and `SHORTCUTS_DIR`, instead of passing `--conf` and `--shortcuts-dir`.

#### Install

Install [`gem`](https://rubygems.org/pages/download), and [`bundle`](https://bundler.io/)

```
# Clone and cd
git clone https://github.com/seanbreckenridge/shortcuts && cd shortcuts
# Install dependencies
bundler install
# Copy shortcuts and config file to somewhere on your $PATH
sudo cp shortcuts /usr/local/bin
cp sample-config.toml ~/.config/shortcuts.toml
# Add your shortcuts dir to your $PATH, by adding a line to your `.bashrc`/`.profile`/`.zshenv`: `export PATH=$PATH:~/.shortcuts`
shortcuts create --debug
```

If you edit this in vim, you can put the following line in your configuration, so that `shortcuts create` runs whenever you save the file:

```
autocmd BufWritePost shortcuts.toml !shortcuts create
```

#### Tests

```
ruby tests.rb
```
