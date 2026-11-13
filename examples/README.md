# Worked examples

Small, runnable examples make the guidance reviewable. Each example states its public contract, tests the important behavior and names what remains outside its evidence.

- [A narrow interface with deep tests](narrow-interface/README.md): a pure Ruby retry schedule, separated from Rails jobs, clocks and external requests.
- [Database uniqueness under contention](database-contention/README.md) shows the race in check-then-insert and tests a composite unique index on PostgreSQL.
