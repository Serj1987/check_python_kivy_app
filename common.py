from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen  # , WipeTransition
from kivy.core.window import Window
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
import sqlite3

Window.size = 375, 667


class MainMenu(Screen):
    pass


class SendScreen(Screen):

    def btn_add_press(self):  # this func work with text from textinput and spinner
        if self.ids.number_detail.text != '':
            self.detail = self.ids.number_detail.text, self.ids.name_detail.text, self.ids.quantity.text, \
                          self.ids.comment.text
            con = sqlite3.connect('container.db')  # (r'G:\задачи\project\tkinter\container.db')
            cur = con.cursor()
            tag = 'отправка'
            rows = (
                self.ids.number_detail.text, self.ids.name_detail.text, self.ids.quantity.text, self.ids.comment.text,
                tag)
            cur.execute("INSERT INTO send VALUES(?, ?, ?, DATE('now'), ?, ?)", rows)
            # sql requests write here ^ to add one string to table

            cur.execute("SELECT * FROM send WHERE date = DATE('now')")  # number_det/name_det/note

            all_data = cur.fetchall()
            con.commit()
            print('Done')


class ArriveScreen(Screen):
    """ this class will work with added parts in database in two tables arrived or sent parts """

    def __init__(self, **kw):
        super().__init__(**kw)
        self.detail = None

    def add_arrive(self):  # add parts into details(arrived) table
        if self.ids.number_detail.text != '':
            self.detail = self.ids.number_detail.text, self.ids.name_detail.text, self.ids.quantity.text, \
                          self.ids.comment.text
            con = sqlite3.connect('container.db')  # (r'G:\задачи\project\tkinter\container.db')
            cur = con.cursor()
            tag = 'приход'
            rows = (
                self.ids.number_detail.text, self.ids.name_detail.text, self.ids.quantity.text, self.ids.comment.text,
                tag)
            cur.execute("INSERT INTO details VALUES(?, ?, ?, DATE('now'), ?, ?)", rows)
            # sql requests write here ^ to add one string to table

            cur.execute("SELECT * FROM details WHERE date = DATE('now')")  # number_det/name_det/note

            all_data = cur.fetchall()
            con.commit()
            print('Done')
            self.update_lbl_ar.text = str('последняя деталь: ' + str(self.ids.number_detail.text) + ' ' +
                                          str(self.ids.name_detail.text) + ' ' + str(self.ids.quantity.text) + ' '
                                          + self.ids.comment.text)
        # print(self.detail)


class Browse(Screen):

    def show_det(self):
        print(type(int(self.ids.input_det.text)), 'number')


class TableAllWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.con = None
        self.data_tables = None
        self.cur = None
        self.rows = None

    def add_all_table(self):
        self.con = sqlite3.connect('container.db')
        self.cur = self.con.cursor()
        self.cur.execute("SELECT * FROM details UNION SELECT * FROM send ORDER BY date DESC")
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
        self.add_all_table()


class TableDetWindow(Screen):

    def add_det_table(self):
        self.con_send = sqlite3.connect('container.db')
        self.con_arr = sqlite3.connect('container.db')

        self.cur_send = self.con_send.cursor()
        self.cur_arr = self.con_arr.cursor()

        browse = self.manager.get_screen('browse')
        self.det = browse.ids.input_det.text

        self.cur_send.execute("SELECT * FROM send WHERE number_detail = ? ORDER BY date DESC", (self.det,))
        self.cur_arr.execute("SELECT * FROM details WHERE number_detail = ? ORDER BY date DESC", (self.det,))

        self.rows = self.cur_send.fetchall()
        self.rows_arr = self.cur_arr.fetchall()
        layout = AnchorLayout()
        self.data_table_send = MDDataTable(
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
        self.add_widget(self.data_table_send)

        self.data_table_arr = MDDataTable(
            use_pagination=True,
            column_data=[
                ("№ детали", dp(20)),
                ("Наименование", dp(30)),
                ("Количество", dp(15)),
                ("Дата", dp(20)),
                ("Примечание", dp(20)),
                ("Метка", dp(30)),
            ],
            row_data=[self.row for self.row in self.rows_arr],
        )

        self.add_widget(self.data_table_arr)
        return layout

    def on_enter(self):
        self.add_det_table()


class TableDateWindow(Screen):

    def add_date_table(self):
        self.con = sqlite3.connect('container.db')
        self.cur = self.con.cursor()
        browse = self.manager.get_screen('browse')
        self.date = browse.ids.input_det.text

        self.cur.execute("SELECT * FROM send WHERE date = ? ORDER BY date DESC", (self.date,))

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
        self.add_date_table()


class CommonApp(MDApp):

    def build(self):
        sm = ScreenManager()  # transition=WipeTransition())
        sm.add_widget(MainMenu(name='main_menu'))
        sm.add_widget(SendScreen(name='send_screen'))
        sm.add_widget(ArriveScreen(name='arrive_screen'))
        sm.add_widget(Browse(name='browse'))
        sm.add_widget(TableAllWindow(name='table_all'))
        sm.add_widget(TableDetWindow(name='table_det'))
        sm.add_widget(TableDateWindow(name='table_date'))
        return sm


if __name__ == '__main__':
    CommonApp().run()
