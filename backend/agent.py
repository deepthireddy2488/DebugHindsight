import os
import re

from dotenv import load_dotenv
from groq import Groq
from hindsight_client import Hindsight


load_dotenv()


# =========================================================
# CONFIGURATION
# =========================================================

BANK_ID = "debughindsight"

GROQ_MODEL = "openai/gpt-oss-20b"

HINDSIGHT_URL = "https://api.hindsight.vectorize.io"


# =========================================================
# CLIENTS
# =========================================================

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

hindsight_client = Hindsight(
    base_url=HINDSIGHT_URL,
    api_key=os.getenv("HINDSIGHT_API_KEY"),
    timeout=60.0
)


# =========================================================
# HINDSIGHT BANK
# =========================================================

try:
    hindsight_client.create_bank(
        bank_id=BANK_ID,
        name="DebugHindsight"
    )
except Exception:
    pass


# =========================================================
# EXTRACT MARKDOWN SECTION
# =========================================================

def extract_section(text, title):

    if not text:
        return ""

    pattern = re.compile(
        rf"(?is)"
        rf"(?:^|\n)\s*"
        rf"(?:#+\s*)?"
        rf"\*{{0,2}}\s*{re.escape(title)}\s*\*{{0,2}}"
        rf"\s*\n?"
        rf"(.*?)"
        rf"(?=\n\s*(?:#+\s*)?\*{{0,2}}\s*"
        rf"(?:Memory Check|Previous Experience|Current Investigation|Recommended Next Steps)"
        rf"\s*\*{{0,2}}\s*(?:\n|$)|\Z)"
    )

    match = pattern.search(text)

    if match:
        return match.group(1).strip()

    return ""


# =========================================================
# CLEAN SECTION
# =========================================================

def clean_section(text):

    if not text:
        return ""

    lines = []

    for line in text.splitlines():

        stripped = line.strip()

        if not stripped:
            continue

        # Remove empty list items such as:
        # 1.
        # • 1.
        # - 1.
        if re.fullmatch(
            r"(?:[•\-\*]\s*)?\d+[\.\)]\s*",
            stripped
        ):
            continue

        lines.append(line)

    return "\n".join(lines).strip()


# =========================================================
# CHECK WHETHER SECTION HAS REAL CONTENT
# =========================================================

def section_has_real_content(text):

    if not text:
        return False

    cleaned = clean_section(text)

    if not cleaned:
        return False

    test = re.sub(
        r"[\s|*_:#>\-]",
        "",
        cleaned
    )

    return len(test) >= 15


# =========================================================
# DETECT WHETHER MEMORY WAS FOUND
# =========================================================

def detect_memory_found(memory_check):

    text = memory_check.lower().strip()

    # -----------------------------------------------------
    # Explicit negative statements
    # -----------------------------------------------------

    negative_phrases = [

        "no closely related incident",
        "no similar incident",
        "no closely related experience",
        "no relevant memory",
        "no relevant memories",
        "no previous debugging experience",
        "no related debugging experience",
        "no related experience",
        "nothing closely related",
        "nothing similar",
        "could not find a closely related",
        "could not find a similar",
        "could not find any relevant",
        "no previous experience was found",
        "no relevant previous experience was found",

    ]

    if any(
        phrase in text
        for phrase in negative_phrases
    ):
        return False

    # -----------------------------------------------------
    # Explicit positive statements
    # -----------------------------------------------------

    positive_phrases = [

        "relevant memory was found",
        "relevant memory found",
        "genuinely relevant memory was found",
        "genuinely relevant memory found",
        "genuinely relevant",
        "relevant incident was found",
        "relevant incident found",
        "similar incident was found",
        "similar incident found",
        "closely related incident was found",
        "closely related incident found",
        "found a similar incident",
        "found a closely related incident",
        "related incident was found",
        "relevant previous experience was found",
        "relevant previous debugging incident was found",
        "relevant previous debugging experience was found",
        "previous debugging experience was found",
        "previous experience was found",

    ]

    if any(
        phrase in text
        for phrase in positive_phrases
    ):
        return True

    return False


# =========================================================
# CONVERT HINDSIGHT MEMORY TO JSON-SAFE DATA
# =========================================================

def serialize_memory(memory):

    return {
        "id": getattr(
            memory,
            "id",
            None
        ),
        "text": getattr(
            memory,
            "text",
            ""
        ),
        "type": getattr(
            memory,
            "fact_type",
            getattr(
                memory,
                "type",
                None
            )
        ),
        "state": getattr(
            memory,
            "state",
            None
        ),
    }


# =========================================================
# MEMORY CHECK FALLBACK
# =========================================================

def create_memory_check(memories):

    if memories:

        return (
            "A relevant previous debugging incident was found. "
            "The retrieved experience contains technical approaches "
            "that may help investigate the current issue."
        )

    return (
        "No closely related previous debugging experience was found "
        "in Hindsight for this issue."
    )


