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


async def linkChecker(url):
    reg = re.compile(r".+\/\/1drv.ms\/(v?|u?)\/")
    m = reg.match(url)
    if not m:
        return 0
    if 'u' in m.group(0):
        url = re.sub(m.group(1),"v", url, 1)
        return await shareLink(url)
    else:
        return await shareLink(url)


# Video codecs: MP4(H264), WEBM(VP8, VP9), OGV, Audio: AAC, MP3, OGG/Vorbis. FFMPEG update for hole would allow for more fileformats


async def shareLink(url):
    p = await playwright().start()  # Starts playwright

    context = await p.chromium.launch_persistent_context(
        user_data_dir="/cache", headless=True, devtools=True, channel="chrome"
    )
    page = await context.new_page()  # Initialize a new page
    await page.goto(
        url,
        timeout=20000,
        wait_until="networkidle",
    )

    url_re = re.compile(r"^.+\.files\.1drv\.com\/(.+)(\/)\b")  # url pattern
    codec_re = re.compile(r"(mp4|webm|ogg)$")
    async with page.expect_response(url_re) as response_info:
        await asyncio.sleep(2)
        await page.get_by_label("Download").click()
        response = await response_info.value
        codec = await response.header_value("Content-Type")
        match_url = re.match(url_re, response.url).group()
        match_type = re.search(codec_re, str(codec)).group()

    await context.close()
    await p.stop()

    link = str()

    match match_type:
        case "mp4":
            link = await filechecker(match_url, match_type)
        case "webm":
            link = await filechecker(match_url, match_type)
        case "ogg":
            link = await filechecker(match_url, match_type)
        case _:
            print("Invalid format!")

    return link
