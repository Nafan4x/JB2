from vkbottle import Keyboard, Text
from logic.registration import registration, states as reg_states
from logic.main_menu import main_menu


async def handle_message(fsm, message_text):

    user_data = await fsm.get_user_data()
    print(user_data)
    if not user_data or (None in user_data.values() and fsm.state in reg_states):
        return await registration(fsm, message_text)
    else:
        return await main_menu(fsm, message_text)
