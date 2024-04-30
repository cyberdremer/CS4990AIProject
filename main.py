# This is a sample Python script.
import AIRelated.AI
import PromptHelper.PromptHelper
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import customtkinter
from AIRelated.AI import AI
from JsonHelpers import JsonReader, JsonEditor
import PromptHelper
from GUI.App import App


def init_parts_list() -> {}:
    reader = JsonReader.JsonReader()
    parts_list = reader.read_in_data("ScrapedPCPartData")
    return parts_list


def init_assistant_message(parts_list) -> str:
    assistant_message = PromptHelper.PromptHelper.construct_assistant_message(parts_list)
    return assistant_message


def main():
    parts = init_parts_list()
    assistant_message = init_assistant_message(parts)
    app = App(assistant_message)
    app.mainloop()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
