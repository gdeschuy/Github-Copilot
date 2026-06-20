# Prompt Development Guide

## 1. Assign an Explicit Persona
Define the exact role, expertise, and perspective the model must adopt to unlock the correct knowledge patterns and tone.

**DO**
- State a specific professional role and seniority (e.g., "Senior Data Analyst").
- Define the target audience for the output.

**DON'T**
- Use vague descriptions like "Be an expert" without specifying the field.

**Example**
```markdown
Bad: Write an explanation of how a blockchain works.
Good: Persona: Senior Cloud Architect. Audience: Non-technical business stakeholders. Explain how a blockchain works in under 100 words.
```

## 2. Use Strong, Unambiguous Language
Use strict, enforceable wording to eliminate variance and behavior drift.

**DO**
- MUST / MUST NOT
- DO / DO NOT
- ONLY IF / UNLESS

**DON'T**
- try to / prefer / avoid
- should / should not

**Example**
```markdown
Bad: Try to not hallucinate and avoid making assumptions.
Good: You MUST NOT generate information not grounded in the provided context. If required information is missing, state "DATA_UNAVAILABLE".
```

## 3. Define Precise Scope
Clearly define inputs, outputs, and strict boundaries to prevent off-topic generations.

**DO**
- Specify exact target variables or focus areas.
- Explicitly exclude out-of-scope topics.

**DON'T**
- Use open-ended verbs (e.g., "Analyze this").

**Example**
```markdown
Bad: Summarize the document.
Good: Summarize ONLY key business risks in the document. DO NOT include background history or implementation details.
```

## 4. Add Explicit Failure Handling
Define strict fallback rules for incomplete, missing, or invalid data.

**DO**
- Provide an exact error or fallback string.
- Forbid guessing, assuming, or extrapolating.

**DON'T**
- Let the model hallucinate or improvise when data is missing.

**Example**
```markdown
If the input document is incomplete or ambiguous, you MUST NOT guess. Return EXCLUSIVELY: "INSUFFICIENT_INFORMATION".
```

## 5. Break Tasks into Steps
Guide the model through a linear execution path to reduce cognitive load per token.

**DO**
- Use sequential, numbered steps.
- Isolate data ingestion from processing and formatting.

**DON'T**
- Ask for simultaneous analysis and formatting in one sentence.

**Example**
```markdown
Execute these steps in order:
1. Identify all financial figures in the text.
2. Filter out figures below \$10,000.
3. Format the remaining figures as a markdown list.
```

## 6. Segment Inputs with XML Tags
Separate instructions, reference context, and user inputs cleanly. This prevents context confusion.

**DO**
- Use short, descriptive tags (e.g., `<ctx>`, `<rules>`).
- Wrap dynamic user variables or data payloads in tags.

**DON'T**
- Use verbose transition phrases to separate text parts.

**Example**
```markdown
Summarize <doc> based on <rules>.

<rules>
- Max 3 bullet points.
- Focus only on metrics.
</rules>

<doc>
[Insert Data]
</doc>
```

## 7. Use Few-Shot Prompting
Provide concrete examples to enforce exact format, style, and logic constraints efficiently.

**DO**
- Use short, clear delimiters (e.g., `In:`, `Out:`).
- Keep examples ultra-concise to save token budget.

**DON'T**
- Write long text descriptions explaining desired output style.

**Example**
```markdown
Identify the core sentiment.

In: The product broke after two days.
Out: NEGATIVE

In: [User Input]
Out:
```

## 8. Enforce Structured Outputs
Force machine-readable data for seamless upstream parsing and programmatic consumption.

**DO**
- Specify exact formats (JSON, CSV, Markdown tables).
- Define target keys or strict schemas.

**DON'T**
- Allow prose, markdown code blocks (unless specified), or conversational filler.

**Example**
```markdown
Output ONLY a valid JSON object. No markdown wrappers, no explanations.

Schema:
{
  "risk_id": string,
  "impact": "HIGH" | "MEDIUM" | "LOW"
}
```

## 9. Trigger Chain-of-Thought (CoT)
Force complex reasoning, calculations, or multi-layered logic before generating the final answer.

**DO**
- Isolate reasoning inside specific scratchpad tags (e.g., `<thinking>`).
- Place the thinking step BEFORE the final output.

**DON'T**
- Ask for explanations *after* the final answer is already output.

**Example**
```markdown
Follow this exact output sequence:
1. State step-by-step reasoning inside <thinking> tags.
2. Provide the final answer inside <answer> tags.
```