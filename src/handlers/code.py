from aiogram.types import Message
from aiogram.types import BufferedInputFile
from app import logger
import tempfile
import subprocess
import os


async def execute(message: Message, code: str, params):
    print("Execute started!!!!")

    action = params["output"].capitalize()
    if not message:
        logger.error("No callback message in execute")
        return

    with tempfile.TemporaryDirectory() as tmpdir:
        script_path = os.path.join(tmpdir, "script.py")
        with open(script_path, "w") as script_file:
            script_file.write(code)

        try:
            command = ["python", script_path]
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=5,
                cwd=tmpdir,
            )
            output = result.stdout if result.stdout else result.stderr

            if action == "File":
                stdout_file_path = os.path.join(tmpdir, "stdout.txt")
                with open(stdout_file_path, "w") as stdout_file:
                    stdout_file.write(output)

                if len(os.listdir(tmpdir)) > 10:
                    await message.edit_text(
                        "You Dont have any files or there are too many of them\n"
                    )
                for file in os.listdir(tmpdir):
                    if file != "script.py":
                        file_path = os.path.join(tmpdir, file)
                        with open(file_path, "rb") as f:
                            await message.answer_document(
                                BufferedInputFile(
                                    f.read(), filename=file_path)
                            )
                return

        except subprocess.TimeoutExpired:
            output = "Timeout bro."

    if len(output) > 4096:
        for out in range(0, len(output), 4096):
            await message.answer(output[out:out + 4096])
    else:
        await message.answer(
            f"Your stdout\n{output}"
        )
