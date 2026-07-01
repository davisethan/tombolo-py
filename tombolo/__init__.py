"""Python interface to R statistics via Docker.

Statistical computations run inside a Docker container using R. Pull the image before use:

```
docker pull ethandavisecd/tombolo:latest
```

See the [Docker Hub image](https://hub.docker.com/r/ethandavisecd/tombolo) for details.
"""

from .methods.bnma import bnma
from .methods.nma import nma

__all__ = [bnma.__name__, nma.__name__]
