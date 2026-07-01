"""Python interface to R statistics via Docker.

Statistical computations run inside a Docker container using R. Pull the image before use:

```
docker pull ethandavisecd/tombolo:latest
```

See the [Docker Hub image](https://hub.docker.com/r/ethandavisecd/tombolo) for details.
"""

from .run import bnma, nma
from . import plots

__all__ = ["nma", "bnma", "plots"]
