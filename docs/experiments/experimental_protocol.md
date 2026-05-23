# H4 Hyperparameter Experiments — Complete Experimental Protocol
## Project: Trinity-v33 Transformer Training Study

**Version:** 1.0  
**Date:** 2025-01-15  
**Objective:** Systematically evaluate H4 hyperparameter configurations for decoder-only transformer language models, targeting BPB < 1.50 on WikiText-103 and C4 evaluation sets.

---

## Table of Contents
1. [Overview & Hypothesis](#1-overview--hypothesis)
2. [Experimental Variables](#2-experimental-variables)
3. [Core Experiments (5 Runs)](#3-core-eximents)
4. [Dataset & Tokenization](#4-dataset--tokenization)
5. [Model Architecture Configs](#5-model-architecture-configs)
6. [Training Configuration](#6-training-configuration)
7. [Evaluation Protocol](#7-evaluation-protocol)
8. [Control Baselines](#8-control-baselines)
9. [Statistical Significance Plan](#9-statistical-significance-plan)
10. [Ablation Studies](#10-ablation-studies)
11. [Scaling Study](#11-scaling-study)
12. [Context Length Study](#12-context-length-study)
13. [Implementation Details](#13-implementation-details)
14. [Expected Results & Analysis Plan](#14-expected-results--analysis-plan)
15. [Appendix: Full Configs](#15-appendix-full-configs)

---

## 1. Overview & Hypothesis

### Research Question
Which combination of H4 hyperparameters (hidden size, learning rate, MuON scaling, weight decay, context length) produces the most compute-efficient transformer language model under 24M parameters?

### H4 Framework
The H4 protocol decomposes transformer training into four tunable axes:
- **H**: Hidden dimension (model width)
- **L**: Layer count (model depth)  
- **LR**: Learning rate schedule
- **Ctx**: Context window length

### Primary Hypothesis
> *There exists a configuration in the H4 search space that achieves BPB < 1.50 on WikiText-103 with fewer than 25M parameters and fewer than 50B training tokens, through synergistic tuning of width, depth, learning dynamics, and context window.*

### Success Criteria
| Metric | Target | Threshold |
|--------|--------|-----------|
| WikiText-103 BPB | < 1.50 | Hard constraint |
| C4 BPB | < 2.10 | Secondary target |
| Training stability | Zero divergences | Hard constraint |
| Wall-clock efficiency | < 48h on 4x A100 | Soft target |

---

## 2. Experimental Variables

### Independent Variables

| Variable | Symbol | Range | Levels |
|----------|--------|-------|--------|
| Hidden dimension | `h` | 128–3712 | 5 levels |
| Number of layers | `d` | 4–24 | Adaptive to `h` |
| Learning rate | `lr` | 1e-4 – 0.1 | Log-scale sweep |
| MuON LR scale | `muon_lr_scale` | 0.01 – 1.0 | Multiplicative factor |
| Weight decay (WSD) | `wsd_decay` | 0.5 – 1.5 | Schedule parameter |
| Context length | `ctx` | 2 – 30 | 4 levels |
| Attention heads | `n_heads` | 4–32 | `h / 64` default |

### Dependent Variables

| Metric | Description | Frequency |
|--------|-------------|-----------|
| `bpb_wt103` | Bits per byte on WikiText-103 | Every 1000 steps |
| `bpb_c4` | Bits per byte on C4 validation | Every 1000 steps |
| `train_loss` | Training cross-entropy loss | Every 100 steps |
| `perplexity` | Token-level perplexity | Every 1000 steps |
| `grad_norm` | Global gradient L2 norm | Every 100 steps |
| `effective_lr` | Actual LR after scheduling | Every 100 steps |
| `throughput` | Tokens/sec training speed | Every 500 steps |

---

## 3. Core Experiments

### Experiment 1: h4-phi3-muon — MuON Optimizer Scaling
**Purpose:** Evaluate the MuON optimizer's learning rate scaling factor at moderate model width.

| Parameter | Value | Notes |
|-----------|-------|-------|
| `experiment_id` | `h4-phi3-muon` | |
| `hidden_size` (`h`) | **1408** | Fixed per spec |
| `num_layers` (`d`) | 12 | Standard depth |
| `num_heads` | 22 | `ceil(h/64) = 22` |
| `head_dim` | 64 | Fixed |
| `learning_rate` | **0.0236** | Per spec |
| `muon_lr_scale` | **0.236** | MuON multiplier |
| `context_length` | **12** | Per spec |
| `wsd_decay` | 1.0 (default) | Not varied |
| **Total parameters** | ~18.5M | |
| **Optimizer** | MuON (primary) + AdamW (embeddings) | |
| **Runs** | 3 seeds (42, 123, 456) | |

**Hypothesis:** `muon_lr_scale = 0.236` provides optimal signal-to-noise ratio for the 1408-width regime, enabling faster convergence than standard AdamW at lr=0.0236 alone.

---

### Experiment 2: h4-l02-lr — Low Learning Rate Baseline
**Purpose:** Test whether a very low learning rate with standard AdamW can match or exceed higher-rate MuON configurations.

| Parameter | Value | Notes |
|-----------|-------|-------|
| `experiment_id` | `h4-l02-lr` | |
| `hidden_size` (`h`) | **1408** | Fixed per spec |
| `num_layers` (`d`) | 12 | Standard depth |
| `num_heads` | 22 | `ceil(h/64) = 22` |
| `head_dim` | 64 | Fixed |
| `learning_rate` | **0.000103** | Very low, per spec |
| `muon_lr_scale` | N/A | Standard AdamW only |
| `context_length` | **12** | Per spec |
| `wsd_decay` | 1.0 (default) | Not varied |
| **Total parameters** | ~18.5M | |
| **Optimizer** | AdamW (standard) | |
| **Runs** | 3 seeds (42, 123, 456) | |

**Hypothesis:** Low LR (1.03e-4) with sufficient training steps achieves comparable final BPB to high-LR runs, with superior stability and lower gradient variance.

---

### Experiment 3: h4-360phi3-base — Aggressive Learning Rate
**Purpose:** Push the learning rate boundary to test convergence speed vs. stability tradeoff at high LR.

| Parameter | Value | Notes |
|-----------|-------|-------|
| `experiment_id` | `h4-360phi3-base` | |
| `hidden_size` (`h`) | **1408** | Fixed per spec |
| `num_layers` (`d`) | 12 | Standard depth |
| `num_heads` | 22 | `ceil(h/64) = 22` |
| `head_dim` | 64 | Fixed |
| `learning_rate` | **0.08506** | Aggressive, per spec |
| `muon_lr_scale` | N/A | AdamW with lr warmup critical |
| `context_length` | **12** | Per spec |
| `wsd_decay` | 1.0 (default) | Not varied |
| **Total parameters** | ~18.5M | |
| **Optimizer** | AdamW with aggressive warmup | |
| **Runs** | 3 seeds (42, 123, 456) | |

**Hypothesis:** With proper warmup (5% of steps), LR=0.08506 can achieve faster convergence without divergence, reaching target BPB in 30-40% fewer steps.

---

### Experiment 4: h4-loop-corr — Weight-Decay Schedule Tuning
**Purpose:** Evaluate the impact of WSD (Warmup-Stable-Decay) weight decay parameter on training dynamics and final performance.

| Parameter | Value | Notes |
|-----------|-------|-------|
| `experiment_id` | `h4-loop-corr` | |
| `hidden_size` (`h`) | **1408** | Fixed per spec |
| `num_layers` (`d`) | 12 | Standard depth |
| `num_heads` | 22 | `ceil(h/64) = 22` |
| `head_dim` | 64 | Fixed |
| `learning_rate` | 0.0018 | Moderate default |
| `muon_lr_scale` | N/A | AdamW |
| `context_length` | **12** | Per spec |
| `wsd_decay` | **1.013** | WSD schedule parameter, per spec |
| **Total parameters** | ~18.5M | |
| **Optimizer** | AdamW + WSD schedule | |
| **Runs** | 3 seeds (42, 123, 456) | |

**Hypothesis:** `wsd_decay = 1.013` provides optimal late-training regularization, reducing overfit and improving generalization BPB by 0.03–0.08 relative to default `wsd_decay = 1.0`.

---

### Experiment 5: h4-e3d3-full — Wide Model, Long Context
**Purpose:** Evaluate a significantly wider model with extended context window, testing the H4 scaling hypothesis.

| Parameter | Value | Notes |
|-----------|-------|-------|
| `experiment_id` | `h4-e3d3-full` | |
| `hidden_size` (`h`) | **2432** | Wider per spec |
| `num_layers` (`d`) | 16 | Increased depth for balance |
| `num_heads` | 38 | `ceil(h/64) = 38` |
| `head_dim` | 64 | Fixed |
| `learning_rate` | 0.0025 | Moderate (wider model) |
| `muon_lr_scale` | 0.15 | Reduced for stability |
| `context_length` | **20** | Extended per spec |
| `wsd_decay` | 1.0 (default) | Not varied |
| **Total parameters** | ~42.1M | Largest config |
| **Optimizer** | MuON + AdamW | |
| **Runs** | 3 seeds (42, 123, 456) | |

**Hypothesis:** The h=2432/ctx=20 configuration leverages increased model capacity and longer-range dependencies to break the BPB < 1.40 barrier, justifying the additional compute.

---

## 4. Dataset & Tokenization

### Primary Dataset: WikiText-103
| Property | Value |
|----------|-------|
| Source | Salesforce/WikiText-103 |
| Size | 103M tokens (train) |
| Vocabulary | GPT-2 BPE (50257 tokens) |
| Format | Raw text, sentence-level |
| Split | Train / Valid / Test |

### Secondary Dataset: C4 (validation only)
| Property | Value |
|----------|-------|
| Source | allenai/c4 |
| Eval subset | 5M tokens (en-validation) |
| Tokenizer | GPT-2 BPE (50257 tokens) |
| Purpose | Cross-dataset generalization check |

### Custom Pretraining Dataset (for scaling study)
| Property | Value |
|----------|-------|
| Source | SlimPajama 6B subset |
| Size | 6B tokens |
| Mix | 60% web, 20% code, 20% academic |
| Purpose | Context length and scaling studies |

### Tokenization Config
```python
tokenizer_config = {
    "name": "gpt2",
    "vocab_size": 50257,
    "bos_token_id": 50256,
    "eos_token_id": 50256,
    "pad_token_id": 50256,
    "max_length": 2048,  # Will be truncated to ctx
}
```

---

## 5. Model Architecture Configs

### Base Architecture Template
```python
def get_model_config(experiment_id: str) -> dict:
    configs = {
        "h4-phi3-muon": {
            "hidden_size": 1408,
            "num_layers": 12,
            "num_heads": 22,
            "head_dim": 64,
            "intermediate_ratio": 4,      # MLP expansion
            "intermediate_size": 5632,    # 1408 * 4
            "max_position_embeddings": 512,
            "context_window": 12,
            "rope_theta": 10000.0,
            "rope_scaling": None,
            "tie_word_embeddings": False,
            "use_bias": False,
            "norm_type": "rmsnorm",
            "norm_eps": 1e-6,
            "activation": "swiglu",
            "initializer_range": 0.02,
            "use_cache": False,
        },
        "h4-l02-lr": {
            "hidden_size": 1408,
            "num_layers": 12,
            "num_heads": 22,
            "head_dim": 64,
            "intermediate_ratio": 4,
            "intermediate_size": 5632,
            "max_position_embeddings": 512,
            "context_window": 12,
            "rope_theta": 10000.0,
            "rope_scaling": None,
            "tie_word_embeddings": False,
            "use_bias": False,
            "norm_type": "rmsnorm",
            "norm_eps": 1e-6,
            "activation": "swiglu",
            "initializer_range": 0.02,
            "use_cache": False,
        },
        "h4-360phi3-base": {
            "hidden_size": 1408,
            "num_layers": 12,
            "num_heads": 22,
            "head_dim": 64,
            "intermediate_ratio": 4,
            "intermediate_size": 5632,
            "max_position_embeddings": 512,
            "context_window": 12,
            "rope_theta": 10000.0,
            "rope_scaling": None,
            "tie_word_embeddings": False,
            "use_bias": False,
            "norm_type": "rmsnorm",
            "norm_eps": 1e-6,
            "activation": "swiglu",
            "initializer_range": 0.02,
            "use_cache": False,
        },
        "h4-loop-corr": {
            "hidden_size": 1408,
            "num_layers": 12,
            "num_heads": 22,
            "head_dim": 64,
            "intermediate_ratio": 4,
            "intermediate_size": 5632,
            "max_position_embeddings": 512,
            "context_window": 12,
            "rope_theta": 10000.0,
            "rope_scaling": None,
            "tie_word_embeddings": False,
            "use_bias": False,
            "norm_type": "rmsnorm",
            "norm_eps": 1e-6,
            "activation": "swiglu",
            "initializer_range": 0.02,
            "use_cache": False,
        },
        "h4-e3d3-full": {
            "hidden_size": 2432,
            "num_layers": 16,
            "num_heads": 38,
            "head_dim": 64,
            "intermediate_ratio": 4,
            "intermediate_size": 9728,    # 2432 * 4
            "max_position_embeddings": 512,
            "context_window": 20,
            "rope_theta": 10000.0,
            "rope_scaling": None,
            "tie_word_embeddings": False,
            "use_bias": False,
            "norm_type": "rmsnorm",
            "norm_eps": 1e-6,
            "activation": "swiglu",
            "initializer_range": 0.02,
            "use_cache": False,
        },
    }
    return configs[experiment_id]
```

### Parameter Count Summary
| Experiment | Hidden | Layers | Heads | Intermediate | **Total Params** | FLOPs/forward |
|------------|--------|--------|-------|-------------|-----------------|---------------|
| h4-phi3-muon | 1408 | 12 | 22 | 5632 | **18.5M** | ~2.1e9 |
| h4-l02-lr | 1408 | 12 | 22 | 5632 | **18.5M** | ~2.1e9 |
| h4-360phi3-base | 1408 | 12 | 22 | 5632 | **18.5M** | ~2.1e9 |
| h4-loop-corr | 1408 | 12 | 22 | 5632 | **18.5M** | ~2.1e9 |
| h4-e3d3-full | 2432 | 16 | 38 | 9728 | **42.1M** | ~7.8e9 |

---

## 6. Training Configuration

### Global Training Hyperparameters
```python
training_config = {
    # Duration
    "max_steps": 50000,           # Primary target
    "warmup_steps": 2500,         # 5% of max_steps
    "eval_every": 1000,
    "save_every": 5000,
    "log_every": 100,
    
    # Batch configuration
    "per_device_batch_size": 32,
    "gradient_accumulation_steps": 4,
    "global_batch_size": 128,     # 32 * 4
    "total_tokens": 6_400_000_000, # 128 * 500 * 50000 (approx)
    
    # Optimization
    "weight_decay": 0.1,
    "max_grad_norm": 1.0,
    "beta1": 0.9,
    "beta2": 0.95,
    "eps": 1e-8,
    
    # Precision
    "dtype": "bfloat16",
    "gradient_checkpointing": True,
    
    # LR Schedule (WSD - Warmup Stable Decay)
    "lr_schedule": "wsd",
    "warmup_fraction": 0.05,
    "stable_fraction": 0.75,
    "decay_fraction": 0.20,
    "decay_type": "cosine",
    
    # Distributed
    "nnodes": 1,
    "nproc_per_node": 4,          # 4x A100
}
```

### Experiment-Specific Training Overrides

| Experiment | LR | muon_lr_scale | wsd_decay | Optimizer | Special |
|------------|-----|---------------|-----------|-----------|---------|
| h4-phi3-muon | 0.0236 | 0.236 | 1.0 | MuON | MuON for all params except embeds |
| h4-l02-lr | 0.000103 | — | 1.0 | AdamW | Extended stable phase |
| h4-360phi3-base | 0.08506 | — | 1.0 | AdamW | Aggressive warmup (10%) |
| h4-loop-corr | 0.0018 | — | **1.013** | AdamW+WSD | Custom decay schedule |
| h4-e3d3-full | 0.0025 | 0.15 | 1.0 | MuON | RoPE extension for ctx=20 |

### MuON Optimizer Configuration
```python
muon_config = {
    "enabled_experiments": ["h4-phi3-muon", "h4-e3d3-full"],
    "muon_lr_scale": 0.236,       # Exp 1
    "muon_lr_scale_alt": 0.15,    # Exp 5
    "momentum": 0.9,
    "nesterov": True,
    "adamw_for_embeddings": True,
    "adamw_for_head": True,
    "ns_steps": 5,                # Newton-Schulz iterations
}
```

---

## 7. Evaluation Protocol

### Primary Metric: Bits Per Byte (BPB)
```
BPB = total_bits / total_bytes
    = sum(-log2(P(token|context))) * num_tokens / (num_bytes)
```

Lower BPB = better compression = better model.

### Evaluation Pipeline
```python
eval_config = {
    "datasets": {
        "wikitext103": {
            "split": "validation",
            "metric": "bpb",
            "target": 1.50,
            "stride": 512,        # Sliding window stride
            "max_eval_tokens": 1_000_000,
        },
        "c4": {
            "split": "validation",
            "metric": "bpb",
            "target": 2.10,
            "stride": 512,
            "max_eval_tokens": 1_000_000,
        },
    },
    "frequency": 1000,            # Every 1000 steps
    "best_checkpoint_metric": "wikitext103/bpb",
    "checkpoint_mode": "min",
}
```

### Secondary Metrics
1. **Token-level perplexity**: `exp(cross_entropy)`
2. **Training loss curve smoothness**: Variance of loss over 100-step windows
3. **Gradient norm trajectory**: Monitor for instability
4. **Effective throughput**: Tokens/sec at steady state

---

## 8. Control Baselines

### Baseline A: Standard Small Transformer (Baseline-S)
A conventional configuration matching common literature baselines.

| Parameter | Value |
|-----------|-------|
| `hidden_size` | 512 |
| `num_layers` | 8 |
| `num_heads` | 8 |
| `learning_rate` | 0.001 |
| `optimizer` | AdamW |
| `context_length` | 512 |
| **Total params** | ~14M |
| **Expected BPB** | ~1.65 (WikiText-103) |

### Baseline B: Standard Medium Transformer (Baseline-M)
A medium-sized baseline comparable to our primary configs.

| Parameter | Value |
|-----------|-------|
| `hidden_size` | 768 |
| `num_layers` | 12 |
| `num_heads` | 12 |
| `learning_rate` | 0.001 |
| `optimizer` | AdamW |
| `context_length` | 512 |
| **Total params** | ~28M |
| **Expected BPB** | ~1.45 (WikiText-103) |

### Baseline C: H4 Default (Baseline-H4)
Our H4 framework default without any special tuning.

| Parameter | Value |
|-----------|-------|
| `hidden_size` | 1408 |
| `num_layers` | 12 |
| `num_heads` | 22 |
| `learning_rate` | 0.001 |
| `optimizer` | AdamW |
| `context_length` | 512 |
| **Total params** | ~18.5M |
| **Expected BPB** | ~1.52 (WikiText-103) |

### Baseline Comparison Table
| Baseline | Params | LR | Optimizer | Ctx | Expected BPB | Purpose |
|----------|--------|-----|-----------|-----|-------------|---------|
| Baseline-S | 14M | 0.001 | AdamW | 512 | 1.65 | Small model reference |
| Baseline-M | 28M | 0.001 | AdamW | 512 | 1.45 | Medium model reference |
| Baseline-H4 | 18.5M | 0.001 | AdamW | 512 | 1.52 | Same-architecture default |

---

## 9. Statistical Significance Plan

### Replication Strategy
Each core experiment runs with **3 random seeds** (42, 123, 456) for statistical reliability.

### Seed Configuration
```python
seed_config = {
    "seeds": [42, 123, 456],
    "deterministic": True,
    "torch_seed": "seed",
    "numpy_seed": "seed",
    "random_seed": "seed",
    "cuda_deterministic": False,  # Allow for performance
}
```

### Analysis Protocol
1. **Point estimate**: Mean BPB across 3 seeds
2. **Variability**: Standard deviation and 95% CI
3. **Significance test**: Paired t-test between experiment and Baseline-H4
4. **Effect size**: Cohen's d for practical significance
5. **Early stopping criterion**: If 2 of 3 seeds diverge (loss > 5.0), abort experiment

### Minimum Detectable Effect
With 3 seeds and expected sigma_BPB ~0.02:
- Minimum detectable difference (80% power, alpha=0.05): **~0.033 BPB**
- Therefore, differences > 0.05 BPB are reliably detectable

---

## 10. Ablation Studies

### Ablation 1: Optimizer Component (MuON vs AdamW)
| Config | Optimizer | LR | Expected Impact |
|--------|-----------|-----|-----------------|
| Full (Exp 1) | MuON | 0.0236 | Reference |
| Abl-1a | AdamW | 0.0236 | Test MuON benefit at same LR |
| Abl-1b | AdamW | 0.001 | Standard LR comparison |
| Abl-1c | MuON | 0.001 | Low LR with MuON |

### Ablation 2: Context Length Impact
| Config | Context | Expected BPB | Notes |
|--------|---------|-------------|-------|
| Full (Exp 1) | 12 | Reference | Short context |
| Abl-2a | 2 | +0.15 BPB | Minimal context |
| Abl-2b | 6 | +0.05 BPB | Medium-short context |
| Abl-2c | 20 | -0.03 BPB | Extended context |
| Abl-2d | 30 | -0.02 BPB | Long context (diminishing returns) |

### Ablation 3: Learning Rate Schedule
| Config | LR Schedule | Expected Impact |
|--------|-------------|-----------------|
| Full (Exp 4) | WSD (wsd=1.013) | Reference |
| Abl-3a | Cosine decay | +0.02 BPB |
| Abl-3b | Linear decay | +0.03 BPB |
| Abl-3c | Constant LR | +0.05 BPB |
| Abl-3d | WSD (wsd=1.05) | -0.01 to +0.02 BPB |

### Ablation 4: Width-Depth Tradeoff
| Config | Hidden | Layers | Heads | Params | Purpose |
|--------|--------|--------|-------|--------|---------|
| Abl-4a | 1408 | 8 | 22 | 12.8M | Shallower, same width |
| Abl-4b | 1408 | 16 | 22 | 24.2M | Deeper, same width |
| Abl-4c | 1024 | 12 | 16 | 12.5M | Narrower, same depth |
| Abl-4d | 1792 | 12 | 28 | 28.1M | Wider, same depth |

### Ablation Execution Plan
```
Total ablation runs: 4 ablations * 4 configs * 3 seeds = 48 runs
Priority order: Abl-1 (optimizer) > Abl-2 (context) > Abl-3 (schedule) > Abl-4 (width-depth)
```

---

## 11. Scaling Study

### Scaling Law Evaluation
Systematically evaluate model performance across hidden dimensions to identify compute-optimal configuration.

### Scaling Configurations
| Config ID | Hidden (h) | Layers (d) | Heads | Params | Ctx | LR | Scaling Factor |
|-----------|-----------|-----------|-------|--------|-----|-----|---------------|
| Scale-128 | 128 | 4 | 2 | 0.6M | 12 | 0.004 | 0.09x |
| Scale-256 | 256 | 6 | 4 | 2.1M | 12 | 0.004 | 0.18x |
| Scale-512 | 512 | 8 | 8 | 6.8M | 12 | 0.003 | 0.36x |
| Scale-768 | 768 | 10 | 12 | 14.2M | 12 | 0.002 | 0.55x |
| Scale-1024 | 1024 | 12 | 16 | 24.5M | 12 | 0.002 | 0.73x |
| Scale-1408 | 1408 | 12 | 22 | 18.5M | 12 | 0.002 | 1.00x (reference) |
| Scale-1792 | 1792 | 14 | 28 | 35.8M | 12 | 0.0015 | 1.27x |
| Scale-2432 | 2432 | 16 | 38 | 42.1M | 12 | 0.0015 | 1.73x |
| Scale-3072 | 3072 | 18 | 48 | 67.4M | 12 | 0.001 | 2.18x |
| Scale-3712 | 3712 | 20 | 58 | 93.2M | 12 | 0.001 | 2.64x |

### Scaling Study Protocol
1. **Train each config** for 50K steps on WikiText-103
2. **Measure**: Final BPB, training time, throughput
3. **Fit scaling law**: L(N) = A/N^alpha + L_inf
4. **Identify**: Compute-optimal frontier

### Expected Scaling Behavior
```
Predicted BPB (WikiText-103):
  h=128:   ~2.80 BPB
  h=512:   ~1.85 BPB
  h=1024:  ~1.55 BPB
  h=1408:  ~1.45 BPB
  h=2432:  ~1.30 BPB
  h=3712:  ~1.18 BPB
```

### Scaling Study Runs
```
10 configs * 3 seeds = 30 runs
Estimated compute: ~240 GPU-hours on A100
```

---

## 12. Context Length Study

### Context Window Evaluation
Evaluate how context length affects performance across different model sizes.

### Context Length Configurations
| Config ID | Context | h=512 | h=1408 | h=2432 | Purpose |
|-----------|---------|-------|--------|--------|---------|
| Ctx-2 | 2 | Yes | Yes | Yes | Minimum viable context |
| Ctx-6 | 6 | Yes | Yes | No | Short context |
| Ctx-12 | 12 | Yes | Yes | Yes | Standard (reference) |
| Ctx-20 | 20 | No | Yes | Yes | Extended context |
| Ctx-30 | 30 | No | No | Yes | Long context |

### Context Length Protocol
1. **Sliding window evaluation**: Stride = ctx // 2 for fair comparison
2. **Perplexity by position**: Measure how prediction quality varies across token positions
3. **Attention pattern analysis**: Visualize attention maps at different contexts

### Expected Context Scaling
```
For h=1408 model:
  ctx=2:  BPB ~1.85 (very limited context)
  ctx=6:  BPB ~1.65 (short context)
  ctx=12: BPB ~1.50 (standard)
  ctx=20: BPB ~1.42 (extended)
  ctx=30: BPB ~1.40 (diminishing returns)

Optimal context for h=1408: predicted 16-20 tokens
```

### Context Study Runs
```
10 configs * 3 seeds = 30 runs
Estimated compute: ~180 GPU-hours on A100
```

---

## 13. Implementation Details

### Hardware Requirements
| Resource | Spec | Count |
|----------|------|-------|
| GPU | NVIDIA A100 80GB | 4 |
| CPU | 64 cores | 1 node |
| RAM | 512 GB | 1 node |
| Storage | 2TB NVMe | 1 node |
| Network | InfiniBand | 1 node |

### Software Stack
```yaml
pytorch: "2.3.0"
cuda: "12.1"
transformers: "4.40.0"
datasets: "2.19.0"
accelerate: "0.30.0"
wandb: "0.17.0"
flash-attn: "2.5.8"
triton: "2.3.0"
```

### Experiment Tracking
```python
wandb_config = {
    "project": "trinity-v33-h4",
    "entity": "transformer-research",
    "tags": ["h4", "bpb-target", "wikitext103"],
    "log_model": True,
    "save_code": True,
}
```

### Checkpointing Strategy
- Save every 5,000 steps
- Keep top-3 checkpoints by eval BPB
- Final checkpoint always saved
- Total storage per experiment: ~2GB * 10 checkpoints = 20GB

### Early Stopping Criteria
```python
early_stopping = {
    "patience": 10,           # 10 eval cycles without improvement
    "min_delta": 0.005,       # 0.005 BPB improvement threshold
    "divergence_threshold": 5.0,  # Loss > 5.0 = divergence
    "grad_norm_threshold": 100.0, # Grad norm explosion detection
}
```

---

## 14. Expected Results & Analysis Plan

### Expected Results Summary Table

| Experiment | Expected BPB | Range (3 seeds) | Confidence |
|------------|-------------|-----------------|------------|
| h4-phi3-muon | **1.42** | 1.40 – 1.44 | High |
| h4-l02-lr | **1.48** | 1.46 – 1.50 | Medium |
| h4-360phi3-base | **1.50** | 1.45 – 1.55 (unstable) | Low |
| h4-loop-corr | **1.44** | 1.42 – 1.46 | High |
| h4-e3d3-full | **1.30** | 1.28 – 1.32 | High |
| Baseline-H4 | **1.52** | 1.50 – 1.54 | High |

### Analysis Plan

#### Phase 1: Single-Experiment Analysis (Week 1)
1. **Loss curve inspection**: Smoothness, convergence rate, plateau behavior
2. **BPB trajectory**: Time to reach BPB < 1.50 (if achieved)
3. **Gradient norm analysis**: Stability indicators
4. **Per-seed consistency**: Variance across random seeds

#### Phase 2: Cross-Experiment Comparison (Week 2)
1. **BPB ranking**: Sort all configurations by final BPB
2. **Statistical testing**: Pairwise t-tests vs. Baseline-H4
3. **Convergence speed**: Steps to target BPB
4. **Efficiency frontier**: BPB vs. training compute (FLOPs)

#### Phase 3: Component Importance (Week 3)
1. **Ablation impact ranking**: Which component changes matter most?
2. **Interaction effects**: LR x Optimizer, Width x Context, etc.
3. **Scaling law fit**: N^alpha relationship
4. **Context scaling**: Diminishing returns analysis

#### Phase 4: Synthesis (Week 4)
1. **Best configuration report**: Optimal H4 settings
2. **Scaling recommendations**: Guidance for larger models
3. **Limitations**: What we couldn't answer
4. **Next steps**: Follow-up experiments

### Deliverables
| Deliverable | Format | Timeline |
|-------------|--------|----------|
| Training logs | WandB + local JSON | Real-time |
| Loss curves | PNG/Matplotlib | Weekly |
| BPB comparison table | Markdown | Week 2 |
| Statistical report | Jupyter notebook | Week 3 |
| Final report | PDF + Markdown | Week 4 |

---

## 15. Appendix: Full Configs

### Complete Training Script Config (YAML)
```yaml
# === GLOBAL CONFIG ===
project: trinity-v33-h4
output_dir: ./outputs
seed: 42

# === MODEL ===
model:
  vocab_size: 50257
  max_position_embeddings: 512
  tie_word_embeddings: false
  use_bias: false
  norm_type: rmsnorm
  norm_eps: 1.0e-6
  activation: swiglu
  initializer_range: 0.02
  rope_theta: 10000.0
  use_cache: false

# === TRAINING ===
training:
  max_steps: 50000
  per_device_batch_size: 32
  gradient_accumulation_steps: 4
  gradient_checkpointing: true
  max_grad_norm: 1.0
  dtype: bfloat16
  dataloader_num_workers: 8
  dataloader_pin_memory: true

# === OPTIMIZER ===
optimizer:
  name: adamw  # or muon
  lr: 0.001
  weight_decay: 0.1
  beta1: 0.9
  beta2: 0.95
  eps: 1.0e-8
  muon_lr_scale: null  # Set for MuON experiments

# === LR SCHEDULE (WSD) ===
schedule:
  name: wsd
  warmup_fraction: 0.05
  stable_fraction: 0.75
  decay_fraction: 0.20
  decay_type: cosine
  wsd_decay: 1.0  # Override for h4-loop-corr

# === DATA ===
data:
  dataset: wikitext103
  tokenizer: gpt2
  context_length: 512  # Override per experiment
  stride: 256

# === EVAL ===
eval:
  every: 1000
  datasets:
    - wikitext103
    - c4
  stride: 512
  max_eval_tokens: 1000000

# === CHECKPOINTING ===
checkpoint:
  every: 5000
  keep_top_k: 3
  metric: wikitext103/bpb
  mode: min

# === LOGGING ===
logging:
  use_wandb: true
  project: trinity-v33-h4
  log_every: 100
  watch_model: false
```

### Experiment-Specific Config Overrides

#### h4-phi3-muon.yaml
```yaml
experiment_id: h4-phi3-muon
model:
  hidden_size: 1408
  num_layers: 12
  num_heads: 22
  intermediate_size: 5632
  context_window: 12
training:
  context_length: 12
optimizer:
  name: muon
  lr: 0.0236
  muon_lr_scale: 0.236
```

#### h4-l02-lr.yaml
```yaml
experiment_id: h4-l02-lr
model:
  hidden_size: 1408
  num_layers: 12
  num_heads: 22
  intermediate_size: 5632
  context_window: 12
training:
  context_length: 12
optimizer:
  name: adamw
  lr: 0.000103
```

#### h4-360phi3-base.yaml
```yaml
experiment_id: h4-360phi3-base
model:
  hidden_size: 1408
  num_layers: 12
  num_heads: 22
  intermediate_size: 5632
  context_window: 12
training:
  context_length: 12
optimizer:
  name: adamw
  lr: 0.08506
schedule:
  warmup_fraction: 0.10  # Extended warmup for high LR
```

#### h4-loop-corr.yaml
```yaml
experiment_id: h4-loop-corr
model:
  hidden_size: 1408
  num_layers: 12
  num_heads: 22
  intermediate_size: 5632
  context_window: 12
training:
  context_length: 12
optimizer:
  name: adamw
  lr: 0.0018
schedule:
  wsd_decay: 1.013
```

#### h4-e3d3-full.yaml
```yaml
experiment_id: h4-e3d3-full
model:
  hidden_size: 2432
  num_layers: 16
  num_heads: 38
  intermediate_size: 9728
  context_window: 20
training:
  context_length: 20
optimizer:
  name: muon
  lr: 0.0025
  muon_lr_scale: 0.15
```

### Compute Budget Summary

| Phase | Experiments | Runs | GPU-hours (A100) | Wall Time |
|-------|------------|------|-----------------|-----------|
| Core experiments (5) | 5 configs * 3 seeds | 15 | ~300 | ~3 days |
| Baselines (3) | 3 configs * 3 seeds | 9 | ~180 | ~2 days |
| Ablations | 4 studies * 4 configs * 3 seeds | 48 | ~720 | ~7 days |
| Scaling study | 10 configs * 3 seeds | 30 | ~600 | ~6 days |
| Context study | 10 configs * 3 seeds | 30 | ~450 | ~4 days |
| **TOTAL** | | **132** | **~2250** | **~22 days** |

### Execution Priority
```
P0 (Must run): Core 5 experiments + 3 baselines = 24 runs
P1 (Should run): Optimizer + Schedule ablations = 24 runs
P2 (Nice to have): Scaling + Context studies = 60 runs
P3 (Stretch): Remaining ablations = 24 runs
```

---

## Summary Checklist

- [x] 5 core experiments defined with complete hyperparameter configs
- [x] Dataset selected: WikiText-103 (primary) + C4 (validation)
- [x] Model architectures specified (layers, heads, params)
- [x] Training duration: 50K steps per experiment
- [x] Evaluation metric: BPB with target < 1.50
- [x] Control baselines: 3 baselines (S, M, H4-default)
- [x] Statistical significance: 3 seeds per experiment
- [x] Ablation studies: 4 components (optimizer, context, schedule, width-depth)
- [x] Scaling study: h=128 to h=3712 (10 configs)
- [x] Context length study: ctx=2 to ctx=30 (5 configs)
- [x] Implementation details: hardware, software, tracking
- [x] Analysis plan: 4-phase analysis over 4 weeks
- [x] Compute budget: ~2250 GPU-hours total
- [x] Execution priority: P0-P3 prioritization

---

*Document version: 1.0*  
*Protocol status: Ready for execution*  
*Next step: Initialize training infrastructure and launch P0 experiments*
