"""Учебный CRUD API курсов с хранилищем в памяти процесса."""

from fastapi import APIRouter, FastAPI, HTTPException, Response, status
from pydantic import BaseModel, PrivateAttr, RootModel

app = FastAPI()

courses_router = APIRouter(
    prefix="/api/v1/courses",
    tags=["courses-service"],
)


class CourseIn(BaseModel):
    """Данные создания и полного обновления курса без ID."""

    title: str
    max_score: int
    min_score: int
    description: str


class CourseOut(CourseIn):
    """Сохранённый курс с автоматически присвоенным идентификатором."""

    id: int


class CoursesStore(RootModel):
    """Хранить курсы в списке и выдавать ID независимо от удалений."""

    root: list[CourseOut]
    _next_id: int = PrivateAttr(default=1)

    def find(self, course_id: int) -> CourseOut | None:
        """Найти курс по ID или вернуть None."""
        return next((course for course in self.root if course.id == course_id), None)

    def create(self, course_in: CourseIn) -> CourseOut:
        """Присвоить новый ID внутри хранилища и добавить курс."""
        # Учитываем и счётчик, и возможные исходные записи хранилища.
        course_id = max(self._next_id, max((course.id for course in self.root), default=0) + 1)
        course = CourseOut(id=course_id, **course_in.model_dump())
        self.root.append(course)
        self._next_id = course_id + 1
        return course

    def update(self, course_id: int, course_in: CourseIn) -> CourseOut:
        """Заменить данные существующего курса, сохранив его ID."""
        index = next(index for index, course in enumerate(self.root) if course.id == course_id)
        updated = CourseOut(id=course_id, **course_in.model_dump())
        self.root[index] = updated
        return updated

    def delete(self, course_id: int) -> None:
        """Удалить курс из списка, не уменьшая счётчик ID."""
        self.root = [course for course in self.root if course.id != course_id]


store = CoursesStore(root=[])


@courses_router.get("/{course_id}", response_model=CourseOut)
async def get_course(course_id: int) -> CourseOut:
    """Получить курс по ID или вернуть 404."""
    course = store.find(course_id)
    if course is None:
        raise HTTPException(
            detail=f"Course with id {course_id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return course


@courses_router.get("", response_model=list[CourseOut])
async def get_courses() -> list[CourseOut]:
    """Получить все курсы из памяти приложения."""
    return store.root


@courses_router.post("", response_model=CourseOut, status_code=status.HTTP_201_CREATED)
async def create_course(course: CourseIn) -> CourseOut:
    """Создать курс с автоматически сгенерированным ID."""
    return store.create(course)


@courses_router.put("/{course_id}", response_model=CourseOut)
async def update_course(course_id: int, course: CourseIn) -> CourseOut:
    """Полностью обновить курс или вернуть 404."""
    if store.find(course_id) is None:
        raise HTTPException(
            detail=f"Course with id {course_id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return store.update(course_id, course)


@courses_router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: int) -> Response:
    """Удалить курс; успешный ответ 204 не содержит тела."""
    if store.find(course_id) is None:
        raise HTTPException(
            detail=f"Course with id {course_id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    store.delete(course_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


app.include_router(courses_router)
