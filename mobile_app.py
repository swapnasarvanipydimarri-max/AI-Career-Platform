import flet as ft


LIVE_APP_URL = "https://ai-career-platform-sarvani.streamlit.app/"


def main(page: ft.Page):
    page.title = "AI Career Intelligence"
    page.padding = 30

    title = ft.Text(
        "🤖 AI Career Intelligence",
        size=24,
    )

    description = ft.Text(
        "AI-powered career guidance, resume analysis, "
        "skill-gap detection, and interview preparation."
    )

    async def open_app(e):
        launcher = ft.UrlLauncher()
        await launcher.launch_url(
            LIVE_APP_URL,
            mode=ft.LaunchMode.IN_APP_WEB_VIEW,
        )

    open_button = ft.Button(
        "Open AI Career Platform",
        on_click=open_app,
    )

    page.add(
        title,
        ft.Divider(),
        description,
        open_button,
    )


ft.run(main)