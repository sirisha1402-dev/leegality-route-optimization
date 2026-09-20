# Network Route Optimization API

A Django REST Framework API for managing network nodes and directed edges and calculating the shortest route based on network latency.

## Tech Stack

* Python
* Django
* Django REST Framework
* SQLite
* Dijkstra's shortest-path algorithm

## Setup

Clone the repository:

```bash
git clone <repository-url>
cd leegality-route-optimization
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

### Windows

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Run tests:

```bash
python manage.py test
```

Start the server:

```bash
python manage.py runserver
```

## API Endpoints

### Create Node

`POST /nodes/`

Request:

```json
{
    "name": "ServerA"
}
```

Response:

```json
{
    "id": 1,
    "name": "ServerA"
}
```

### Create Edge

`POST /edges/`

Request:

```json
{
    "source": "ServerA",
    "destination": "ServerB",
    "latency": 12.5
}
```

### Find Shortest Route

`POST /routes/shortest/`

Request:

```json
{
    "source": "ServerA",
    "destination": "ServerD"
}
```

Example response:

```json
{
    "total_latency": 23.4,
    "path": [
        "ServerA",
        "ServerB",
        "ServerD"
    ]
}
```

### Route History

`GET /routes/history/`

Optional query parameters:

* `source`
* `destination`
* `limit`
* `date_from`
* `date_to`

Example:

```text
GET /routes/history/?source=ServerA&destination=ServerD&limit=10
```

## Optional Endpoints

### List Nodes

`GET /nodes/`

### List Edges

`GET /edges/`

### Delete Node

`DELETE /nodes/{id}/`

### Delete Edge

`DELETE /edges/{id}/`

## Algorithm

The shortest route is calculated using Dijkstra's algorithm.

Each edge has a positive latency, making Dijkstra's algorithm suitable for this problem.

The implementation uses a priority queue (`heapq`) to efficiently select the next node with the smallest known distance.

Approximate complexity:

`O((V + E) log V)`

where:

* `V` = number of nodes
* `E` = number of edges

## Assumptions

* Edges are directed.
* Latency must be greater than zero.
* Node names are unique.
* Duplicate directed edges are not allowed.
* A successful shortest-route calculation is stored in route history.
* SQLite is used for local development and assessment purposes.

## Testing

Run:

```bash
python manage.py test
```

The test suite covers node creation, duplicate validation, edge creation, invalid latency, shortest-path calculation, unavailable routes, and route history.
