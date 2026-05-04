from hmp_core.storage import SqlRunner


def get_user_id_by_pseudonym(pseudonym: str, *, db: SqlRunner) -> int | None:
    return (
        db.query("""
        SELECT id FROM users WHERE pseudonym = :pseudonym
    """)
        .bind(pseudonym=pseudonym)
        .scalar(lambda x: x)
    )


def get_public_key_by_pseudonym(pseudonym: str, *, db: SqlRunner) -> bytes | None:
    return (
        db.query("""
        SELECT public_key FROM users WHERE pseudonym = :pseudonym
    """)
        .bind(pseudonym=pseudonym)
        .scalar(lambda x: x)
    )
