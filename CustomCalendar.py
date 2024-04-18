import datetime, calendar
import flet


class CustomCalendar(flet.Container):
    _current_month = datetime.date.today().month
    _current_year = datetime.date.today().year
    _current_day = datetime.date.today().day
    _first_day_in_month, _last_day_in_month = calendar.monthrange(_current_year, _current_month)
    _day_of_week = {0: "ПН", 1: "ВТ", 2: "СР", 3: "ЧТ", 4: "ПТ", 5: "СБ", 6: "ВС"}
    _months = {0: "Январь", 1: "Февраль", 3: "Март", 4: "АПРЕЛЬ", 5: "Май", 6: "Июнь",
               7: "Июль", 8: "Август", 9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"}

    def __init__(self, width: int, bgcolor="#e2e2e2",
                 font_color="#3c4457", font_color_accent="#ffffff",
                 accent_color="#108ef2", header_font_color="#d2334c",
                 hover_color = "#eeeeee", border_radius=15):
        super().__init__(
            # ширина виджета задаётся пользователем
            width=width,
            # высота считается автоматом, header = width / 7, row = width / 8
            # весь календарь это таблица 2 заголовочные строки + 5 строк на даты, 0.5 на отступы
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
        custom_calendar = flet.Column(
            controls=[
                # заголовок с названием месяца и годом
                flet.Row(
                    controls=[
                        flet.Text(
                            value=str(self._months.get(self._current_month)) + " ",
                            spans=[
                                flet.TextSpan(str(self._current_year),
                                              flet.TextStyle(weight=flet.FontWeight.BOLD))
                                ],
                            weight=flet.FontWeight.W_400,
                            color=self.font_color,
                            size=self.font_size + 2,
                            height=self.width / 7,
                        )
                    ],
                    alignment=flet.MainAxisAlignment.CENTER
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
                )
            ],
            # убирает лишние отступы между элементами Column
            spacing=0,
        )
        self._fill_dates(custom_calendar)
        return custom_calendar

    def _fill_dates(self, custom_calendar: flet.Column):
        day_counter = 1
        day_bgcolor = self.bgcolor
        day_font_color = self.font_color
        day_data="just_a_day"

        for row in range(0, 5):
            current_row = flet.Row(alignment=flet.MainAxisAlignment.CENTER, spacing=0)
            # if row == 4:
            #     current_row.alignment = flet.MainAxisAlignment.START

            for day in range(0, 7):
                if day_counter == self._current_day:
                    # для выделения текущего дня в календаре
                    day_bgcolor = self.accent_color
                    day_font_color = self.font_accent_color
                    day_data="today"
                if row == 0 and day < self._first_day_in_month:
                    current_row.controls.append(flet.Container(width=(self.width - self.width * 0.05) / 8))
                elif self._last_day_in_month >= day_counter:
                    current_row.controls.append(flet.Container(
                        content=flet.Text(
                            value=str(day_counter),
                            text_align=flet.TextAlign.CENTER,
                            weight=flet.FontWeight.W_500,
                            color=day_font_color,
                            size=self.font_size + 2
                        ),
                        bgcolor=day_bgcolor,
                        width=(self.width - self.width * 0.05) / 8,
                        height=self.width / 8,
                        alignment=flet.alignment.center,
                        shape=flet.BoxShape.CIRCLE,
                        on_hover=self._on_hover_date,
                        data=day_data
                    ))
                    day_counter += 1
                    day_bgcolor = self.bgcolor
                    day_font_color = self.font_color
                    day_data="just_a_day"
                else:
                    current_row.controls.append(flet.Container(width=(self.width - self.width * 0.05) / 8))
            custom_calendar.controls.append(current_row)

    def _on_hover_date(self, e):
        # Когда мышь на элементе e.data = "true"
        e.control.bgcolor = self.hover_color if e.data == "true" and e.control.data != "today" else \
            (self.accent_color if e.control.data == "today" else self.bgcolor)
        e.control.update()

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
