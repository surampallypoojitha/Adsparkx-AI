from pathlib import Path
import sys

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from persona_support_agent.config import load_settings  # noqa: E402
from persona_support_agent.pipeline import answer_support_message  # noqa: E402


st.set_page_config(
    page_title="Persona-Adaptive Support Agent",
    layout="wide",
)


@st.cache_data(show_spinner=False)
def get_settings():
    return load_settings()


def render_sources(results):
    if not results:
        st.info("No sources retrieved.")
        return

    for index, result in enumerate(results, start=1):
        with st.expander(f"{index}. {result.file_name} - score {result.relevance_score:.2f}"):
            st.caption(result.source)
            st.write(result.content)


def main() -> None:
    settings = get_settings()

    st.title("Persona-Adaptive Customer Support Agent")

    with st.sidebar:
        st.header("Settings")
        st.text_input("Gemini model", value=settings.gemini_model, disabled=True)
        st.text_input("Embedding model", value=settings.gemini_embedding_model, disabled=True)
        st.text_input("Chroma collection", value=settings.chroma_collection_name, disabled=True)
        failed_attempt_count = st.number_input(
            "Failed attempts",
            min_value=0,
            max_value=10,
            value=0,
            step=1,
            help="Used by the escalation engine.",
        )

    if not settings.google_api_key or settings.google_api_key == "your_google_api_key_here":
        st.error("GOOGLE_API_KEY is missing. Add it to .env before running the app.")
        st.stop()

    user_message = st.text_area(
        "User message",
        value="I am frustrated and still cannot access my account",
        height=120,
    )

    submitted = st.button("Generate response", type="primary")

    if not submitted:
        st.stop()

    if not user_message.strip():
        st.warning("Enter a support message first.")
        st.stop()

    with st.spinner("Retrieving context and generating response..."):
        result = answer_support_message(
            user_message=user_message,
            settings=settings,
            failed_attempt_count=int(failed_attempt_count),
        )

    metric_cols = st.columns(4)
    metric_cols[0].metric("Detected persona", str(result.persona.persona))
    metric_cols[1].metric("Persona confidence", f"{result.persona.confidence:.2f}")
    metric_cols[2].metric("Retrieval confidence", f"{result.retrieval.confidence:.2f}")
    metric_cols[3].metric(
        "Escalation",
        "Yes" if result.escalation.should_escalate else "No",
    )

    left_col, right_col = st.columns([1.2, 1])

    with left_col:
        st.subheader("Generated response")
        st.write(result.generated_response.answer)

        st.subheader("Persona signals")
        for persona, score in result.persona.scores.items():
            signals = ", ".join(result.persona.matched_signals[persona]) or "none"
            st.write(f"**{persona}:** {score} ({signals})")

    with right_col:
        st.subheader("Escalation status")
        if result.escalation.should_escalate:
            st.error("Human escalation recommended.")
            st.write(
                ", ".join(reason.value for reason in result.escalation.reasons)
            )
            st.write(result.escalation.recommended_action)
        else:
            st.success("Automated response is acceptable.")

        st.subheader("Retrieved sources")
        render_sources(result.retrieval.results)

    if result.handoff_summary is not None:
        st.subheader("Human handoff summary")
        st.markdown(result.handoff_summary.to_markdown())


if __name__ == "__main__":
    main()
