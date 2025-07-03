from vkbottle import Keyboard, Text

keyboard_main_menu = (
    Keyboard(one_time=False)  # `one_time=True` — клавиатура исчезает после нажатия
    .add(Text("Статистика"))
    .row()
    .add(Text("Бизнес"))
    .add(Text("Город"))
    .row()
    .add(Text("Действия"))
)

keyboard_choose_type = (
    Keyboard(one_time=True)  # `one_time=True` — клавиатура исчезает после нажатия
    .add(Text("Полицейский"))
    .add(Text("Бандит"))
)

keyboard_choose_gender = (
    Keyboard(one_time=True)  # `one_time=True` — клавиатура исчезает после нажатия
    .add(Text("Мужчина"))
    .add(Text("Женщина"))
)
