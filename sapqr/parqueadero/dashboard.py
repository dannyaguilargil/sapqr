# parqueadero/dashboard.py
from jet.dashboard.dashboard import Dashboard, AppIndexDashboard
from jet.dashboard.modules import LinkList, AppList


class CustomIndexDashboard(Dashboard):
    columns = 3

class CustomAppIndexDashboard(AppIndexDashboard):
    pass
