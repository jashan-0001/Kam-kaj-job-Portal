import matplotlib.pyplot as plt
import streamlit as st

from services.analytics_service import (
    get_ats_scores,
    get_recommendation_distribution,
    get_applications_per_job
)


def show_ats_chart(employer_id):
    """
    Display ATS Score Distribution Chart.
    """

    scores = get_ats_scores(employer_id)

    if not scores:
        st.info("No ATS scores available.")
        return

    fig, ax = plt.subplots(figsize=(7, 4))

    ax.hist(
        scores,
        bins=10
    )

    ax.set_title("ATS Score Distribution")
    ax.set_xlabel("ATS Score")
    ax.set_ylabel("Number of Candidates")

    st.pyplot(fig)


def show_recommendation_chart(employer_id):
    """
    Display Recommendation Distribution Pie Chart.
    """

    data = get_recommendation_distribution(employer_id)

    if not data:
        st.info("No recommendation data available.")
        return

    labels = [
        row["recommendation"]
        for row in data
    ]

    values = [
        row["total"]
        for row in data
    ]

    fig, ax = plt.subplots(figsize=(6, 6))

    ax.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90
    )

    ax.set_title("Recommendation Distribution")

    st.pyplot(fig)


def show_job_chart(employer_id):
    """
    Display Applications Per Job Bar Chart.
    """

    data = get_applications_per_job(employer_id)

    if not data:
        st.info("No job data available.")
        return

    job_titles = [
        row["title"]
        for row in data
    ]

    application_counts = [
        row["total"]
        for row in data
    ]

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.bar(
        job_titles,
        application_counts
    )

    ax.set_title("Applications Per Job")
    ax.set_xlabel("Job Title")
    ax.set_ylabel("Applications")

    plt.xticks(rotation=25, ha="right")

    plt.tight_layout()

    st.pyplot(fig) 