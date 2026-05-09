from typing import cast
from openapidocs.v3 import Info
from rodi import Container
from blacksheep import Application
from blacksheep.server.openapi.v3 import OpenAPIHandler
from blacksheep_prometheus import use_prometheus_metrics
from sqlalchemy.ext.asyncio import AsyncSession

from shared_kernel.storage import PostgresClient
from shared_kernel.marshal import from_b64
from config import get_settings


import identity_api  # noqa: F401
from identity_core.ports.incoming import (
    CreateUserPort,
    GetUserPort,
    GetUserPublicKeyPort,
    UpdateUserPort,
    InitLoginPort,
    FinalizeLoginPort,
    CreateInitialUserPort,
    InitialUserCreateCommand,
)
from identity_core.use_cases import (
    CreateUserUseCase,
    GetUserUseCase,
    GetUserPublicKeyUseCase,
    UpdateUserUseCase,
    InitLoginUseCase,
    FinalizeLoginUseCase,
    CreateInitialUserUseCase,
)
from identity_core.ports.outgoing.user_repository import UserRepositoryPort
from identity_core.ports.outgoing.auth_repository import AuthRepositoryPort
from identity_core.ports.outgoing.challenge_repository import ChallengeRepositoryPort
from identity_core.ports.outgoing.token_provider import TokenProviderPort
from identity_core.ports.outgoing.identity_provider import IdentityProviderPort
from identity_core.ports.outgoing.challenge_generator import ChallengeGeneratorPort
from identity_core.ports.outgoing.signature_verifier import SignatureVerifierPort

from identity_postgres import (
    PostgresUserRepositoryAdapter,
    PostgresAuthRepositoryAdapter,
)
from identity_redis import RedisChallengeRepositoryAdapter
from identity_jwt import JwtTokenProviderAdapter
from identity_id import PseudonymIdentityProviderAdapter
from identity_ch_gen import NativeChallengeGeneratorAdapter
from identity_signture import SignatureVerifierAdapter

import education_api  # noqa: F401
from education_core.ports.incoming import (
    GetUserProjectsPort,
    GetProjectPort,
    CreateProjectPort,
    UpdateProjectPort,
    GetProjectStudentsPort,
    AssignStudentToProjectPort,
    RemoveStudentFromProjectPort,
)
from education_core.use_cases import (
    GetUserProjectsUseCase,
    GetProjectUseCase,
    CreateProjectUseCase,
    UpdateProjectUseCase,
    GetProjectStudentsUseCase,
    AssignStudentToProjectUseCase,
    RemoveStudentFromProjectUseCase,
)
from education_core.ports.outgoing.project_repository import ProjectRepositoryPort
from education_core.ports.outgoing.project_student_repository import (
    ProjectStudentRepositoryPort,
)
from education_core.ports.outgoing.identity_service import IdentityServicePort

from education_postgres import (
    PostgresProjectRepositoryAdapter,
    PostgresProjectStudentRepositoryAdapter,
)
from education_identity_bridge import IdentityServiceAdapter

from utils import use_postgres, use_redis


app = Application()

settings = get_settings()

docs = OpenAPIHandler(info=Info(title="HearMyPaper Leader", version="0.0.1"))
docs.bind_app(app)

use_prometheus_metrics(app)
use_postgres(app, settings.postgres.url)
use_redis(app, settings.redis.url)

jwt_provider = JwtTokenProviderAdapter(
    secret=settings.jwt.secret,
    lifetime_sec=settings.jwt.lifetime_sec,
    algorithm=settings.jwt.algorithm,
)


(
    cast(Container, app.services)
    # Outgoing identity adapters
    .add_instance(jwt_provider, TokenProviderPort)
    .add_singleton(IdentityProviderPort, PseudonymIdentityProviderAdapter)
    .add_singleton(ChallengeGeneratorPort, NativeChallengeGeneratorAdapter)
    .add_singleton(SignatureVerifierPort, SignatureVerifierAdapter)
    .add_scoped(ChallengeRepositoryPort, RedisChallengeRepositoryAdapter)
    .add_scoped(UserRepositoryPort, PostgresUserRepositoryAdapter)
    .add_scoped(AuthRepositoryPort, PostgresAuthRepositoryAdapter)
    # Identity use cases
    .add_scoped(CreateUserPort, CreateUserUseCase)
    .add_scoped(GetUserPort, GetUserUseCase)
    .add_scoped(GetUserPublicKeyPort, GetUserPublicKeyUseCase)
    .add_scoped(UpdateUserPort, UpdateUserUseCase)
    .add_scoped(InitLoginPort, InitLoginUseCase)
    .add_scoped(FinalizeLoginPort, FinalizeLoginUseCase)
    .add_scoped(CreateInitialUserPort, CreateInitialUserUseCase)
    # Outgoing education adapters
    .add_scoped(ProjectRepositoryPort, PostgresProjectRepositoryAdapter)
    .add_scoped(ProjectStudentRepositoryPort, PostgresProjectStudentRepositoryAdapter)
    .add_scoped(IdentityServicePort, IdentityServiceAdapter)
    # Education use cases
    .add_scoped(GetUserProjectsPort, GetUserProjectsUseCase)
    .add_scoped(GetProjectPort, GetProjectUseCase)
    .add_scoped(CreateProjectPort, CreateProjectUseCase)
    .add_scoped(UpdateProjectPort, UpdateProjectUseCase)
    .add_scoped(GetProjectStudentsPort, GetProjectStudentsUseCase)
    .add_scoped(AssignStudentToProjectPort, AssignStudentToProjectUseCase)
    .add_scoped(RemoveStudentFromProjectPort, RemoveStudentFromProjectUseCase)
)


@app.lifespan
async def initialize(app: Application):
    services = cast(Container, app.services).provider
    postgres_client = services.get(PostgresClient)

    with services.create_scope() as scope:
        async with postgres_client.transactional_session() as session:
            # Seed the session into the lifespan's scope
            scope.scoped_services[AsyncSession] = session

            create_initial_user = scope.get(CreateInitialUserPort)

            user_id = settings.init_user.id

            cmd = InitialUserCreateCommand(
                id=user_id,
                name=settings.init_user.name,
                surname=settings.init_user.surname,
                email=settings.init_user.email,
                public_key=from_b64(settings.init_user.public_key_b64),
            )

            try:
                created = await create_initial_user(cmd)
                if created:
                    print(f"[INFO] Initial user with ID {user_id} created")
            except Exception as e:
                print(f"[ERROR] Failed to create initial user: {e}")

    yield