# =========================================================
# PREVIOUS EXPERIENCE FALLBACK
# =========================================================

def create_previous_experience(memories):

    if not memories:

        return (
            "No relevant previous debugging experience was found."
        )

    experiences = []

    for memory in memories[:3]:

        memory_text = getattr(
            memory,
            "text",
            ""
        ).strip()

        if not memory_text:
            continue

        previous = extract_section(
            memory_text,
            "Previous Experience"
        )

        if section_has_real_content(previous):

            experiences.append(
                previous
            )

        else:

            experiences.append(
                memory_text
            )

    if not experiences:

        return (
            "A relevant previous debugging experience was retrieved "
            "from Hindsight."
        )

    return "\n\n".join(
        experiences[:2]
    )


# =========================================================
# CURRENT INVESTIGATION
#
# Generated by the application instead of relying on
# Groq to return numbered content correctly.
# =========================================================

def create_current_investigation(
    bug,
    memories
):

    if memories:

        memory_note = (
            "The retrieved Hindsight experience should be treated "
            "as a reference and verified against the current system."
        )

    else:

        memory_note = (
            "No relevant previous experience was retrieved, so the "
            "investigation starts from the current system behavior."
        )

    return f"""1. Reproduce the reported problem and identify exactly when the failure or slowdown occurs.

2. Inspect the application logs, stack traces, request behavior, configuration, and the component directly involved in the problem.

3. Check the likely bottleneck or failure mechanism instead of assuming that a previous solution is the root cause.

4. Compare the current behavior with the relevant Hindsight experience and verify whether the same technical condition exists.

5. Test the suspected cause independently before applying a fix.

{memory_note}"""


# =========================================================
# RECOMMENDED NEXT STEPS
#
# Generated by the application instead of relying on
# Groq to return numbered content correctly.
# =========================================================

def create_recommended_steps(
    bug,
    memories
):

    steps = [

        "Reproduce the bug and capture the complete error message, application logs, and stack trace.",

        "Inspect the affected code path and its configuration for the condition that triggers the problem.",

        "Measure or observe the failing behavior before changing the implementation.",

        "Apply the smallest appropriate fix based on the confirmed cause.",

        "Repeat the original failing scenario and verify that the problem is resolved.",

    ]

    if memories:

        steps.append(
            "Compare the result with the previous Hindsight experience and record whether the previous approach succeeded or failed."
        )

    return "\n".join(
        f"{index}. {step}"
        for index, step in enumerate(
            steps,
            start=1
        )
    )


# =========================================================
# CREATE MEMORY TO STORE IN HINDSIGHT
# =========================================================

def create_clean_memory(
    bug,
    memory_check,
    previous_experience,
    current_investigation,
    recommended_steps
):

    return f"""
Software debugging experience.

Bug:

{bug}

Memory Check:

{memory_check}

Previous Experience:

{previous_experience}

Current Investigation:

{current_investigation}

Recommended Next Steps:

{recommended_steps}

This debugging experience should be useful for future debugging incidents
that are similar to this problem.
""".strip()


# =========================================================
# MAIN DEBUGGING FUNCTION
# =========================================================

