
![alt text](./lebowski.jpeg)

# Lebowski
"And that's the Dude, in Los Angeles. And even if he's a lazy man... and the Dude was certainly that. Quite possibly the laziest in Los Angeles County, which would place him high in the runnin' for laziest worldwide."

__Lebowski__ is a simple framework for globally enabling lazy imports in Python. This framework has the following advantages over others that exist:

1. You don't have to specify every library that you want lazyily imported.

2. It is fully compatible with libraries that swap out modules in sys.modules (unlike Python's native LazyLoader).

3. Import errors are NOT delayed to the first use of the library. Existance of the library is checked at the time of declaration of the import.

4. It has an extremely simple interface.

## Support

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Issues

Any issues found should be reported as GitHub issues on this repository.

## Overview

The use of the lebowski library is simple. Just follow the following code snippet:

```python
import lebowski
lebowski.enable()

import pandas
import sklearn
# etc...

lebowski.disable() # If desired
```