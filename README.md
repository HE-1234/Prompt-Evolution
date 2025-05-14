# Prompt Evolution

**Prompt Evolution** is the official repository for the MSR 2025 (co-located with ICSE 2025) paper *“Prompting in the Wild: An Empirical Study of Prompt Evolution in Software Repositories.”* This work presents the first large-scale empirical analysis of how prompts are **managed and evolved** in LLM-integrated software development. Prompts serve as the primary interface between software applications and Large Language Models (LLMs), yet there has been limited understanding of *how developers iteratively refine these prompts over time*. In this study, we analyzed **1,262 prompt changes** across **243 GitHub repositories** to uncover patterns in prompt modifications, their relationships with code changes, documentation practices, and impacts on system behavior.

Our findings show that developers most often evolve prompts through **additions of new instructions or examples and modifications to existing prompt content**, with the majority of prompt changes occurring alongside new feature development. However, prompt changes are **rarely documented** in commit messages (only about 21.9% include any prompt-related notes), and they can introduce **logical inconsistencies** or misalignments between the prompt and the LLM’s expected behavior. These insights highlight the need for better tooling in LLM-based software – such as specialized testing frameworks, automated validation tools, and improved documentation practices – to ensure prompt changes do not degrade the reliability of LLM-integrated applications.

This repository provides the **code and data** used in our analysis of prompt evolution. Researchers and practitioners can use this to replicate our study or to explore prompt engineering practices in their own projects. Below we detail how to set up the project, the repository structure, and key results from the study, including tables and figures illustrating the types of prompt changes, their frequencies, common reasons, and examples of evolution patterns.

## Installation and Setup

To use the code in this repository, please ensure you have **Python 3.8+** installed. We recommend creating a virtual environment and installing the required dependencies. You can install the necessary packages via pip:

```bash
pip install openai pandas gitpython
```

**Dependencies:**

* `openai`
* `pandas`
* `gitpython`
* `json`, `csv`, `importlib`, `re`, `os`, `traceback`, `ast` (Python standard libraries)
* `qa_prompts.py` (custom module in this repo)

If you're running LLM-related tasks, ensure your OpenAI API key is set (e.g., via `OPENAI_API_KEY`).

## Repository Structure

```
├── prompt-finder/            # Utilities for identifying and extracting prompts
├── analyze.ipynb             # Main analysis notebook generating tables/figures
├── repo_analysis.ipynb       # Maps prompt changes to maintenance activities
├── clean_analysis.ipynb      # Preprocessing and filtering
├── data_cleaner.ipynb        # Additional data filtering/cleaning
├── detect_changes.py         # Diffs prompt changes and classifies edits
├── check-inconsistency.py    # Detects logical inconsistencies in prompts
├── qa_prompts.py             # Prompt component definitions and utilities
```

## Results

### Table I: Categories of Prompt Changes, Definitions, and Frequencies

| **Change Category**     | **Change Type** | **Definition**                                   | **Frequency** | **Percentage** |
| ----------------------- | --------------- | ------------------------------------------------ | ------------: | -------------: |
| *Component-dependent*   | Addition        | New instruction/example added                    |           440 |          30.1% |
|                         | Modification    | Semantic/behavioral change to existing component |           373 |          25.5% |
|                         | Removal         | Removal of component                             |           129 |           8.8% |
| *Component-independent* | Rephrase        | Semantics unchanged, language reworded           |           254 |          17.4% |
|                         | Formatting      | Aesthetic/template changes                       |           116 |           7.9% |
|                         | Correction      | Fixing typos/grammar                             |            71 |           4.9% |
|                         | Generalization  | Replace specifics with placeholders              |            34 |           2.3% |
|                         | Restructure     | Reorganize components without adding/removing    |            29 |           2.0% |
| *Uncategorized*         | -               | Unique/ambiguous                                 |            17 |           1.1% |
| **Total**               |                 |                                                  |      **1463** |       **100%** |

### Table II: Frequency of Edits on Each Prompt Component

| **Prompt Component**   | **Addition (%)** | **Modification (%)** | **Removal (%)** | **Change Frequency** | **% of Total** |
| ---------------------- | ---------------- | -------------------- | --------------- | -------------------- | -------------: |
| Consideration          | 51.1%            | 35.7%                | 13.2%           | 569                  |         60.40% |
| Additional Information | 36.0%            | 27.9%                | 36.0%           | 154                  |         16.35% |
| Output Instruction     | 25.9%            | 71.4%                | 2.7%            | 112                  |         11.89% |
| Example                | 44.0%            | 46.7%                | 9.3%            | 75                   |          7.96% |
| Role                   | 13.3%            | 73.3%                | 13.3%           | 30                   |          3.18% |
| Directive              | 0.0%             | 100.0%               | 0.0%            | 2                    |          0.21% |

### Table III: Reasons for Prompt Changes

| **Category**                  | **Count** |
| ----------------------------- | --------: |
| Task-Specific Change          |        40 |
| Typo Fix & Grammar Correction |         7 |
| Output Modification           |         5 |
| Template Update               |         3 |
| Technology Change/Adaptation  |         3 |
| Reformat Prompt Structure     |         2 |
| Handle Hallucination          |         2 |

### Table IV: Inconsistencies Introduced by Prompt Changes

| **Category**                 | **Count** |
| ---------------------------- | --------: |
| Contradictory Considerations |         8 |
| Structural Conflict          |         4 |
| Format Misalignment          |         3 |

### Figures

Add the following figures (make sure they are in the repo `assets/` folder):

* ![](assets/figure_heatmap.png) — *Prompt co-change heatmap*
* ![](assets/figure_component_by_activity.png) — *Component-level changes by maintenance activity*
* ![](assets/figure_independent_by_activity.png) — *Independent changes by maintenance activity*

## Citation

If you use this dataset or build upon this work, please cite our paper:

> Mahan Tafreshipour, Aaron Imani, Eric Huang, Eduardo Almeida, Thomas Zimmermann, Iftekhar Ahmed. "Prompting in the Wild: An Empirical Study of Prompt Evolution in Software Repositories." In Proceedings of the 20th International Conference on Mining Software Repositories (MSR 2025). [arXiv:2411.04299](https://arxiv.org/abs/2411.04299)

```bibtex
@inproceedings{PromptingInTheWild2025,
  author    = {Mahan Tafreshipour and Aaron Imani and Eric Huang and Eduardo Almeida and Thomas Zimmermann and Iftekhar Ahmed},
  title     = {Prompting in the Wild: An Empirical Study of Prompt Evolution in Software Repositories},
  booktitle = {Proceedings of the 20th Intl. Conf. on Mining Software Repositories (MSR)},
  year      = {2025},
  note      = {Co-located with ICSE 2025, Lisbon},
  url       = {https://arxiv.org/abs/2411.04299}
}
```

## License

This repository is licensed under the **MIT License**. Feel free to use, modify, and distribute it with attribution.

---

For questions or collaborations, feel free to open an issue or contact us via the GitHub repository.
