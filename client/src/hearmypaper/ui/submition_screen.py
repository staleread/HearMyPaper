from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QComboBox, QHeaderView
)
from PyQt5.QtCore import Qt


class SubmissionsListScreen(QWidget):
    def __init__(self, user_role, projects):
        """
        user_role: str -> "Student", "Curator", "Instructor"
        projects: list of dict
        """
        super().__init__()
        self.user_role = user_role
        self.projects = projects
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Course Projects Overview")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #3F51B5;")
        layout.addWidget(title)

        filter_layout = QHBoxLayout()
        self.course_filter = QComboBox()
        self.course_filter.addItem("All Courses")
        self.course_filter.addItems(sorted({p["title"] for p in self.projects}))
        filter_layout.addWidget(QLabel("Filter by Course:"))
        filter_layout.addWidget(self.course_filter)

        self.status_filter = QComboBox()
        self.status_filter.addItems(["All", "Submitted", "Pending", "Late"])
        filter_layout.addWidget(QLabel("Filter by Status:"))
        filter_layout.addWidget(self.status_filter)

        layout.addLayout(filter_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Title", "Syllabus", "Status", "Deadline"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.populate_table()

        if self.user_role == "Curator":
            self.add_button = QPushButton("Create New Project")
            self.add_button.setStyleSheet("background:#3F51B5; color:white; border-radius:8px; padding:8px;")
            layout.addWidget(self.add_button)

        self.setLayout(layout)

    def populate_table(self):
        self.table.setRowCount(len(self.projects))
        for row, project in enumerate(self.projects):
            self.table.setItem(row, 0, QTableWidgetItem(project["title"]))
            self.table.setItem(row, 1, QTableWidgetItem(project["syllabus"]))

            status_item = QTableWidgetItem(project["status"])
            if project["status"] == "Submitted":
                status_item.setBackground(Qt.green)
            elif project["status"] == "Pending":
                status_item.setBackground(Qt.yellow)
            elif project["status"] == "Late":
                status_item.setBackground(Qt.red)
            self.table.setItem(row, 2, status_item)

            self.table.setItem(row, 3, QTableWidgetItem(project["deadline"]))
