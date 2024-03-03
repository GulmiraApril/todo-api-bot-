# from aiogram import Bot, Dispatcher, types, executor
# import requests
#
# API_BASE_URL = "http://127.0.0.1:8000/todos/"
#
# TOKEN_API = "7125228403:AAFKCgfckkgW59N5yBZay5DlkakdPwk94vU"
# bot = Bot(TOKEN_API)
# db = Dispatcher(bot)
#
#
# @db.message_handler(commands=['start'])
# async def start(message: types.Message):
#     # backendga zapros jonartib malumot olib kelsih kk , requests ishlatiladi!!!
#     # alohida alohida funksiya hammasiga
#     # help ,new ... list
#     # list = ['todo1:shopping', 'intervierw', 'dars qilish!']
#     await message.answer(text="Welcome to my : ) Todo Bot!\n\n"
#                          "You can use the following commands:\n"
#                          "/new <title> [description] - Create a new todo item\n"
#                          "/list - List all todo items\n"
#                          "/delete <id> - Delete a todo item by id\n"
#                          "/update <id> <new title> [new description] [completed] - Update a todo item\n"
#                          "/help - Show a list of commands and usage instructions")
#
# @db.message_handler(commands=['list'])
# async def mytodolist(message: types.Message):
#     # backendga zapros jonartib malumot olib kelsih kk , requests ishlatiladi!!!
#     # alohida alohida funksiya hammasiga
#     # help ,new ... list
#     list = ['todo1:shopping', 'intervierw', 'dars qilish!']
#     for i in list:
#         await message.answer(text=i)
#
#
# @db.message_handler()
# async def echo(message: types.Message):
#     await message.answer(text=message.text)
#
#
# if __name__ == '__main__':
#     executor.start_polling(db, skip_updates=True)

from aiogram import Bot, Dispatcher, types, executor
import requests

API_BASE_URL = "http://127.0.0.1:8000/todos/"

TOKEN_API = "7125228403:AAFKCgfckkgW59N5yBZay5DlkakdPwk94vU"
bot = Bot(TOKEN_API)
db = Dispatcher(bot)


@db.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(text="Welcome to my Todo Bot!\n\n"
                              "You can use the following commands:\n"
                              "/new <title> [description] - Create a new todo item\n"
                              "/list - List all todo items\n"
                              "/delete <id> - Delete a todo item by id\n"
                              "/update <id> <new title> [new description] [completed] - Update a todo item\n"
                              "/help - Show a list of commands and usage instructions")


@db.message_handler(commands=['list'])
async def mytodolist(message: types.Message):
    try:
        response = requests.get(API_BASE_URL)
        todos = response.json()
        if todos:
            for todo in todos:
                await message.answer(text=f"{todo['id']}: {todo['title']} - {todo.get('description', '')}")
        else:
            await message.answer(text="No todos found.")
    except Exception as e:
        await message.answer(text=f"An error occurred: {e}")


@db.message_handler(commands=['new'])
async def new_todo(message: types.Message):
    try:
        command_parts = message.text.split(maxsplit=1)
        if len(command_parts) < 2:
            raise ValueError("Command format is incorrect. Usage: /new <title> [description]")

        title, *description = command_parts[1].split(' ', 1)
        description = description[0] if description else None

        data = {'title': title, 'description': description}
        response = requests.post(API_BASE_URL, json=data)
        new_todo = response.json()
        await message.answer(
            text=f"New todo created:\n{new_todo['id']}: {new_todo['title']} - {new_todo.get('description', '')}")
    except Exception as e:
        await message.answer(text=f"An error occurred: {e}")


@db.message_handler(commands=['delete'])
async def delete_todo(message: types.Message):
    try:
        command_parts = message.text.split(maxsplit=1)
        if len(command_parts) < 2:
            raise ValueError("Command format is incorrect. Usage: /delete <id>")

        todo_id = command_parts[1]
        response = requests.delete(API_BASE_URL + todo_id)
        if response.status_code == 204:
            await message.answer(text=f"Todo with ID {todo_id} deleted successfully.")
        else:
            await message.answer(text=f"Todo with ID {todo_id} not found.")
    except Exception as e:
        await message.answer(text=f"An error occurred: {e}")


# @db.message_handler(commands=['update'])
# async def update_todo(message: types.Message):
#     try:
#         command_parts = message.text.split(maxsplit=1)
#         if len(command_parts) < 2:
#             raise ValueError("Command format is incorrect. Usage: /update <id> <new title> [new description]")
#
#         todo_id, *rest = command_parts[1].split(' ', 1)
#         title, *description = rest[0].split(' ', 1)
#         description = description[0] if description else None
#
#         data = {'title': title, 'description': description}
#         response = requests.put(API_BASE_URL + todo_id, json=data)
#         if response.status_code == 200:
#             updated_todo = response.json()
#             await message.answer(
#                 text=f"Todo updated:\n{updated_todo['id']}: {updated_todo['title']} - {updated_todo.get('description', '')}")
#         else:
#             await message.answer(text=f"Todo with ID {todo_id} not found.")
#     except Exception as e:
#         await message.answer(text=f"An error occurred: {e}")

@db.message_handler(commands=['update'])
async def update_todo(message: types.Message):
    try:
        command_parts = message.text.split(maxsplit=1)
        if len(command_parts) < 2:
            raise ValueError("Command format is incorrect. Usage: /update <id> <new title> [new description]")

        todo_id, *rest = command_parts[1].split(' ', 1)
        title, description = rest[0].split(' ', 1) if rest else (None, None)

        response = requests.put(API_BASE_URL + todo_id, json={'title': title, 'description': description})

        if response.status_code == 200:
            updated_todo = response.json()
            await message.answer(
                text=f"Todo updated:\n{updated_todo['id']}: {updated_todo['title']} - {updated_todo.get('description', '')}")
        else:
            await message.answer(text=f"Todo with ID {todo_id} not found.")
    except Exception as e:
        await message.answer(text=f"An error occurred: {e}")


@db.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer(text="You can use the following commands:\n"
                              "/new <title> [description] - Create a new todo item\n"
                              "/list - List all todo items\n"
                              "/delete <id> - Delete a todo item by id\n"
                              "/update <id> <new title> [new description] [completed] - Update a todo item\n"
                              "/help - Show a list of commands and usage instructions")


if __name__ == '__main__':
    executor.start_polling(db, skip_updates=True)
