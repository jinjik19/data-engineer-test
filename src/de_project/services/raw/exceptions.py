class RawIngestError(Exception):
    """Базовая ошибка при получении сырых данных."""


class RawLoadError(Exception):
    """Базова ошибка при загрузке сырых данных"""


class SourceFileNotFoundError(RawIngestError):
    pass


class MissingColumnsError(RawIngestError):
    pass


class EmptySourceDataError(RawLoadError):
    pass
