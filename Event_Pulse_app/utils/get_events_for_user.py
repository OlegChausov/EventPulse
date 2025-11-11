user_event_queries = await session.execute(
    select(EventQuery).where(EventQuery.user_id == some_user.id)
)
user_event_queries = user_event_queries.scalars().all()
