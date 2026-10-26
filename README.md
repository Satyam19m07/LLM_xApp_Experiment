## Abstract

This work explores how **Large Language Models (LLMs)** can support intelligent **radio resource allocation in 5G O-RAN**. Instead of directly controlling the network, the LLM generates several possible allocation actions, while a local critic evaluates them and selects the most suitable one.

The proposed **TNAS (Top-N Action Sampling)** framework combines LLM reasoning with real-time network feedback to improve resource allocation across different network slices. The system continuously observes traffic demand, throughput, and resource usage, then adapts PRB allocation to improve **utility, reliability, and QoS**.

In simple terms:

```text
Observe Network
      ↓
LLM Suggests Actions
      ↓
Local Critic Selects Best Action
      ↓
Allocate PRBs
      ↓
Measure Performance
      ↓
Learn and Repeat
```

This creates a practical and adaptive way to use LLMs for **O-RAN resource management** while keeping the final control decision locally evaluated and measurable.
