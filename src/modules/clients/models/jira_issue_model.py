from dataclasses import dataclass, asdict

@dataclass
class JiraIssueModel:
    id: str
    key: str
    summary: str
    status: str
    assignee: str
    issue_type: str

    def to_dict(self):
        return asdict(self)