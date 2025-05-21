course_data = {
    "name": "Курсы по родЫам",
    "modules": [
        {
            "name": "שיעורי מבוא לכל הקורסים",
            "id": 0,
            "lections": [
                {"name": "Урок 1", "id": 0, "path": "videos/introduction/l1.mp4"},
                {"name": "Урок 2", "id": 1, "path": "videos/introduction/l2.mp4"},
                {"name": "הקדמה לכל הקורסים", "id": 2, "path": "videos/introduction/in.mp4"},
            ]
        },
        {
            "name": "קורס הכנה ללידה",
            "id": 1,
            "lections": [
                {"name": "הקדמה של קורס הכנה ללידה", "id": 1, "path": "videos/module1/1.mp4"},
                {"name": "שיעור 1 - איך לנשום נכון", "id": 1, "path": "videos/module1/l1.mp4"},
                {"name": "שיעור 2 - מה זה פרינאום", "id": 2, "path": "videos/module1/l2.mp4"},
                {"name": "שיעור 3 - חמישה תנאים אנטומיים ללידה", "id": 3, "path": "videos/module1/l3.mp4"},
                {"name": "שיעור 4 - שיעורי בית", "id": 4, "path": "videos/module1/l4.mp4"},
                {"name": "שיעור 5 - איך להתכופף נכון", "id": 5, "path": "videos/module1/l5.mp4"},
                {"name": "שיעור 6 - שלבי לידה", "id": 6, "path": "videos/module1/l6.mp4"},
                {"name": "שיעור 7 - התנהגות נכונה בלידה", "id": 7, "path": "videos/module1/l7.mp4"},
                {"name": "שיעור 8 - המלצות למלווה של היולדת", "id": 8, "path": "videos/module1/l8.mp4"},
                {"name": "שיעור 9 - איך לעשות דמיון מודרך ללידה", "id": 9, "path": "videos/module1/l9.mp4"},
                {"name": "שיעור 10 - תיק ללידה", "id": 10, "path": "videos/module1/l10.mp4"},
                {"name": "שיעור 11 - חדר לידה", "id": 11, "path": "videos/module1/l11.mp4"},
                {"name": "שיעור 12 - אפידורל", "id": 12, "path": "videos/module1/l12.mp4"},
            ]
        },
        {
            "name": "קורס הכנה ללידה עם צלקת על הרחם",
            "id": 2,
            "lections": [
                {"name": "הקדמה של לידה עם צלקת על הרחם", "id": 0, "path": "videos/module2/1.mp4"},
                {"name": "שיעור 1 - נוכחות מלווה הלידה", "id": 1, "path": "videos/module2/l1.mp4"},
                {"name": "שיעור 2 - המלצות לזמן היריון", "id": 2, "path": "videos/module2/l2.mp4"},
                {"name": "שיעור 3 - המלצות בזמן הלידה", "id": 3, "path": "videos/module2/l3.mp4"},
                {"name": "שיעור 4 - התנהגות נכונה אחרי לידה", "id": 4, "path": "videos/module2/l4.mp4"},
                {"name": "שיעור 5 - שמירה על תשוקה לאחר הלידה", "id": 5, "path": "videos/module2/l5.mp45"},
            ]
        },
    ]
}


def get_module_by_id(module_id: int) -> dict | None:
    for module in course_data.get("modules", []):
        if module.get("id") == module_id:
            return module
    return None


def get_lection_by_id(module_id: int, lection_id: int) -> dict | None:
    module = get_module_by_id(module_id)
    if not module:
        return None
    for lection in module.get("lections", []):
        if lection.get("id") == lection_id:
            return lection
    return None
