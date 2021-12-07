from kivy.uix.anchorlayout import AnchorLayout
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen  # , WipeTransition
from kivy.core.window import Window
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
import sqlite3

Window.size = 375, 667


class MainMenu(Screen):
    pass


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
            print(self.ids.input_det.text, 'number')

        if chk_date:
            print(self.ids.input_det.text, 'date')

        if chk_all:
            print(self.ids.input_det.text, 'all')


class TableWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.data_tables = None
        self.cur = None
        self.rows = None

    def add_table(self):
        self.con = sqlite3.connect('container.db')
        self.cur = self.con.cursor()
        self.cur.execute("SELECT * FROM details")
        self.rows = self.cur.fetchall()

        layout = AnchorLayout()
        self.data_tables = MDDataTable(
            use_pagination=True,
            column_data=[
                ("№ детали", dp(20)),
                ("Наименование", dp(30)),
                ("Количество", dp(15)),
                ("Дата", dp(20)),
                ("Примечание", dp(20)),
                ("Метка", dp(30)),
            ],
            row_data=[self.row for self.row in self.rows],
        )
        self.add_widget(self.data_tables)
        return layout

    def on_enter(self):
        self.add_table()


class CommonApp(MDApp):

    def build(self):
        sm = ScreenManager()  # transition=WipeTransition())
        sm.add_widget(MainMenu(name='main_menu'))
        sm.add_widget(SecondScreen(name='second_screen'))
        sm.add_widget(Browse(name='browse'))
        sm.add_widget(TableWindow(name='table'))
        return sm


if __name__ == '__main__':
    CommonApp().run()
