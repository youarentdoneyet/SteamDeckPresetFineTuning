from pathlib import Path

import unrealsdk
from mods_base import build_mod, get_pc, hook
from unrealsdk.hooks import Type


print("[SteamDeckPresetFineTuning] __init__.py loaded")


SETTINGS_FILE = Path(__file__).parent / "settings.txt"


def apply_settings() -> None:
    pc = get_pc()

    if pc is None:
        print("[SteamDeckPresetFineTuning] ERROR: PlayerController not available")
        return

    if not SETTINGS_FILE.exists():
        print(f"[SteamDeckPresetFineTuning] ERROR: {SETTINGS_FILE} not found")
        return

    for line in SETTINGS_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        try:
            context = unrealsdk.make_struct(
                "ReplicatedConsoleCommandContext",
                Flags=0,
                CommandAndArgs=line,
            )

            pc.ServerGbxConsoleCommand(context)

            print(f"[SteamDeckPresetFineTuning] Applied: {line}")

        except Exception as e:
            print(
                f"[SteamDeckPresetFineTuning] ERROR applying '{line}': "
                f"{type(e).__name__}: {e}"
            )


@hook(
    "/Game/UI/Scripts/ui_script_menu_base.ui_script_menu_base_C:MenuOpen",
    Type.POST,
)
def on_menu_open(obj, args, ret, func):
    print("[SteamDeckPresetFineTuning] MENU OPEN HOOK FIRED!")
    apply_settings()


build_mod(
    author="DrunkenSpycrab",
    name="SteamDeckPresetFineTuning",
    description="Apply tuned graphic settings for Steam Deck Preset",
    version="1.0.0",
)
