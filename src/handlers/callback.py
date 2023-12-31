from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery
from keyboards import kb
from data.macros import macros
from typing import Optional, List
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from states.states import ExecuteCode
import tempfile
import subprocess
from app import logger, scheduler
import os
import json
from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile
from handlers.code import execute
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime

# from states.states import ExecuteCode

router = Router()


class UserMacros(CallbackData, prefix="macros"):
    action: str
    user_id: int
    macros_name: str


@router.callback_query(F.data == "show_list_of_macros")
async def callback_show_list(callback: types.CallbackQuery):
    user_id = int(
        callback.from_user.id) if callback.from_user else None
    if not user_id:
        logger.error("No user")
        return
    info = macros.get_user_macro(user_id)

    list_of_macros = []
    if not info:
        await callback.message.edit_text("You dont have macros assigned to you")
        await callback.answer()
        return

    for mac in info:
        list_of_macros.append({"user_id": user_id, "macros_name": str(mac)})

    await callback.message.edit_text("You got:\n", reply_markup=kb.btns(list_of_macros))
    await callback.answer()


@router.callback_query(F.data == "add_macros")
async def callback_add_macros(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Enter the name of the macros\n")
    await state.set_state(ExecuteCode.add_macros_name)
    await callback.answer()


@router.message(ExecuteCode.add_macros_name, F.text)
async def add_macros_name(message: Message, state: FSMContext):
    user_id = int(message.from_user.id) if message.from_user else None
    if not user_id:
        return
    try:
        msg = message.text.split()
        if len(msg) > 1 or not msg:
            await message.reply("Wrong Format:\n{name}")
            return
    except Exception:
        await message.reply("Wrong Format:\n{name}")
        return
    name = msg[0]
    if macros.get_macros_code(user_id, name)[0]:
        await message.reply("Macros with this name already exists\n")
        return
    await state.update_data(macros_name=name, user_id=user_id)
    await state.set_state(ExecuteCode.add_macros_code)
    await message.reply("Write down the code:\n")


@router.message(ExecuteCode.add_macros_code, F.text)
async def add_macros_code(message: Message, state: FSMContext):
    user_id = int(message.from_user.id) if message.from_user else None
    data = await state.get_data()
    if not user_id or user_id != data.get("user_id"):
        return
    name = data.get("macros_name")
    code = str(message.text) if message.text else ""
    await state.update_data(code=code)
    await state.set_state(ExecuteCode.add_macros_params)
    await message.reply("Choose the output:\n", reply_markup=kb.btns_output_format())


@router.callback_query(F.data == "output_file", ExecuteCode.add_macros_params)
async def output_file(callback: types.CallbackQuery, state: FSMContext):
    params = {
        "output": "file"
    }
    await state.update_data(params=params)
    await callback.message.edit_text("Type any other params, (JSON formatted msg) or type <NONE>")
    await callback.answer()


@router.callback_query(F.data == "output_stdout", ExecuteCode.add_macros_params)
async def output_stdout(callback: types.CallbackQuery, state: FSMContext):
    params = {
        "output": "stdout"
    }
    await state.update_data(params=params)
    await callback.message.edit_text("Type any other params, (JSON formatted msg) or type <NONE>")
    await callback.answer()


@router.message(ExecuteCode.add_macros_params, F.text)
async def add_macros_params(message: Message, state: FSMContext):
    user_id = int(message.from_user.id) if message.from_user else None
    data = await state.get_data()
    if not user_id or user_id != data.get("user_id"):
        logger.error("No user match")
        return
    name = data.get("macros_name")
    code = data.get("code")
    out_params = data.get("params")
    out_params = out_params if isinstance(out_params, dict) else {}

    user_params = dict()
    if message.text and message.text.capitalize() != "None":
        try:
            user_params = json.loads(str(message.text))
        except Exception:
            await message.reply("Wrong Format:\nJSON format params")
            return

    check = set(out_params.keys()) & set(user_params.keys())
    if check:
        await message.reply("Wrong Params, try again\n")
        return

    params = {**out_params, **user_params}

    macros.set_user_macro(user_id, name, code, params)
    await message.answer("Possibly Success!\nCheck your macros;)")
    await state.clear()


@router.callback_query(UserMacros.filter())
async def callbacks_macros(
    callback: types.CallbackQuery,
    callback_data: UserMacros,
    state: FSMContext
):
    user_id = callback_data.user_id
    macros_name = callback_data.macros_name
    action = callback_data.action
    await state.clear()

    match action:
        case "Show":
            await callback.message.edit_text(
                "Choose:\n",
                reply_markup=kb.btns_action(callback_data)
            )
        case "Code":
            code, params = macros.get_macros_code(user_id, macros_name)
            await callback.message.edit_text(
                f"Your params below:\n\n{params}\n\nAnd code:\n\n{code}"
            )
        case "Run":
            code, params = macros.get_macros_code(user_id, macros_name)
            await callback.message.edit_text(
                "Result:\n"
            )
            await execute(callback.message, str(code), params)
        case "Edit":
            code, params = macros.get_macros_code(user_id, macros_name)
            await state.set_state(ExecuteCode.editcode)
            await state.update_data(user_id=user_id, macros_name=macros_name, code=code, params=params)
            await callback.message.edit_text(
                "Let's edit your script:\n..."
            )
        case "Delete":
            macros.delete_macro(user_id, macros_name)
            await callback.message.edit_text(
                "Successfully deleted!"
            )

        case "Schedule":
            code, params = macros.get_macros_code(user_id, macros_name)
            await state.set_state(ExecuteCode.schedule)
            await state.update_data(user_id=user_id, macros_name=macros_name, code=code, params=params)
            await callback.message.edit_text(
                "Please send the cron expression for scheduling this macro.\n"
                "Format: * * * * * (min hour day month day-of-week)"
            )

    await callback.answer()


@router.message(ExecuteCode.editcode, F.text)
async def cmd_editcode(message: Message, state: FSMContext):
    data = await state.get_data()
    macros_name = data.get("macros_name")
    user_id = data.get("user_id")
    macros.update_macro_code(user_id, macros_name, str(message.text))
    await state.clear()
    await message.reply("Success!")


@router.message(ExecuteCode.schedule, F.text)
async def schedule_macro(message: types.Message, state: FSMContext):
    data = await state.get_data()
    cron_expression = message.text.strip()

    # Здесь должна быть валидация cron выражения
    if not validate_cron_expression(cron_expression):
        await message.reply("The provided cron expression is not valid. Please try again.")
        return

    user_id = data.get("user_id")
    macros_name = data.get("macros_name")
    user_id = data.get("user_id")
    code = data.get("code")
    params = data.get("params")
    callback = data.get("callback")
    parts = cron_expression.split()

    # Планирование выполнения скрипта
    # scheduler.add_job(user_id, macros_name, code, params, cron_expression)
    try:
        # scheduler.add_job(
        #     execute,
        #     args=[message, code, params],
        #     trigger="cron",
        #     cron=cron_expression
        # )
        scheduler.start()
        scheduler.add_job(
            execute,
            args=[message, code, params],
            trigger=CronTrigger(minute=1, start_date=datetime.now())
        )
        await message.reply("Your macro has been scheduled!")
    except ValueError as e:
        await message.reply(f"Error scheduling the macro: {e}")

    await state.clear()


def validate_cron_expression(cron_expression):
    if not cron_expression:
        return False
    return True
