from fastapi import Header


async def tenant_context(x_organization_id: str | None = Header(default=None)) -> str:
    return x_organization_id or "demo-org"
