import datetime, calendar
import flet


class CustomCalendar(flet.Container):

    _current_month = datetime.date.today().month
    _current_year = datetime.date.today().year
    _current_day = datetime.date.today().day
    _first_day_in_month, _last_day_in_month = calendar.monthrange(_current_year, _current_month)
    _day_of_week = {0: "ПН", 1: "ВТ", 2: "СР", 3: "ЧТ", 4: "ПТ", 5: "СБ", 6: "ВС"}

    def __init__(self, width: int):
        super().__init__(
            width=width,
            height=width / 8 * 5 + width / 6 + 20
        )
        # temp = width / 8 * 5 + width / 6
        # print(temp)
        self.content = self._draw()

    def _draw(self) -> flet.DataTable:
        # Скелет календаря таблица 5*7
        custom_calendar = flet.DataTable(
            border_radius=15,
            #два атрибута ниже отступы между колонками, и внутренний отступ от границ
            column_spacing=0,
            horizontal_margin=self.width * 0.04,
            #vertical_lines=flet.border.BorderSide(1, "#f1f1f1"),
            #horizontal_lines=flet.border.BorderSide(1, "#f1f1f1"),
            data_row_max_height=self.width / 8,
            heading_row_height=self.width / 6,
            bgcolor="#f1f1f1",
            columns=[flet.DataColumn(flet.Text(
                value=self._day_of_week.get(i),
                text_align=flet.TextAlign.CENTER,
                width=(self.width - self.width * 0.08) / 7,
                weight=flet.FontWeight.W_300,
                size=self.width * 0.06
            )) for i in range(0, 7)],
            rows=[flet.DataRow(cells=[]) for i in range(0, 5)]
        )

        day_counter = 1
        day_bgcolor = "#f1f1f1"
        day_padding = 0
        day_color = "#000000"

        # Заполнение календаря
        for row_index, row in enumerate(custom_calendar.rows):
            for cell_index in range(0, 7):
                if day_counter == self._current_day:
                    #для выделения текущего дня в календаре
                    day_bgcolor = "#1695f6"
                    day_padding = custom_calendar.data_row_max_height * 0.09
                    # print(day_padding)
                    day_color = "#ffffff"
                if row_index == 0 and cell_index < self._first_day_in_month:
                    row.cells.append(flet.DataCell(content=flet.Text(value="")))
                elif self._last_day_in_month >= day_counter:

                    row.cells.append(flet.DataCell(
                        content=flet.Container(content=flet.Text(
                            value=str(day_counter),
                            text_align=flet.TextAlign.CENTER,
                            weight=flet.FontWeight.W_600,
                            color=day_color,
                            size=self.width * 0.06
                        ),
                            bgcolor=day_bgcolor,
                            padding=day_padding,
                            width=(self.width - self.width * 0.08) / 7,
                            shape=flet.BoxShape.CIRCLE
                        )),

                    )
                    # temp = (self.width - self.width * 0.08) / 7
                    # print(f"{temp}")
                    day_counter += 1
                    day_bgcolor = "#f1f1f1"
                    day_padding = 0
                    day_color = "#000000"
                else:
                    row.cells.append(flet.DataCell(content=flet.Text(value="")))

        return custom_calendar


def main_page(page: flet.Page):
    my_calendar = CustomCalendar(200)
    page.add(my_calendar)


if __name__ == "__main__":
    flet.app(target=main_page)
