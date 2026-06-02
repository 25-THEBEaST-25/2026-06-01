from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.entities import Alert, Asset, Organization, ReportRecord, Scan
from app.schemas.security import ScanResponse


class OrganizationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_name(self, name: str) -> Organization | None:
        result = await self.session.execute(select(Organization).where(Organization.name == name))
        return result.scalar_one_or_none()


class AssetRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_for_org(self, organization_id: str) -> list[Asset]:
        result = await self.session.execute(select(Asset).where(Asset.organization_id == organization_id))
        return list(result.scalars())


class ScanRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save_scan(self, asset_id: str, scan: ScanResponse) -> Scan:
        record = Scan(
            asset_id=asset_id,
            score=scan.risk_score,
            findings=[finding.model_dump(mode="json") for finding in scan.findings],
            recommendations=[
                recommendation.model_dump(mode="json") for recommendation in scan.recommendations
            ],
        )
        self.session.add(record)
        await self.session.flush()
        return record


class AlertRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_open_for_org(self, organization_id: str) -> list[Alert]:
        result = await self.session.execute(
            select(Alert).join(Asset).where(Asset.organization_id == organization_id, Alert.status == "open")
        )
        return list(result.scalars())


class ReportRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, organization_id: str, domain: str, storage_uri: str) -> ReportRecord:
        report = ReportRecord(
            organization_id=organization_id,
            asset_value=domain,
            storage_uri=storage_uri,
        )
        self.session.add(report)
        await self.session.flush()
        return report
