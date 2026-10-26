# LLM-xApp Experiment

This repository contains an experimental setup for studying **LLM-assisted resource allocation in 5G O-RAN network slicing**.

The main goal is to understand how an LLM-assisted controller can observe the current network condition, generate multiple possible resource-allocation actions, evaluate those actions using a local critic, and select a suitable PRB allocation for different network slices.

---

## 1. Research Paper

This implementation is based on the research work:

**LLM-xApp: A Large Language Model Empowered Radio Resource Management xApp for 5G O-RAN**

### Paper Authors

- Xingqi Wu
- Junaid Farooq
- Yuhui Wang
- Juntao Chen

### Publication

**IEEE INFOCOM Workshop 2026**

### Paper Link

[LLM-xApp: A Large Language Model Empowered Radio Resource Management xApp for 5G O-RAN](https://doi.org/10.1109/INFOCOM59046.2026.11571592)

The paper studies how Large Language Models can help perform adaptive radio resource allocation for different network slices in O-RAN.

---

## 2. What is this project?

In a 5G/O-RAN system, radio resources such as PRBs are limited.

Different network slices may need different amounts of resources.

For example:

```text
Total radio resources
        |
        |---- Slice 1
        |
        |---- Slice 2
```

The controller has to decide:

```text
How many PRBs should Slice 1 get?

How many PRBs should Slice 2 get?
```

This repository studies different ways to make that decision.

The main methods are:

```text
Equal
Random
Proportional
TNAS
```

The most important method is:

**TNAS — Top-N Action Sampling**

---

## 3. Main idea of TNAS

TNAS does not directly allow the LLM to control the network.

Instead, the workflow is:

```text
Current network state
        |
        v
LLM / local stub
        |
        v
Generate multiple candidate actions
        |
        v
Local critic evaluates candidates
        |
        v
Best action selected
        |
        v
Action converted to PRBs
        |
        v
Synthetic RAN environment
        |
        v
Measured throughput
        |
        v
Utility / shortfall / reward
        |
        v
Critic learns from the result
```

The important idea is:

```text
LLM
→ proposes possible actions

Local critic
→ evaluates the actions

Network environment
→ shows what actually happens

Performance metrics
→ measure whether the selected action was good
```

---

## 4. Important repository files

```text
LLM-xApp/
|
|-- ran_llm_xapp/
|   |
|   |-- config.py
|   |   Experiment configuration
|   |
|   |-- env.py
|   |   Synthetic RAN/network environment
|   |
|   |-- metrics.py
|   |   Utility, reliability, reward and PRB mapping
|   |
|   |-- prompts.py
|   |   Builds the prompt given to the LLM
|   |
|   |-- plotting.py
|   |   Generates result figures
|   |
|   |-- policies/
|   |   |
|   |   |-- equal.py
|   |   |-- random.py
|   |   |-- proportional.py
|   |   |-- tnas.py
|   |
|   |-- llm_clients/
|       |
|       |-- openai_client.py
|       |-- deepseek_client.py
|       |-- google_client.py
|       |-- stub_client.py
|
|-- scripts/
|   |
|   |-- run_experiments.py
|   |-- run_seed_sweep_sys_metrics.py
|   |-- show_results.py
|
|-- tests/
|
|-- outputs/
|
|-- README.md
|
|-- pyproject.toml
```

### Easy meaning of important files

| File | Purpose |
|---|---|
| `env.py` | Simulates the RAN/network |
| `metrics.py` | Calculates utility, reliability, shortfall and reward |
| `prompts.py` | Converts network information into an LLM prompt |
| `tnas.py` | Main TNAS controller and local critic |
| `run_experiments.py` | Runs the complete experiment |
| `show_results.py` | Displays important results in a clean table |

---

## 5. Requirements

Recommended environment:

```text
Ubuntu Linux
Python 3
Git
Python virtual environment
```

Check Python:

```bash
python3 --version
```

Check Git:

```bash
git --version
```

---

## 6. Go to the project directory

If the project is already available on the system, move into the main experiment folder:

```bash
cd ~/LLM_xApp_Experiment/LLM-xApp
```

Check the current directory:

```bash
pwd
```

Expected format:

```text
/home/<username>/LLM_xApp_Experiment/LLM-xApp
```

Check repository files:

```bash
ls
```

---

## 7. Create and activate Python virtual environment

Create the virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

After activation, the terminal should look similar to:

```text
(.venv) user@system:~/LLM_xApp_Experiment/LLM-xApp$
```

Upgrade pip:

```bash
python3 -m pip install -U pip
```

Install the project:

```bash
python3 -m pip install -e .
```

Install pandas for clean result tables:

```bash
python3 -m pip install pandas
```

---

## 8. Run unit tests

Before starting the experiment, check that the main functions are working:

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

A successful test should end with:

```text
OK
```

This means the basic implementation is working correctly.

---

## 9. Run TNAS only

For the first experiment, use the local deterministic `stub` client.

The stub does not require an external LLM API or API key.

Run:

```bash
python3 -m scripts.run_experiments \
  --methods tnas \
  --seed 0 \
  --out outputs/demo_tnas \
  --llm-runs stub:stub
```

### Meaning of the options

```text
--methods tnas
→ Run only TNAS

--seed 0
→ Use the same random seed so the experiment is reproducible

--out outputs/demo_tnas
→ Save experiment outputs in this directory

--llm-runs stub:stub
→ Use the local deterministic stub instead of an online LLM
```

---

## 10. Understanding the TNAS terminal output

During execution, the terminal may show:

```text
TNAS t=700 candidates=8 chosen_idx=7 action=(128, 1) prbs=(158, 2) score=3767.77 mode=real
```

Easy meaning:

| Field | Meaning |
|---|---|
| `t=700` | Current simulation time |
| `candidates=8` | Number of candidate actions |
| `chosen_idx=7` | Candidate selected by the controller |
| `action=(128,1)` | Selected controller action |
| `prbs=(158,2)` | PRBs after action-to-PRB mapping |
| `score=...` | Score given by the local critic |
| `mode=real` | RealScore critic mode |

The simple workflow is:

```text
Network observation
        |
        v
Generate candidate actions
        |
        v
Critic evaluates candidates
        |
        v
Select best action
        |
        v
Convert action to PRBs
```

---

## 11. Check TNAS output files

After the experiment finishes:

```bash
ls -lh outputs/demo_tnas
```

Typical output files include:

```text
timeseries_tnas_stub_stub.csv
config_used.yaml
llm_cache/
PNG figures
PDF figures
```

---

## 12. Show experiment results as a clean table

The complete CSV contains many columns and can be difficult to read directly.

Use:

```bash
python3 scripts/show_results.py \
  outputs/demo_tnas/timeseries_tnas_stub_stub.csv
```

This displays important parameters in a cleaner form.

Typical important values are:

```text
Time
PRB1
PRB2
Required rate
Measured rate
Shortfall
Utility
V_k_soft
```

### Important columns

| Column | Meaning |
|---|---|
| `t` | Simulation time |
| `prb1` | PRBs allocated to Slice/UE1 |
| `prb2` | PRBs allocated to Slice/UE2 |
| `sigma1` | Requested throughput of UE1 |
| `sigma2` | Requested throughput of UE2 |
| `hat_sigma1` | Measured throughput of UE1 |
| `hat_sigma2` | Measured throughput of UE2 |
| `shortfall1` | UE1 throughput shortage |
| `shortfall2` | UE2 throughput shortage |
| `u1` | Utility of UE1 |
| `u2` | Utility of UE2 |
| `V_k_soft` | Real performance reward used by TNAS |

---

## 13. Run all four methods

The framework supports:

```text
Equal
Random
Proportional
TNAS
```

Run all four using:

```bash
python3 -m scripts.run_experiments \
  --methods all2 \
  --seed 0 \
  --out outputs/all_methods_stub \
  --llm-runs stub:stub
```

After completion:

```bash
ls -lh outputs/all_methods_stub
```

Important CSV files include:

```text
timeseries_equal.csv
timeseries_random.csv
timeseries_proportional.csv
timeseries_tnas_stub_stub.csv
```

These files allow the different allocation strategies to be compared.

---

## 14. Important result figures

The experiment generates several useful figures.

### Overall experiment behavior

```text
fig4.png
```

### System utility

```text
fig5a_sys_utility.png
```

### System reliability/severity

```text
fig5b_sys_reliability_severity.png
```

### Average utility comparison

```text
fig5c_avg_utility.png
```

### Average reliability/severity comparison

```text
fig5d_avg_reliability_severity.png
```

For a short demonstration, the most useful figures are:

```text
fig4.png

fig5c_avg_utility.png

fig5d_avg_reliability_severity.png
```

---

## 15. Running the experiment on a remote VM

If the experiment is running on a headless VM, graphical figures may not open directly.

For example:

```bash
xdg-open figure.png
```

may fail because the VM has no graphical display.

In this case, copy the figures to the local computer.

Example:

```bash
scp 'student@VM_IP:/home/student/LLM_xApp_Experiment/LLM-xApp/outputs/all_methods_stub/*.png' \
  ~/LLM_xApp_Figures/
```

Then open the local figure directory:

```bash
xdg-open ~/LLM_xApp_Figures
```

---

## 16. Recommended live demo sequence

A simple demo can be performed using the following sequence.

### Step 1 — Connect to VM

```bash
ssh student@VM_IP
```

### Step 2 — Enter the project

```bash
cd ~/LLM_xApp_Experiment/LLM-xApp
```

### Step 3 — Activate Python environment

```bash
source .venv/bin/activate
```

### Step 4 — Show repository files

```bash
ls
```

### Step 5 — Run unit tests

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

### Step 6 — Run TNAS

```bash
python3 -m scripts.run_experiments \
  --methods tnas \
  --seed 0 \
  --out outputs/demo_tnas \
  --llm-runs stub:stub
```

### Step 7 — Check generated output

```bash
ls -lh outputs/demo_tnas
```

### Step 8 — Display clean result table

```bash
python3 scripts/show_results.py \
  outputs/demo_tnas/timeseries_tnas_stub_stub.csv
```

### Step 9 — Show comparison results

```bash
ls -lh outputs/all_methods_stub
```

This sequence provides a short and clear demonstration of the complete framework.

---

## 17. Complete TNAS workflow

```text
Synthetic RAN environment
          |
          v
Network observation
          |
          v
Prompt generation
          |
          v
LLM / Stub
          |
          v
Top-N candidate actions
          |
          v
Feasibility / validation
          |
          v
Local RealScore critic
          |
          v
Best action
          |
          v
Action-to-PRB mapping
          |
          v
Apply allocation
          |
          v
Measure throughput
          |
          v
Utility / shortfall / V_k_soft
          |
          v
Critic update
          |
          +------> Next control interval
```

---

## 18. Methods implemented

### Equal

The total available resources are divided equally.

Example:

```text
160 total PRBs

Slice 1 = 80
Slice 2 = 80
```

### Random

The controller randomly selects resource allocations.

This method is mainly used as a baseline.

### Proportional

Resources are allocated according to the current traffic requirement.

A slice with more demand generally receives more resources.

### TNAS

TNAS stands for:

```text
Top-N Action Sampling
```

The process is:

```text
Current network state
        |
        v
Generate several possible actions
        |
        v
Local critic evaluates them
        |
        v
Select the best candidate
```

---

## 19. Why use the local stub?

The deterministic `stub` is useful for initial experiments.

Advantages:

```text
No API key required

No external LLM cost

No dependency on Internet-based LLM services

Repeatable experiment behavior

Easy debugging

Good for demonstrations
```

After the complete workflow is verified, the same architecture can be tested with supported online LLM clients.

---

## 20. How to understand the result

The basic result flow is:

```text
Requested throughput
        |
        v
PRB allocation
        |
        v
Measured throughput
        |
        v
Shortfall
        |
        v
Utility
        |
        v
Reward / reliability evaluation
```

For example:

```text
Required rate = 40 Mbps

Measured rate = 30 Mbps
```

means the slice is experiencing a throughput shortfall.

The controller tries to choose allocations that reduce these shortages while using radio resources efficiently.

---

## 21. Updating the GitHub repository

After modifying code, results, or documentation:

Check changes:

```bash
git status
```

Add changes:

```bash
git add .
```

Commit:

```bash
git commit -m "Describe the changes"
```

Push:

```bash
git push
```

---

## 22. Exit the experiment environment

Leave the Python environment:

```bash
deactivate
```

If connected to the experiment system using SSH:

```bash
exit
```

---

## Paper Credit

This experimental implementation is based on the research work:

**LLM-xApp: A Large Language Model Empowered Radio Resource Management xApp for 5G O-RAN**

Authors:

- Xingqi Wu
- Junaid Farooq
- Yuhui Wang
- Juntao Chen

Published/accepted in:

**IEEE INFOCOM Workshop 2026**

Paper:

[https://doi.org/10.1109/INFOCOM59046.2026.11571592](https://doi.org/10.1109/INFOCOM59046.2026.11571592)

If you use or extend this work for academic research, please cite the original paper.

The original project provides the core simulation framework for LLM-assisted radio resource management in 5G O-RAN.

This repository is used for learning, experimentation, result analysis, and extending the workflow in an easy-to-understand form.
