# Copyright (c) 2022 Itz-fork
# Don't kang this else your dad is gae

import json

from pyrogram import Client
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton
from functools import partial
from asyncio import get_running_loop

from megadl.helpers_nexa.account import m
from megadl.helpers_nexa.mega_help import humanbytes, send_errors
from .callbacks import get_buttons
from .user_account import USER_ACC_INFO
from config import Config


@Client.on_inline_query()
async def inline_megadl(client, query):
    try:
        answers = []
        megadl_q = query.query.strip().lower()
        if megadl_q.strip() == "":
            aboutinlinemsg = """
            ✪ **[Mega.nz-Bot](https://t.me/mjmegabot)**
`A Simple ` [Open Source](https://t.me/mjmegabot)` Telegram Bot to Do `[More](https://t.me/mjwebhack)` with Mega.nz Cloud Storage.`
                
**Developed with ❤️ by [MJLearning](https://t.me/mjlearning)**
"""
            helpinlinemsg = """
**Hey, Choose the help mod using below buttons 😇**
"""
            answers_nexa = (
                InlineQueryResultArticle(
                    title="About Mega.nz-Bot",
                    description="A Simple Bot to Do More with Mega.nz",
                    thumb_url="https://telegra.ph/file/583f46da57641b90c28f9.png",
                    input_message_content=InputTextMessageContent(aboutinlinemsg, disable_web_page_preview=True),
                    reply_markup=await get_buttons("start"),
                ),
                InlineQueryResultArticle(
                    title="Get Help",
                    description="Click here if you don't know how to use this bot.",
                    thumb_url="https://telegra.ph/file/92df448c01c9a46ec32b3.png",
                    input_message_content=InputTextMessageContent(helpinlinemsg, disable_web_page_preview=True),
                    reply_markup=await get_buttons("inline"),
                )
            )
            await client.answer_inline_query(
                query.id,
                results=answers_nexa,
                switch_pm_text=f"@{(await client.get_me()).username}'s Inline Functions",
                switch_pm_parameter="inline",
                cache_time=15)
            return
        
        elif megadl_q.split()[0] == "details":
            inline_down_butotns = []
            if not Config.IS_PUBLIC_BOT:
                if query.from_user.id not in Config.AUTH_USERS:
                    await client.answer_inline_query(
                        query.id,
                        results=answers,
                        switch_pm_text=f"Only Admins Can Use Bot's Inline Dwonload Mode!",
                        switch_pm_parameter="inline",
                        cache_time=10)
                    return
            else:
                pass
            if len(megadl_q.split()) < 2:
                await client.answer_inline_query(
                query.id,
                results=answers,
                switch_pm_text=f"Usage: your_mega_link_here",
                switch_pm_parameter="inline",
                cache_time=10)
                return
            # Getting file size before download
            try:
                url = query.query.strip().split(None, 1)[1]
                json_f_info = m.get_public_url_info(url)
                dumped_j_info = json.dumps(json_f_info)
                loaded_f_info = json.loads(dumped_j_info)
                mega_f_size = loaded_f_info['size']
                mega_f_name = loaded_f_info['name']
                readable_f_size = humanbytes(mega_f_size)
            except Exception as e:
                await client.answer_inline_query(
                        query.id,
                        results=answers,
                        switch_pm_text="An Error Happend!",
                        switch_pm_parameter="inline",
                        cache_time=10)
                send_errors(e)
                return
            details_inline_msg = f"""
》 **File Details**


**File Name:** `{mega_f_name}`
**File Size:** `{readable_f_size}`
**Url:** {url}

**Powered by @MJWebHack**
"""
            d_inline_keyborad = [InlineKeyboardButton("PM Mega.nz-Bot", url=f"https://t.me/{(await client.get_me()).username}")]
            inline_down_butotns.append(d_inline_keyborad)
            INLINE_DWN_B = InlineKeyboardMarkup(inline_down_butotns)
            answers.append(
                InlineQueryResultArticle(
                    title="Got Requested Url's Details",
                    description="Hey, I got your mega.nz url details. Click here to see them",
                    input_message_content=InputTextMessageContent(details_inline_msg, disable_web_page_preview=True),
                    reply_markup=INLINE_DWN_B,
                )
            )
            await client.answer_inline_query(
                query.id,
                results=answers,
                switch_pm_text=f"@{(await client.get_me()).username}'s Inline Functions!",
                switch_pm_parameter="inline",
                cache_time=20)
        
        elif megadl_q.split()[0] == "info":
            if query.from_user.id not in Config.AUTH_USERS:
                await client.answer_inline_query(
                query.id,
                results=answers,
                switch_pm_text=f"Not Authorized to Use This Bot!",
                switch_pm_parameter="inline",
                cache_time=10)
                return
            if not Config.MEGA_EMAIL or not Config.MEGA_PASSWORD:
                await client.answer_inline_query(
                query.id,
                results=answers,
                switch_pm_text=f"Setup an User Account to Use this Feature!",
                switch_pm_parameter="inline",
                cache_time=10)
                return
            loop = get_running_loop()
            inf = await loop.run_in_executor(None, partial(USER_ACC_INFO))
            answers.append(
                InlineQueryResultArticle(
                    title="About Your Mega.nz Account",
                    description="Some info about your Mega.nz Account",
                    input_message_content=InputTextMessageContent(inf)
                )
            )
            await client.answer_inline_query(
                query.id,
                results=answers,
                switch_pm_text=f"@{(await client.get_me()).username}'s Inline Functions",
                switch_pm_parameter="inline",
                cache_time=20)
        else:
            await client.answer_inline_query(
                query.id,
                results=answers,
                switch_pm_text=f"No Result! Go ahead and learn how to use this",
                switch_pm_parameter="inline",
                cache_time=10)
    except Exception as e:
        await send_errors(e)
