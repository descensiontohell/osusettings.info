from aiohttp.web_exceptions import HTTPForbidden
from aiohttp.web_response import StreamResponse


class SuperuserRequiredMixin:
    def _iter(self) -> StreamResponse:
        if not getattr(self.request, "is_superuser", None):
            raise HTTPForbidden
        return super(SuperuserRequiredMixin, self)._iter()
