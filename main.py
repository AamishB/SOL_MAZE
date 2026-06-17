# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pygame-ce",
#     "numpy",
# ]
# ///
import sys
import pygame
import asyncio
import numpy  # imported here so pygbag discovers it for pre-install

# Style the default Pygbag interaction infobox when running on web
if sys.platform == "emscripten":
    import platform
    if hasattr(platform, "window"):
        style = platform.window.document.createElement('style')
        style.innerHTML = """
        #infobox {
            background-color: #0f1423 !important;
            color: #ffb432 !important;
            border: 2px solid #ffb432 !important;
            border-radius: 10px;
            font-family: sans-serif;
            font-size: 18px !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
            padding: 15px 30px !important;
        }
        """
        platform.window.document.head.appendChild(style)


from ui.menus import main_menu

async def main():
    try:
        await main_menu()
    finally:
        pygame.quit()

asyncio.run(main())