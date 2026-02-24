# Multi-Criteria Procurement Planner

 

A **constrained optimization engine** designed to solve the **Supplier Selection and Order Sizing Problem**. 

The planner determines an optimal procurement schedule that ensures all components for a **Bill of Materials (BOM)** arrive before a target assembly date **while minimizing total cost**, subject to operational, contractual, and risk constraints.

 

---

 

## Problem Overview

 

In complex manufacturing environments, procurement decisions must balance:

- Cost minimization

- Lead-time feasibility

- Minimum Order Quantities (MOQs)

- Supplier risk and diversification

- Assembly deadline constraints

 

This project formulates procurement planning as an **Integer Linear Programming (ILP)** problem and solves it using Python.

 

## Data Modeling & Architecture

 

### Enterprise Context (Conceptual)

 

The model mirrors a **Data Warehouse Star Schema**, commonly used in ERP and Supply Chain systems. Below is an example of how the fact and dimension table in ERP system would look like:

 

#### Dimension Tables

- `dim_parts`

  - Part specifications

  - Weight

  - Category

- `dim_suppliers`

  - Location

  - Risk rating

  - Contract terms

 

#### Fact Tables

- `fact_supplier_quotes`

  - Intersection of Parts × Suppliers

  - Unit cost

  - Lead time

  - MOQ

 

#### BOM Table

- Defines required quantity of each part for final assembly

 

---

 

### Technical Implementation (Demo)

 

For simplicity and portability, data is modeled using **JSON-style nested dictionaries**.

 

**Why this design?**

- Mimics REST API responses from modern ERP systems

- Easily convertible to Pandas DataFrames

- Clean interface between raw data and the optimization solver

 

---

 

##  Optimization Engine

 

### Why Integer Linear Programming (ILP)?

 

Procurement problem aims to **minimize total cost while satisfying**:

- Required component quantities

- Lead time constraints

- Whole-number (integer) purchase decisions

 



 

**Library Used:** `PuLP`

 

---

 

### How ILP Works (Conceptual)

 

The solver uses **different combinations of suppliers and quantities**:

- It eliminates combinations that violate constraints.

- It calculates total cost for feasible solutions.

- It selects the solution with the minimum total cost.
 

---

 

### Comparison of Optimization Approaches

 

| Method              | Advantages                               | Drawbacks                                   |

|---------------------|-------------------------------------------|----------------------------------------------|

| Greedy Heuristic    | Instant execution                         | Sub-optimal, ignores MOQs & long-term effects |

| Genetic Algorithms  | Handles non-linear, messy data            | No optimality guarantee                      |

| **MILP (Chosen)**   | Guarantees global optimum                 | Slower at very large scales                  |

 

---

 

## Risk Diversification & Uncertainty Modeling

 

To move beyond a “perfect world” solution, the model incorporates **resilience features**.

 

---

 

### Supplier Risk Diversification

 

Instead of a *winner-takes-all* strategy:

 

#### Objective Function Enhancements

- Add **Fixed Order Costs**:

- Discourages unnecessary supplier splitting unless risk reduction justifies it

 

#### Additional Constraints

- **Sourcing Cap**

 

- **Multi-Sourcing Rule**

- Critical components must be sourced from *at least two suppliers*

 

---

 

### Lead Time Uncertainty Handling

 

#### Safety Buffers

- Replace static lead times:

- σ represents historical lead-time variance

 

#### Stochastic Robustness (Optional Extension)

- Monte Carlo wrapper:

- Run MILP **1,000 simulations**

- Randomize lead-time delays

- Select solution that succeeds in **≥95% of scenarios**

 

This produces a **robust procurement plan**, not just a cost-optimal one.
