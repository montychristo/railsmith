# Database uniqueness under contention

A reading list can contain each book once. The [migration](db/migrate/20261113000000_create_reading_list_entries.rb)
puts that rule in a unique index on `(list_id, book_id)` and makes both IDs
non-null. The [model](app/models/reading_list_entry.rb) exposes one operation:

```ruby
ReadingListEntry.add(list_id: 1, book_id: 10) # => :added
ReadingListEntry.add(list_id: 1, book_id: 10) # => :already_present
```

[Active Record's insert](https://api.rubyonrails.org/v8.1.4/classes/ActiveRecord/Relation.html#method-i-insert)
targets the composite index and uses PostgreSQL's
[`ON CONFLICT DO NOTHING` and `RETURNING`](https://www.postgresql.org/docs/16/sql-insert.html).
Only an inserted row produces a returned ID. The operation bypasses model
validations and callbacks, so the database owns the demonstrated constraints.
Use it for already-authorized IDs. The example does not define parent tables,
foreign keys or authorization.

## Run the tests

Use Ruby 3.4 and a disposable PostgreSQL 16 test database. Set
`RAILSMITH_EXAMPLE_DATABASE_URL` to its connection URL. The role needs to create
schemas. Each test creates and drops its own schema.

```sh
gem install minitest --no-document
gem install activerecord -v '~> 8.1.0' --no-document
gem install pg -v '~> 1.6' --no-document
ruby examples/database-contention/test/reading_list_entry_test.rb
```

The [tests](test/reading_list_entry_test.rb) hold two separate connections.
In the baseline, the index is absent. A queue pauses one caller after its
existence check, allowing the other to insert before the first resumes.
The baseline test expects the bug and observes two rows for one pair.

The indexed case holds the first insert open in a transaction until
`pg_blocking_pids` identifies the second session waiting on it. After commit,
the calls report one addition and one duplicate, and a fresh query sees one row.
Bounded checkpoints and database timeouts surface failures. The test also checks
that distinct pairs remain legal and a direct duplicate write fails.

This exercises the committed database invariant under PostgreSQL's read-committed
isolation. It covers one transaction outcome and one database engine. For an
existing table, plan duplicate cleanup and index rollout for that application's
data and write traffic before adopting the migration.
