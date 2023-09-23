"""
Converts a TOML config file to a directory of shell scripts
"""

from pathlib import Path

from dataclasses import dataclass, field
from typing import List, ClassVar, Set, Dict, Any, Optional, Union

import click
import toml


Json = Dict[str, Any]

DEFAULT_PERMISSIONS = 0o755


def expand_path(path: Union[Path, str]) -> Path:
    """
    Take a path or a string, expand '~' and convert to an absolute path
    """
    return Path(path).expanduser().absolute()


@dataclass
class Config:
    """
    Global configuration/data for the application
    """

    raw: Json
    debug: bool = False
    shebang: str = "#!/bin/sh"
    config_file: Path = field(default=Path("~/.config/shortcuts.toml").expanduser())
    shortcuts_dir: Path = field(default=Path("~/.shortcuts/").expanduser())

    @classmethod
    def from_file(cls, debug: bool, config_file: str, shortcuts_dir: str) -> "Config":
        """
        Parse a config file, reading the default shebang value and raw shortcut values
        """
        with open(config_file, "r") as toml_f:
            blob: Dict[str, Any] = dict(toml.load(toml_f).items())
        conf = expand_path(config_file)
        assert conf.exists(), f"config file at {conf} doesn't exist"
        short_dir = expand_path(shortcuts_dir)
        if short_dir.is_file():
            raise FileExistsError(f"File exists at {short_dir}, can't create directory")
        if not short_dir.exists():
            short_dir.mkdir(parents=True)

        # use the default shebang field from the config file otherwise the application default
        resolved_shebang = blob.pop("default_shebang", cls.shebang)

        return cls(
            raw=blob,
            debug=debug,
            shebang=resolved_shebang,
            config_file=conf,
            shortcuts_dir=short_dir,
        )


@dataclass
class Shortcut:
    """
    One shortcut - the name, any additional links and the command text
    """

    name: str
    command: str
    shebang: Optional[str] = None
    links: List[str] = field(default_factory=list)

    REQUIRED_KEYS: ClassVar[Set[str]] = set(["command"])
    ALLOWED_KEYS: ClassVar[Set[str]] = set(["links", "link", "shebang"]) | REQUIRED_KEYS

    @classmethod
    def from_blob(cls, name: str, blob: Json) -> "Shortcut":
        """
        Convert a table loaded from TOML into a Shortcut
        """
        kset: Set[str] = set(blob.keys())
        for req in cls.REQUIRED_KEYS:
            if req not in kset:
                assert f"{req} must be in {blob}"
        for key in kset:
            if key not in cls.ALLOWED_KEYS:
                assert f"unknown key {key}; allowed keys {cls.ALLOWED_KEYS}"

        # combine link string with links array
        links: List[str] = blob.get("links", [])

        if "link" in blob:
            links.append(blob["link"])

        assert "command" in blob, f"{blob} must include 'command'"

        return cls(
            name=name,
            command=blob["command"],
            shebang=blob.get("shebang"),
            links=links,
        )

    def create(self, conf: Config) -> None:
        """
        Combines the shebang and the links to create the corresponding scripts
        """
        for target_name in [self.name, *self.links]:
            target_file: Path = conf.shortcuts_dir / target_name
            if conf.debug:
                click.echo(f"Creating {target_file}")
            with target_file.open(mode="w") as target_f:
                # use default if not specified
                target_f.write(conf.shebang if self.shebang is None else self.shebang)
                target_f.write("\n")
                target_f.write(self.command.strip())
                target_f.write("\n")
            target_file.chmod(DEFAULT_PERMISSIONS)


def create_shortcuts(debug: bool, conf: str, shortcuts_dir: str) -> None:
    """
    'main' - reads files and creates shortcuts
    """
    config = Config.from_file(debug, conf, shortcuts_dir)
    for name, blob in config.raw.items():
        Shortcut.from_blob(name, blob).create(config)
