from sqladmin import ModelView

from core.database.models import AudioRecord


class AudioAdmin(ModelView, model=AudioRecord):
    column_list = [
        AudioRecord.id,
        AudioRecord.user,
    ]
    column_searchable_list = [AudioRecord.audio_file]
    column_default_sort = [("created_at", True)]
    name = "Запись"
    name_plural = "Записи"
    icon = "fa-solid fa-music"
