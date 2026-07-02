from bot import Bot


def init_events(client: Bot):
    @client.event
    async def on_ready():
        print(f"Logged in as {client.user} | {client.user.id}")
