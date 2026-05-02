import toga
from datetime import datetime
from toga.style import Pack
from toga.style.pack import ROW, COLUMN


class DateTimePicker:
    def __init__(self, initial_value: datetime | None = None):
        self.initial_dt = initial_value or datetime.now()

        self.hour_input = toga.NumberInput(
            min=0, max=23, value=self.initial_dt.hour, style=Pack(width=60)
        )
        self.minute_input = toga.NumberInput(
            min=0, max=59, value=self.initial_dt.minute, style=Pack(width=60)
        )

        self.year_input = toga.NumberInput(
            min=2000, max=2100, value=self.initial_dt.year, style=Pack(width=80)
        )

        months = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
        self.month_selector = toga.Selection(items=months)
        self.month_selector.value = months[self.initial_dt.month - 1]

        self.day_input = toga.NumberInput(
            min=1, max=31, value=self.initial_dt.day, style=Pack(width=60)
        )

        # Time section with vertical layout
        hour_row = toga.Box(
            children=[
                toga.Label("Hour:", style=Pack(width=50, text_align="left")),
                self.hour_input,
            ],
            style=Pack(direction=ROW, margin_bottom=5),
        )

        minute_row = toga.Box(
            children=[
                toga.Label("Min:", style=Pack(width=50, text_align="left")),
                self.minute_input,
            ],
            style=Pack(direction=ROW, margin_bottom=5),
        )

        time_box = toga.Box(
            children=[
                toga.Label("Time:", style=Pack(font_weight="bold", margin_bottom=8)),
                hour_row,
                minute_row,
            ],
            style=Pack(direction=COLUMN, margin_right=30),
        )

        # Date section with vertical layout
        year_row = toga.Box(
            children=[
                toga.Label("Year:", style=Pack(width=60, text_align="left")),
                self.year_input,
            ],
            style=Pack(direction=ROW, margin_bottom=5),
        )

        month_row = toga.Box(
            children=[
                toga.Label("Month:", style=Pack(width=60, text_align="left")),
                self.month_selector,
            ],
            style=Pack(direction=ROW, margin_bottom=5),
        )

        day_row = toga.Box(
            children=[
                toga.Label("Day:", style=Pack(width=60, text_align="left")),
                self.day_input,
            ],
            style=Pack(direction=ROW, margin_bottom=5),
        )

        date_box = toga.Box(
            children=[
                toga.Label("Date:", style=Pack(font_weight="bold", margin_bottom=8)),
                year_row,
                month_row,
                day_row,
            ],
            style=Pack(direction=COLUMN),
        )

        self.widget = toga.Box(
            children=[time_box, date_box],
            style=Pack(direction=ROW, margin=10, gap=30, align_items="start"),
        )

    @property
    def value(self):
        try:
            month_index = [
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December",
            ].index(self.month_selector.value) + 1

            return datetime(
                year=int(self.year_input.value),
                month=month_index,
                day=int(self.day_input.value),
                hour=int(self.hour_input.value),
                minute=int(self.minute_input.value),
            )
        except (ValueError, TypeError):
            return self.initial_dt

    def set_value(self, dt):
        if dt is None:
            dt = datetime.now()

        self.hour_input.value = dt.hour
        self.minute_input.value = dt.minute
        self.year_input.value = dt.year

        months = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
        self.month_selector.value = months[dt.month - 1]
        self.day_input.value = dt.day
