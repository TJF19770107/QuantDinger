# workspace.json

> 原始文件: `workspace.json`  |  类型: `.json`  |  自动转换

```json
{
  "main": {
    "id": "main",
    "type": "split",
    "children": [
      {
        "id": "left",
        "type": "tabs",
        "children": [
          {
            "id": "file-explorer",
            "type": "leaf",
            "state": {
              "type": "file-explorer",
              "state": {
                "sortOrder": "alphabetical"
              }
            }
          },
          {
            "id": "search",
            "type": "leaf",
            "state": {
              "type": "search",
              "state": {}
            }
          }
        ]
      },
      {
        "id": "center",
        "type": "split",
        "children": [
          {
            "id": "note-view",
            "type": "tabs",
            "children": [
              {
                "id": "welcome",
                "type": "leaf",
                "state": {
                  "type": "markdown",
                  "state": {
                    "file": "Notes/Welcome.md",
                    "mode": "source",
                    "source": false
                  }
                }
              }
            ]
          }
        ]
      },
      {
        "id": "right",
        "type": "tabs",
        "children": [
          {
            "id": "backlinks",
            "type": "leaf",
            "state": {
              "type": "backlink",
              "state": {}
            }
          },
          {
            "id": "outline",
            "type": "leaf",
            "state": {
              "type": "outline",
              "state": {}
            }
          }
        ]
      }
    ],
    "direction": "horizontal",
    "width": 300
  },
  "active": "welcome",
  "lastOpenFiles": ["Notes/Welcome.md"],
  "enabledPlugins": [
    "file-explorer",
    "global-search",
    "switcher",
    "graph",
    "backlink",
    "canvas",
    "outgoing-link",
    "tag-pane",
    "page-preview",
    "note-composer",
    "command-palette",
    "editor-status",
    "bookmarks",
    "markdown-importer",
    "outline",
    "word-count",
    "workspaces",
    "file-recovery",
    "templates"
  ]
}

```
