"""The build's relational tables. PostgreSQL remains the durable source for graph walks."""

from sqlalchemy import JSON, Column, Date, ForeignKey, MetaData, Table, Text
from sqlalchemy.dialects.postgresql import TSVECTOR
from pgvector.sqlalchemy import Vector

EMBEDDING_MODEL = "openai/text-embedding-3-small"
VECTOR_SIZE = 1536
metadata = MetaData()

people = Table("people", metadata,
    Column("person_id", Text, primary_key=True), Column("username", Text, nullable=False, unique=True),
    Column("display_name", Text, nullable=False), Column("department", Text, nullable=False),
    Column("country", Text, nullable=False))
groups = Table("groups", metadata,
    Column("group_id", Text, primary_key=True), Column("name", Text, nullable=False),
    Column("kind", Text, nullable=False))
assets = Table("assets", metadata,
    Column("asset_id", Text, primary_key=True), Column("name", Text, nullable=False),
    Column("sensitivity", Text, nullable=False),
    Column("owner_id", Text, ForeignKey("people.person_id"), nullable=False))
devices = Table("devices", metadata,
    Column("device_id", Text, primary_key=True), Column("kind", Text, nullable=False),
    Column("name", Text, nullable=False))
networks = Table("networks", metadata,
    Column("network_id", Text, primary_key=True), Column("address", Text, nullable=False),
    Column("kind", Text, nullable=False), Column("name", Text, nullable=False),
    Column("person_id", Text, ForeignKey("people.person_id")))
memberships = Table("memberships", metadata,
    Column("membership_id", Text, primary_key=True),
    Column("group_id", Text, ForeignKey("groups.group_id"), nullable=False),
    Column("person_id", Text, ForeignKey("people.person_id"), nullable=False))
grants = Table("grants", metadata,
    Column("grant_id", Text, primary_key=True),
    Column("group_id", Text, ForeignKey("groups.group_id"), nullable=False),
    Column("asset_id", Text, ForeignKey("assets.asset_id"), nullable=False))
device_assignments = Table("device_assignments", metadata,
    Column("assignment_id", Text, primary_key=True),
    Column("device_id", Text, ForeignKey("devices.device_id"), nullable=False),
    Column("person_id", Text, ForeignKey("people.person_id"), nullable=False))
ORG_TABLES = {table.name: table for table in
              (people, groups, assets, devices, networks, memberships, grants, device_assignments)}

# PGEngine creates this table. This declaration supplies typed Core queries and foreign keys.
chunks = Table("chunks", metadata,
    Column("chunk_id", Text, primary_key=True), Column("content", Text, nullable=False),
    Column("embedding", Vector(VECTOR_SIZE), nullable=False), Column("content_tsv", TSVECTOR),
    Column("document_type", Text), Column("technique_id", Text), Column("incident_id", Text),
    Column("version", Text), Column("effective_date", Date), Column("langchain_metadata", JSON))
FILTER_COLUMNS = ["document_type", "technique_id", "incident_id", "version", "effective_date"]

mentions = Table("chunk_mentions_entity", metadata,
    Column("chunk_id", Text, ForeignKey("chunks.chunk_id"), primary_key=True),
    Column("entity_type", Text, primary_key=True), Column("entity_id", Text, primary_key=True))

# One row: the fingerprint of the world this database was built from (staleness guard, T18).
build_record = Table("build_record", metadata, Column("fingerprint", Text, primary_key=True))
