# shortcuts

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

Some ruby to create arbitrary shell scripts - shortcuts.

The scripts are described as a [toml](https://github.com/toml-lang/toml) file, see [`sample-config.toml`](./sample-config.toml) for an example. You can specify the interpreter, file mode, and any links you'd want to create, and the command itself. Running `shortcut create` creates individual shell scripts at `~/.shortcuts`

A similar functionality could be created with aliases, but those aren't on your $PATH; aren't visible to other scripts or accessible by system utilities like [rofi](https://github.com/davatorium/rofi) (the major inspiration for writing this)

This allows me to create/change scripts in one place, instead of creating/deleting/linking/copying files around in some bin directory manually.

```
shortcuts 0.1.0

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
                          [default ~/.config/shortcuts.conf]
  --shortcuts-dir=<DIR>   Specify a shortcuts directory
                          [default ~/.shortcuts/]
```

You can also set the evironment variables `SHORTCUTS_CONFIG` and `SHORTCUTS_DIR`, instead of passing `--conf` and `--shortcuts-dir`.

#### Install

Install [`gem`](https://rubygems.org/pages/download), and [`bundle`](https://bundler.io/)

```
# Clone and cd
git clone https://github.com/seanbreckenridge/shortcuts
cd shortcuts
# Install dependencies
bundler install
# Copy shortcuts to somewhere on your $PATH
cp shortcuts /usr/local/bin
cp sample-config.toml ~/.config/shortcuts.toml
# Add your shortcuts dir to your $PATH, by adding a line to your `.bashrc`/`.profile`/`.zshenv`: `export PATH=$PATH:~/.shortcuts`
shortcuts create --debug
```

#### Tests

```
ruby tests.rb
```
