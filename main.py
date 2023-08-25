#imports
import asyncio
import numpy as npy
import sys, os
import flet as ft
import aiofiles as aiof
import itertools as itt
#import specifics
from link import verifyLink
from loophole import *


async def main(page: ft.Page):
    page.title = "Loophole"
    page.bgcolor = "#273034"
    page.window_resizable = False
    page.window_height = 900
    page.window_width = 1600
    page.window_min_height = page.window_height
    page.window_min_width = page.window_width
    page.window_maximizable = False
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.fonts = {"REM": "fonts/REM-VariableFont_wght.ttf"}

    page.theme = ft.Theme(font_family="REM")

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
        await page.set_clipboard_async(bRef.current.text)
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Link Copied!"),
            action="Ok.",
            open=True,
            duration=300,
        )
        await page.update_async()

    async def linkCheck(e):
        while True:
            match await verifyLink(tf.value):
                case 0:
                    tf.error_text = "Not a valid OneDrive link! Valid link examples: 'https://1drv.ms/u/s!' or 'https://1drv.ms/v/s!'"
                    await tf.update_async()
                    break
                case url:
                    if tf.error_text is not None:
                        tf.error_text = None
                        await tf.update_async()
                    tf.value = url
                    tf.disabled = True
                    await tf.update_async()
                    await asyncio.sleep(1)
                    await pushLink(tf.value)
                    break

    async def pushLink(e):
        count = 0

        copyB = ft.TextButton(
            style=tb_Style,
            icon="COPY",
            tooltip="Click to copy to clipboard!",
            on_click=copied,
            ref=bRef,
        )

        title = ft.Text(
            size=18,
            style=ft.TextThemeStyle.DISPLAY_MEDIUM,
            weight=ft.FontWeight.W_700,
            ref=tRef,
        )

        progRef.current = ft.ProgressRing(
            scale=10,
            right=page.width / 2,
            bottom=page.height / 2.5,
            stroke_width=5,
            color="#299FD2",
        )

        bStack.controls.append(progRef.current)
        res = asyncio.create_task(shareLink(tf.value))
        while not res.done():
            await page.update_async()
            await asyncio.sleep(0.02)
            if res.done():
                newlink, name = res.result()
                textBox.controls.extend(
                    [
                        title,
                        copyB,
                    ]
                )
                bStack.controls.remove(progRef.current)
                bRef.current.text = newlink
                tRef.current.value = name
                tf.value = None
                print(len(textBox.controls))
                await bStack.update_async()
                await asyncio.sleep(1)
                break

        tf.disabled = False
        await page.update_async()

    async def saveFile(e):
        async with aiof.open(file_dialog.result.path+'.txt', mode="a+") as outfile:
            print(file_dialog.result.path)
            textItems = textBox.controls.copy()
            for i, v in enumerate(textItems, 0):
                if v._get_attr('value'):
                    await outfile.writelines(v.value+': '+'\n')
                if v._get_attr('text'):
                    await outfile.writelines(v.text+'\n')
                    await outfile.write('\n')

    async def show_FileDialog(e):
        if bRef.current.text:
            file_dialog.visible = True
            await file_dialog.save_file_async(
                allowed_extensions=[
                    "txt",
                ],
                dialog_title="Save your links",
                file_name="filename",
                initial_directory=str(os.path.expanduser("~\\Documents\\")),
                file_type=ft.FilePickerFileType.CUSTOM,
            ),
            await page.update_async()
        else:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(
                    "Nothing to save",
                    weight=ft.FontWeight.W_500,
                    color="White",
                    size=17,
                ),
                action="Okape.",
                action_color="White",
                open=True,
                duration=1500,
                bgcolor="#D72E14",
            )
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

    logoImg = await resource_path("assets/images/logo.png")

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
        hint_text="Enter your OneDrive Sharelink, then click 'Get Link!'",
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
        on_submit=linkCheck,
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
        on_click=linkCheck,
    )

    file_dialog = ft.FilePicker(
        visible=False,
        on_result=saveFile,
    )
    page.overlay.append(file_dialog)

    settingsB = ft.Container(
        ft.Icon(
            ft.icons.SETTINGS,
            size=18,
            color="white",
        ),
    )

    header = ft.Container(
        ft.Row(
            [
                logoBox,
                tf,
                button,
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=1,
        ),
    )
    footer = ft.Container(
        ft.Row(
            [
                # infoB,
                # helpB,
                settingsB,
            ],
            alignment=ft.MainAxisAlignment.END,
            vertical_alignment=ft.CrossAxisAlignment.END,
            expand=1,
        ),
    )

    bRef = ft.Ref[ft.TextButton]()

    tRef = ft.Ref[ft.Text]()

    prog = ft.ProgressRing
    progRef = ft.Ref[prog]()

    textBox = ft.ListView(
        spacing=10,
        padding=10,
        # item_extent=60,
        divider_thickness=2,
        height=page.window_height - 118,
    )

    saveItem = ft.Container(
        ft.IconButton(
            icon="SAVE_ALT",
            scale=1.2,
            icon_color="White",
            style=ft.ButtonStyle(
                shape={
                    ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=1),
                },
            ),
            on_click=show_FileDialog,
        ),
        height=40,
        width=page.window_width,
        right=4,
        bottom=0,
        alignment=ft.alignment.center_right,
    )

    bStack = ft.Stack(
        controls=[
            textBox,
            saveItem,
        ],
    )

    body = ft.Container(
        content=bStack,
        bgcolor="#1F2629",
        border_radius=ft.border_radius.all(5),
        expand=3,
    )

    containment = ft.Column(
        controls=[
            header,
            body,
            footer,
        ],
        expand=1,
        spacing=10,
    )

    await page.add_async(containment)
    await page.update_async()
    await page.window_center_async()


ft.app(target=main, assets_dir="assets")
