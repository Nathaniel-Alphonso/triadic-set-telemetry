#!/usr/bin/env python3
"""calibrate_triadic_v7.py -- Baseline activation telemetry for the v29.6
z-score Tier D gate and the v29.7 entropy-gated Tier A clamp.

CHANGES vs v6:
  1. Emits std_mean / sigma_std per layer -- the distributional parameters
     the v29.6 evaluator's Tier D gate consumes (delta > 3*sigma_std).
     These are computed from the FULL sampled distribution of decode-step
     stds (true np.std), not the p99/2.326 derivation.
  2. Adds a CODE domain (raw HumanEval-style completion prompts, no chat
     template -- matching how evaluate_triadic_v29 runs HumanEval with
     apply_chat_template=False). Domain-split stats are exported under
     'decode_stats' per layer so a per-task config can be built.
  3. Self-check upgraded to test the ACTUAL v29.6 gate: reports the 3-sigma
     z-score fire rate per layer per domain. Every layer should show ~<=1%
     on healthy decode steps.

v7.1:
  4. Emits ent_mean / ent_sigma in the embed_tokens section -- the mean and
     spread of the per-decode-step EMBEDDING ENTROPY distribution, consumed
     by the v29.7 evaluator's Tier A gate (clamp fires only when
     (entropy - ent_mean) > 3 * ent_sigma). Per-domain entropy stats are
     exported under embed_tokens['entropy_stats'].
  5. Self-check extended to the Tier A gate: 3-sigma embedding-entropy fire
     rate per domain must be <=2% on healthy decode steps.
"""

import json
import torch
import numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset

# ==========================================
# CONFIG
# ==========================================
MODEL_ID = "meta-llama/Llama-3.2-1B-Instruct"
NUM_MATH_PROMPTS = 20      # GSM8K
NUM_MMLU_PROMPTS = 20      # MMLU-style questions
NUM_PROSE_PROMPTS = 10     # plain prose
NUM_CODE_PROMPTS = 20      # HumanEval-style raw completions
DECODE_STEPS = 256         # greedy generation length for decode-phase stats
OUTPUT_PATH = "triadic_layer_config.json"

SAMPLE_MMLU_QUESTIONS = [
    "What is the primary function of the mitochondria in a eukaryotic cell?",
    "Which economic policy involves government spending to stimulate demand during a recession?",
    "In constitutional law, what does the 'due process' clause guarantee?",
    "Which programming paradigm treats computation as the evaluation of mathematical functions?",
    "What is the chemical formula of the compound responsible for ocean acidification?",
    "Who authored 'The Wealth of Nations', and what economic system did it defend?",
    "What does Heisenberg's uncertainty principle state about position and momentum?",
    "Which psychological disorder is characterized by persistent deficits in social communication?",
    "What was the primary cause of the 1929 stock market crash?",
    "In statistics, what does a p-value below 0.05 conventionally indicate?",
    "What is the difference between meiosis and mitosis?",
    "Which philosopher wrote 'Critique of Pure Reason'?",
    "What is the time complexity of binary search on a sorted array?",
    "Which hormone regulates blood sugar levels in the human body?",
    "What treaty formally ended World War I?",
    "What is the function of the Federal Reserve's interest rate policy?",
    "Which gas makes up approximately 78% of Earth's atmosphere?",
    "What distinguishes civil law from common law legal systems?",
    "What is the mass-energy equivalence equation, and who derived it?",
    "Which cognitive bias describes relying too heavily on the first piece of information encountered?",
]

SAMPLE_PROSE_PROMPTS = [
    "Write a short paragraph describing a quiet morning in a coastal village.",
    "Explain why people enjoy gardening, in a few sentences.",
    "Describe the atmosphere of a library in the late afternoon.",
    "Summarize the appeal of long-distance running to a curious beginner.",
    "Write a brief note about the smell of rain on dry earth.",
    "Describe an old bookstore from the perspective of a first-time visitor.",
    "Explain, in plain language, why the ocean appears blue.",
    "Write a few sentences about the sound of a train passing at night.",
    "Describe what makes a good cup of coffee.",
    "Write a short reflection on the changing colors of autumn leaves.",
]

