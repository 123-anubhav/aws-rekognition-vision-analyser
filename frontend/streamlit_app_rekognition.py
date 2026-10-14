
import sys
from pathlib import Path

import pandas as pd
import streamlit as st
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.rekognition_service import detect_image_labels


st.set_page_config(
    page_title="Rekognition Vision",
    page_icon="👁️",
    layout="wide",
)

# -------------------------------
# Custom UI styling
# -------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: #f5f7fb;
    }

    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
    }

    .hero {
        padding: 1.6rem 1.9rem;
        border-radius: 20px;
        background: linear-gradient(
            120deg, #172554, #1d4ed8, #0e7490
        );
        color: white;
        margin-bottom: 1.25rem;
    }

    .hero h1 {
        color: white;
        margin: 0;
        font-size: 2.15rem;
    }

    .hero p {
        color: #dbeafe;
        margin: 0.45rem 0 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>👁️ Rekognition Vision</h1>
        <p>
            Upload an image and let Amazon Rekognition
            identify objects and visual labels.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------------------
# Sidebar settings
# -------------------------------
with st.sidebar:
    st.header("⚙️ Detection Settings")

    max_labels = st.slider(
        "Maximum labels",
        min_value=1,
        max_value=20,
        value=10,
    )

    min_confidence = st.slider(
        "Minimum confidence (%)",
        min_value=0,
        max_value=100,
        value=70,
    )

    st.caption(
        "A higher confidence threshold may return fewer labels."
    )

# -------------------------------
# Image upload
# -------------------------------
st.markdown("### Upload an image")

uploaded_file = st.file_uploader(
    "Choose a JPG, JPEG, or PNG image",
    type=["jpg", "jpeg", "png"],
    key="rekognition_upload",
)

if uploaded_file is not None:

    # IMPORTANT: Pass bytes to the backend, not Path(bytes).
    image_bytes = uploaded_file.getvalue()

    left, right = st.columns([1, 1.15], gap="large")

    with left:
        st.markdown("#### Image Preview")

        try:
            preview = Image.open(uploaded_file)

            st.image(
                preview,
                caption=uploaded_file.name,
                width="stretch",
            )

            st.caption(
                f"File size: {len(image_bytes) / 1024:.1f} KB"
            )

        except Exception:
            st.error(
                "Could not preview the image. "
                "Please upload a valid JPG or PNG."
            )

    with right:
        st.markdown("#### Analyze Image")

        st.write(
            "Ready to detect labels in your uploaded image."
        )

        analyze = st.button(
            "🔍 Analyze Image",
            type="primary",
            width="stretch",
        )

        if analyze:
            with st.spinner(
                "Amazon Rekognition is analyzing your image..."
            ):
                try:
                    labels = detect_image_labels(
                        image_bytes=image_bytes,
                        max_labels=max_labels,
                        min_confidence=min_confidence,
                    )

                    st.session_state["rekognition_results"] = {
                        "filename": uploaded_file.name,
                        "labels": labels,
                    }

                    st.session_state.pop(
                        "rekognition_error", None
                    )

                except Exception as exc:
                    st.session_state.pop(
                        "rekognition_results", None
                    )

                    st.session_state["rekognition_error"] = str(
                        exc
                    )

# -------------------------------
# Error handling
# -------------------------------
if st.session_state.get("rekognition_error"):
    st.error(
        "Could not analyze the image: "
        + st.session_state["rekognition_error"]
    )

    st.info(
        "Check your AWS credentials, region, and "
        "rekognition:DetectLabels permission."
    )

# -------------------------------
# Display results
# -------------------------------
results = st.session_state.get("rekognition_results")

if results:
    st.markdown("---")
    st.markdown("### 🧠 Detection Results")

    st.caption(f"Image: {results['filename']}")

    labels = results["labels"]

    if not labels:
        st.warning(
            "No labels matched the selected confidence threshold."
        )

    else:
        col1, col2 = st.columns(2)

        col1.metric(
            "Labels Detected",
            len(labels),
        )

        highest_confidence = max(
            item["Confidence"] for item in labels
        )

        col2.metric(
            "Highest Confidence",
            f"{highest_confidence:.2f}%",
        )

        df = pd.DataFrame(
            [
                {
                    "Detected Label": item["Name"],
                    "Confidence (%)": round(
                        item["Confidence"], 2
                    ),
                }
                for item in labels
            ]
        )

        st.dataframe(
            df,
            width="stretch",
            hide_index=True,
            column_config={
                "Confidence (%)": st.column_config.ProgressColumn(
                    "Confidence (%)",
                    min_value=0,
                    max_value=100,
                    format="%.2f%%",
                )
            },
        )

        csv_data = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "⬇️ Download Results as CSV",
            data=csv_data,
            file_name="rekognition_labels.csv",
            mime="text/csv",
        )

else:
    st.info(
        "Upload an image and click Analyze Image "
        "to view detected labels here."
    )

st.caption(
    "Powered by Amazon Rekognition. "
    "The image is sent to AWS when you analyze it."
)
