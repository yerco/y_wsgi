# Forms
## Skeleton
Refer to the code at `src/forms`

## Note:
Instead for using to return something like
```python
return Response(
            status='200 OK',
            body=[form.render().encode('utf-8')],
            headers=[('Content-Type', 'text/html')]
        )
```
We create a helper at `src/forms/fields.py` to return the response
```python
def render_response(self, status: str = '200 OK') -> Response:
    return Response(
        status=status,
        body=[self.render().encode('utf-8')],
        headers=[('Content-Type', 'text/html')]
    )
```
