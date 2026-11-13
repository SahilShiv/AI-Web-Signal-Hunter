"""Plotly visualization charts styled for enterprise intelligence dashboards."""

from typing import List
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from config.constants import CATEGORY_COLORS, RELEVANT_CATEGORIES
from models.signal import Signal
from models.opportunity import Opportunity


# Dark/Clean theme layout defaults
LAYOUT_DEFAULTS = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, -apple-system, sans-serif", color="#94A3B8", size=12),
    margin=dict(l=20, r=20, t=30, b=20),
)


def create_category_distribution_chart(signals: List[Signal]) -> go.Figure:
    """Creates a sleek donut chart showing the breakdown of signal categories."""
    if not signals:
        fig = go.Figure()
        fig.update_layout(**LAYOUT_DEFAULTS)
        return fig

    data = []
    for s in signals:
        data.append({"Category": s.signal_category})
    df = pd.DataFrame(data)
    counts = df["Category"].value_counts().reset_index()
    counts.columns = ["Category", "Count"]

    colors = [CATEGORY_COLORS.get(cat, "#64748B") for cat in counts["Category"]]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=counts["Category"],
                values=counts["Count"],
                hole=0.55,
                marker=dict(colors=colors, line=dict(color="#0F172A", width=2)),
                textinfo="percent+label",
                textposition="inside",
                hoverinfo="label+value+percent",
            )
        ]
    )

    fig.update_layout(
        **LAYOUT_DEFAULTS,
        showlegend=False,
        height=280,
    )
    return fig


def create_opportunity_ranking_chart(opportunities: List[Opportunity]) -> go.Figure:
    """Creates a horizontal bar chart displaying top opportunity scores."""
    if not opportunities:
        fig = go.Figure()
        fig.update_layout(**LAYOUT_DEFAULTS)
        return fig

    # Top opportunities in reverse order for horizontal chart
    opps = list(reversed(opportunities[:6]))
    titles = [o.title[:38] + ("..." if len(o.title) > 38 else "") for o in opps]
    scores = [o.opportunity_score for o in opps]

    fig = go.Figure(
        go.Bar(
            x=scores,
            y=titles,
            orientation="h",
            marker=dict(
                color=scores,
                colorscale=[[0, "#3B82F6"], [0.5, "#6366F1"], [1.0, "#10B981"]],
                line=dict(color="#1E293B", width=1),
            ),
            text=[f"{s:.1f}" for s in scores],
            textposition="auto",
        )
    )

    fig.update_layout(
        **LAYOUT_DEFAULTS,
        xaxis=dict(range=[0, 100], title="Opportunity Score (/100)", gridcolor="#1E293B"),
        yaxis=dict(showgrid=False),
        height=300,
    )
    return fig


def create_signal_scatter_chart(signals: List[Signal]) -> go.Figure:
    """Creates a scatter plot showing Relevance vs Urgency by category."""
    if not signals:
        fig = go.Figure()
        fig.update_layout(**LAYOUT_DEFAULTS)
        return fig

    rows = []
    for s in signals:
        rows.append({
            "Summary": s.summary[:50] + "...",
            "Category": s.signal_category,
            "Relevance": s.relevance_score,
            "Urgency": s.urgency_score,
            "Confidence": s.confidence_score,
            "Domain": s.source_domain,
        })
    df = pd.DataFrame(rows)

    fig = px.scatter(
        df,
        x="Relevance",
        y="Urgency",
        color="Category",
        size="Confidence",
        hover_data=["Summary", "Domain"],
        color_discrete_map=CATEGORY_COLORS,
    )

    fig.update_layout(
        **LAYOUT_DEFAULTS,
        xaxis=dict(range=[40, 105], title="Relevance Score", gridcolor="#1E293B"),
        yaxis=dict(range=[40, 105], title="Urgency Score", gridcolor="#1E293B"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=320,
    )
    return fig


def create_domain_distribution_chart(signals: List[Signal]) -> go.Figure:
    """Creates a bar chart of signals by source domain."""
    if not signals:
        fig = go.Figure()
        fig.update_layout(**LAYOUT_DEFAULTS)
        return fig

    domains = [s.source_domain for s in signals if s.source_domain]
    df = pd.DataFrame({"Domain": domains})
    counts = df["Domain"].value_counts().head(8).reset_index()
    counts.columns = ["Domain", "Count"]

    fig = go.Figure(
        go.Bar(
            x=counts["Domain"],
            y=counts["Count"],
            marker=dict(color="#475569", line=dict(color="#334155", width=1)),
            text=counts["Count"],
            textposition="auto",
        )
    )

    fig.update_layout(
        **LAYOUT_DEFAULTS,
        xaxis=dict(tickangle=-30, showgrid=False),
        yaxis=dict(title="Signals Count", gridcolor="#1E293B"),
        height=260,
    )
    return fig

