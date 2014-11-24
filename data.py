import json
import os.path

SETTINGS_JSON = os.path.expanduser("~/.hafif/settings.json")


class JsonObject:
    def _attr_from_dict(self, dict, attrs):
        for attr in attrs:
            self.__dict__[attr] = dict[attr]


class Shortcut(JsonObject):
    def __init__(self, shortcut_json):
        self._attr_from_dict(shortcut_json, ['title', 'command', 'icon'])


class Link(JsonObject):
    def __init__(self, link_json):
        self._attr_from_dict(link_json, ['title', 'type', 'data', 'icon'])


class Todo(JsonObject):
    def __init__(self, todo_json):
        self._attr_from_dict(todo_json, ['date', 'note'])


class Project(JsonObject):
    def __init__(self, project_json):
        self._attr_from_dict(project_json, ['title', 'icon'])
        self.shortcuts = [Shortcut(json) for json in project_json['shortcuts']]
        self.links = [Link(json) for json in project_json['links']]
        self.todos = [Todo(json) for json in project_json['todos']]


def load():
    with open(SETTINGS_JSON) as file:
        projects = []
        for project_json in json.load(file)["projects"]:
            projects.append(Project(project_json))
        return projects


def save(projects):
    with open(SETTINGS_JSON, "w") as file:
        json.dump({
                      "projects": projects
                  }, default=lambda x: x.__dict__, indent=4, fp=file)