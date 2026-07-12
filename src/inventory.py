#!/usr/bin/env python3
"""
Inventory Optimization Module
Implements EOQ (Economic Order Quantity) and safety stock calculations.

Author: Mupo Mubita <mubitamupo@outlook.com>
GitHub: https://github.com/Mubita767
"""

import math
from dataclasses import dataclass


@dataclass
class InventoryItem:
    """Represents a product in inventory."""
    sku: str
    name: str
    unit_cost: float
    annual_demand: int
    ordering_cost: float
    holding_cost_rate: float
    lead_time_days: int
    daily_demand_std: float
    service_level_z: float = 1.65  # 95% service level

    @property
    def holding_cost_per_unit(self):
        """Annual holding cost per unit."""
        return self.unit_cost * self.holding_cost_rate

    def eoq(self):
        """
        Calculate Economic Order Quantity.
        Formula: sqrt(2 * D * S / H)
        """
        return math.sqrt(
            (2 * self.annual_demand * self.ordering_cost) 
            / self.holding_cost_per_unit
        )

    def reorder_point(self):
        """
        Calculate reorder point with safety stock.
        ROP = (daily_demand * lead_time) + safety_stock
        """
        daily_demand = self.annual_demand / 365
        lead_time_demand = daily_demand * self.lead_time_days
        safety_stock = self.service_level_z * self.daily_demand_std * math.sqrt(self.lead_time_days)
        return lead_time_demand + safety_stock

    def total_inventory_cost(self, order_quantity=None):
        """Calculate total annual inventory cost."""
        q = order_quantity or self.eoq()
        ordering_cost = (self.annual_demand / q) * self.ordering_cost
        holding_cost = (q / 2) * self.holding_cost_per_unit
        purchase_cost = self.annual_demand * self.unit_cost
        return ordering_cost + holding_cost + purchase_cost


def optimize_inventory(items):
    """Optimize inventory levels for multiple items."""
    results = []
    for item in items:
        results.append({
            'sku': item.sku,
            'name': item.name,
            'eoq': round(item.eoq(), 2),
            'reorder_point': round(item.reorder_point(), 2),
            'total_cost': round(item.total_inventory_cost(), 2)
        })
    return results


if __name__ == "__main__":
    items = [
        InventoryItem(
            sku="WID-001", name="Widget A",
            unit_cost=25.0, annual_demand=12000,
            ordering_cost=100.0, holding_cost_rate=0.20,
            lead_time_days=7, daily_demand_std=15
        ),
        InventoryItem(
            sku="WID-002", name="Widget B",
            unit_cost=45.0, annual_demand=6000,
            ordering_cost=150.0, holding_cost_rate=0.25,
            lead_time_days=10, daily_demand_std=8
        )
    ]

    for result in optimize_inventory(items):
        print(f"\n{result['name']} ({result['sku']}):")
        print(f"  EOQ: {result['eoq']} units")
        print(f"  Reorder Point: {result['reorder_point']} units")
        print(f"  Total Annual Cost: ${result['total_cost']}")
