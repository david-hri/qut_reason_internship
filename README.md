# Symbolic-Agentic Reasoning Framework

This repository contains the implementation of a hybrid architecture combining symbolic reasoning with large language models (LLMs). The approach is developed and evaluated in the research paper:

**Improving Reasoning in Large Language Models: A Symbolic-Agentic Hybrid Approach**  
David Houri, Queensland university of technology

## Overview

Recent developments in LLMs have shown promising performance in natural language understanding and generation. However, these models still face critical limitations such as hallucinations and lack of logical consistency in multi-step reasoning tasks.

This work introduces a hybrid reasoning framework that integrates:
- A symbolic module, based on rule-based logical inference
- An agentic LLM, capable of interacting with the symbolic layer to generate verifiable, explainable outputs

The objective is to enhance both the reasoning accuracy and interpretability of LLM responses in tasks requiring structured logic.

## Architecture

The system consists of three main components:

- **Retriever**: Selects relevant subgraphs and context from a document corpus, using Retrieval-Augmented Generation (RAG) techniques. Extracted context is represented as symbolic facts and candidate rules.
- **Symbolic Reasoning Module**: Based on a Prolog-style logic engine (using [pytholog](https://github.com/AlvinChristianson/pytholog)), it performs first-order logical inference over the extracted rules and facts.
- **LLM Generator**: A frozen LLM receives the original query and the output of the reasoning module, and generates a final response constrained by the logical structure.

## Use Cases

The system has been tested across several domains:
- Medical reasoning (diagnosis based on symptoms and medical rules)
- Legal reasoning (eligibility for transport refunds, employment law)
- Administrative logic (rights related to housing or contracts)
- Structured factual justification (legal, regulatory, or technical questions)

Examples are available in `tests/test_symbolic_ai/`.


## Running the System

1. Clone the repository
2. Set up the Python environment:
    pip install -r requirements.txt  
3. Add your OpenAi API key on a api_key.txt file
4. Execute the reasoning module:


python tests/test_symbolic_ai/main.py

The reasoning input (pdf of the rules and different prompts) can be modified via the corresponding files in test_symbolic_ai.


## Evaluation 
The goal of the system is to evaluate the framework on the RuleArena benchmark, which includes rule-intensive tasks from real-world domains such as:

- Airline refund policies

- Tax regulations

- NBA contractual rules

This benchmark highlights the limitations of existing LLMs in rule compliance and structured reasoning, and provides a suitable testbed for symbolic-agentic methods.

Known Limitations
- Limited support for numeric comparisons (e.g., X > 10)

- Incomplete fact extraction from unstructured text

- Occasional omission or misinterpretation of rules during extraction

- Challenges in dealing with underspecified user inputs

- Dependence on manually selected documents in current implementation