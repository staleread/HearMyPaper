import asyncio
from typing import cast
from openapidocs.v3 import Info
from rodi import Container
from blacksheep import Application
from blacksheep.server.openapi.v3 import OpenAPIHandler
from blacksheep.server.authentication.jwt import JWTBearerAuthentication
from blacksheep_prometheus import use_prometheus_metrics
from essentials.secrets import Secret
from sqlalchemy.ext.asyncio import AsyncSession

from shared_kernel.storage import PostgresClient
from shared_kernel.storage.object import ObjectStorageClient
from shared_kernel.marshal import from_b64
from shared_kernel.events import RabbitMQClient
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
    GradeLabAttemptPort,
    UpdateProjectPort,
    GetProjectStudentsPort,
    AssignStudentToProjectPort,
    RemoveStudentFromProjectPort,
    CanStudentSubmitPort,
    RegisterAttemptPort,
    ViewSubmissionPort,
    GetProjectAttemptsPort,
    GetLabAttemptPort,
)
from education_core.use_cases import (
    GetUserProjectsUseCase,
    GetProjectUseCase,
    CreateProjectUseCase,
    GradeLabAttemptUseCase,
    UpdateProjectUseCase,
    GetProjectStudentsUseCase,
    AssignStudentToProjectUseCase,
    RemoveStudentFromProjectUseCase,
    CanStudentSubmitUseCase,
    RegisterAttemptUseCase,
    ViewSubmissionUseCase,
    GetProjectAttemptsUseCase,
    GetLabAttemptUseCase,
)
from education_core.ports.outgoing.project_repository import ProjectRepositoryPort
from education_core.ports.outgoing.project_student_repository import (
    ProjectStudentRepositoryPort,
)
from education_core.ports.outgoing.identity_service import IdentityServicePort
from education_core.ports.outgoing.attempt_repository import AttemptRepositoryPort
from education_core.ports.outgoing.download_url_provider import DownloadUrlProviderPort

from education_postgres import (
    PostgresProjectRepositoryAdapter,
    PostgresProjectStudentRepositoryAdapter,
    PostgresAttemptRepositoryAdapter,
)
from education_identity_bridge import IdentityServiceAdapter
from education_rabbitmq import RabbitMQEventConsumer

import submissions_api  # noqa: F401
from submissions_core.ports.incoming import (
    RequestUploadUrlPort,
    CommitSubmissionPort,
    GetSubmissionPort,
    ListProjectSubmissionsPort,
)
from submissions_core.use_cases import (
    RequestUploadUrlUseCase,
    CommitSubmissionUseCase,
    GetSubmissionUseCase,
    ListProjectSubmissionsUseCase,
)
from submissions_core.ports.outgoing import (
    SubmissionRepositoryPort,
    StoragePort,
    SubmissionEligibilityPort,
    EventPublisherPort as SubmissionsEventPublisherPort,
)
from submissions_postgres import PostgresSubmissionRepositoryAdapter
from submissions_storage import S3StorageAdapter
from submissions_education_bridge import (
    EducationServiceAdapter,
    DownloadUrlProviderAdapter,
)
from submissions_rabbitmq import (
    RabbitMQEventPublisherAdapter as SubmissionsRabbitMQEventPublisherAdapter,
)

import processing_api  # noqa: F401
from processing_core.ports.incoming.request_conversion import RequestConversionPort
from processing_core.ports.incoming.commit_conversion import CommitConversionPort
from processing_core.ports.incoming.update_conversion_status import (
    UpdateConversionStatusPort,
)
from processing_core.ports.incoming.get_my_conversions import GetMyConversionsPort
from processing_core.use_cases import (
    RequestConversionUseCase,
    CommitConversionUseCase,
    UpdateConversionStatusUseCase,
    GetMyConversionsUseCase,
)
from processing_core.ports.outgoing.resource_broker import ResourceBrokerPort
from processing_core.ports.outgoing.conversion_repository import (
    ConversionRepositoryPort,
)
from processing_core.ports.outgoing.file_storage import FileStoragePort
from processing_core.ports.outgoing.identity import (
    IdentityPort as ProcessingIdentityPort,
)
from processing_orchestrator_bridge.resource_broker import (
    OrchestratorResourceBrokerAdapter,
)
from processing_postgres.conversion_repository import (
    PostgresConversionRepositoryAdapter,
)
from processing_storage.s3_adapter import S3StorageAdapter as ProcessingS3StorageAdapter
from processing_identity_bridge import IdentityAdapter as ProcessingIdentityAdapter
from processing_rabbitmq import ProcessingStatusConsumer

