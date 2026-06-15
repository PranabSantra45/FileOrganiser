from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivymd.uix.card import MDCard
from kivy.uix.boxlayout import BoxLayout

class CategoryCard(MDCard):
    """
    Custom Card displaying a category with its icon, name, file count, and theme color.
    """
    category_name = StringProperty("")
    file_count = NumericProperty(0)
    icon_name = StringProperty("folder")
    bg_color = ListProperty([1, 1, 1, 1])

class FilePreviewItem(BoxLayout):
    """
    Row element in the preview list showing:
    [Filename] -> [Target Category Subdirectory/Filename]
    """
    filename = StringProperty("")
    target_path = StringProperty("")
    index = NumericProperty(0)
    icon_name = StringProperty("file-outline")


