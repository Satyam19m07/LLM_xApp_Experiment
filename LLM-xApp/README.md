# LLM-xApp Experiment

This repository contains my experimental setup for studying **LLM-assisted resource allocation in 5G O-RAN network slicing**.

The project is based on the original **LLM-xApp** repository by Fangzhou-Code and is used here to understand, run, and analyze the TNAS-based resource allocation workflow.

Original project:
`https://github.com/Fangzhou-Code/LLM-xApp`

---

## 1. What is this project?

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

The most important method is **TNAS — Top-N Action Sampling**.

---

## 2. Main idea of TNAS

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

This makes the system easier to control and evaluate.

---

## 3. Important repository files

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
| `run_experiments.py` | Runs the full experiment |
| `show_results.py` | Displays important CSV results in a clean table |

---

## 4. Requirements

Recommended environment:

```text
Ubuntu Linux
Python 3
Git
Python virtual environment
```

---

## 5. Clone the repository

```bash
git clone https://github.com/Satyam19m07/LLM_xApp_Experiment.git
```

Enter the project:

```bash
cd LLM_xApp_Experiment/LLM-xApp
```

---

## 6. Create Python virtual environment

Create the environment:

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

Install pandas for the clean result-table script:

```bash
python3 -m pip install pandas
```

---

## 7. Run unit tests

Before running the experiment, check whether the basic code is working:

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

A successful run should end with:

```text
OK
```

---

## 8. Run TNAS only

For the first experiment, use the local deterministic `stub` client.

This does not require an external API key.

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
Run only the TNAS controller.

--seed 0
Use a fixed random seed so the experiment is reproducible.

--out outputs/demo_tnas
Save the experiment results in this folder.

--llm-runs stub:stub
Use the local deterministic stub instead of an online LLM.
```

---

## 9. Understanding the TNAS terminal output

During execution, you may see something similar to:

```text
TNAS t=700 candidates=8 chosen_idx=7 action=(128, 1) prbs=(158, 2) score=3767.77 mode=real
```

Easy meaning:

| Field | Meaning |
|---|---|
| `t=700` | Current simulation time |
| `candidates=8` | Eight candidate actions are being considered |
| `chosen_idx=7` | Candidate number 7 was selected |
| `action=(128,1)` | Selected controller action |
| `prbs=(158,2)` | Actual PRB allocation after mapping |
| `score=...` | Score predicted by the local critic |
| `mode=real` | RealScore critic mode |

The main idea is:

```text
Network observation
        |
        v
Generate candidates
        |
        v
Critic scores them
        |
        v
Select best candidate
        |
        v
Apply PRBs
```

---

## 10. Check TNAS output files

After the experiment finishes:

```bash
ls -lh outputs/demo_tnas
```

Typical outputs include:

```text
timeseries_tnas_stub_stub.csv
config_used.yaml
figures
llm_cache
```

---

## 11. Show experiment result as a clean table

Instead of reading the full CSV directly, use:

```bash
python3 scripts/show_results.py \
  outputs/demo_tnas/timeseries_tnas_stub_stub.csv
```

This shows only important values such as:

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

### Main columns

| Column | Meaning |
|---|---|
| `t` | Simulation time |
| `prb1` | PRBs given to Slice/UE1 |
| `prb2` | PRBs given to Slice/UE2 |
| `sigma1` | Required throughput of UE1 |
| `sigma2` | Required throughput of UE2 |
| `hat_sigma1` | Measured throughput of UE1 |
| `hat_sigma2` | Measured throughput of UE2 |
| `shortfall1` | How far UE1 is below its target |
| `shortfall2` | How far UE2 is below its target |
| `u1` | Utility of UE1 |
| `u2` | Utility of UE2 |
| `V_k_soft` | Real reward/evaluation used by TNAS |

---

## 12. Run all four methods

To compare:

```text
Equal
Random
Proportional
TNAS
```

run:

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

Important CSV files:

```text
timeseries_equal.csv
timeseries_random.csv
timeseries_proportional.csv
timeseries_tnas_stub_stub.csv
```

---

## 13. Important figures

The experiment generates several figures.

Useful ones include:

```text
fig4.png
```

Overall experiment behavior.

```text
fig5a_sys_utility.png
```

System utility.

```text
fig5b_sys_reliability_severity.png
```

System reliability/severity.

```text
fig5c_avg_utility.png
```

Average utility comparison between methods.

```text
fig5d_avg_reliability_severity.png
```

Average reliability/severity comparison.

---

## 14. Running the project on a remote VM

If the experiment is running on a headless VM, the figures may not open directly with:

```bash
xdg-open figure.png
```

In this case, copy the figures to the local machine.

Example:

```bash
scp 'student@VM_IP:/home/student/LLM_xApp_Experiment/LLM-xApp/outputs/all_methods_stub/*.png' \
  ~/LLM_xApp_Figures/
```

Then open the folder locally:

```bash
xdg-open ~/LLM_xApp_Figures
```

---

## 15. Recommended demo sequence

For a short live demo:

### Step 1 — Connect to VM

```bash
ssh student@VM_IP
```

### Step 2 — Go to repository

```bash
cd ~/LLM_xApp_Experiment/LLM-xApp
```

### Step 3 — Activate environment

```bash
source .venv/bin/activate
```

### Step 4 — Show repository

```bash
ls
```

### Step 5 — Run tests

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

### Step 7 — Check output

```bash
ls -lh outputs/demo_tnas
```

### Step 8 — Show clean result table

```bash
python3 scripts/show_results.py \
  outputs/demo_tnas/timeseries_tnas_stub_stub.csv
```

### Step 9 — Show comparison results

```bash
ls -lh outputs/all_methods_stub
```

---

## 16. Complete TNAS workflow

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
Feasibility check
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

## 17. Methods implemented

### Equal

Resources are divided equally between slices.

Example:

```text
160 total PRBs

UE1 = 80
UE2 = 80
```

### Random

Resource allocation is selected randomly.

This is mainly used as a comparison baseline.

### Proportional

Resources are allocated according to traffic demand.

Higher demand receives more resources.

### TNAS

TNAS stands for:

```text
Top-N Action Sampling
```

The LLM generates several possible actions.

The local critic evaluates them.

The best candidate is selected and applied to the simulated network.

---

## 18. Why use a local stub?

The repository supports a deterministic local `stub`.

Benefits:

```text
No API key required
No API cost
No Internet LLM dependency
Repeatable results
Good for debugging and demonstrations
```

The same controller architecture can later be tested with supported online LLM providers.

---

## 19. Output interpretation

The experiment should be understood as:

```text
Requested throughput
        |
        v
Resource allocation
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
Reliability / reward
```

The main research question is:

> Can an LLM-assisted controller generate useful resource-allocation candidates while a local critic safely selects the best action?

---

## 20. Updating the GitHub repository

After changing code or results:

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

## 21. Exit the environment

Leave the Python virtual environment:

```bash
deactivate
```

If connected through SSH:

```bash
exit
```

---

## Acknowledgment

This experimental repository is based on the original **LLM-xApp** project:

```text
Fangzhou-Code/LLM-xApp
```

Original repository:

`https://github.com/Fangzhou-Code/LLM-xApp`

The original project provides the core simulation framework for LLM-assisted radio resource management in 5G O-RAN.

This repository is used for learning, experimentation, result analysis, and extending the workflow in an easy-to-understand form.
