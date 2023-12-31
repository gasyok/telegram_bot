from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram import types
from handlers.callback import UserMacros


def btns(macros: list):
    kb = InlineKeyboardBuilder()
    for macro in macros:
        kb.button(
            text=macro.get("macros_name"),
            callback_data=UserMacros(
                action="Show",
                user_id=macro.get("user_id"),
                macros_name=macro.get("macros_name"),
            ).pack()
        )
    kb.adjust(len(macros))

    return kb.as_markup()


def btns_options():
    kb = InlineKeyboardBuilder()
    kb.button(
        text="Show",
        callback_data="show_list_of_macros"
    )
    kb.button(
        text="Add",
        callback_data="add_macros"
    )

    return kb.as_markup(resize_keyboard=True)


def btns_output_format():
    kb = InlineKeyboardBuilder()
    kb.button(
        text="FILE",
        callback_data="output_file"
    )
    kb.button(
        text="STDOUT",
        callback_data="output_stdout"
    )

    return kb.as_markup(resize_keyboard=True)


def btns_action(data: UserMacros):
    kb = InlineKeyboardBuilder()
    actions = ["Code", "Run", "Schedule", "Edit", "Delete"]
    for action in actions:
        kb.button(
            text=action,
            callback_data=UserMacros(
                action=action,
                user_id=data.user_id,
                macros_name=data.macros_name,
            ).pack()
        )

    return kb.as_markup(resize_keyboard=True)


def btns_run_format(data: UserMacros):
    kb = InlineKeyboardBuilder()
    actions = ["File", "Stdout"]
    for action in actions:
        kb.button(
            text=action,
            callback_data=UserMacros(
                action=action,
                user_id=data.user_id,
                macros_name=data.macros_name,
            ).pack()
        )

    return kb.as_markup(resize_keyboard=True)
