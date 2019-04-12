# validator-backup

### Systemd monitor
```
>>> from pystemd.systemd1 import Unit
>>> unit = Unit(b'polkadot-validator.service')
>>> unit.load()
>>> unit.Unit.ActiveState
b'active'
>>> unit.Unit.ActiveState.decode('utf-8')
'active'
```
