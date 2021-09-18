from ninja import NinjaAPI

from ralph.clients.authorization.router import router as authentication_router
from ralph.clients.check.router import router as check_router
from ralph.clients.registration.router import router as registration_router

from ralph.common.exception_handlers import add_exception_handlers

api = NinjaAPI()

# Add routes.
api.add_router("", authentication_router)
api.add_router("", check_router)
api.add_router("", registration_router)

# Add exception handlers.
add_exception_handlers(api)
