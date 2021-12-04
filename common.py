from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen  # , WipeTransition
from kivy.core.window import Window
from kivymd.uix.list import OneLineListItem
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp

Window.size = 375, 667


class MainMenu(Screen):

    def check(self):
        print('просмотр данных')


class SecondScreen(Screen):

    def btn_add_press(self):  # this func work with text from textinput and spinner
        if self.ids.number_detail.text != '':
            print(self.ids.number_detail.text, self.ids.name_detail.text,
                  self.ids.quantity.text, self.ids.comment.text)

            self.ids.number_detail.text = ''
            self.ids.name_detail.text = 'Наименование'
            self.ids.quantity.text = ''
            self.ids.comment.text = ''


class Browse(Screen):

    def show_changes(self, chk_number, chk_date, chk_all):

        if chk_number:
            # self.add_datatable()
            print(self.ids.input_det.text, 'number')

        if chk_date:
            print(self.ids.input_det.text, 'date')

        # for i in range(20):
        #    self.ids.container.add_widget(OneLineListItem(text=f"Single-line item {i}"))

        if chk_all:
            print(self.ids.input_det.text, 'all')


class CommonApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_tables = None

    def build(self):
        sm = ScreenManager()  # transition=WipeTransition())
        sm.add_widget(MainMenu(name='main_menu'))
        sm.add_widget(SecondScreen(name='second_screen'))
        sm.add_widget(Browse(name='browse'))

        return sm


'''
    def add_datatable(self): # need to add a table in browse screen
        self.data_tables = MDDataTable(
            size_hint=(0.9, 0.8),
            column_data=[
                ("No.", dp(30)),
                ("User", dp(30)),
                ("Password", dp(30)),
            ],
            row_data=[
                (
                    "1",
                    "The pitonist",
                    "Strong password",
                ),
                (
                    "2",
                    "The c++ lover",
                    "Save me!!!:)",
                ),
            ]
        )
        self.root.ids.data_scr.add_widget(self.data_tables)
'''

if __name__ == '__main__':
    CommonApp().run()
