import ttkbootstrap as tb
import requests as req
from ttkbootstrap.constants import *
from k import *


class SearchBar(tb.Frame):
    def __init__(self, master, url_string):
        super().__init__(master)
        self.pack(padx=PM, pady=(0, PM), fill=BOTH, expand=True)
        self.url_string = url_string


        self.label_text = tb.StringVar(value='Nothing here bitch')

        self.search_bar = tb.Entry(self, font=BODY)
        self.search_button = tb.Button(self, text='SEARCH', command=self.get_records)
        self.search_results_label = tb.Label(self, textvariable=self.label_text, font=LEAD, justify=CENTER)

        self.search_results_label.pack(expand=True, padx=PM, pady=PM, side=BOTTOM)
        self.search_bar.pack(side=LEFT, fill=X, expand=True)
        self.search_button.pack(side=LEFT, padx=(PXS, 0))

    def get_records(self):
        #self.label_text.set(value='SMIC')
        name = self.search_bar.get()
        if len(name) < 1:
            self.label_text.set(value='ERROR\nNo Query Given')
        else:
            url_string = f'{self.url_string}{name}'
            response = req.get(url_string).json()
            if 'msg' in response:
                self.label_text.set(value=response['msg'])
            else:
                response_string = f"""
                Name: {response['name']}
                Grade: {response['name']}
                GPA: {response['gpa']}
                """
                self.label_text.set(value=response_string)

class ButtonGroup(tb.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(padx=PM, pady=PM, fill=X)

        self.submit_button = tb.Button(self, text='submit', bootstyle=SUCCESS)
        self.cancel_button = tb.Button(self, text='cancel', bootstyle=(OUTLINE, SECONDARY))

        self.submit_button.pack(side=RIGHT)
        self.cancel_button.pack(side=RIGHT)

class PrisonerSearch(tb.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.pack(expand=True, fill=BOTH)

        subtitle = 'Tool for searching Mug Shot records and academic failures'

        self.title_label = tb.Label(self, bootstyle=PRIMARY, font=H1, text='SMIC PRISONER')
        self.subtitle_label = tb.Label(self, text=subtitle, font=LEAD)

        self.title_label.pack(padx=PM, pady=(PM, PS), anchor=W)
        self.subtitle_label.pack(padx=PM, pady=(0, PM), anchor=W)
        self.search_bar = SearchBar(self, url_string='http://192.168.3.203:8000/prison/')

class ProbationSearch(tb.Frame):

    def __init__(self, master):
        super().__init__(master)
        #self.pack(expand=True, fill=BOTH)

        subtitle = 'Tool for searching Class failures'

        self.title_label = tb.Label(self, bootstyle=PRIMARY, font=H1, text='SMIC ACADEMIC PROBATION RECORDS')
        self.subtitle_label = tb.Label(self, text=subtitle, font=LEAD)

        self.title_label.pack(padx=PM, pady=(PM, PS), anchor=W)
        self.subtitle_label.pack(padx=PM, pady=(0, PM), anchor=W)
        self.search_bar = SearchBar(self, url_string="")

class App(tb.Window):
    def __init__(self):
        super().__init__(themename='darkly')

        self.title('Frames')
        self.geometry('1920x1080')

        self.nav_frame = tb.Frame(self, bootstyle=PRIMARY)
        self.nav_frame.pack(fill=X, ipadx=PXS, ipady=PXS)

        self.container = tb.Frame(self)
        self.container.pack(fill=BOTH, expand=True)

        self.crime_button = tb.Button(
            self.nav_frame,
            text='Crime Records',
            bootstyle=SECONDARY,
            command=lambda: self.change_frame(name='crime')
        )
        self.crime_button = tb.Button(
            self.nav_frame,
            text='Crime Records',
            bootstyle=SECONDARY,
            command=lambda: self.change_frame(name='fail')
        )

        self.crime_button.pack(side=RIGHT, padx=PXS)
        self.crime_button.pack(side=RIGHT, padx=PXS)

        self.frames = {
            'crime': PrisonerSearch(self.container),
            'fail': ProbationSearch(self.container),
        }

        self.current_frame = 'crime'
        self.set_frame()

    def set_frame(self):
        self.frames[self.current_frame].pack(fill=BOTH, expand=True)

    def remove_frame(self):
        self.frames[self.current_frame].pack_forget()

    def change_frame(self, name):
        self.remove_frame()
        self.current_frame = name
        self.set_frame()


if __name__ == '__main__':
    app = App()
    app.place_window_center()
    app.mainloop()
