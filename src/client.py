from collections.abc import AsyncIterable
import grpc
import anzen.v1.anzen_pb2_grpc as anzen_pb2_grpc
from anzen.v1 import events_pb2, security_pb2, commands_pb2, plugins_pb2
import tomli

class Client:
    def __init__(self,
                 ip: str,
                 port: int,
                 plugin_name: str,
                 login_key: str,
                 plugin_type: plugins_pb2.PluginType
                 ):
        self.channel = grpc.insecure_channel(f"{ip}:{port}")
        self.stub = anzen_pb2_grpc.AnzenServiceStub(self.channel)

        token = security_pb2.SecurityToken(origin=plugin_name, key=login_key)
        register = commands_pb2.RegisterRequest(token=token, plugin_type=plugin_type)

        response = self.stub.Register(register)

        self._token = response.token.key
        self._name = response.token.origin

        self._metadata = (
            ("p-name", self._name),
            ("authorization", f"Bearer {self._token}")
        )

        self.opts = tomli.loads(response.plugin_opts)

    def get_opts(self):
        return self.opts

    async def event_stream(self) -> AsyncIterable[events_pb2.EventResponse]:
        event_request = events_pb2.EventRequest()

        response = self.stub.Event(request=event_request, metadata=self._metadata)

        for event in response:
            yield event

    async def command_stream(self) -> AsyncIterable[commands_pb2.CommandResponse] :
        command_request = commands_pb2.CommandRequest()

        response = self.stub.Command(request=command_request, metadata=self._metadata)

        for command in response:
            yield command

    async def info(self) -> commands_pb2.InfoResponse:
        info_request = commands_pb2.InfoRequest()

        response = self.stub.Info(request=info_request, metadata=self._metadata)

        return response
