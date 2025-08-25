import asyncio
from playwright.async_api import async_playwright, expect
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Navigate to the local index.html file
        await page.goto(f"file://{os.getcwd()}/index.html")

        # Take a screenshot of the initial state
        await page.screenshot(path="jules-scratch/verification/initial_state.png")

        # Click the strict mode checkbox
        await page.locator("input[type='checkbox']").check()

        # Start the game
        await page.locator("#level-title").click()

        # Wait for a button to be animated, this indicates the sequence has started
        await page.wait_for_function("() => document.querySelector('.pressed')")

        # Get the id of the pressed button
        pressed_button_id = await page.evaluate("() => document.querySelector('.pressed').id")

        # Define all button ids
        all_buttons = ["green", "red", "yellow", "blue"]

        # Find a button to click that is not the pressed one
        wrong_button_id = next(btn for btn in all_buttons if btn != pressed_button_id)

        # Click the wrong button
        await page.locator(f"#{wrong_button_id}").click()

        # Expect the game over class to be applied
        await expect(page.locator("body")).to_have_class("game-over")

        # Take a screenshot of the game over state
        await page.screenshot(path="jules-scratch/verification/game_over_strict.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
