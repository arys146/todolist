from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from schemas.tag import TagRead


FIELDS_TO_EXCLUDE = {"tag_ids"}
MIN_PRIORITY = 1
MAX_PRIORITY = 10


class HabbitCreate(BaseModel):
    title: str
    description: Optional[str] = None
    schedule: str
    priority: int = Field(default=5, ge=MIN_PRIORITY, le=MAX_PRIORITY)
    tag_ids: Optional[List[int]] = []


    @field_validator("schedule")
    @classmethod
    def validate_schedule(cls, v: str) -> str:
        if not isinstance(v, str):
            raise ValueError("schedule должен быть строкой вида 'type,interval,values...'")

        # парсинг
        parts = [p.strip() for p in v.split(",") if p.strip() != ""]
        if len(parts) < 3:
            raise ValueError("schedule: нужно минимум 3 элемента: type,interval,values...")

        # type
        try:
            type_ = int(parts[0])
        except ValueError:
            raise ValueError("schedule: type должен быть 0 (неделя) или 1 (месяц)")
        if type_ not in (0, 1):
            raise ValueError("schedule: type должен быть 0 (неделя) или 1 (месяц)")

        # interval (>=1; 1 значит «каждую неделю/месяц»)
        try:
            interval = int(parts[1])
        except ValueError:
            raise ValueError("schedule: interval должен быть целым числом ≥ 1")
        if interval < 1:
            raise ValueError("schedule: interval должен быть ≥ 1 (1 = без пропуска)")

        # values...
        vals_raw = parts[2:]
        if not vals_raw:
            raise ValueError("schedule: должен содержать хотя бы одно значение дня")

        values: List[int] = []
        for item in vals_raw:
            try:
                n = int(item)
            except ValueError:
                raise ValueError(f"schedule: значение '{item}' не является числом")
            values.append(n)

        # диапазоны
        if type_ == 0:
            # недельный: ISO 1..7 (1=Пн .. 7=Вс)
            bad = [n for n in values if not (1 <= n <= 7)]
            if bad:
                raise ValueError(f"schedule: для недельного повтора допустимы только 1..7, найдено: {bad}")
        else:
            # месячный: 1..31
            bad = [n for n in values if not (1 <= n <= 31)]
            if bad:
                raise ValueError(f"schedule: для месячного повтора допустимы только 1..31, найдено: {bad}")

        # нормализация: уберём дубликаты и отсортируем
        values = sorted(set(values))

        # вернём нормализованную строку
        normalized = ",".join([str(type_), str(interval), *map(str, values)])
        return normalized


class HabbitRead(BaseModel):
    id: int
    title: str
    description: str
    priority: int
    schedule: str
    created_at: datetime
    updated_at: datetime
    tags: List[TagRead]

    model_config = {
        "from_attributes": True
    }


class HabbitUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    schedule: str
    priority: Optional[int] = Field(default=5, ge=MIN_PRIORITY, le=MAX_PRIORITY)
    tag_ids: Optional[List[int]] = []

class HabbitElement(BaseModel):
    id: int
    title: str
    description: str
    priority: int
    schedule: str
    is_checked: Optional[bool] = False
    created_at: datetime
    updated_at: datetime
    tags: List[TagRead]

    model_config = {
        "from_attributes": True
    }