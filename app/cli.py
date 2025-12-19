import typer
import questionary
import os
import time
import sys
import subprocess
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.table import Table

try:
    from app.cliAssets.main import HELIX_LOGO, MOCKPILOT_SYSTEM_CONTENT
except ModuleNotFoundError:
    from cliAssets.main import HELIX_LOGO, MOCKPILOT_SYSTEM_CONTENT

app = typer.Typer()
console = Console()

COLORS = {
    "primary": "#C701AE",
    "secondary": "#8D018E",
    "tertiary": "#130A82",
    "dark": "#040556",
    "success": "#00FF88",
    "warning": "#FFD700",
    "error": "#FF3366"
}


@app.command()
def start(
        host: str = typer.Option("0.0.0.0", help="Хост для запуска сервера"),
        port: int = typer.Option(8000, help="Порт для запуска сервера"),
        reload: bool = typer.Option(True, help="Включить авто-перезагрузку (для разработки)")
):
    """
    Запускает API сервер Helix.
    """
    if not check_env_file():
        ConsoleClass.header("Ошибка запуска", "MISSING CONFIG")
        ConsoleClass.error("Конфигурация не найдена. Сначала выполните команду 'init'")
        return

    ConsoleClass.header("System Status", "STARTING SERVER")

    config = read_env_config()
    provider = config.get("HELIX_AI_PROVIDER", "unknown")

    ConsoleClass.info(f"AI Provider: [bold {COLORS['primary']}]{provider}[/]")
    ConsoleClass.success(f"Server initializing at http://{host}:{port}")
    console.print()

    import uvicorn

    try:
        uvicorn.run(
            "app.main:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
    except Exception as e:
        ConsoleClass.error(f"Failed to start server: {str(e)}")

class ConsoleClass:
    @staticmethod
    def typewrite(text: str, style: str = "#8D018E", speed: float = 0.01):
        for char in text:
            console.print(char, style=style, end="")
            sys.stdout.flush()
            time.sleep(speed)
        print()

    @staticmethod
    def header(title: str, subtitle: str = ""):
        console.clear()
        console.print("\n")
        logo_text = Text(HELIX_LOGO, style=f"bold {COLORS['primary']}")
        console.print(Align.center(logo_text))

        if subtitle:
            panel_content = Text(f"\n{title}\n", justify="center", style="bold white")
        else:
            panel_content = Text(f"\n{title}\n", justify="center", style="bold white")

        panel = Panel(
            panel_content,
            title=f"[bold {COLORS['secondary']}] {subtitle or 'HELIX CLI'} [/]",
            border_style=COLORS['secondary'],
            padding=(0, 4),
            width=70
        )
        console.print(Align.center(panel))
        console.print()

    @staticmethod
    def success(message: str):
        console.print(f"[{COLORS['success']}]> {message}[/]")

    @staticmethod
    def warning(message: str):
        console.print(f"[{COLORS['warning']}]> {message}[/]")

    @staticmethod
    def error(message: str):
        console.print(f"[{COLORS['error']}]> {message}[/]")

    @staticmethod
    def info(message: str):
        console.print(f"[dim]> {message}[/]")

    @staticmethod
    def section(title: str):
        console.rule(f"[bold {COLORS['primary']}]{title}[/]")


def get_project_root():
    current = Path(__file__).resolve()
    if current.parent.name == "app":
        return current.parent.parent
    return current.parent


def check_docker():
    try:
        subprocess.run(
            ["docker", "--version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def setup_redis():
    if not check_docker():
        ConsoleClass.warning("Docker not found. Skipping Redis setup")
        return False

    ConsoleClass.info("Checking Redis container status...")
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=helix-redis", "--format", "{{.Names}}"],
            capture_output=True,
            text=True
        )
        if "helix-redis" in result.stdout:
            ConsoleClass.success("Redis is already running")
            return True

        ConsoleClass.info("Starting Redis container...")
        subprocess.run(
            ["docker", "run", "-d", "-p", "6379:6379", "--name", "helix-redis", "redis:7-alpine"],
            check=True,
            stdout=subprocess.DEVNULL
        )
        ConsoleClass.success("Redis started successfully")
        return True
    except subprocess.CalledProcessError:
        ConsoleClass.error("Failed to start Redis container")
        return False


def create_env_file(config: dict):
    root = get_project_root()
    env_example_path = root / ".env.example"
    env_path = root / ".env"

    if not env_example_path.exists():
        ConsoleClass.error(".env.example file not found")
        return False

    content = env_example_path.read_text(encoding="utf-8")

    provider_mappings = {
        "demo": {
            "HELIX_AI_PROVIDER": "demo"
        },
        "ollama": {
            "HELIX_AI_PROVIDER": "ollama",
            "HELIX_OLLAMA_HOST": config.get("ollama_host", "http://localhost:11434")
        },
        "deepseek": {
            "HELIX_AI_PROVIDER": "deepseek",
            "HELIX_OPENROUTER_API_KEY": config.get("openrouter_key", "")
        },
        "groq": {
            "HELIX_AI_PROVIDER": "groq",
            "HELIX_GROQ_API_KEY": config.get("groq_key", "")
        }
    }

    provider = config.get("provider", "demo")
    env_vars = provider_mappings.get(provider, {})

    replacements = {
        "HELIX_AI_PROVIDER=demo": f"HELIX_AI_PROVIDER={env_vars.get('HELIX_AI_PROVIDER', 'demo')}",
        "# HELIX_OPENROUTER_API_KEY=sk-or-v1-your-key-here":
            f"HELIX_OPENROUTER_API_KEY={env_vars.get('HELIX_OPENROUTER_API_KEY', '')}"
            if "HELIX_OPENROUTER_API_KEY" in env_vars else "# HELIX_OPENROUTER_API_KEY=sk-or-v1-your-key-here",
        "# HELIX_GROQ_API_KEY=gsk_your-key-here":
            f"HELIX_GROQ_API_KEY={env_vars.get('HELIX_GROQ_API_KEY', '')}"
            if "HELIX_GROQ_API_KEY" in env_vars else "# HELIX_GROQ_API_KEY=gsk_your-key-here",
        "# HELIX_OLLAMA_HOST=http://localhost:11434":
            f"HELIX_OLLAMA_HOST={env_vars.get('HELIX_OLLAMA_HOST', 'http://localhost:11434')}"
            if "HELIX_OLLAMA_HOST" in env_vars else "# HELIX_OLLAMA_HOST=http://localhost:11434",
    }

    for old, new in replacements.items():
        content = content.replace(old, new)

    env_path.write_text(content, encoding="utf-8")
    ConsoleClass.success("Environment file configured successfully")
    return True


def check_env_file():
    root = get_project_root()
    env_path = root / ".env"
    return env_path.exists()


def update_env_file(config: dict):
    root = get_project_root()
    env_path = root / ".env"

    if not env_path.exists():
        ConsoleClass.warning("Environment file not found. Creating new one...")
        return create_env_file(config)

    content = env_path.read_text(encoding="utf-8")
    lines = content.split("\n")
    updated_lines = []

    provider = config.get("provider", "demo")

    updates = {
        "HELIX_AI_PROVIDER": provider,
    }

    if provider == "ollama":
        updates["HELIX_OLLAMA_HOST"] = config.get("ollama_host", "http://localhost:11434")
    elif provider == "deepseek":
        updates["HELIX_OPENROUTER_API_KEY"] = config.get("openrouter_key", "")
    elif provider == "groq":
        updates["HELIX_GROQ_API_KEY"] = config.get("groq_key", "")

    for line in lines:
        updated = False
        for key, value in updates.items():
            if line.startswith(f"{key}=") or line.startswith(f"# {key}="):
                updated_lines.append(f"{key}={value}")
                updated = True
                break
        if not updated:
            updated_lines.append(line)

    env_path.write_text("\n".join(updated_lines), encoding="utf-8")
    ConsoleClass.success("Environment file updated successfully")
    return True


def read_env_config():
    root = get_project_root()
    env_path = root / ".env"

    if not env_path.exists():
        return None

    config = {}
    content = env_path.read_text(encoding="utf-8")

    for line in content.split("\n"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            config[key.strip()] = value.strip()

    return config


def get_provider_config():
    provider = questionary.select(
        "Select AI provider:",
        choices=[
            questionary.Choice("demo - Free, no API keys required", value="demo"),
            questionary.Choice("ollama - Local LLM, private and unlimited", value="ollama"),
            questionary.Choice("deepseek - OpenRouter, cost-effective", value="deepseek"),
            questionary.Choice("groq - Ultra-fast inference, free tier available", value="groq")
        ],
        style=questionary.Style([
            ('selected', f'fg:{COLORS["primary"]} bold'),
            ('pointer', f'fg:{COLORS["primary"]} bold'),
            ('highlighted', f'fg:{COLORS["secondary"]}'),
        ])
    ).ask()

    config = {"provider": provider}

    if provider == "ollama":
        config["ollama_host"] = questionary.text(
            "Ollama host URL:",
            default="http://localhost:11434"
        ).ask()
    elif provider == "deepseek":
        config["openrouter_key"] = questionary.password("OpenRouter API key:").ask()
    elif provider == "groq":
        config["groq_key"] = questionary.password("Groq API key:").ask()

    return config


@app.command()
def init():
    ConsoleClass.header("AI-Powered API Mocking Platform", "SETUP WIZARD")

    existing_config = read_env_config()
    if existing_config:
        ConsoleClass.warning("Existing configuration detected")
        reconfigure = questionary.confirm(
            "Reconfigure environment?",
            default=False
        ).ask()

        if not reconfigure:
            ConsoleClass.info("Using existing configuration")
            console.print()
            return

    ConsoleClass.section("1. AI Provider Configuration")
    config = get_provider_config()

    console.print()
    ConsoleClass.section("2. Environment Setup")

    with console.status(f"[bold {COLORS['primary']}]Applying configuration...[/]", spinner="dots"):
        time.sleep(0.5)

        if check_env_file():
            update_env_file(config)
        else:
            create_env_file(config)

        root = get_project_root()
        dirs = ["assets/AI", "templates/default_pages", "tests", "static"]
        for d in dirs:
            (root / d).mkdir(parents=True, exist_ok=True)
        ConsoleClass.success("Directory structure created")

        system_prompt_path = root / "assets" / "AI" / "MOCKPILOT_SYSTEM.md"
        if not system_prompt_path.exists():
            system_prompt_path.write_text(MOCKPILOT_SYSTEM_CONTENT, encoding="utf-8")
            ConsoleClass.success("AI system prompt initialized")
        else:
            ConsoleClass.info("System prompt already exists")

    console.print()
    ConsoleClass.section("3. Infrastructure")
    setup_redis()

    console.print()
    console.rule(f"[bold {COLORS['success']}]Setup Complete[/]")
    console.print()

    success_panel = Panel(
        Align.center(
            f"[bold {COLORS['success']}]Configuration Applied Successfully[/]\n\n"
            "Start the server:\n"
            f"[bold {COLORS['dark']} on white] helix start [/]\n\n"
            f"Provider: [bold {COLORS['primary']}]{config['provider'].upper()}[/]"
        ),
        border_style=COLORS['success'],
        padding=(1, 2),
        expand=False
    )
    console.print(Align.center(success_panel))
    console.print()


@app.command()
def status():
    ConsoleClass.header("Configuration Status", "CURRENT SETTINGS")

    config = read_env_config()

    if not config:
        ConsoleClass.error("No configuration found. Run 'init' command first")
        return

    table = Table(
        title=f"[bold {COLORS['primary']}]Active Configuration[/]",
        border_style=COLORS['secondary'],
        header_style=f"bold {COLORS['primary']}",
        show_header=True,
        show_lines=True
    )

    table.add_column("Parameter", style=f"bold {COLORS['tertiary']}", width=30)
    table.add_column("Value", style="white", width=40)

    table.add_row("AI Provider", config.get("HELIX_AI_PROVIDER", "Not configured"))
    table.add_row("Redis URL", config.get("HELIX_REDIS_URL", "redis://localhost:6379"))
    table.add_row("Server Port", config.get("HELIX_PORT", "8000"))

    if config.get("HELIX_AI_PROVIDER") == "ollama":
        table.add_row("Ollama Host", config.get("HELIX_OLLAMA_HOST", "Not set"))
    elif config.get("HELIX_AI_PROVIDER") == "deepseek":
        key = config.get("HELIX_OPENROUTER_API_KEY", "")
        table.add_row("OpenRouter Key", f"{key[:10]}..." if key else "Not set")
    elif config.get("HELIX_AI_PROVIDER") == "groq":
        key = config.get("HELIX_GROQ_API_KEY", "")
        table.add_row("Groq Key", f"{key[:10]}..." if key else "Not set")

    console.print(Align.center(table))
    console.print()


@app.command()
def config():
    ConsoleClass.header("Configuration Manager", "MODIFY SETTINGS")

    if not check_env_file():
        ConsoleClass.error("No configuration found. Run 'init' command first")
        return

    action = questionary.select(
        "What would you like to configure?",
        choices=[
            questionary.Choice("Change AI Provider", value="provider"),
            questionary.Choice("Update API Keys", value="keys"),
            questionary.Choice("Reset Configuration", value="reset"),
            questionary.Choice("Exit", value="exit")
        ],
        style=questionary.Style([
            ('selected', f'fg:{COLORS["primary"]} bold'),
            ('pointer', f'fg:{COLORS["primary"]} bold'),
            ('highlighted', f'fg:{COLORS["secondary"]}'),
        ])
    ).ask()

    if action == "exit":
        ConsoleClass.info("Configuration unchanged")
        return

    if action == "reset":
        confirm = questionary.confirm(
            "This will delete current configuration. Continue?",
            default=False
        ).ask()

        if confirm:
            root = get_project_root()
            env_path = root / ".env"
            if env_path.exists():
                env_path.unlink()
                ConsoleClass.success("Configuration reset successfully")
            ConsoleClass.info("Run 'init' command to reconfigure")
        return

    if action == "provider":
        ConsoleClass.section("Provider Configuration")
        new_config = get_provider_config()

        with console.status(f"[bold {COLORS['primary']}]Updating configuration...[/]", spinner="dots"):
            time.sleep(0.3)
            update_env_file(new_config)

        ConsoleClass.success("Provider configuration updated")

    elif action == "keys":
        current_config = read_env_config()
        provider = current_config.get("HELIX_AI_PROVIDER", "demo")

        if provider == "demo":
            ConsoleClass.info("Demo mode does not require API keys")
            return

        ConsoleClass.section("API Key Configuration")

        if provider == "ollama":
            new_host = questionary.text(
                "New Ollama host URL:",
                default=current_config.get("HELIX_OLLAMA_HOST", "http://localhost:11434")
            ).ask()
            update_env_file({"provider": provider, "ollama_host": new_host})
        elif provider == "deepseek":
            new_key = questionary.password("New OpenRouter API key:").ask()
            update_env_file({"provider": provider, "openrouter_key": new_key})
        elif provider == "groq":
            new_key = questionary.password("New Groq API key:").ask()
            update_env_file({"provider": provider, "groq_key": new_key})

        ConsoleClass.success("API credentials updated")

    console.print()


if __name__ == "__main__":
    app()