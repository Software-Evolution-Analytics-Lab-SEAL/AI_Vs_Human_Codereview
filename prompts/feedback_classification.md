# LLM Prompts Used in This Study

## Feedback Type Classification (Figure 3)

### Model
- GPT-4.1-mini (OpenAI)
- Structured JSON output mode

### Prompt (Figure 3)
```
Based on the feedback type definitions from Table II, classify the following
code review comment into the most appropriate feedback type. Return the
feedback type with a confidence score (1-10). Code review comment: {comment_body}
```

### Output Schema
```json
{
  "type": "string (one of the 9 feedback types from Table II)",
  "confidence": "number (1-10)"
}
```

## Feedback Type Taxonomy (Table II)

The taxonomy is based on Bacchelli and Bird (ICSE 2013) with rephrased descriptions.

| Feedback Type | Description |
|---------------|-------------|
| Code Improvement | Suggestions to enhance code clarity, style, structure, or maintainability without fixing defects. |
| Defect Detection | Identification of functional, logical, or correctness issues in the proposed changes. |
| External Impact | Comments about broader system-level consequences beyond the local code diff. |
| Knowledge Transfer | Reviewer explains concepts, conventions, best practices, or provides learning resources. |
| Misc | Comments that do not fit any defined category or are context-irrelevant. |
| No Feedback | Conversations where the reviewer provides no substantive technical feedback. |
| Social | Interpersonal statements not directly tied to technical content (e.g., appreciation, encouragement). |
| Testing | Comments about adding, updating, or fixing tests and test coverage. |
| Understanding | Clarification questions to understand context, rationale, design decisions, or implementation intent. |
