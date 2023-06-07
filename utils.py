from pathlib import Path
from tempfile import TemporaryDirectory

import pygit2
import plotly.graph_objects as go


def get_source_code(git_repo_url: str) -> TemporaryDirectory:
    print("Downloading git repository")
    temp_directory = TemporaryDirectory()
    pygit2.clone_repository(url=git_repo_url, path=temp_directory.name)
    return temp_directory


def get_source_file_paths_to_analyze(sources_path: Path, directories: list[str], extensions: list[str]) -> list[Path]:
    file_paths_to_analyze = []
    for subdirectory in directories:
        for extension in extensions:
            file_paths_to_analyze.extend(
                list(sources_path.glob(f"{subdirectory}/**/*{extension}"))
            )

    return file_paths_to_analyze


# TODO: Refactor this analytical mess
def render_repository_metrics(repository_metrics):
    headers = {
        "values": [
            "File name",
            "LOC",
            "Empty LOC",
            "Physical LOC",
            "Logical LOC",
            "Comment Lines",
            "Comment Level (F)",
        ]
    }

    cells = {
        "values": []
    }

    total_values = {
        "File name": "",
        "LOC": 0,
        "Empty LOC": 0,
        "Physical LOC": 0,
        "Logical LOC": 0,
        "Comment Lines": 0,
        "Comment Level (F)": 0,
    }

    for header in headers["values"]:
        col = []

        for file_path, metrics in repository_metrics.items():
            if header == "File Path":
                col.append(file_path)
                total_values[header] = "Total"
            elif header == "Highest CC function":
                if total_values[header][1] < metrics[header][1]:
                    total_values[header] = metrics[header]

                col.append(" ".join(map(str, metrics[header])))
            else:
                col.append(metrics[header])
                total_values[header] += metrics[header]

        if header == "Highest CC function":
            col.append(" ".join(map(str, total_values[header])))
        elif header == "Comment Level (F)":
            avg_comment_level = total_values["Comment Lines"] / total_values["LOC"]
            col.append("Avg F: %.2f" % avg_comment_level)
        else:
            col.append(total_values[header])

        cells["values"].append(col)

    fig = go.Figure(
        data=[
            go.Table(
                header=headers,
                cells=cells
            )
        ]
    )
    fig.show()
