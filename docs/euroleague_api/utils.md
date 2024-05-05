# Module euroleague_api.utils

## Functions

    
### get_requests

```python3
def get_requests(
    url: str,
    params: dict = {},
    headers: dict = {'Accept': 'application/json'}
) -> requests.models.Response
```

A wrapper to `requests.get()` which handles unsuccesful requests too.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| url | str | _description_ | None |
| params | dict | The `params` variables in get requests.<br>Defaults to {}. | None |
| headers | dict | the `header` variable in get requests.<br>Defaults to {"Accept": "application/json"}. | None |

**Returns:**

| Type | Description |
|---|---|
| requests.models.Response | The response object. |

**Raises:**

| Type | Description |
|---|---|
| Requests Error | If get request was not succesful |

    
### raise_error

```python3
def raise_error(
    var: Optional[str],
    descripitve_var: str,
    available_vals: List,
    allow_none: bool = False
) -> None
```

A function that raises a ValueError with specific message.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| var | str | The input variable by the user | None |
| descripitve_var | str | A description in plain English of this variable | None |
| available_vals | List | The available variables | None |
| allow_none | bool | If `var` can take None value.<br>Defaults to False. | None |

**Raises:**

| Type | Description |
|---|---|
| ValueError | if `var` not applicable |