from orchestrator_core.ports.incoming.acquire_worker import AcquireWorkerPort
from orchestrator_core.ports.incoming.dispatch_task import DispatchTaskPort
from orchestrator_core.ports.incoming.register_worker import RegisterWorkerPort
from orchestrator_core.ports.incoming.heartbeat import HeartbeatPort
from orchestrator_core.ports.incoming.update_task_status import UpdateTaskStatusPort
from orchestrator_core.use_cases import (
    AcquireWorkerUseCase,
    RegisterWorkerUseCase,
    HeartbeatUseCase,
    DispatchTaskUseCase,
    UpdateTaskStatusUseCase,
)
from orchestrator_core.ports.outgoing.worker_registry import WorkerRegistryPort
from orchestrator_core.ports.outgoing.task_repository import TaskRepositoryPort
from orchestrator_core.ports.outgoing.event_publisher import (
    EventPublisherPort as OrchestratorEventPublisherPort,
)
from orchestrator_redis import RedisWorkerRegistryAdapter, RedisTaskRepositoryAdapter
from orchestrator_rabbitmq import (
    RabbitMQEventPublisherAdapter as OrchestratorRabbitMQEventPublisherAdapter,
    TaskStatusConsumer,
)
import orchestrator_api  # noqa: F401

from utils import use_postgres, use_redis


app = Application()

settings = get_settings()

docs = OpenAPIHandler(info=Info(title="HearMyPaper Leader", version="0.0.1"))
docs.bind_app(app)

use_prometheus_metrics(app)
use_postgres(app, settings.postgres.url)
use_redis(app, settings.redis.url)

app.use_authentication().add(
    JWTBearerAuthentication(
        secret_key=Secret(settings.jwt.secret, direct_value=True),
        algorithms=[settings.jwt.algorithm],
        valid_audiences=[settings.jwt.audience],
        valid_issuers=[settings.jwt.issuer],
    )
)
app.use_authorization()

jwt_provider = JwtTokenProviderAdapter(
    secret=settings.jwt.secret,
    lifetime_sec=settings.jwt.lifetime_sec,
    audience=settings.jwt.audience,
    issuer=settings.jwt.issuer,
    algorithm=settings.jwt.algorithm,
)


storage_client = ObjectStorageClient(
    endpoint_url=settings.minio.url,
    access_key=settings.minio.access_key,
    secret_key=settings.minio.secret_key,
)

