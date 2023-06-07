from pathlib import Path

from cli import parse_cli_args
from utils import get_source_code, get_source_file_paths_to_analyze, render_repository_metrics
from software_metrics import SourceMetrics

if __name__ == '__main__':
    cli_arguments = parse_cli_args()
    source_code_dir = get_source_code(cli_arguments.repository_link)

    file_paths_to_analyze = get_source_file_paths_to_analyze(
        Path(source_code_dir.name),
        cli_arguments.directories,
        cli_arguments.extensions
    )

    repository_metrics = {}

    for file_path_to_analyze in file_paths_to_analyze:

        source_file_metrics = SourceMetrics(file_path_to_analyze)

        repository_metrics[file_path_to_analyze.name] = {
            "File name": file_path_to_analyze.name,
            "LOC": source_file_metrics.get_line_count(),
            "Empty LOC": source_file_metrics.get_empty_line_count(),
            "Physical LOC": source_file_metrics.get_physical_line_count(),
            "Logical LOC": source_file_metrics.get_logical_line_count(),
            "Comment Lines": source_file_metrics.get_comment_line_count(),
            "Comment Level (F)": source_file_metrics.get_comment_level(),
        }

    render_repository_metrics(repository_metrics)
