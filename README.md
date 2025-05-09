# Santa’s Toy Distribution Optimizer – ASA Project 3 (2024/25)

## 🔍 Overview
The program chooses **which toy each child receives** so that the largest possible number of kids
around the world get a present **while respecting production and trade rules**.

Inputs describe  
* **n factories** – each produces a single toy type and has limited stock,  
* **m countries** – each sets  
  * a *minimum* number `pmin` of toys that must stay inside the country and  
  * a *maximum* export quota `pmax`,  
* **t children** – each child lives in one country and lists the toys (factories) they would accept.  

Each child can receive **at most one** toy.  
If it is impossible to satisfy *all* per‑country rules the solver outputs **`‑1`**. Otherwise it outputs
the **maximum number of happy children**.

## 💡 Formulation
The task is modelled as a **0‑1 Integer Linear Program** using *PuLP*:

| Symbol | Description |
|--------|-------------|
| `e_{c,f}` | binary, 1 iff child *c* gets a toy from factory *f* |
| `stock_f` | available toys at factory *f* |
| `pmin_j` / `pmax_j` | country‑level minima / export caps |

Objective  
```
max  Σ_{c,f}  e_{c,f}
```

Constraints  
1. **One toy per child** – Σ_f e_{c,f} ≤ 1  
2. **Factory stock** – Σ_c e_{c,f} ≤ stock_f  
3. **Exports** – for each country j  
   Σ_{c∉j, f∈j} e_{c,f} ≤ pmax_j  
4. **Domestic minima** – for each country j  
   Σ_{c∈j} Σ_{f} e_{c,f} ≥ pmin_j  

The ILP is solved with **GLPK** in a few hundred milliseconds for the public datasets.

## ⚙️ Setup & Execution
```bash
# Install dependencies
python3 -m pip install pulp    

# Solve an instance
python3 proj3.py < input.txt
```

### 🧪 Generating test cases
```bash
# Arguments: N_factories N_countries N_children variance max_cap max_requests
python3 generator.py 50 10 200 0.3 5 4 > input.txt
```
The generator outputs *always‑feasible* instances covering corner cases and large random
scenarios.
