import plotly.graph_objects as go
from pandas import DataFrame
from plotly.offline import plot


def plot_main(merged_dfs: DataFrame, username: str) -> str:
    # NOTE: Plots (main/scores)
    def generate_plot_data(column: str, color: str, name: str):
        plot_df = merged_dfs.value_counts(column).reset_index().sort_values(by=column)
        return go.Scatter(
            x=plot_df[column],
            y=plot_df["count"],
            mode="lines+markers",
            name=name,
            line=dict(color=color),
            marker=dict(color=color),
        )

    user_score_trace = generate_plot_data("user_score", "#00bbbc", username)
    average_score_trace = generate_plot_data("average_score", "#00c79c", "AniList")
    fig = go.Figure(data=[user_score_trace, average_score_trace])

    fig.update_layout(
        template="plotly_dark",
        title="",
        xaxis_title="Score",
        yaxis_title="Count",
        legend_title="",
        legend=dict(yanchor="top", y=1.03, xanchor="left", x=0.01),
        showlegend=True,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        hoverlabel=dict(bgcolor="#141414"),
        hovermode="x unified",
    )

    plt_div_main = plot(
        fig,
        output_type="div",
        include_plotlyjs=False,
        show_link=False,
        link_text="",
    )

    return plt_div_main


def plot_genres(genre_insights: DataFrame, username: str) -> str:
    fig = go.Figure(
        data=[
            go.Bar(
                x=genre_insights["genres"],
                y=genre_insights["weighted_user"],
                marker=dict(color="#00bbbc"),
                name=username,
            ),
            go.Bar(
                x=genre_insights["genres"],
                y=genre_insights["weighted_average"],
                marker=dict(color="#00c79c"),
                name="AniList",
            ),
        ],
    )
    ymin = min(
        genre_insights["weighted_user"].min(), genre_insights["weighted_average"].min()
    )
    ymax = max(
        genre_insights["weighted_user"].max(), genre_insights["weighted_average"].max()
    )
    fig.update_yaxes(range=[ymin - 10, ymax + 5])
    fig.update_layout(
        template="plotly_dark",
        title="",
        xaxis_title="Genre",
        yaxis_title="Score",
        legend_title="",
        showlegend=True,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(yanchor="top", y=1, xanchor="right", x=1),
        hoverlabel=dict(bgcolor="#141414"),
        hovermode="x unified",
    )
    plt_div_genres = plot(
        fig,
        output_type="div",
        include_plotlyjs=False,
        show_link=False,
        link_text="",
    )

    return plt_div_genres