# Raw HumanEval-style completion prompts (apply_chat_template=False regime).
SAMPLE_CODE_PROMPTS = [
    "from typing import List\n\n\ndef has_close_elements(numbers: List[float], threshold: float) -> bool:\n    \"\"\" Check if in given list of numbers, are any two numbers closer to each other than\n    given threshold.\n    >>> has_close_elements([1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.3) == True\n    \"\"\"\n",
    "\n\ndef truncate_number(number: float) -> float:\n    \"\"\" Given a positive floating point number, it can be decomposed into\n    and integer part (largest integer smaller than given number) and decimals\n    (leftover part always smaller than 1)\n    >>> truncate_number(3.5)\n    0.5\n    \"\"\"\n",
    "from typing import List\n\n\ndef separate_paren_groups(paren_string: str) -> List[str]:\n    \"\"\" Input to this function is a string containing multiple groups of nested parentheses. Your goal is to\n    separate those group into separate strings.\n    >>> separate_paren_groups('( ) (( )) (( )( ))') == ['()', '(())', '(()())']\n    \"\"\"\n",
    "\n\ndef is_palindrome(string: str) -> bool:\n    \"\"\" Test if given string is a palindrome \"\"\"\n",
    "\n\ndef encode_cyclic(s: str):\n    \"\"\"\n    returns encoded string by cycling groups of three characters.\n    \"\"\"\n    # split string to groups. Each of length 3.\n    groups = [s[(3 * i):min((3 * i + 3), len(s))] for i in range((len(s) + 2) // 3)]\n    # cycle elements in each group. Unless it has one element.\n    groups = [(group[0:-1] + group[-1:]) if len(group) == 3 else group for group in groups]\n    return ''.join(groups)\n\n\ndef decode_cyclic(s: str):\n    \"\"\"\n    takes as input a string encoded with encode_cyclic function. Returns the decoded string.\n    \"\"\"\n",
    "from typing import List\n\n\ndef below_zero(operations: List[int]) -> bool:\n    \"\"\" You're given a list of deposit and withdrawal operations on a bank account that starts with\n    zero balance. Your task is to detect if at any point the balance of account falls below zero.\n    >>> below_zero([1, 2, 3]) == False\n    \"\"\"\n",
    "\n\ndef search(lst):\n    '''\n    You are given a non-empty list of positive integers. Return the greatest integer that is greater than \n    zero, and has a frequency greater than or equal to the value of the integer itself. \n    The frequency of an integer is the number of times it appears in the list.\n    '''\n",
    "def circular_shift(x, shift):\n    \"\"\"Circular shift the digits of the integer x, shift the digits right by shift\n    and return the result as a string.\n    >>> circular_shift(12, 1) == '21'\n    \"\"\"\n",
    "def triangle_area(a, b, c):\n    '''\n    Given the lengths of the three sides of a triangle. Return the area of\n    the triangle rounded to 2 decimal points if the three sides form a valid triangle. \n    Otherwise return -1\n    '''\n",
    "def smallest_change(arr):\n    \"\"\"\n    Given an array arr of integers, find the minimum number of elements that\n    need to be changed to make the array palindromic.\n    \"\"\"\n",
    "def search_min_diff(ls):\n    '''\n    Given a list of numbers, find the minimum difference between any two elements.\n    '''\n",
    "def count_upper(s):\n    \"\"\"\n    Given a string s, count the number of upper-case characters in it.\n    \"\"\"\n",
    "def sum_squared_errors(y, y_hat):\n    \"\"\"\n    Given two lists of numbers, return the sum of squared errors between them.\n    \"\"\"\n",
    "def rolling_max(numbers):\n    \"\"\"\n    From a given list of integers, generate a list of rolling maximum element found until given moment\n    in the sequence.\n    \"\"\"\n",
    "def is_happy(s):\n    \"\"\"\n    You are given a string s. Your task is to check if the string is happy or not.\n    A string is happy if its length is at least 3 and every 3 consecutive letters are distinct\n    \"\"\"\n",
    "def numerical_letter_grade(grades):\n    \"\"\"The last week of semester is coming. Teacher already gave the grades. Return the grade letters.\n    \"\"\"\n",
    "def solve(N):\n    \"\"\"\n    Given a positive integer N, return the total sum of its digits in binary.\n    \"\"\"\n",
    "def anti_shuffle(s):\n    \"\"\"\n    Given a string s, return a new string where each word is alphabetically sorted\n    but the words appear in the original order.\n    \"\"\"\n",
    "def compare_one(a, b):\n    \"\"\"\n    Given two values, compare them and return the larger one.\n    \"\"\"\n",
    "def count_nums(arr):\n    \"\"\"\n    Given an array of integers, count how many of them have a digits sum greater than 0.\n    \"\"\"\n",
]


