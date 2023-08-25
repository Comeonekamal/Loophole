import asyncio
import re

async def verifyLink(url):
    reg = re.compile(r".+\/\/1drv.ms\/(v?|u?)\/")
    m = reg.match(url)
    if not m:
        return 0
    if "u" in m.group(0):
        url = re.sub(m.group(1), "v", url, 1)
        return url
    else:
        return url
            