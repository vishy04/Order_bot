from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# creating a base class ( sqlal docs said this )
class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    product_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    price: Mapped[float] = mapped_column(Float)
    tax: Mapped[float] = mapped_column(Float, nullable=True)


class Customer(Base):
    __tablename__ = "customers"

    customer_id: Mapped[int] = mapped_column(primary_key=True)
    customer_name: Mapped[str] = mapped_column(String(50))
    customer_contact: Mapped[str] = mapped_column(String, unique=True, index=True)
    # relation to orders
    orders: Mapped[list["Orders"]] = relationship(back_populates="customer")


class Orders(Base):
    __tablename__ = "orders"

    order_id: Mapped[int] = mapped_column(primary_key=True)

    product_id: Mapped[int] = mapped_column(ForeignKey("products.product_id"))
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.customer_id"))
    ordered_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # relationship back to customer
    customer: Mapped["Customer"] = relationship(back_populates="orders")
