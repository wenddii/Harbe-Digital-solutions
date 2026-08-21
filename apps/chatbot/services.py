from django.conf import settings

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from .prompts import SYSTEM_PROMPT


# ============================================================
# GEMINI MODEL
# ============================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=settings.GEMINI_API_KEY,
    temperature=0.7,
)


# ============================================================
# PROMPT
# ============================================================

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "{conversation}"),
    ]
)


# ============================================================
# LANGCHAIN CHAIN
# ============================================================

chain = prompt | llm


# ============================================================
# NORMAL RESPONSE
# ============================================================

def ask_llm(messages):

    conversation = ""

    for message in messages:
        conversation += (
            f"{message['role']}: {message['content']}\n"
        )

    response = chain.invoke(
        {
            "conversation": conversation
        }
    )

    return response.content


# ============================================================
# STREAMING RESPONSE
# ============================================================

def stream_llm(messages):

    conversation = ""

    for message in messages:
        conversation += (
            f"{message['role']}: {message['content']}\n"
        )

    for chunk in chain.stream(
        {
            "conversation": conversation
        }
    ):

        content = chunk.content

        # LangChain may return content as a list
        if isinstance(content, list):

            for item in content:

                if isinstance(item, dict):

                    text = item.get("text")

                    if text:
                        yield text

        # Or it may return content directly as a string
        elif isinstance(content, str):

            yield content