import re
import asyncio
import random
from filenames import filters
from playwright.async_api import async_playwright as playwright


async def filechecker(url, extension):
    # Check for acceptable types
    name = random.choice(filters)
    filename = name + "." + extension
    link = url + filename
    return link


# Video codecs: MP4(H264), WEBM(VP8, VP9), OGV, Audio: AAC, MP3, OGG/Vorbis. FFMPEG update for hole would allow for more fileformats


async def shareLink(url):
    
    p = await playwright().start()  # Starts playwright

    context = await p.chromium.launch_persistent_context(
        user_data_dir="/cache", headless=True   , devtools=False, channel="chrome"
    )
    page = await context.new_page()  # Initialize a new page
    await page.goto(
        url,
        timeout=0,
        wait_until="networkidle",
    )

    url_re = re.compile(r"^.+\.files\.1drv\.com\/(.+)(\/)\b")  # url pattern
    codec_re = re.compile(r"(mp4|webm|ogg)$")  # codec pattern
    async with page.expect_response(url_re) as response_info:
        await asyncio.sleep(2)
        await page.get_by_label("Download").click()
        await page.get_by_label("Show detailed information").click()
        await asyncio.sleep(2)
        response = await response_info.value
        codec = await response.header_value("Content-Type")
        match_url = re.match(url_re, response.url).group()
        match_type = re.search(codec_re, str(codec)).group()

    link = str()
    filename = str()

    match match_type:
        case "mp4":
            link = await filechecker(match_url, match_type)
            filename = await page.inner_text("#__bolt-details-panel-title")
        case "webm":
            link = await filechecker(match_url, match_type)
            filename = await page.inner_text("#__bolt-details-panel-title")
        case "ogg":
            link = await filechecker(match_url, match_type)
            filename = await page.inner_text("#__bolt-details-panel-title")
        case _:
            print("Invalid format!")
            return 0

    await context.close()
    await p.stop()


    return link, filename