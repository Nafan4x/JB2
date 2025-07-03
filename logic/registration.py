from vkbottle import Keyboard, Text
from config import photos_path
from pathlib import Path

from logic.keyboards import (
    keyboard_choose_gender,
    keyboard_choose_type,
    keyboard_main_menu,
)
from service import input_check

states = [
    "start",
    "waiting_name",
    "waiting_gender",
    "waiting_avatar",
    "waiting_type",
    "main_menu",
]

transitions = [
    {
        "trigger": "start_registration",
        "source": "start",
        "dest": "waiting_name",
        "after": "after_state_change",
    },
    {
        "trigger": "set_name",
        "source": "waiting_name",
        "dest": "waiting_gender",
        "after": "after_state_change",
    },
    {
        "trigger": "set_gender",
        "source": "waiting_gender",
        "dest": "waiting_avatar",
        "after": "after_state_change",
    },
    {
        "trigger": "set_avatar",
        "source": "waiting_avatar",
        "dest": "waiting_type",
        "after": "after_state_change",
    },
    {
        "trigger": "set_type",
        "source": "waiting_type",
        "dest": "main_menu",
        "after": "after_state_change",
    },
]


def find_image_paths(folder_path):
    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}
    folder = Path(folder_path)
    return [str(p) for p in folder.rglob("*") if p.suffix.lower() in image_extensions]


female_paths = find_image_paths(f"{photos_path}/female_photos")
male_paths = find_image_paths(f"{photos_path}/male_photos")


async def registration(fsm, message_text):
    if fsm.state == "start":
        fsm.start_registration()
        return {"text": "Привет! Как тебя зовут?"}
    elif fsm.state == "waiting_name":
        name = message_text
        if not await input_check(name, 50):
            return {"text": "Неправильно введены данные"}
        await fsm.set_arg("name", name)
        fsm.set_name()
        return {"text": "Укажи пол", "keyboard": keyboard_choose_gender}
    elif fsm.state == "waiting_gender":
        gender = message_text
        if not await input_check(gender, 20, ["Мужчина", "Женщина"]):
            return {"text": "Неправильно введены данные"}
        await fsm.set_arg("gender", gender)
        fsm.set_gender()
        if gender == "Мужчина":
            phtotos = male_paths
        else:
            phtotos = female_paths
        return {
            "text": f"Выберите avatar",
            "photos": phtotos,
        }
    elif fsm.state == "waiting_avatar":
        gender = await fsm.get_user_data()
        gender = gender["gender"]
        if gender == "Мужчина":
            if not await input_check(
                message_text, 1, [str(i + 1) for i in range(len(male_paths))]
            ):
                return {"text": "Неправильно введены данные"}
            message_text = int(message_text) - 1
            avatar_path = male_paths[message_text]
        else:
            if not await input_check(
                message_text, 1, [str(i + 1) for i in range(len(female_paths))]
            ):
                return {"text": "Неправильно введены данные"}
            message_text = int(message_text) - 1
            avatar_path = female_paths[message_text]
        await fsm.set_arg("avatar_path", avatar_path)
        fsm.set_avatar()
        return {"text": f"Выберите тип", "keyboard": keyboard_choose_type}
    elif fsm.state == "waiting_type":
        type = message_text
        if not await input_check(type, 50, ["Полицейский", "Бандит"]):
            return {"text": "Неправильно введены данные"}
        await fsm.set_arg("type", type)
        fsm.set_type()
        return {"text": f"Регистрация завершена!", "keyboard": keyboard_main_menu}
    else:
        return {"text": "Напишите /start, чтобы начать регистрацию."}
