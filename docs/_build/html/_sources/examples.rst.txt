Example Gallery
===============

This gallery showcases various examples of CodeVideoRenderer in action, demonstrating different use cases and configurations.

Basic Examples
--------------

Simple Python Function
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from CodeVideoRenderer import CameraFollowCursorCV

   code = '''def fibonacci(n):
    """Calculate the nth Fibonacci number"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Example usage
result = fibonacci(10)
print(f"Fibonacci(10) = {result}")'''

   renderer = CameraFollowCursorCV(
       code=('string', code),
       language='python',
       formatter_style='github-dark',
       video_name='FibonacciExample'
   )
   renderer.render()

JavaScript Example
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   js_code = '''function debounce(func, wait) {
       let timeout;
       return function executedFunction(...args) {
           const later = () => {
               clearTimeout(timeout);
               func(...args);
           };
           clearTimeout(timeout);
           timeout = setTimeout(later, wait);
       };
   }

   // Usage example
   const debouncedSearch = debounce(searchFunction, 300);'''

   renderer = CameraFollowCursorCV(
       code=('string', js_code),
       language='javascript',
       formatter_style='monokai'
   )
   renderer.render()

Intermediate Examples
---------------------

File-based Animation
^^^^^^^^^^^^^^^^^^^^

Animate code from an existing file:

.. code-block:: python

   renderer = CameraFollowCursorCV(
       code=('file', 'src/algorithm.py'),
       language='python',
       video_name='AlgorithmImplementation'
   )
   renderer.render()

Custom Typing Speed
^^^^^^^^^^^^^^^^^^^

Simulate different coding styles:

.. code-block:: python

   # Fast typing (expert coder)
   renderer_fast = CameraFollowCursorCV(
       code=('string', 'code'),
       language='python',
       interval_range=(0.03, 0.06)
   )

   # Slow typing (learning/teaching)
   renderer_slow = CameraFollowCursorCV(
       code=('string', 'code'),
       language='python',
       interval_range=(0.2, 0.4)
   )

Advanced Examples
-----------------

Multi-language Demonstration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Showcase code in different programming languages:

.. code-block:: python

   languages_examples = [
       ('python', 'python_code'),
       ('javascript', 'js_code'),
       ('java', 'java_code'),
       ('cpp', 'cpp_code')
   ]

   for lang, code in languages_examples:
       renderer = CameraFollowCursorCV(
           code=('string', code),
           language=lang,
           video_name=f'{lang}_example'
       )
       renderer.render()

Custom Styling
^^^^^^^^^^^^^^

Experiment with different syntax highlighting themes:

.. code-block:: python

   styles = ['github-dark', 'monokai', 'solarized-dark', 'dracula']

   for style in styles:
       renderer = CameraFollowCursorCV(
           code=('string', 'example_code'),
           language='python',
           formatter_style=style,
           video_name=f'style_{style}'
       )
       renderer.render()

Real-world Use Cases
--------------------

Algorithm Explanation
^^^^^^^^^^^^^^^^^^^^^

Demonstrate sorting algorithms:

.. code-block:: python

   sorting_code = '''def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

# Example usage
numbers = [3, 6, 8, 10, 1, 2, 1]
sorted_numbers = quicksort(numbers)'''

Code Review Demonstration
^^^^^^^^^^^^^^^^^^^^^^^^^

Show before/after code improvements:

.. code-block:: python

   # Original code
   original = '''def calculate_total(items):
    total = 0
    for item in items:
        total += item.price
    return total'''

   # Improved code
   improved = '''from typing import List
    from dataclasses import dataclass

    @dataclass
    class Item:
        price: float

    def calculate_total(items: List[Item]) -> float:
        """Calculate total price of items."""
        return sum(item.price for item in items)'''

Video Output Examples
---------------------

Generated videos will feature:

* **Smooth typing animation** with realistic timing
* **Syntax highlighting** appropriate for each language
* **Camera movement** that follows the cursor naturally
* **Professional appearance** suitable for presentations

Getting the Examples
--------------------

All examples can be found in the GitHub repository:

* `Example scripts <https://github.com/yourusername/CodeVideoRenderer/tree/main/examples>`_
* `Sample output videos <https://github.com/yourusername/CodeVideoRenderer/tree/main/samples>`_

.. seealso::
   :doc:`tutorials` for step-by-step guides
   :doc:`reference` for detailed API documentation
   :doc:`installation` for setup instructions