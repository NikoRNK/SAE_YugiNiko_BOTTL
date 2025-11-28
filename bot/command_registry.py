COMMANDS_HELP: dict[str, str] = {}


def register_command(name: str, description: str) -> None:
    COMMANDS_HELP[f"/{name}"] = description
