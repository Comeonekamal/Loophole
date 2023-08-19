import asyncio
import numpy as npy
import flet as ft
import sys, os
from loopholeasync import linkChecker


async def main(page: ft.Page):
    page.title = "Loophole"
    page.bgcolor = "#273034"
    page.window_resizable = False
    page.window_height = 900
    page.window_width = 1600
    page.window_min_height = page.window_height
    page.window_min_width = page.window_width
    page.window_maximizable = False

    tb_Style = ft.ButtonStyle(
        color="white",
        overlay_color={ft.MaterialState.HOVERED: "#687F89"},
        side={ft.MaterialState.HOVERED: ft.BorderSide(1.0, "#687F89")},
        padding=22,
        shape={
            ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=2.5),
        },
    )

    async def copied(e):
        await page.set_clipboard_async(buttonRef.current.text)
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Link Copied!"), action="Ok.", open=True, duration=300
        )
        await page.update_async()

    async def focusError(e):
        if not tf.on_blur and not tf.value:
            tf.cursor_color = "#FFA1A1"
            tf.focused_bgcolor = "#612F2F"
            tf.focused_color = "#DC0000"
            tf.focused_border_color = "#FF4848"
            tf.hint_text = "Please enter a OneDrive link!"
            tf.hint_style = ft.TextStyle(
                color="#DC0000",
                weight=ft.FontWeight.W_500,
            )
            await tf.update_async()

    async def isOnChange(e):
        if tf.value:
            tf.hint_text = "Your OneDrive Sharelink"
            tf.cursor_color = "#299FD2"
            tf.focused_color = "#778E98"
            tf.focused_border_color = "#299FD2"
            tf.focused_bgcolor = "#222A2D"
            tf.hint_style = ft.TextStyle(
                color="#5B7078",
                weight=ft.FontWeight.W_500,
            )
            await tf.update_async()

    # note to self: possibly convert this to link regex match case.
    async def pushLink(e):
        if not tf.value:
            await tf.focus_async()
            tf.on_focus = focusError
            tf.on_change = isOnChange
            await tf.update_async()
        else:
            tf.disabled = True

            progRef.current = ft.ProgressRing(
                right=page.width/2,
                bottom=page.height/2,
                stroke_width=8,
                color="#299FD2",
            )

            buttonRef.current = ft.TextButton(
                expand=1,
                icon=ft.icons.COPY,
                style=tb_Style,
                tooltip="Click to copy to clipboard!",
                on_click=copied,
            )

            bStack.controls.append(progRef.current)
            newLink = asyncio.create_task(linkChecker(tf.value))
            while not newLink.done():
                for i in npy.linspace(0, 1, 200):
                    progRef.current.value = i
                    print(progRef.current.value)
                    await page.update_async()
                    await asyncio.sleep(0.03)
                    loadTime = progRef.current.value
                    print(loadTime)
                if newLink.done():
                    for i in npy.arange(loadTime, 1.0, 0.01):
                        progRef.current.value = i * 2
                        await bStack.update_async()
                        await asyncio.sleep(1)
                        break
                    textBox.controls.append(buttonRef.current)
                    bStack.controls.remove(progRef.current)
                    buttonRef.current.text = newLink.result()
                    await bStack.update_async()
                    await asyncio.sleep(1)
                    break

            tf.disabled=False
            await page.update_async()

    async def imgHover(e):
        logoBox.scale = ft.Scale(1.15) if e.data == "true" else ft.Scale(1.0)
        await logoBox.update_async()

    async def resource_path(relative_path):
        """Get absolute path to resource, works for dev and for PyInstaller"""
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    logo = ft.Ref[(ft.Image)]()

    logoImg = await resource_path("images/logo.png")

    logo.current = ft.Image(src=logoImg, height=25)

    logoBox = ft.Container(
        content=logo.current,
        animate_scale=ft.animation.Animation(1000, "easeOutExpo"),
        padding=ft.padding.only(10.0, 10.0, 10.0, 5.0),
        margin=ft.margin.all(0),
        on_hover=imgHover,
        ink=False,
        url="https://coolhole.org/",
        tooltip="GET IN COOLHOLE",
    )

    tf = ft.TextField(
        # Inner label:
        label="URL",
        label_style=ft.TextStyle(
            color="#dcdedd",
            weight=ft.FontWeight.W_600,
        ),
        # Hint text and style:
        hint_text="Your OneDrive Sharelink",
        hint_style=ft.TextStyle(
            color="#5B7078",
            weight=ft.FontWeight.W_500,
        ),
        expand=1,
        content_padding=ft.padding.only(10, 0, 5, 0),
        # Static text, bgcolor, and border color:
        color="#273034",
        bgcolor="#344045",
        border_color="#5B7078",
        # Focused text color
        focused_color="#CCD5D8",
        focused_bgcolor="#222A2D",
        focused_border_color="#299FD2",
        cursor_color="#299FD2",
        # Extra settings
        max_lines=1,
    )

    button = ft.OutlinedButton(
        "Get Link!",
        style=ft.ButtonStyle(
            color="white",
            overlay_color={ft.MaterialState.HOVERED: "#299FD2"},
            side={ft.MaterialState.HOVERED: ft.BorderSide(1.0, "#299FD2")},
            padding=20.5,
            shape={
                ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=5),
            },
        ),
        tooltip="Click here to grab the new link.",
        on_click=pushLink,
    )

    header = ft.Row(
        controls=[logoBox, tf, button],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    copyButton = ft.TextButton
    buttonRef = ft.Ref[copyButton]()

    prog = ft.ProgressRing
    progRef = ft.Ref[prog]()

    textBox = ft.ListView(
        spacing=10,
        padding=10,
        item_extent=60,
        divider_thickness=2,
        height=page.window_height - 118,
    )

    # add info footer and settings box.

    bStack = ft.Stack(
        controls=[
            textBox,
        ],
        expand=1,
        width=page.window_width,
    )

    body = ft.Row(
        controls=[
            ft.Container(
                content=bStack,
                bgcolor="#1F2629",
                expand=1,
                margin=ft.margin.symmetric(10,0),
                border_radius=ft.border_radius.all(5),
            )
        ],
        height=page.window_height - 118,
    )

    await page.add_async(header, body)
    await page.update_async()
    await page.window_center_async()
    

ft.app(target=main)
