import json
import pretty_errors
import asyncio
from anzen.v1 import commands_pb2, events_pb2, plugins_pb2
from anzen.v1.data_pb2 import ARM_STATUS_ARMED
from copy import deepcopy
from client import Client
from pritiorty_queue import Queue
from security_email import EmailClient


class Main:
    """
    Main running code to listen to commands and events
    Distributes via email
    """
    def __init__(self) -> None:
        self.client = Client("[::1]", 50_000, "security", "12345", plugins_pb2.PLUGIN_TYPE_OUTPUT)
        self.opts = self.client.get_opts()

        sender_email = self.opts["email"]["sender_email"]
        sender_pwd = self.opts["email"]["sender_pwd"]
        sender_name = self.opts["email"]["sender_name"]
        email_server = self.opts["email"]["server_ip"]
        email_port = self.opts["email"]["port"]

        target_emails = self.opts["send_mail"]

        self.emails: Queue[str] = Queue()
        
        for email in target_emails:
            priority = email["priority"] 
            address = email["address"] 
            self.emails.insert(address, priority)

        self.emailClient = EmailClient(sender_email, email_server, email_port)
        self.emailClient.login(sender_name, sender_pwd)

    async def handle_all(self):
        pass

    async def handle_event(self, event: events_pb2.Event):
        if event.arm_status != ARM_STATUS_ARMED:
            return

        await asyncio.sleep(120)
        
        data = await self.client.info()
        
        if data.armed:
            await self.dispatch_emails(event)

    async def handle_command(self, command: commands_pb2.Command):
        if command.command_type != commands_pb2.COMMAND_TYPE_INFO:
            return

        data = json.loads(command.data)
        
        command_type = data.get("request")
        priority = data.get("priority")
        email = data.get("email")

        if not command_type or not priority or not email:
            print(f"{data} does not contain required data")
            return

        await self.add_email(email, priority)

    async def add_email(self, email: str, priority: int):
        self.emails.insert(email, priority)

    async def dispatch_emails(self, event: events_pb2.Event):
        queue_copy = deepcopy(self.emails)

        message = f"""
        The security system has been triggered whilst armed.

        Device:     {event.device_id}
        Plugin:     {event.origin}
        Data:       {event.data}
        Extra data: {event.extra_data}
        """
        
        while (email := queue_copy.remove()) != None:
            self.emailClient.send_email([email], "Triggered security event", message)


if __name__ == "__main__":
    # asyncio.run(main(client))
    pass
