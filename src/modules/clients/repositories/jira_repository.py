from logger_tracker import logg_info, logg_debug, logg_error
from src.modules.clients.models.jira_issue_model import JiraIssueModel

class JiraRepository:
    def __init__(self, jira_client):
        self.jira_client = jira_client

    def get_list_issues(self, project_key, status, type):
        try:
            logg_info(f"Obteniendo la lista de issues del proyecto {project_key} con estado {status}")
            jql_query = f"project = {project_key} AND status = '{status}' AND issuetype = '{type}'"
            jira_issues = self.jira_client.search_issues(jql_query)
            logg_debug(f"Issues obtenidos: {len(jira_issues)}")
            issue_models = []
            for issue in jira_issues:
                model = JiraIssueModel(
                    key=issue.key,
                    id=issue.id,
                    summary=issue.fields.summary,
                    status=issue.fields.status.name,
                    issue_type=issue.fields.issuetype.name,
                    assignee=issue.fields.assignee.displayName if issue.fields.assignee else "No asignado"
                )
                issue_models.append(model)
            logg_debug(f"Modelos de issues creados: {len(issue_models)}")
            return issue_models
        except Exception as e:
            logg_error(f"Error al obtener la lista de issues del proyecto {project_key}: {e}")
            return None

    def get_issue(self, issue_id):
        try:
            logg_info(f"Obteniendo el issue {issue_id}")
            issue = self.jira_client.issue(issue_id)
            logg_debug(f"Issue obtenido: {issue.key} - {issue.fields.summary}")
            return issue
        except Exception as e:
            logg_error(f"Error al obtener el issue {issue_id}: {e}")
            return None

    def create_issue(self, project_key, summary, description, issue_type):
        try:
            issue = self.jira_client.create_issue(
                project=project_key,
                summary=summary,
                description=description,
                issuetype={"name": issue_type}
            )
            return issue
        except Exception as e:
            logg_error(f"Error al crear el issue: {e}")
            return None

    def update_issue(self, issue_id, fields):
        try:
            issue = self.jira_client.issue(issue_id)
            issue.update(fields)
            return issue
        except Exception as e:
            logg_error(f"Error al actualizar el issue {issue_id}: {e}")
            return None

    def delete_issue(self, issue_id):
        try:
            issue = self.jira_client.issue(issue_id)
            issue.delete()
            return True
        except Exception as e:
            logg_error(f"Error al eliminar el issue {issue_id}: {e}")
            return False