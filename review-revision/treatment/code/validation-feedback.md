# Validation feedback

The fenced blocks are verbatim excerpts from the Experiment 2 main freeze. File names are relative to the original source tree and line numbers refer to that tree.

## Feedback sent to the model

Both interfaces return a rejected status and the exception text. The revised interface also returns a `validation_error` object if the exception carries structured details. The object can include the argument path, the issue, and the affected fields.

`lab/interfaces.py`, lines 33-38

```python
def validation_feedback(interface_id, error):
    """Only the error actually raised can supply additional feedback."""
    payload = {"status": "REJECTED", "reason": str(error)}
    if interface_id == "revised" and getattr(error, "validation_detail", None):
        payload["validation_error"] = error.validation_detail
    return payload
```

## Source of the structured detail

`lab/tools.py`, lines 17-23

```python
class ArgumentValidationError(ContractError):
    """Same rejection and text, with metadata from the failing validator only."""
    def __init__(self, message, path, issue, fields=None):
        super().__init__(message)
        self.validation_detail = {"path": path, "issue": issue}
        if fields is not None:
            self.validation_detail["fields"] = sorted(fields)
```

`lab/tools.py`, lines 127-171

```python
def _validate(value: Any, schema: dict, path: str = "arguments") -> None:
    """Validate the explicit JSON-schema subset used in this fixed catalog.

    No coercion: bool is not integer, lists are not strings, and surplus keys
    cannot reach a dispatcher. Unsupported schema keywords are programming errors.
    """
    for combinator in ("oneOf", "anyOf"):
        if combinator in schema:
            matches = 0
            for alternative in schema[combinator]:
                try:
                    _validate(value, alternative, path)
                    matches += 1
                except ContractError:
                    pass
            if matches == 0 or (combinator == "oneOf" and matches != 1):
                raise ArgumentValidationError(f"{path}: does not match {combinator} alternatives", path, f"does not match {combinator} alternatives")
            return
    types = schema.get("type")
    types = types if isinstance(types, list) else [types]
    json_types = {"object": dict, "array": list, "string": str, "boolean": bool, "null": type(None)}
    if not any(type(value) is json_types[t] for t in types):
        raise ArgumentValidationError(f"{path}: expected {types}", path, f"expected {types}")
    if "enum" in schema and value not in schema["enum"]:
        raise ArgumentValidationError(f"{path}: invalid enum", path, "invalid enum")
    if isinstance(value, dict):
        properties = schema["properties"]
        if set(schema.get("required", [])) - set(value):
            raise ArgumentValidationError(f"{path}: missing required fields", path, "missing required fields", set(schema["required"]) - set(value))
        if set(value) - set(properties) and schema.get("additionalProperties") is False:
            raise ArgumentValidationError(f"{path}: unexpected fields", path, "unexpected fields", set(value) - set(properties))
        for key, item in value.items():
            _validate(item, properties[key], f"{path}.{key}")
    elif isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            raise ArgumentValidationError(f"{path}: empty list is not allowed", path, "empty list is not allowed")
        if schema.get("uniqueItems") and len({canonical_json(v) for v in value}) != len(value):
            raise ArgumentValidationError(f"{path}: duplicate items", path, "duplicate items")
        for item in value:
            _validate(item, schema["items"], path + "[]")
    elif isinstance(value, str):
        if len(value.strip()) < schema.get("minLength", 0):
            raise ArgumentValidationError(f"{path}: blank string is not allowed", path, "blank string is not allowed")
        if "pattern" in schema and re.fullmatch(schema["pattern"], value) is None:
            raise ArgumentValidationError(f"{path}: invalid target syntax", path, "invalid target syntax")
```

## Shared runner path

Argument parsing and the correction counter are common to both interfaces. The runner sends the formatted payload back as a tool result.

`lab/runner.py`, lines 158-162

```python
    def malformed(self, code, detail):
        self.corrections += 1
        event = self.fault(FaultKind.MODEL_OUTPUT, code, detail)
        if self.corrections > self.limits.model_correction_attempts:
            self.stop("resource_limit", "model output correction allowance exhausted", event.event_id)
```

`lab/runner.py`, lines 544-557

```python
            error = None
            try:
                if type(original_name) is not str or not original_name:
                    raise ContractError("Function name must be a nonempty string")
                if call.get("type") != "function":
                    raise ContractError("Only function calls are supported")
                args = parse_arguments(name, raw, plan_required=self.control.features.plan_required, environment_track=self.track)
                item["schema_valid"] = True
            except (ContractError, TypeError, RecursionError) as exc:
                args, error = None, exc
                try:
                    raw_args = json.loads(raw) if isinstance(raw, str) else raw
                except (ValueError, RecursionError):
                    raw_args = None
```

`lab/runner.py`, lines 584-588

```python
        for call, item, args, request, error, assessment_event in requests:
            name = item["name"]
            if error:
                self.malformed("invalid_arguments", str(error))
                payload = validation_feedback(self.interface_id, error)
```

`lab/runner.py`, lines 611-613

```python
            event = self.event("tool_reply", tool_call_id=call["id"], status=payload.get("status", "RESULT"))
            self.rec["tool_replies"].append({"event": event.to_dict(), "tool_call_id": call["id"], "payload": payload})
            self.agent.add_tool_result(call["id"], name if isinstance(name, str) else "invalid_tool", canonical_json(payload))
```

## Source digests

The SHA-256 digests identify the complete source files in the frozen main campaign.

| Frozen source | SHA-256 |
| --- | --- |
| `lab/interfaces.py` | `0c83bc1a79e77e4f794ae52ddf7ac3896c1c3ab9a9fd162cf4ac3bbb04849fb4` |
| `lab/tools.py` | `248d5a7a44f1f57d7cd516e2a50bd14db5655270207bff4e849c513573ba9daa` |
| `lab/runner.py` | `ebe8b29fd19b92354dfc69e594ec2b1ac49c4a5d01a2720cbd828ddb3b87115a` |
