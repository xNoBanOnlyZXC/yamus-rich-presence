# 'project': {
#     'name': 'YaMus Rich Presence',
#     'version': '1.2',
#     'author': {
#         'name': '~$ sudo',
#         'telegram': 'nobanonlyzxc'
#     },
# }

from winsdk.windows.media.control import \
    GlobalSystemMediaTransportControlsSessionManager as MediaManager
from pypresence import Presence
import time, asyncio
from pypresence.exceptions import PipeClosed

THUMBNAIL_BUFFER_SIZE = 5 * 1024 * 1024
CID = '00000000000000000000'

rpc = Presence(CID)
def run():
    while True:
        try:
            rpc.connect()
            print('[\033[01;38;05;46m•\033[m] Connected to Discord')
            break
        except:
            print('[\033[38;05;226m•\033[m] Waiting discord running to connect...')
            time.sleep(10)
            continue

async def get_media_info():
    sessions = await MediaManager.request_async()
    current_session = sessions.get_current_session()
    if current_session:
        info = await current_session.try_get_media_properties_async()
        info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != '_'}
        info_dict['genres'] = list(info_dict['genres'])
        return info_dict
    return {'title': 'Неизвестно', 'artist': 'Неизвестно'}

async def get_time_info() -> str:
    sessions = await MediaManager.request_async()
    current_session = sessions.get_current_session()
    if current_session:
        info = current_session.get_timeline_properties()
        return info.end_time

async def get_player_info() -> str:
    sessions = await MediaManager.request_async()
    current_session = sessions.get_current_session()
    if current_session:
        id = current_session.source_app_user_model_id
        return str(id).replace(".", " ").title()
    return 'Неизвестный плеер'

buttons = [
    {
        "label": "Only Sq.",
        "url": "https://t.me/OnlySq"
    },
    {
        "label": "v1.2",
        "url": "https://t.me/NoBanOnlyZXC"
    }
    
]

media = ''
title = ''

run()

while True:
    time.sleep(3)
    try:
        media = asyncio.run(get_media_info())
        if title != media["title"]:
            title = media["title"]
            f = str(asyncio.run(get_player_info())).replace(".", " ").title()
            rpc.update(details=f'Слушает {f}', state=f'{media["artist"]} - {media["title"]}', large_image='modhash-icon', large_text='ModHash power', buttons=buttons, start=time.time())
        else:
            time.sleep(3)
    except TypeError:
        rpc.update(details=f'Ничего не играет', state='Нет данных', large_image='modhash-icon', large_text='ModHash power', buttons=buttons)
        rpc.clear()
    except PipeClosed:
        print('[\033[38;05;196m•\033[m] Connection to Discord lost, reconnecting...')
        time.sleep(5)
        run()