# ==========================================
# METRICS
# ==========================================
def compute_l1_entropy(x_fp32: torch.Tensor) -> torch.Tensor:
    """Spatial entropy from L1-normalized absolute magnitudes."""
    abs_x = torch.abs(x_fp32)
    p_x = abs_x / (torch.sum(abs_x, dim=-1, keepdim=True) + 1e-9)
    return -torch.sum(p_x * torch.log2(torch.clamp(p_x, min=1e-9)), dim=-1)


def phase_stats(x_fp32: torch.Tensor, phase: str, ledger):
    std_dev = torch.std(x_fp32, dim=-1)
    mean = torch.mean(x_fp32, dim=-1)
    density = (x_fp32 > 0).float().mean(dim=-1) * 100.0
    entropy = compute_l1_entropy(x_fp32)

    for key, tensor in (("std_dev", std_dev), ("mean", mean),
                        ("density", density), ("entropy", entropy)):
        for v in tensor.flatten().tolist():
            ledger[phase][key].append(v)


# ==========================================
# HOOKS
# ==========================================
def generate_calibration_hook(key_name, ledger, inspect_input=False):
    def hook(module, input, output):
        if inspect_input and input:
            x = input[0]
        else:
            x = output[0] if isinstance(output, tuple) else output

        x_fp32 = x.to(torch.float32).detach()
        if x_fp32.dim() != 3:
            return

        bsz, seq_len, _ = x_fp32.shape
        if seq_len > 1:
            phase_stats(x_fp32, "prefill", ledger[key_name])
        else:
            phase_stats(x_fp32, "decode", ledger[key_name])
    return hook


# ==========================================
# CORPUS ASSEMBLY
# ==========================================
def build_corpus(tokenizer):
    """Returns a list of (domain_tag, prompt_text, use_chat_template)."""
    prompts = []

    print(f"Streaming GSM8K calibration prompts ({NUM_MATH_PROMPTS})...")
    gsm = load_dataset("openai/gsm8k", "main", split=f"train[:{NUM_MATH_PROMPTS}]")
    for item in gsm:
        prompts.append(("math", item["question"], True))

    print(f"Adding MMLU-style questions ({NUM_MMLU_PROMPTS})...")
    for q in SAMPLE_MMLU_QUESTIONS[:NUM_MMLU_PROMPTS]:
        prompts.append(("mmlu", q, True))

    print(f"Adding prose prompts ({NUM_PROSE_PROMPTS})...")
    for p in SAMPLE_PROSE_PROMPTS[:NUM_PROSE_PROMPTS]:
        prompts.append(("prose", p, True))

    print(f"Adding code completion prompts ({NUM_CODE_PROMPTS})...")
    for c in SAMPLE_CODE_PROMPTS[:NUM_CODE_PROMPTS]:
        # v7: HumanEval runs with apply_chat_template=False (raw completion),
        # so code-domain calibration must match that regime exactly.
        prompts.append(("code", c, False))

    return prompts


