# Experiment 2 supplement for S8

This supplement accompanies §§5.8 and 6.13 of *Large Language Models in Linux Security Maintenance*. S8 (`VM_S8`) is the kernel maintenance scenario with separate package installation and reboot actions.

## Compare the model-facing prompts

| Configuration | Original system prompt | Revised system prompt |
| --- | --- | --- |
| B3 | [Original B3](prompts/original-B3-system.txt) | [Revised B3](prompts/revised-B3-system.txt) |
| B4 | [Original B4](prompts/original-B4-system.txt) | [Revised B4](prompts/revised-B4-system.txt) |

Compare across each row to see the treatment described in §5.8. All four groups received the same [task prompt](prompts/shared-task.txt) as the initial user message. The five text files contain the exact UTF-8 prompt strings, including their original line breaks and absence of a trailing newline.

## Inspect the policy, schema, and implementation

| File | Contents |
| --- | --- |
| [S8-policy.yaml](S8-policy.yaml) | Verbatim frozen scenario policy, including the permitted transaction effects and reboot trigger. |
| [submit_decision.json](submit_decision.json) | Frozen tool definition, formatted as standalone JSON. The definition is identical in original-B3, revised-B3, original-B4, and revised-B4. |
| [Validation feedback](code/validation-feedback.md) | Verbatim excerpts showing the shared rejection path and the extra structured diagnostic in the revised interface. |
| [Proposal admissibility](code/proposal-admissibility.md) | Verbatim excerpts showing how the frozen `structured-v10` evaluator classified action proposals. |

The prose in this README and around the code blocks is explanatory. The offline score regeneration and replay in §6.13 used the private frozen archive.

## Frozen provenance

The inputs come from the main campaign `experiment-2-main-v1` in the `experiment-2-20261104-v1` freeze. The campaign manifest's content SHA-256 is `88bef69aacf1282b4892a1d71775587e3e759cdf89149e6bb4c92c22b8e471d7`. The prompt strings and tool definition were extracted from the manifest-verified `interface-inputs.json` (SHA-256 `16e401ef2b9ff9902ea6aa2d295969c9674ef2dd6c76e7d576fd97832c0edf0d`). The policy has SHA-256 `e59a182143671815281aba4603a0d193b523cb53ba3c0140b827a6c8313fdcc0`. Each excerpt page lists the original line ranges and the SHA-256 digests of the verified source files.
