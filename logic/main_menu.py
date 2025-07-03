# MainMenu


from service import input_check
from logic.keyboards import keyboard_main_menu
from logic.stats import stats

states = ["stats", "main_menu"]
transitions = []


main_menu_message = {"text": "Main Menu", "keyboard": keyboard_main_menu}


input_strs = ["Статистика", "Бизнес", "Город", "Действия"]


async def main_menu(fsm, message_text):
    if fsm.state == "main_menu":
        is_checked = await input_check(message_text, 15, input_strs)
        print(is_checked)
        if not is_checked:
            return {"text": "Неизвестная команда"}
        if message_text == "Статистика":
            stats_message = await stats(fsm, message_text)
            return stats_message
        else:
            return main_menu_message

    elif fsm.state == "stats":
        ...

    else:
        return {"text": "Main Menu", "keyboard": keyboard_main_menu}
