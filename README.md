# cash-flow
Personal cash management

## Development

### Requirements
- Python 3.7+

### Installing
Install dependencies
```console
make install
```

### Testing
```console
make test
```

### Migrating
Generate migration files automatically for changes to models. Make sure all models are imported on `models/__init__.py`
```console
make db_generate_migration description="your description"
```
