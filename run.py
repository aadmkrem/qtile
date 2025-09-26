#!/usr/bin/env python3
import asyncio
import websockets
import json
import requests
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Input, Button, Static, RichLog
from textual.screen import Screen, ModalScreen
from textual.reactive import reactive


class LoginScreen(ModalScreen):
    """Экран входа/регистрации"""

    def compose(self) -> ComposeResult:
        yield Container(
            Static("🔐 Sea Messenger", classes="header"),
            Input(placeholder="Логин", id="username"),
            Input(placeholder="Пароль", password=True, id="password"),
            Horizontal(
                Button("Войти", id="login", variant="primary"),
                Button("Регистрация", id="register"),
            ),
            Static(id="status", classes="status"),
            classes="dialog"
        )

    @on(Button.Pressed, "#login")
    def on_login(self) -> None:
        """Обработка входа"""
        asyncio.create_task(self.do_login())

    @on(Button.Pressed, "#register")
    def on_register(self) -> None:
        """Обработка регистрации"""
        asyncio.create_task(self.do_register())

    async def do_login(self):
        """Выполняем вход"""
        username = self.query_one("#username").value
        password = self.query_one("#password").value

        if not username or not password:
            self.query_one("#status").update("❌ Заполните все поля")
            return

        try:
            response = requests.post(
                "https://sea.dash756.ru/api/login",
                json={"username": username, "password": password}
            )

            if response.status_code == 200:
                self.app.current_user = username
                self.app.logged_in = True
                self.dismiss()
                await self.app.connect_websocket()
            else:
                self.query_one("#status").update("❌ Ошибка входа")

        except Exception as e:
            self.query_one("#status").update(f"❌ Ошибка: {e}")

    async def do_register(self):
        """Выполняем регистрацию"""
        username = self.query_one("#username").value
        password = self.query_one("#password").value

        if not username or not password:
            self.query_one("#status").update("❌ Заполните все поля")
            return

        try:
            response = requests.post(
                "https://sea.dash756.ru/api/register",
                json={"username": username, "password": password}
            )

            if response.status_code == 200:
                self.query_one("#status").update("✅ Регистрация успешна! Теперь войдите.")
            else:
                self.query_one("#status").update("❌ Ошибка регистрации")

        except Exception as e:
            self.query_one("#status").update(f"❌ Ошибка: {e}")


class MessengerClient(App):
    """Консольный мессенджер для Sea Messenger"""

    CSS = """
    Screen {
        layout: horizontal;
    }

    #sidebar {
        width: 30%;
        border: solid $accent;
        background: $surface;
    }

    #chat-area {
        width: 70%;
        border: solid $accent;
    }

    #messages {
        height: 80%;
        border: solid $panel;
    }

    #input-area {
        height: 20%;
        border: solid $panel;
    }

    .message {
        margin: 1;
        padding: 1;
    }
    """

    BINDINGS = [
        ("ctrl+q", "quit", "Quit"),
        ("ctrl+r", "refresh", "Refresh"),
    ]

    def __init__(self):
        super().__init__()
        self.websocket = None
        self.base_url = "https://sea.dash756.ru/api"
        self.ws_url = "wss://sea.dash756.ru/ws"
        self.current_user = ""
        self.logged_in = False
        self.messages = []

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Vertical(
                Static("💬 Sea Messenger", id="app-title"),
                Static(f"Пользователь: {self.current_user}", id="user-info"),
                Button("Обновить", id="refresh"),
                Button("Выйти", id="logout"),
                id="sidebar"
            ),
            Vertical(
                RichLog(id="messages", wrap=True, markup=True),
                Horizontal(
                    Input(placeholder="Введите сообщение...", id="message-input"),
                    Button("Отправить", id="send-btn"),
                ),
                id="chat-area"
            ),
        )
        yield Footer()

    async def on_mount(self) -> None:
        """Запускаем при загрузке"""
        if not self.logged_in:
            await self.show_login_screen()

    async def show_login_screen(self):
        """Показываем экран логина"""
        await self.push_screen(LoginScreen())

    async def connect_websocket(self):
        """Подключаемся к WebSocket серверу"""
        try:
            self.websocket = await websockets.connect(self.ws_url)
            asyncio.create_task(self.listen_messages())
            self.notify("✅ Подключено к серверу", severity="information")

            # Обновляем интерфейс
            self.query_one("#user-info").update(f"Пользователь: {self.current_user}")

        except Exception as e:
            self.notify(f"❌ Ошибка подключения: {e}", severity="error")

    async def listen_messages(self):
        """Слушаем входящие сообщения"""
        try:
            async for message in self.websocket:
                data = json.loads(message)
                await self.handle_message(data)
        except Exception as e:
            self.notify(f"❌ Ошибка WebSocket: {e}", severity="error")

    async def handle_message(self, data):
        """Обрабатываем входящие сообщения"""
        msg_type = data.get("type")

        if msg_type == "message":
            # Добавляем сообщение в лог
            messages_widget = self.query_one("#messages")
            sender = data.get("sender", "Unknown")
            text = data.get("text", "")
            messages_widget.write(f"[bold]{sender}:[/bold] {text}")

        elif msg_type == "echo":
            self.notify(f"Эхо: {data.get('text', '')}")

    async def action_send_message(self, text: str):
        """Отправляем сообщение"""
        if not text.strip():
            return

        message_data = {
            "type": "message",
            "text": text,
            "sender": self.current_user,
            "timestamp": str(asyncio.get_event_loop().time())
        }

        if self.websocket:
            await self.websocket.send(json.dumps(message_data))

        # Добавляем в лог
        messages_widget = self.query_one("#messages")
        messages_widget.write(f"[bold blue]Вы:[/bold blue] {text}")

        # Очищаем поле ввода
        input_widget = self.query_one("#message-input")
        input_widget.value = ""

    @on(Input.Submitted, "#message-input")
    def on_message_submitted(self, event: Input.Submitted) -> None:
        """Обработка отправки сообщения по Enter"""
        asyncio.create_task(self.action_send_message(event.value))

    @on(Button.Pressed, "#send-btn")
    def on_send_button(self, event: Button.Pressed) -> None:
        """Обработка кнопки отправки"""
        input_widget = self.query_one("#message-input")
        asyncio.create_task(self.action_send_message(input_widget.value))

    @on(Button.Pressed, "#refresh")
    def on_refresh(self, event: Button.Pressed) -> None:
        """Обновление интерфейса"""
        self.query_one("#messages").clear()
        self.query_one("#messages").write("💬 Чат обновлен")
        self.notify("Чат обновлен")

    @on(Button.Pressed, "#logout")
    def on_logout(self, event: Button.Pressed) -> None:
        """Выход из системы"""
        self.logged_in = False
        self.current_user = ""
        if self.websocket:
            asyncio.create_task(self.websocket.close())
        asyncio.create_task(self.show_login_screen())


if __name__ == "__main__":
    app = MessengerClient()
    app.run()