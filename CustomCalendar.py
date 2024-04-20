import datetime, calendar
import flet
import copy


class CustomCalendar(flet.Container):
    _current_month = datetime.date.today().month
    _current_year = datetime.date.today().year
    _current_day = datetime.date.today().day
    _first_day_in_month, _last_day_in_month = calendar.monthrange(_current_year, _current_month)
    _day_of_week = {0: "ПН", 1: "ВТ", 2: "СР", 3: "ЧТ", 4: "ПТ", 5: "СБ", 6: "ВС"}
    _months = {1: "ЯНВАРЬ", 2: "ФЕВРАЛЬ", 3: "МАРТ", 4: "АПРЕЛЬ", 5: "МАЙ", 6: "ИЮНЬ",
               7: "ИЮЛЬ", 8: "АВГУСТ", 9: "СЕНТЯБРЬ", 10: "ОКТЯБРЬ", 11: "НОЯБРЬ", 12: "ДЕКАБРЬ"}

    def __init__(self, width: int, bgcolor="#e2e2e2",
                 font_color="#3c4457", font_color_accent="#ffffff",
                 accent_color="#108ef2", header_font_color="#d2334c",
                 hover_color="#eeeeee", border_radius=15):
        super().__init__(
            # ширина виджета задаётся пользователем
            width=width,
            # высота считается автоматом, заголовок = width / 7, строка = width / 8
            # весь календарь это таблица 2 заголовочные строки + 5 строк на даты, ~0.5 на отступы
            height=width / 8 * 5 + width / 7 * 2.5,
            border_radius=border_radius,
            padding=flet.padding.only(0, width * 0.08, 0, 0),
            bgcolor=bgcolor,
            alignment=flet.alignment.center
        )
        self.font_color = font_color
        self.header_font_color = header_font_color
        self.accent_color = accent_color
        self.hover_color = hover_color
        self.font_accent_color = font_color_accent
        self.font_size = width * 0.045
        self.content = self._draw_base()

    def _draw_base(self):
        day_container = flet.Container(
            content=flet.Text(
                value="",
                text_align=flet.TextAlign.CENTER,
                weight=flet.FontWeight.W_500,
                size=self.font_size + 2,
                color=self.font_color
            ),
            width=(self.width - self.width * 0.05) / 8,
            height=self.width / 8,
            alignment=flet.alignment.center,
            shape=flet.BoxShape.CIRCLE,
            on_hover=self._on_hover_date,
            data=""
        )
        custom_calendar = flet.Column(
            controls=[
                # заголовок с названием месяца и годом, кнопками для перелистывания календаря
                flet.Row(
                    controls=[
                        flet.Container(flet.IconButton(
                            icon=flet.icons.KEYBOARD_ARROW_LEFT_SHARP,
                            height=self.width / 11,
                            width=self.width / 7,
                            icon_size=self.font_size,
                            padding=0,
                            icon_color=self.font_color,
                            data="left_flip",
                            on_click=self._flip_calendar
                        ),
                            height=self.width / 8,
                            alignment=flet.alignment.center
                        ),
                        flet.Container(flet.Text(
                            # value=str(self._months.get(self._current_month)) + " ",
                            value="",
                            spans=[
                                flet.TextSpan("",
                                              flet.TextStyle(weight=flet.FontWeight.BOLD))
                                ],
                            weight=flet.FontWeight.W_400,
                            color=self.font_color,
                            size=self.font_size + 2,
                            text_align=flet.alignment.center,
                        ),
                            height=self.width / 8,
                            alignment=flet.alignment.center
                        ),
                        flet.Container(flet.IconButton(
                            icon=flet.icons.KEYBOARD_ARROW_RIGHT_SHARP,
                            icon_size=self.font_size,
                            height=self.width / 10,
                            width=self.width / 7,
                            padding=0,
                            data="right_flip",
                            on_click=self._flip_calendar,
                            icon_color=self.font_color
                        ),
                            height=self.width / 8,
                            alignment=flet.alignment.center
                        ),
                    ],
                    alignment=flet.MainAxisAlignment.CENTER,
                    vertical_alignment=flet.CrossAxisAlignment.START,
                ),
                # заголовок с днями недели
                flet.Row(
                    controls=[
                        flet.Text(
                            value=self._day_of_week.get(i),
                            text_align=flet.TextAlign.CENTER,
                            width=(self.width - self.width * 0.08) / 7.8,
                            weight=flet.FontWeight.W_400,
                            size=self.font_size,
                            color=self.header_font_color,
                            height=self.width / 8,
                        ) for i in range(0, 7)
                    ],
                    alignment=flet.MainAxisAlignment.CENTER,
                    height=self.width / 10,
                    # убирает лишние отступы между элементами Row
                    spacing=0
                ),
                # пять строк на даты, создаём их и распаковываем в controls
                *[flet.Row(
                    controls=[copy.deepcopy(day_container) for i in range(0, 7)],
                    alignment=flet.MainAxisAlignment.CENTER,
                    spacing=0
                ) for i in range(0, 5)],
            ],
            # убирает лишние отступы между элементами Column
            spacing=0,
        )
        self._fill_dates(custom_calendar)
        return custom_calendar

    def _fill_dates(self, custom_calendar):
        day_counter = 1
        self._first_day_in_month, self._last_day_in_month = calendar.monthrange(self._current_year, self._current_month)
        custom_calendar.controls[0].controls[1].content.value = self._months.get(self._current_month)
        custom_calendar.controls[0].controls[1].content.spans[0].text = " " + str(self._current_year)
        for row_id, row in enumerate(custom_calendar.controls):
            # первые две строки это заголовки календаря
            if row_id < 2:
                continue
            for column_id, column in enumerate(row.controls):
                if row_id - 2 == 0 and column_id < self._first_day_in_month:
                    column.content.value = "ꟷ"
                    column.content.weight=flet.FontWeight.W_200
                elif self._last_day_in_month >= day_counter:
                    column.content.value = str(day_counter)
                    column.content.weight = flet.FontWeight.W_500
                    if day_counter == self._current_day and self._current_month == CustomCalendar._current_month \
                            and self._current_year == CustomCalendar._current_year:
                        column.bgcolor = self.accent_color
                        column.content.color = self.font_accent_color
                        column.data = "today"
                    else:
                        column.bgcolor = self.bgcolor
                        column.content.color = self.font_color
                        column.data = "just_a_day"
                    day_counter += 1
                else:
                    column.content.value = "ꟷ"
                    column.content.weight = flet.FontWeight.W_200

    def _on_hover_date(self, e: flet.ControlEvent):
        # Когда мышь на элементе e.data = "true"
        e.control.bgcolor = self.hover_color if e.data == "true" and e.control.data != "today" else \
            (self.accent_color if e.control.data == "today" else self.bgcolor)
        e.control.update()

    def _flip_calendar(self, e: flet.ControlEvent):
        if e.control.data == "left_flip":
            if self._current_month - 1 > 0:
                self._current_month = self._current_month - 1
            else:
                self._current_month = 12
                self._current_year = self._current_year - 1
        elif e.control.data == "right_flip":
            if self._current_month + 1 < 12:
                self._current_month = self._current_month + 1
            else:
                self._current_month = 1
                self._current_year = self._current_year + 1
        self._fill_dates(self.content)
        self.content.update()


def main_page(page: flet.Page):
    page.title = "Custom Calendar Widget"
    my_calendar = CustomCalendar(width=250)
    my_calendar2 = CustomCalendar(width=250,
                                  bgcolor="#282c35",
                                  hover_color="#34d409",
                                  font_color="#ffffff",
                                  font_color_accent="#000000",
                                  accent_color="#f9c629",
                                  header_font_color="#ffffff")
    my_calendar3 = CustomCalendar(width=250,
                                  bgcolor="#71a95a",
                                  font_color="#ffffff",
                                  hover_color="#34d409",
                                  font_color_accent="#84ff17",
                                  accent_color="#d2334c",
                                  header_font_color="#ffffff")
    my_calendar4 = CustomCalendar(width=250,
                                  bgcolor="#b09cb8",
                                  font_color="#434054",
                                  accent_color="#fe955e",
                                  header_font_color="#ffffff")
    my_row = flet.Row(controls=[my_calendar, my_calendar2, my_calendar3, my_calendar4], wrap=True)
    page.add(my_row)


if __name__ == "__main__":
    flet.app(target=main_page)
