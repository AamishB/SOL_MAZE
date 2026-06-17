# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pygame-ce",
#     "numpy",
# ]
# ///

import pygame
import asyncio
import numpy  # imported here so pygbag discovers it for pre-install
from ui.menus import main_menu

async def main():
    try:
        await main_menu()
    finally:
        pygame.quit()

asyncio.run(main())