from aiohttp.web_exceptions import HTTPForbidden, HTTPUnauthorized
from aiohttp.web_response import StreamResponse


class SuperuserRequiredMixin:
    def _iter(self) -> StreamResponse:
        if not getattr(self.request, "superuser", None):
            raise HTTPForbidden
        return super(SuperuserRequiredMixin, self)._iter()

