from sqlmodel import Relationship, SQLModel, Field
from datetime import timezone, datetime


class BlogTagLink(SQLModel, table=True):
    blog_id: int | None = Field(default=None, foreign_key="blog.id", primary_key=True)
    tag_id: int | None = Field(default=None, foreign_key="tag.id", primary_key=True)

class Blog(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    thumbnail_url: str | None = Field(default=None)
    content: str
    uploaded_by: int | None = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    comments: list["Comment"] = Relationship(back_populates="blog")
    
    tags: list["Tag"] = Relationship(back_populates="blogs", link_model=BlogTagLink)

class Tag(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str | None = Field(default=None, unique=True, index=True)

    blogs: list[Blog] = Relationship(back_populates="tags", link_model=BlogTagLink)

class Comment(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    content: str
    commented_by: int | None = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_modified: datetime | None= Field(default=None)
    
    blog_id: int | None = Field(default=None, foreign_key="blog.id")
    blog: Blog | None = Relationship(back_populates="comments")