(
    cast(Container, app.services)
    .add_instance(RabbitMQClient(settings.rabbitmq.url), RabbitMQClient)
    .add_instance(storage_client, ObjectStorageClient)
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
    .add_scoped(AttemptRepositoryPort, PostgresAttemptRepositoryAdapter)
    .add_scoped(DownloadUrlProviderPort, DownloadUrlProviderAdapter)
    # Education use cases
    .add_scoped(GetUserProjectsPort, GetUserProjectsUseCase)
    .add_scoped(GetProjectPort, GetProjectUseCase)
    .add_scoped(CreateProjectPort, CreateProjectUseCase)
    .add_scoped(UpdateProjectPort, UpdateProjectUseCase)
    .add_scoped(GetProjectStudentsPort, GetProjectStudentsUseCase)
    .add_scoped(AssignStudentToProjectPort, AssignStudentToProjectUseCase)
    .add_scoped(RemoveStudentFromProjectPort, RemoveStudentFromProjectUseCase)
    .add_scoped(CanStudentSubmitPort, CanStudentSubmitUseCase)
    .add_scoped(RegisterAttemptPort, RegisterAttemptUseCase)
    .add_scoped(ViewSubmissionPort, ViewSubmissionUseCase)
    .add_scoped(GetProjectAttemptsPort, GetProjectAttemptsUseCase)
    .add_scoped(GetLabAttemptPort, GetLabAttemptUseCase)
    .add_scoped(GradeLabAttemptPort, GradeLabAttemptUseCase)
    # Outgoing submissions adapters
    .add_instance(
        S3StorageAdapter(storage_client, bucket="submissions"),
        StoragePort,
    )
    .add_scoped(SubmissionRepositoryPort, PostgresSubmissionRepositoryAdapter)
    .add_scoped(SubmissionEligibilityPort, EducationServiceAdapter)
    .add_scoped(SubmissionsEventPublisherPort, SubmissionsRabbitMQEventPublisherAdapter)
    # Submissions use cases
    .add_scoped(RequestUploadUrlPort, RequestUploadUrlUseCase)
    .add_scoped(CommitSubmissionPort, CommitSubmissionUseCase)
    .add_scoped(GetSubmissionPort, GetSubmissionUseCase)
    .add_scoped(ListProjectSubmissionsPort, ListProjectSubmissionsUseCase)
    # Orchestrator
    .add_scoped(WorkerRegistryPort, RedisWorkerRegistryAdapter)
    .add_scoped(TaskRepositoryPort, RedisTaskRepositoryAdapter)
    .add_scoped(
        OrchestratorEventPublisherPort, OrchestratorRabbitMQEventPublisherAdapter
    )
    .add_scoped(AcquireWorkerPort, AcquireWorkerUseCase)
    .add_scoped(RegisterWorkerPort, RegisterWorkerUseCase)
    .add_scoped(HeartbeatPort, HeartbeatUseCase)
    .add_scoped(DispatchTaskPort, DispatchTaskUseCase)
    .add_scoped(UpdateTaskStatusPort, UpdateTaskStatusUseCase)
    # Processing
    .add_scoped(ConversionRepositoryPort, PostgresConversionRepositoryAdapter)
    .add_instance(
        ProcessingS3StorageAdapter(storage_client, bucket="conversions"),
        FileStoragePort,
    )
    .add_scoped(ResourceBrokerPort, OrchestratorResourceBrokerAdapter)
    .add_scoped(ProcessingIdentityPort, ProcessingIdentityAdapter)
    .add_scoped(RequestConversionPort, RequestConversionUseCase)
    .add_scoped(CommitConversionPort, CommitConversionUseCase)
    .add_scoped(UpdateConversionStatusPort, UpdateConversionStatusUseCase)
    .add_scoped(GetMyConversionsPort, GetMyConversionsUseCase)
)


@app.lifespan
async def initialize(app: Application):
    services = cast(Container, app.services)
    postgres_client = services.provider.get(PostgresClient)
    rabbitmq_client = services.provider.get(RabbitMQClient)
    storage_manager = services.provider.get(ObjectStorageClient)

    # Ensure buckets exist
    async for s3_client in storage_manager.get_client():
        try:
            await s3_client.head_bucket(Bucket="submissions")
        except Exception:
            await s3_client.create_bucket(Bucket="submissions")

        try:
            await s3_client.head_bucket(Bucket="conversions")
        except Exception:
            await s3_client.create_bucket(Bucket="conversions")

    # Start RabbitMQ Consumers
    consumer = RabbitMQEventConsumer(rabbitmq_client, services, postgres_client)
    consumer_task = asyncio.create_task(consumer.start_consuming())

    status_consumer = TaskStatusConsumer(rabbitmq_client, services)
    status_consumer_task = asyncio.create_task(status_consumer.start_consuming())

    processing_status_consumer = ProcessingStatusConsumer(
        rabbitmq_client, services, postgres_client
    )
    processing_status_consumer_task = asyncio.create_task(
        processing_status_consumer.start_listening()
    )

    with services.provider.create_scope() as scope:
        async with postgres_client.transactional_session() as session:
            # Seed the session into the lifespan's scope
            scope.scoped_services[AsyncSession] = session

            create_initial_user = scope.get(CreateInitialUserPort)

            user_id = settings.init_user.id

            cmd = InitialUserCreateCommand(
                user_id=user_id,
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

    # Cleanup
    consumer_task.cancel()
    status_consumer_task.cancel()
    processing_status_consumer_task.cancel()
    try:
        await asyncio.gather(
            consumer_task,
            status_consumer_task,
            processing_status_consumer_task,
            return_exceptions=True,
        )
    except asyncio.CancelledError:
        pass
    await rabbitmq_client.close()
