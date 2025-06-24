# Text Editor using Rope Data Structure

This project is an efficient **Text Editor** implemented using the **Rope Data Structure**. It supports advanced text manipulation features such as fast insertion, deletion, substring retrieval, undo/redo, and search functionality using string hashing.

---

## 📌 Features

- Insert a string at any index  
- Delete a specific number of characters from a given index  
- Retrieve substring or full text  
- Search for occurrences of a substring using a hashing technique  
- Undo and redo any editing operation  
- Efficient memory usage using a balanced Rope  
- Console-based command-line interface  

---

## 🧵 Rope Data Structure

Rope is a binary tree used to store and manipulate very long strings efficiently. It enables:

- Fast insertion and deletion operations (`O(log n)`)  
- Efficient memory usage  
- Good performance for undo/redo via persistent operations stack  

---

## 🛠 Classes

### `Rope`

Core data structure for representing the string. Supports:

- Insertion, Deletion  
- Substring retrieval  
- Concatenation, Splitting  
- Rebalancing to maintain performance  

### `Operation` and `OperationStack`

Tracks insert/delete operations for undo and redo functionality.

### `TextEditor`

Wrapper class managing the rope and operation stacks. Provides:

- `insert_string(index, text)`  
- `delete_chars(index, count)`  
- `get_string()`  
- `get_substring(index, length)`  
- `undo()` and `redo()`  
- `search_string(substring)`  

---

## 🧪 Sample Commands

Once the script is running, use the following commands:

- `i [index]`  
  Inserts a string at given index. You’ll be prompted to enter the string in the next line.
- `p`  
  Prints the entire string.
- `p [index] [length]`  
  Prints a substring of given length from specified index.
- `d [index] [length]`  
  Deletes `length` characters starting from `index`.
- `f [substring]`  
  Finds and returns all starting indices where `substring` is found.
- `u`  
  Undoes the last operation.
- `r`  
  Redoes the last undone operation.
- `l`  
  Prints the total length of the string.
- `ex`  
  Exits the editor.
- `h`  
  Displays help with list of commands.

---

## ✅ Example

```text
> i 0
hello
> i 5
 world
> p
hello world
> d 5 1
> p
helloworld
> u
Undo successful
> p
hello world
> f world
[6]
```

---

## 📦 Dependencies

- Python 3.x  
- No external libraries required  

---

## 📂 File Structure

```
text_editor_rope/
│
├── rope_editor.py     # Contains all classes and main loop
└── README.md          # Project documentation
```

---

## 🧠 Concepts Covered

- Rope Data Structure  
- Recursive tree manipulation  
- Command-line interface  
- Undo/Redo using operation stack  
- Rabin-Karp style hashing for substring search  
