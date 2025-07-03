async def input_check(
    input_str: str, max_length: int, allowed_values: list[str] = None
) -> bool:
    """
    Проверяет строку по следующим параметрам:
    1. Не превышает максимальную длину.
    2. Если указан список допустимых значений — строка должна быть в этом списке.

    :param input_str: Строка для проверки
    :param max_length: Максимально допустимая длина строки
    :param allowed_values: Необязательный список допустимых значений
    :return: True, если строка проходит все проверки, иначе False
    """
    if not isinstance(input_str, str):
        return False

    if len(input_str) > max_length:
        return False

    if allowed_values is not None and input_str not in allowed_values:
        return False

    return True
