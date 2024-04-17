import datetime, calendar
import flet


class CustomCalendar(flet.Container):

    _current_month = datetime.date.today().month
    _current_year = datetime.date.today().year
    _current_day = datetime.date.today().day
    _first_day_in_month, _last_day_in_month = calendar.monthrange(_current_year, _current_month)
    _day_of_week = {0: "ПН", 1: "ВТ", 2: "СР", 3: "ЧТ", 4: "ПТ", 5: "СБ", 6: "ВС"}
    _months = {0: "Январь", 1: "Февраль", 3: "Март", 4: "Апрель", 5: "Май", 6: "Июнь",
               7: "Июль", 8: "Август", 9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"}

    def __init__(self, width: int, bgcolor="#e2e2e2",
                 font_color="#3c4457", font_color_accent="#ffffff",
                 accent_color="#108ef2", header_font_color="#d2334c"):
        super().__init__(
            width=width,
            height=width / 8 * 5 + width / 6 + 10,
            border_radius=15,
            padding=flet.padding.only(0,5,0,0)
        )
        self.bgcolor = bgcolor
        self.font_color = font_color
        self.header_font_color = header_font_color
        self.accent_color = accent_color
        self.font_accent_color = font_color_accent
        self.content = self._draw()

    def _draw(self):
        # Скелет календаря таблица 5*7
        custom_calendar = flet.DataTable(
            border_radius=15,
            #два атрибута ниже отступы между колонками, и внутренний отступ от границ
            column_spacing=0,
            horizontal_margin=self.width * 0.04,
            divider_thickness=0.01,
            data_row_max_height=self.width / 8,
            heading_row_height=self.width / 7,
            bgcolor=self.bgcolor,
            columns=[flet.DataColumn(flet.Text(
                value=self._day_of_week.get(i),
                text_align=flet.TextAlign.CENTER,
                width=(self.width - self.width * 0.08) / 7,
                weight=flet.FontWeight.W_400,
                size=self.width * 0.06,
                color=self.header_font_color
            )) for i in range(0, 7)],
            rows=[flet.DataRow(cells=[]) for i in range(0, 5)]
        )

        day_counter = 1
        day_bgcolor = self.bgcolor
        day_padding = 0
        day_font_color = self.font_color

        # Заполнение календаря
        for row_index, row in enumerate(custom_calendar.rows):
            for cell_index in range(0, 7):
                if day_counter == self._current_day:
                    #для выделения текущего дня в календаре
                    day_bgcolor = self.accent_color
                    day_padding = custom_calendar.data_row_max_height * 0.09
                    day_font_color = self.font_accent_color
                if row_index == 0 and cell_index < self._first_day_in_month:
                    row.cells.append(flet.DataCell(content=flet.Text(value="")))
                elif self._last_day_in_month >= day_counter:
                    row.cells.append(flet.DataCell(
                        content=flet.Container(content=flet.Text(
                            value=str(day_counter),
                            text_align=flet.TextAlign.CENTER,
                            weight=flet.FontWeight.W_600,
                            color=day_font_color,
                            size=self.width * 0.06
                        ),
                            bgcolor=day_bgcolor,
                            padding=day_padding,
                            width=(self.width - self.width * 0.08) / 7,
                            shape=flet.BoxShape.CIRCLE
                        )),

                    )
                    day_counter += 1
                    day_bgcolor = self.bgcolor
                    day_padding = 0
                    day_font_color = self.font_color
                else:
                    row.cells.append(flet.DataCell(content=flet.Text(value="")))
        custom_calendar = flet.Column(controls=[flet.Text(value=str(self._months.get(self._current_month)) + " "
                                                                + str(self._current_year), weight=flet.FontWeight.BOLD,
                                                          color=self.font_color), custom_calendar],
                                      horizontal_alignment=flet.CrossAxisAlignment.CENTER, spacing=0,)
        return custom_calendar


def main_page(page: flet.Page):
    page.title = "Custom Calendar Widget"
    my_calendar = CustomCalendar(width=200)
    my_calendar2 = CustomCalendar(width=200,
                                  bgcolor="#282c35",
                                  font_color="#ffffff",
                                  font_color_accent="#000000",
                                  accent_color="#f9c629",
                                  header_font_color="#ffffff")
    my_calendar3 = CustomCalendar(width=200,
                                  bgcolor="#71a95a",
                                  font_color="#ffffff",
                                  font_color_accent="#84ff17",
                                  accent_color="#d2334c",
                                  header_font_color="#ffffff")
    my_calendar4 = CustomCalendar(width=200,
                                  bgcolor="#b09cb8",
                                  font_color="#434054",
                                  accent_color="#fe955e",
                                  header_font_color="#ffffff")
    my_row = flet.Row(controls=[my_calendar, my_calendar2, my_calendar3, my_calendar4], wrap=True)
    page.add(my_row)


if __name__ == "__main__":
    flet.app(target=main_page)
















