import threading

import customtkinter
from CTkMessagebox import CTkMessagebox

from GUI import InputSanityCheck


import JsonHelpers.JsonReader
import PromptHelper.PromptHelper
import PromptHelper.PromptWriter
import AIRelated


class Messagebox(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

    def incorrect_input(self, message):
        warning_message = CTkMessagebox(title="Warning", message=message, option_1="Retry" ,master=self.master)


class OutputTextFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.output_label = customtkinter.CTkLabel(self, text="Chatbot Build Recommendation",
                                                   font=customtkinter.CTkFont(weight="bold", size=25))
        self.output_label.grid(row=0, column=0)

        self.output_box = customtkinter.CTkTextbox(self, font=customtkinter.CTkFont(size=20), width=400, height=300)
        self.output_box.grid(row=1, column=0, pady=(20, 0))


class EntryBoxFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.budget_label = customtkinter.CTkLabel(self, text="Budget in $",
                                                   font=customtkinter.CTkFont(weight="bold"))
        self.budget_label.grid(row=0, column=0)

        self.entry_box = customtkinter.CTkEntry(self)
        self.entry_box.grid(row=1, column=0)

    def get_entry(self):
        return self.entry_box.get()


class ComboboxFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.comboboxes = []

        self.purpose_label = customtkinter.CTkLabel(self, text="PC Use case")

        self.gpu_label = customtkinter.CTkLabel(self, text="GPU Vendor",
                                                font=customtkinter.CTkFont(weight="bold"))
        self.gpu_label.grid(row=0, column=0)
        self.gpu_combobox = customtkinter.CTkComboBox(self, values=["AMD", "NVIDIA",
                                                                    "NO PREFERENCE"])
        self.gpu_combobox.grid(row=1, column=0),

        self.cpu_label = customtkinter.CTkLabel(self, text="CPU Vendor",
                                                font=customtkinter.CTkFont(weight="bold"))
        self.cpu_label.grid(row=2, column=0)
        self.cpu_combobox = customtkinter.CTkComboBox(self, values=["AMD", "INTEL",
                                                                    "NO PREFERENCE"])
        self.cpu_combobox.grid(row=3, column=0)

        self.purpose_label = customtkinter.CTkLabel(self, text="PC Use case",
                                                    font=customtkinter.CTkFont(weight="bold"))
        self.purpose_label.grid(row=4, column=0)
        self.purpose_combobox = customtkinter.CTkComboBox(self, values=["GAMING", "CONTENT CREATION"])
        self.purpose_combobox.grid(row=5, column=0)

        self.comboboxes.append(self.gpu_combobox)
        self.comboboxes.append(self.cpu_combobox)
        self.comboboxes.append(self.purpose_combobox)

    def get_combobox_choices(self) -> []:
        combobox_entries = []
        for entries in self.comboboxes:
            combobox_entries.append(entries.get())
        return combobox_entries


class App(customtkinter.CTk):
    def __init__(self, assistant_message):
        super().__init__()
        self.client = AIRelated.AI.AI()
        self.assistant_message = assistant_message

        self.geometry("800x500")
        self.title("PC Build Chatbot")
        reader = JsonHelpers.JsonReader.JsonReader()
        self.json_data = reader.read_in_data("ScrapedPCPartData")

        self._set_appearance_mode('dark')
        self.gui_label = customtkinter.CTkLabel(self, text="PC Build Chatbot",
                                                font=customtkinter.CTkFont(size=40, weight="bold"))
        self.gui_label.grid(row=0, column=1, pady=(20, 5), sticky="n")
        self.frame = customtkinter.CTkFrame(self)

        self.frame.grid(row=1, column=1)

        self.combobox_frame = ComboboxFrame(self.frame)
        self.combobox_frame.grid(row=0, column=0, pady=(20, 5), padx=100)

        self.entrybox_frame = EntryBoxFrame(self.combobox_frame)
        self.entrybox_frame.grid(row=6, column=0)

        self.output_frame = OutputTextFrame(self.frame)
        self.output_frame.grid(row=0, column=2, padx=50)

        self.button = customtkinter.CTkButton(self.frame, command=self.generate_build, text="Generate Build")
        self.button.grid(row=1, column=0, padx=20, pady=(20, 5))

        self.dialogue_box = Messagebox(self.frame)

    def generate_build(self):

        try:
            self.output_frame.output_box.delete(0.0, 'end')
            user_choices = self.combobox_frame.get_combobox_choices()
            user_budget = self.entrybox_frame.get_entry()

            if InputSanityCheck.check_valid(user_budget) is False:
                raise TypeError

            user_choices.append(user_budget)
            ai_prompt = PromptHelper.PromptHelper.construct_final_prompt(user_choices, self.assistant_message)

            ai_output = self.client.get_completion(ai_prompt)

            final_output = PromptHelper.PromptHelper.format_output(ai_output)
            self.output_frame.output_box.insert("0.0", final_output)
            PromptHelper.PromptWriter.write_out_prompt(final_output)
        except ValueError as valerr:
            error_message = "There has been an issue in generating the build please try again."
            self.output_frame.output_box.insert("0.0", error_message)
            self.dialogue_box.incorrect_input(error_message)
        except TypeError as typerr:
            self.entrybox_frame.entry_box.delete(first_index=0, last_index=len(user_budget))
            self.dialogue_box.incorrect_input("Invalid input, please try again!")

    def generate_build_async(self):
        thread = threading.Thread(target=self.generate_build)
        thread.start()

    def threaded_build(self):
        self.generate_build_async()
