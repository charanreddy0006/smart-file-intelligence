from pathlib import Path
import sys
from collections import Counter

# Add the project root to Python's import path.
# This allows Streamlit to import the main "app" package.
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import streamlit as st
from sqlalchemy import select

from app.core.database import SessionLocal, init_db
from app.core.models import FileRecord
from app.search.engine import search_files


# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Smart File Intelligence",
    page_icon="📁",
    layout="wide",
)


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.title("Smart File Intelligence")

st.caption(
    "File classification, duplicate detection and semantic-style search"
)


# ---------------------------------------------------------
# Database Initialization
# ---------------------------------------------------------

init_db()


# ---------------------------------------------------------
# Load File Records
# ---------------------------------------------------------

with SessionLocal() as session:
    records = session.scalars(
        select(FileRecord)
    ).all()


# ---------------------------------------------------------
# Calculate Statistics
# ---------------------------------------------------------

total_files = len(records)

total_size = sum(
    record.size_bytes for record in records
)

unique_hashes = len({
    record.sha256 for record in records
})

duplicate_files = total_files - unique_hashes


# ---------------------------------------------------------
# Dashboard Metrics
# ---------------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Files",
    total_files
)

c2.metric(
    "Storage",
    f"{total_size / (1024 * 1024):.2f} MB"
)

c3.metric(
    "Unique Files",
    unique_hashes
)

c4.metric(
    "Possible Duplicates",
    max(duplicate_files, 0)
)


st.divider()


# ---------------------------------------------------------
# File Search
# ---------------------------------------------------------

st.subheader("Search Files")

query = st.text_input(
    "Search your files",
    placeholder="Try: machine learning, invoice, python..."
)

if query:

    results = search_files(query)

    st.subheader("Search Results")

    if results:
        results_df = pd.DataFrame(results)

        st.dataframe(
            results_df,
            use_container_width=True,
            hide_index=True,
        )

    else:
        st.info("No matching files found.")


# ---------------------------------------------------------
# File Categories
# ---------------------------------------------------------

st.subheader("File Categories")

counts = Counter(
    record.category for record in records
)

if counts:

    category_df = pd.DataFrame(
        {
            "Category": list(counts.keys()),
            "Files": list(counts.values()),
        }
    )

    st.bar_chart(
        category_df.set_index("Category")
    )

else:

    st.info(
        "No files have been scanned yet."
    )


# ---------------------------------------------------------
# Recent Files
# ---------------------------------------------------------

st.subheader("Recent Files")

recent = sorted(
    records,
    key=lambda record: record.modified_at,
    reverse=True,
)[:50]


if recent:

    recent_df = pd.DataFrame(
        [
            {
                "Name": record.name,
                "Category": record.category,
                "Size (KB)": round(
                    record.size_bytes / 1024,
                    2,
                ),
                "Modified": record.modified_at,
                "Path": record.path,
            }
            for record in recent
        ]
    )

    st.dataframe(
        recent_df,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.info(
        "Scan a directory to populate the dashboard."
    )