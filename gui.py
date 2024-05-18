import flet
from flet import TextField, ElevatedButton, Column, Page, Text, icons, IconButton, Row
from src.pastebin_poster import PastebinPoster


def post_to_pastebin(page, content, title, result_text):
    poster = PastebinPoster()
    response = poster.post_to_pastebin(content, title)
    result_text.value = response
    page.update()


def switch_theme(page, theme_button):
    new_theme = "light" if page.theme_mode == "dark" else "dark"
    page.theme_mode = new_theme
    theme_button.icon = icons.DARK_MODE if new_theme == "light" else icons.LIGHT_MODE
    page.update()


def main(page):
    page.title = "Pastebin Poster | by xdearboy"
    page.auto_size = True

    theme_button = IconButton(
        icon=icons.LIGHT_MODE,
        on_click=lambda e: switch_theme(page, theme_button),
        tooltip="Change theme",
    )
    header_row = Row(
        controls=[Text(value="Pastebin Poster", size=20), theme_button],
        alignment="spaceBetween",
    )

    title_field = TextField(label="Write the title of the paste", width=400)
    content_field = TextField(label="Write the content of the paste", multiline=True, expand=True)
    result_text = Text()

    def post_click(event):
        post_to_pastebin(page, content_field.value, title_field.value, result_text)

    submit_button = ElevatedButton(text="Post to Pastebin", on_click=post_click)

    main_column = Column(
        controls=[header_row, title_field, content_field, submit_button, result_text],
        expand=True,
        spacing=10,
    )

    page.add(main_column)


if __name__ == "__main__":
    flet.app(target=main)