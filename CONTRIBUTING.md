# Contributing

Thank you for your interest in contributing to **Visemes Converter Tool**!

---

## Project Structure

Before contributing, make sure you are familiar with the project layout:

```
plugin_blender/
├── visemes.py                  # Entry point: bl_info, register/unregister
├── operators/
│   ├── __init__.py
│   ├── vrc.py                  # VRChat viseme operators
│   └── mmd.py                  # MMD conversion operators
├── panels/
│   ├── __init__.py
│   └── main_panel.py           # UI panel
└── utilities/
    ├── constants.py
    ├── functions.py
    └── helpers.py
```

---

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Open the project in your editor of choice
4. Install the add-on in Blender via `Edit > Preferences > Add-ons > Install`

---

## How to Contribute

### Reporting Bugs

- Open an issue and describe the problem clearly
- Include your Blender version and OS
- Attach steps to reproduce the bug

### Suggesting Features

- Open an issue with the `enhancement` label
- Describe the use case and the expected behavior

### Submitting Code

1. Create a new branch from `main`:
   ```
   git checkout -b feature/your-feature-name
   ```
2. Make your changes following the guidelines below
3. Test the add-on inside Blender before submitting
4. Open a pull request with a clear description of the changes

---

## Code Guidelines

- **Language:** all code, variable names, and `bl_description` strings must be in **English**
- **Comments:** do not add inline comments or docstrings — refer to `DOCUMENTATION.md` instead
- **Operators:** new operators go in `operators/vrc.py` or `operators/mmd.py` depending on their scope, and must be exported from `operators/__init__.py`
- **Panels:** UI changes go in `panels/main_panel.py`
- **Data / mappings:** new constants go in `utilities/constants.py`, new mapping data in `utilities/functions.py`
- **Shared utilities:** helper functions and shared state go in `utilities/helpers.py`
- Keep `visemes.py` as a thin entry point — no logic belongs there

---

## Credits

If your contribution is inspired by or based on external work, add a credit line at the top of `visemes.py` in the existing credits block.
