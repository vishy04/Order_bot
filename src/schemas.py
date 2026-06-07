from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class WebhookPayload(BaseModel):
    customer_id: int
    product_id: int