def debug_bug(bug):

    # =====================================================
    # 1. RECALL FROM HINDSIGHT
    # =====================================================

    recall_query = f"""
Find previous debugging experiences genuinely relevant to this bug.

Current bug:

{bug}

Only consider memories relevant when their technical problem,
failure mechanism, debugging approach, or solution is meaningfully
related to the current issue.

Do not consider a memory relevant only because it uses the same
programming language or framework.
""".strip()

    recall_result = hindsight_client.recall(
        bank_id=BANK_ID,
        query=recall_query
    )

    retrieved_memories = getattr(
        recall_result,
        "results",
        []
    )

    # =====================================================
    # 2. REMOVE DUPLICATE MEMORIES
    # =====================================================

    unique_memories = []

    seen = set()

    for memory in retrieved_memories:

        memory_text = getattr(
            memory,
            "text",
            ""
        ).strip()

        if not memory_text:
            continue

        key = memory_text.lower()

        if key in seen:
            continue

        seen.add(key)

        unique_memories.append(
            memory
        )

    retrieved_memories = unique_memories[:5]

    # =====================================================
    # 3. BUILD MEMORY CONTEXT FOR GROQ
    # =====================================================

    if retrieved_memories:

        memory_parts = []

        for index, memory in enumerate(
            retrieved_memories,
            start=1
        ):

            memory_text = getattr(
                memory,
                "text",
                ""
            )

            memory_parts.append(
                f"MEMORY {index}\n{memory_text}"
            )

        memory_context = "\n\n".join(
            memory_parts
        )

    else:

        memory_context = (
            "No previous debugging memories were retrieved."
        )

    # =====================================================
    # 4. GROQ SYSTEM PROMPT
    # =====================================================

    system_prompt = """
You are DebugHindsight, an AI software debugging agent.

Your main purpose is to investigate software bugs while using
previous debugging experience from Hindsight.

Return exactly these four sections:

**Memory Check**

**Previous Experience**

**Current Investigation**

**Recommended Next Steps**

MEMORY CHECK:

Clearly state whether a genuinely relevant previous debugging
incident was found.

PREVIOUS EXPERIENCE:

If relevant experience exists, explain the previous approaches,
their results, and their limitations.

If multiple approaches exist, use this Markdown table:

| Approach | What it addresses | Successes | Limitations / Risks |
| --- | --- | --- | --- |
| Real approach | Real problem | Real result | Real limitation |

The table MUST contain real rows.

If no relevant experience exists, clearly state that no related
experience was found.

CURRENT INVESTIGATION:

Explain the technical reasoning for the current bug.

Do not use empty numbered items.

RECOMMENDED NEXT STEPS:

Explain practical debugging actions.

Do not use empty numbered items.

IMPORTANT:

Do not invent previous experience.

Do not assume a previous solution is automatically correct.

Do not leave Memory Check or Previous Experience empty.

Current Investigation and Recommended Next Steps will be generated
by the application after your analysis, so focus on providing useful
technical reasoning for the current bug.
""".strip()

    # =====================================================
    # 5. GROQ USER PROMPT
    # =====================================================

    user_prompt = f"""
CURRENT BUG:

{bug}

HINDSIGHT MEMORIES:

{memory_context}

Analyze this bug.

Determine whether the retrieved Hindsight memories are genuinely
relevant.

Explain the useful previous experience when relevant.

Provide technical reasoning that can help investigate the current bug.
""".strip()

    # =====================================================
    # 6. CALL GROQ
    # =====================================================

    completion = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    answer = (
        completion
        .choices[0]
        .message
        .content
        .strip()
    )

    # =====================================================
    # 7. EXTRACT GROQ SECTIONS
    # =====================================================

    memory_check = extract_section(
        answer,
        "Memory Check"
    )

    previous_experience = extract_section(
        answer,
        "Previous Experience"
    )

    # =====================================================
    # 8. VALIDATE MEMORY CHECK
    # =====================================================

    if not section_has_real_content(
        memory_check
    ):

        memory_check = create_memory_check(
            retrieved_memories
        )

    # =====================================================
    # 9. VALIDATE PREVIOUS EXPERIENCE
    # =====================================================

    if not section_has_real_content(
        previous_experience
    ):

        previous_experience = create_previous_experience(
            retrieved_memories
        )

    # =====================================================
    # 10. ALWAYS GENERATE CURRENT INVESTIGATION
    # =====================================================

    current_investigation = create_current_investigation(
        bug,
        retrieved_memories
    )

    # =====================================================
    # 11. ALWAYS GENERATE RECOMMENDED NEXT STEPS
    # =====================================================

    recommended_steps = create_recommended_steps(
        bug,
        retrieved_memories
    )

    # =====================================================
    # 12. DETERMINE WHETHER MEMORY WAS FOUND
    # =====================================================

    memory_found = detect_memory_found(
        memory_check
    )

    # =====================================================
    # 13. CONVERT MEMORIES TO JSON-SAFE DATA
    # =====================================================

    relevant_memories = []

    if memory_found:

        relevant_memories = [
            serialize_memory(memory)
            for memory in retrieved_memories[:3]
        ]

    # =====================================================
    # 14. BUILD FINAL ANSWER
    # =====================================================

    final_answer = f"""
**Memory Check**

{memory_check}

**Previous Experience**

{previous_experience}

**Current Investigation**

{current_investigation}

**Recommended Next Steps**

{recommended_steps}
""".strip()

    # =====================================================
    # 15. CREATE NEW MEMORY
    # =====================================================

    clean_memory = create_clean_memory(
        bug=bug,
        memory_check=memory_check,
        previous_experience=previous_experience,
        current_investigation=current_investigation,
        recommended_steps=recommended_steps
    )

    # =====================================================
    # 16. SAVE NEW MEMORY TO HINDSIGHT
    # =====================================================

    memory_saved = False

    try:

        hindsight_client.retain(
            bank_id=BANK_ID,
            content=clean_memory,
            context="software debugging experience"
        )

        memory_saved = True

    except Exception as error:

        print(
            f"Hindsight memory save failed: {error}"
        )

    # =====================================================
    # 17. RETURN JSON-SAFE RESULT
    # =====================================================

    return {
        "answer": final_answer,
        "memories": relevant_memories,
        "memory_found": memory_found,
        "memory_saved": memory_saved
    }