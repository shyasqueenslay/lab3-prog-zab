import tokenize
import ast
from pathlib import Path
from typing import Union
from functools import cache


class SourceMetrics:
    path: Path
    content: str

    def __init__(self, source_file_path: Union[Path, str]):
        self.path = Path(source_file_path)

        with open(self.path, "r") as f:
            self.content = f.read()

        self.syntax_tree = ast.parse(self.content, self.path.name)

    @cache
    def get_line_count(self) -> int:
        return self.content.count("\n") + 1

    @cache
    def get_empty_line_count(self) -> int:
        count = 0
        for line in self.content.split('\n'):
            if line.strip() == '':
                count += 1

        return count

    @cache
    def get_comment_line_count(self) -> int:
        return self._get_single_comment_line_count() + self._get_multiline_comment_line_count(self.syntax_tree)

    @cache
    def get_comment_level(self) -> float:
        return self.get_comment_line_count() / self.get_line_count()

    @cache
    def get_physical_line_count(self) -> int:
        return self.get_line_count() - self.get_comment_line_count() - self.get_empty_line_count()

    @cache
    def get_logical_line_count(self) -> int:
        return self._get_logical_line_count_in_node(self.syntax_tree)

    @staticmethod
    def _get_logical_line_count_in_node(node: ast.AST) -> int:
        count = 0

        if isinstance(node, ast.expr) or isinstance(node, ast.stmt):
            count += 1

        if not hasattr(node, "body"):
            return count

        for node in node.body:
            count += SourceMetrics._get_logical_line_count_in_node(node)

        return count

    def _get_single_comment_line_count(self) -> int:
        count = 0

        with tokenize.open(self.path) as f:
            tokens = tokenize.generate_tokens(f.readline)
            for token in tokens:
                if token.type == tokenize.COMMENT:
                    count += 1

        return count

    @staticmethod
    def _get_multiline_comment_line_count(node: ast.AST) -> int:
        count = 0

        if not hasattr(node, "body"):
            return count

        if type(node) == ast.ClassDef or type(node) == ast.FunctionDef:
            if len(node.body) > 0 and type(node.body[0]) == ast.Expr:
                if type(node.body[0].value) == ast.Constant and type(node.body[0].value.value) == str:
                    count += node.body[0].value.value.count("\n") + 1

        for node in node.body:
            count += SourceMetrics._get_multiline_comment_line_count(node)

        return count

    @staticmethod
    def _get_cyclomatic_complexity_for_a_node(node: ast.FunctionDef):
        new_decision_statement_types = (
            ast.If, ast.While, ast.For, ast.With, ast.Assert,
            ast.comprehension, ast.BoolOp, ast.excepthandler
        )

        count = 0
        for children_node in ast.walk(node):
            if isinstance(children_node, new_decision_statement_types):
                count += 1

        return count

    def calculate_cyclomatic_complexity(self) -> dict[str, int]:
        ccs = {}
        for node in ast.walk(self.syntax_tree):
            if isinstance(node, ast.FunctionDef):
                ccs[node.name] = self._get_cyclomatic_complexity_for_a_node(node)

        return ccs

    def get_the_most_cc_function(self) -> (str, int):
        sorted_ccs = sorted(self.calculate_cyclomatic_complexity().items(), key=lambda complexity: -complexity[1])
        if sorted_ccs:
            return sorted_ccs[0]
        else:
            return "", 0