# ==========================================
# CALIBRATION LOOP
# ==========================================
def run_calibration_loop():
    print(f"Initializing Unmodified {MODEL_ID} Calibration "
          f"(v7: z-score params + code domain)...")
    device = "cuda" if torch.cuda.is_available() else "mps"
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID).to(device)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    tokenizer.pad_token = tokenizer.eos_token

    keys = ["embed_tokens"] + [f"layer_{i}" for i in range(16)] + ["lm_head"]
    ledger = {k: {"prefill": {'std_dev': [], 'mean': [], 'density': [], 'entropy': []},
                  "decode":  {'std_dev': [], 'mean': [], 'density': [], 'entropy': []}}
              for k in keys}
    # v7: per-domain decode stds, for the z-score gate parameters
    domain_ledger = {k: {d: [] for d in ("math", "mmlu", "prose", "code")}
                     for k in keys}
    # v7.1: per-domain decode-step EMBEDDING ENTROPY, for the Tier A gate
    # (embed_tokens only -- the v29.7 clamp lives at the embedding perimeter).
    domain_entropy_ledger = {"embed_tokens": {d: [] for d in ("math", "mmlu", "prose", "code")}}
    hooks = []

    # Capture decode-phase std per domain: the hook reads the CURRENT domain
    # from a mutable cell.
    current_domain = ["math"]

    def make_domain_hook(key_name, track_entropy=False, inspect_input=True):
        def hook(module, input, output):
            # v7.1 FIX: embed_tokens' INPUT is the integer token-id tensor
            # (bsz, seq_len -- 2-D), NOT the embedding. The original v7.1
            # telemetry hook read input[0] for every module, so the
            # embed_tokens domain/entropy ledgers stayed EMPTY: ent_mean /
            # ent_sigma were never emitted, the Tier A self-check passed
            # VACUOUSLY (no rows printed, no alarms), and the he-tri164-aZg-v297
            # run executed with Tier A detection-only. Layer hooks keep
            # reading the input (the hidden state feeding input_layernorm);
            # embed_tokens must read its OUTPUT.
            x = (input[0] if inspect_input else
                 (output[0] if isinstance(output, tuple) else output))
            x_fp32 = x.to(torch.float32).detach()
            if x_fp32.dim() != 3 or x_fp32.shape[1] != 1:
                return
            domain_ledger[key_name][current_domain[0]].append(
                float(torch.std(x_fp32, dim=-1).mean().item())
            )
            # v7.1: same Ledger H(X) the evaluator's Tier A detector computes,
            # on the RAW embedding output (diagnosis before treatment).
            if track_entropy:
                domain_entropy_ledger[key_name][current_domain[0]].append(
                    float(compute_l1_entropy(x_fp32).squeeze(-1).mean().item())
                )
        return hook

    h_embed = model.model.embed_tokens.register_forward_hook(
        generate_calibration_hook("embed_tokens", ledger, inspect_input=False))
    hooks.append(h_embed)
    hooks.append(model.model.embed_tokens.register_forward_hook(
        make_domain_hook("embed_tokens", track_entropy=True, inspect_input=False)))

    for i in range(16):
        target = model.model.layers[i].input_layernorm
        hooks.append(target.register_forward_hook(
            generate_calibration_hook(f"layer_{i}", ledger, inspect_input=True)))
        hooks.append(target.register_forward_hook(
            make_domain_hook(f"layer_{i}")))

    h_lm_head = model.lm_head.register_forward_hook(
        generate_calibration_hook("lm_head", ledger, inspect_input=False))
    hooks.append(h_lm_head)

    prompts = build_corpus(tokenizer)

    print(f"Running {len(prompts)} prompts x (prefill + {DECODE_STEPS} decode steps)...")
    for p_idx, (domain, prompt_text, use_template) in enumerate(prompts):
        current_domain[0] = domain
        if use_template:
            formatted = tokenizer.apply_chat_template(
                [{"role": "user", "content": prompt_text}],
                tokenize=False,
                add_generation_prompt=True
            )
        else:
            formatted = prompt_text
        inputs = tokenizer(formatted, return_tensors="pt", truncation=True).to(device)
        with torch.no_grad():
            model(**inputs)
            model.generate(
                **inputs,
                max_new_tokens=DECODE_STEPS,
                do_sample=False,
                pad_token_id=tokenizer.pad_token_id,
                use_cache=True,
            )
        if (p_idx + 1) % 10 == 0:
            print(f"  {p_idx + 1}/{len(prompts)} prompts calibrated.")

    for h in hooks:
        h.remove()

    # ---------------------------------------------------------
    # COMPILE LEDGER: per-phase baselines + v7 z-score parameters
    # ---------------------------------------------------------
    print("Compiling Baseline Telemetry Configuration Ledger "
          "(phase-split + z-score params)...")
    layer_config = {}
    for key_name, phases in ledger.items():
        entry = {}
        for phase, metrics in phases.items():
            if not metrics['std_dev']:
                continue
            entry[phase] = {
                "sigma_baseline": float(np.mean(metrics['std_dev'])),
                "mu_baseline": float(np.mean(metrics['mean'])),
                "natural_density": float(np.mean(metrics['density'])),
                "spatial_entropy": float(np.mean(metrics['entropy'])),
                "tau_perimeter": float(np.mean(metrics['std_dev']) * 0.15),
                "n_samples": len(metrics['std_dev']),
            }
        dec = entry.get("decode", entry.get("prefill", {}))
        entry.update(dec)

        # v7: z-score gate parameters per layer/module. std_mean and
        # sigma_std describe the distribution of per-decode-step stds
        # ACROSS ALL DOMAINS (merged). Domain-split stats go under
        # 'decode_stats' for per-task config building.
        all_dec = domain_ledger[key_name]
        merged = [v for dom in all_dec.values() for v in dom]
        if merged:
            mu = float(np.mean(merged))
            sigma_std = float(np.std(merged))
            # Floor: a degenerate distribution must not produce a
            # zero-width gate. 1% of mu, matching the evaluator's
            # get_d_calibration_summary guard.
            sigma_std = max(sigma_std, mu * 0.01)
            entry["std_mean"] = mu
            entry["sigma_std"] = sigma_std
            entry["decode_stats"] = {
                dom: {
                    "std_mean": (float(np.mean(v)) if v else None),
                    "sigma_std": (max(float(np.std(v)), float(np.mean(v)) * 0.01)
                                  if v else None),
                    "n_samples": len(v),
                }
                for dom, v in all_dec.items()
            }

        # v7.1: Tier A gate parameters. ent_mean / ent_sigma describe the
        # distribution of per-decode-step embedding entropy (the Ledger's
        # H(X) over the L1-normalized embedding magnitudes). The v29.7
        # evaluator registers a fault AND applies its 3-sigma tensor clamp
        # only when (entropy - ent_mean) > 3 * ent_sigma; without these
        # keys Tier A runs detection-only on the legacy static threshold.
        if key_name == "embed_tokens":
            ent_all = domain_entropy_ledger[key_name]
            ent_merged = [v for dom in ent_all.values() for v in dom]
            if ent_merged:
                ent_mu = float(np.mean(ent_merged))
                ent_sigma = max(float(np.std(ent_merged)), ent_mu * 0.01)
                entry["ent_mean"] = ent_mu
                entry["ent_sigma"] = ent_sigma
                entry["entropy_stats"] = {
                    dom: {
                        "ent_mean": (float(np.mean(v)) if v else None),
                        "ent_sigma": (max(float(np.std(v)), float(np.mean(v)) * 0.01)
                                     if v else None),
                        "n_samples": len(v),
                    }
                    for dom, v in ent_all.items()
                }
        layer_config[key_name] = entry

    # ---------------------------------------------------------
    # SELF-CHECK: does the v29.6 z-score gate misfire on healthy steps?
    # ---------------------------------------------------------
    print("\n=== CALIBRATION SELF-CHECK (v29.6 Tier D + v29.7 Tier A gate fire rates) ===")
    print(f"{'module':<14} {'domain':<7} {'mu':>9} {'3sig trigger':>13} "
          f"{'fire%':>7} status")
    print("-" * 66)

    alarms = []

    for key_name in [f"layer_{i}" for i in range(16)]:
        for dom, vals in domain_ledger[key_name].items():
            if not vals:
                continue
            mu = float(np.mean(vals))
            s = max(float(np.std(vals)), mu * 0.01)
            trigger = mu + 3.0 * s
            rate = 100.0 * sum(1 for v in vals if v > trigger) / len(vals)
            status = "OK" if rate <= 2.0 else "ALARM"
            if rate > 2.0:
                alarms.append(f"{key_name}/{dom}")
            print(f"{key_name:<14} {dom:<7} {mu:>9.5f} {trigger:>13.5f} "
                  f"{rate:>6.1f}% {status}")

    # v7.1: Tier A gate self-check -- the v29.7 embedding-entropy z-score
    # must stay silent on healthy decode steps, exactly like Tier D's.
    # GUARD FIRST: an EMPTY entropy ledger must fail loudly, not pass
    # silently. This exact silent-empty condition shipped the
    # detection-only aZg-v297 run (hook read token IDs instead of the
    # embedding output), so it is a hard failure here, never a pass.
    if not any(domain_entropy_ledger["embed_tokens"].values()):
        print("SELF-CHECK FAILED: embed_tokens entropy telemetry is EMPTY.")
        print("  The Tier A gate cannot emit ent_mean/ent_sigma. This is a")
        print("  bug in the telemetry path, not a pass.")
        alarms.append("embed_tokens-entropy/NO-TELEMETRY")
    for dom, vals in domain_entropy_ledger["embed_tokens"].items():
        if not vals:
            continue
        mu = float(np.mean(vals))
        s = max(float(np.std(vals)), mu * 0.01)
        trigger = mu + 3.0 * s
        rate = 100.0 * sum(1 for v in vals if v > trigger) / len(vals)
        status = "OK" if rate <= 2.0 else "ALARM"
        if rate > 2.0:
            alarms.append(f"embed_tokens-entropy/{dom}")
        print(f"{'embed_tokens':<14} {dom:<7} {mu:>9.5f} {trigger:>13.5f} "
              f"{rate:>6.1f}% {status}  (Tier A entropy gate)")

    print("-" * 66)
    if alarms:
        print(f"SELF-CHECK FAILED for: {', '.join(alarms)}")
        print("The 3-sigma gate fires on >2% of healthy steps for these "
              "layer/domain pairs. Widen the sample (more prompts/steps) or "
              "raise the multiplier before trusting the gate.")
    else:
        print("SELF-CHECK PASSED: 3-sigma gate fires on <=2% of healthy "
              "decode steps for every layer/domain.")
    print("=" * 66)

    layer_config["_meta"] = {
        "calibrator_version": "v7.1",
        "model_id": MODEL_ID,
        "n_math_prompts": NUM_MATH_PROMPTS,
        "n_mmlu_prompts": NUM_MMLU_PROMPTS,
        "n_prose_prompts": NUM_PROSE_PROMPTS,
        "n_code_prompts": NUM_CODE_PROMPTS,
        "decode_steps": DECODE_STEPS,
        "phases_recorded": ["prefill", "decode"],
        "domains_recorded": ["math", "mmlu", "prose", "code"],
        "gate_formula": "fire when (std - std_mean) > 3 * sigma_std",
        "tier_a_gate_formula": "embed_tokens: fire when (entropy - ent_mean) > 3 * ent_sigma",
        "layer_0_note": "layer_0 stats duplicate embed_tokens by construction "
                        "(input_layernorm input == embedding output).",
        "self_check_alarms": alarms,
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(layer_config, f, indent=4)
    print(f"\nCalibration Ledger Exported: {OUTPUT_PATH}")
    print("Top-level std_mean/sigma_std = merged across domains (default gate).")
    print("Per-domain z-score params under 'decode_stats' for per-task configs.")
    print("embed_tokens now carries ent_mean/ent_sigma (v29.7 Tier A clamp gate);")
    print("per-domain entropy params under embed_tokens['entropy_stats'].")


if __name__ == "__main__":
    run_calibration_loop()