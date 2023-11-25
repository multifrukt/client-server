# client-server

## web-front `/`

Offers to fill a form. Submits form to `/form_submit`

## web-front `/form_submit`

Receives form data. Sends data as JSON to API provided by `apiserver`. Receives JSON response, extracts message from it and displays on the web page

## apiserver

Listens on port 7001

Provides API `POST /`

Request example:

```json
{
    "name": "Alice",
    "profession": "Doctor"
}
```

Response example:

```json
{
    "message": "Alice is a cool Doctor"
}
```

Curl for testing:

```bash
curl -X POST http://ubuntu:7001/ \
    -H "Content-Type: application/json" \
    -d '{"name": "Alice", "profession": "Doctor"}'
```

## clicker

Opens `web-front` page, finds submit button, sends example request to the page responsible for the form action. Repeats after configurable interval
