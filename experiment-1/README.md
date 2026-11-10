# Experiment 1 supplement for S8

This supplement accompanies Table 5.1 and Sections 6.5 and 6.8 of *Large Language Models in Linux Security Maintenance*. S8 (`VM_S8`) is the Debian kernel maintenance task that requires package installation followed by a separate reboot.

| Configuration | Frozen definition | Exact S8 system prompt | Cumulative addition |
| --- | --- | --- | --- |
| B0 | [b0.yaml](controls/b0.yaml) | [B0](prompts/B0-system.txt) | Minimal maintenance prompt with the common policy, assessment contract, bounded tools, and limits. |
| B1 | [b1.yaml](controls/b1.yaml) | [B1](prompts/B1-system.txt) | Structured workflow for observation, assessment, action, and reporting. |
| B2 | [b2.yaml](controls/b2.yaml) | [B2](prompts/B2-system.txt) | Fixed maintenance runbook and selected Debian notes. |
| B3 | [b3.yaml](controls/b3.yaml) | [B3](prompts/B3-system.txt) | A structured plan and deterministic authorization before dispatch. |
| B4 | [b4.yaml](controls/b4.yaml) | [B4](prompts/B4-system.txt) | Automatic verification after dispatch and enforced stopping after failed or unknown checks. |

Compare adjacent system prompts to see the additions. Each configuration received the same [initial user task](prompts/shared-task.txt) and [S8 policy](S8-policy.yaml). The B3 and B4 system prompts, initial user task, and policy match their counterparts in the original groups of [Experiment 2](../README.md#experiment-2-supplement-for-s8).

## Generation inputs

The definitions, their [prompt fragments](controls/prompts/), and the S8 policy are verbatim files from the Experiment 1 main freeze `glm-main-20261013-v1`. The exact assembled system and task prompts were reconstructed with the frozen prompt builder and checked against the saved initial messages for every selected S8 run. The assembled prompt files preserve the original line breaks and absence of a trailing newline.

The generation manifest's content SHA-256 is `ff1fe3f88a37eb534c879242860e30cda7a3a0c91cad7f8aa45cd8f9617a297b`. The S8 policy SHA-256 is `e59a182143671815281aba4603a0d193b523cb53ba3c0140b827a6c8313fdcc0`. The frozen generation source includes the earlier `structured-v9` evaluator.

## Reported scoring

[Scoring rules and source excerpts](scoring-v10.md) document first INITIAL correctness, prohibited dispatch, and compliant completion. They use the separate post-collection `structured-v10` analysis archive that supplied the thesis results. The surrounding prose and the configuration table are explanatory.
