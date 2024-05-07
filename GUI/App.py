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
        warning_message = CTkMessagebox(title="Warning", message=message, option_1="Retry", master=self.master)


class ProgressBarFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.slider_progressbar_frame = customtkinter.CTkFrame(master, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=2, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)


class OutputTextFrame(customtkinter.CTkFrame):
    def __init__(self, master, width, font, height):
        super().__init__(master)


        self.output_box = customtkinter.CTkTextbox(master, font=font, width=width, height=height)
        self.output_box.grid(row=1, column=1, padx = (20,20), pady=(0, 0),sticky = "nsew")


class EntryBoxFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.budget_label = customtkinter.CTkLabel(master, text="Budget in $:", anchor="w",
                                                   font=customtkinter.CTkFont(weight="bold"))
        self.budget_label.grid(row=6, column=0, padx = (20,0))

        self.entry_box = customtkinter.CTkEntry(master)
        self.entry_box.grid(row=7, column=0, padx = (40,0))

    def get_entry(self):
        return self.entry_box.get()


class ComboboxFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.comboboxes = []

        self.purpose_label = customtkinter.CTkLabel(self, text="PC Use case:")

        self.gpu_label = customtkinter.CTkLabel(self, text="GPU Vendor:", anchor="w",
                                                font=customtkinter.CTkFont(weight="bold"))
        self.gpu_label.grid(row=0, column=0, padx = (20,0))
        self.gpu_combobox = customtkinter.CTkComboBox(self, values=["AMD", "NVIDIA",
                                                                    "NO PREFERENCE"])
        self.gpu_combobox.grid(row=1, column=0, padx =(40,0)),

        self.cpu_label = customtkinter.CTkLabel(self, text="CPU Vendor:", anchor="w",
                                                font=customtkinter.CTkFont(weight="bold"))
        self.cpu_label.grid(row=2, column=0, padx = (20,0))
        self.cpu_combobox = customtkinter.CTkComboBox(self, values=["AMD", "INTEL",
                                                                    "NO PREFERENCE"])
        self.cpu_combobox.grid(row=3, column=0, padx = (40,0))

        self.purpose_label = customtkinter.CTkLabel(self, text="PC Use case", anchor="w",
                                                    font=customtkinter.CTkFont(weight="bold"))
        self.purpose_label.grid(row=4, column=0, padx = (20,0))
        self.purpose_combobox = customtkinter.CTkComboBox(self, values=["GAMING", "CONTENT CREATION"])
        self.purpose_combobox.grid(row=5, column=0, padx = (40,0))

        self.entry_box = EntryBoxFrame(self)

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
        reader = JsonHelpers.JsonReader.JsonReader()
        self.json_data = reader.read_in_data("ScrapedPCPartData")

        self.geometry(f"{1100}x{580}")
        self.title("PCBuildChatbot.py")
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        """Start constructing sidebar"""

        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.sidebar_frame_label = customtkinter.CTkLabel(self.sidebar_frame,
                                                          text="PC Builder Chatbot",
                                                          font=customtkinter.CTkFont(size=20, weight="bold"))
        self.sidebar_frame_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.combobox_frame = ComboboxFrame(self.sidebar_frame)

        self.combobox_frame.grid(row=1, column=0, sticky="nsew")

        """Start constructing the progress bar"""
        self.progress_bar_frame = ProgressBarFrame(self)
        self.progress_bar = customtkinter.CTkProgressBar(self.progress_bar_frame.slider_progressbar_frame)
        self.progress_bar.grid(row = 1, column = 0, padx =(0,20), pady = (0,0), sticky = "nsew")
        self.progress_bar.configure(mode="intermediate")


        """Start constructing the outputframe"""
        self.output_frame = OutputTextFrame(self,width=500, font=("Arial", 24, "bold"), height=500)

        self.generate_button =  customtkinter.CTkButton(master = self.combobox_frame, text="Generate!", command=self.generate_build, width=90)
        self.generate_button.grid(row =11, column = 0 , padx = (40,0), pady = (20,20) ,sticky = "nsew")
        self.dialogue_box = Messagebox(self)


    def generate_build(self):

        try:
            self.progress_bar.start()
            self.output_frame.output_box.delete(0.0, 'end')
            user_choices = self.combobox_frame.get_combobox_choices()
            user_budget = self.combobox_frame.entry_box.get_entry()

            if InputSanityCheck.check_valid(user_budget) is False:
                raise TypeError

            user_choices.append(user_budget)
            ai_prompt = PromptHelper.PromptHelper.construct_final_prompt(user_choices, self.assistant_message)

            ai_output = self.client.get_completion(ai_prompt)

            final_output = PromptHelper.PromptHelper.format_output(ai_output)
            self.output_frame.output_box.insert("0.0", final_output)
            PromptHelper.PromptWriter.write_out_prompt(final_output)
            self.progress_bar.set(100)
        except ValueError as valerr:
            error_message = "There has been an issue in generating the build please try again."
            self.output_frame.output_box.insert("0.0", error_message)
            self.dialogue_box.incorrect_input(error_message)
        except TypeError as typerr:
            self.combobox_frame.entry_box.entry_box.delete(first_index=0, last_index=len(user_budget))
            self.dialogue_box.incorrect_input("Invalid input, please try again!")

    def generate_build_async(self):
        thread = threading.Thread(target=self.generate_build)
        thread.start()

    def threaded_build(self):
        self.generate_build_async()
