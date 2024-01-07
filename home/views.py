import asyncio
import datetime
from django.http import HttpRequest, StreamingHttpResponse
from django.views.generic import TemplateView
import pytz

NUMBER_EVENTS = 3


class HomeView(TemplateView):
    template_name = "home/index.html"


def createEvent(payload: str) -> bytes:
    return f"data: {payload}\n\n".encode()


async def event_stream(_request: HttpRequest):
    for i in range(NUMBER_EVENTS):
        await asyncio.sleep(0.5)
        timestamp = datetime.datetime.now(pytz.timezone("America/Los_Angeles"))
        payload = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        yield createEvent(payload=payload)

    # CLOSE event is not in SSE specification
    # this is just a convention that can be used to terminate a SSE stream
    yield createEvent("CLOSE")


async def stream(request: HttpRequest) -> StreamingHttpResponse:
    return StreamingHttpResponse(
        event_stream(request), content_type="text/event-stream"
    )
