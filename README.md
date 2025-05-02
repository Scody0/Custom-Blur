# Custom Blur

![Custom Blur Logo](https://via.placeholder.com/150) <!-- Replace with actual logo or screenshot -->

**Custom Blur** is a lightweight Windows application that allows users to apply stunning blur and transparency effects to any window. With an intuitive interface, multilingual support, and customizable profiles, it offers a unique way to enhance your desktop experience. Whether you want a subtle blur or a vibrant acrylic effect, Custom Blur has you covered.

---

## Features

- **Window Effects**: Apply standard or acrylic blur and adjust transparency for any visible window.
- **Multilingual Support**: Available in English, Russian, Ukrainian, Belarusian, German, Spanish, and French.
- **Profile Management**: Save and load effect profiles for quick application to specific windows.
- **Auto-Refresh**: Automatically update the window list to keep your workspace dynamic.
- **Undo & Reset**: Easily revert changes or reset windows to their original state.
- **Fixed Window Size**: Consistent 800x600 interface for a streamlined experience.
- **Dark Mode**: Sleek, modern UI optimized for dark mode.
- **About Section**: Learn about the program with version details and developer info.

---

## Screenshots

| Main Interface | About Dialog |
|----------------|--------------|
| ![Main Interface](https://via.placeholder.com/400x300?text=Main+Interface) | ![About Dialog](https://via.placeholder.com/400x300?text=About+Dialog) |

*Replace placeholders with actual screenshots by uploading images to your repository (e.g., `screenshots/main.png`).*

---

## Installation

### Prerequisites
- **Operating System**: Windows 10 or 11 (with Desktop Window Manager enabled)
- **Python**: Version 3.6 or higher
- **Dependencies**: `customtkinter`, `pygetwindow`

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Scody0/Custom-Blur.git
   cd Custom-Blur
   ```

2. **Install Dependencies**:
   ```bash
   pip install customtkinter pygetwindow
   ```

3. **Run the Application**:
   ```bash
   python custom_blur.py
   ```

Alternatively, install dependencies from `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

## Usage

1. **Launch the Application**:
   Run `custom_blur.py` to open the Custom Blur interface.

2. **Select a Window**:
   - Use the sidebar to view a list of active windows.
   - Click a window title to select it for customization.
   - Enable **Auto-Refresh** to keep the list updated.

3. **Apply Effects**:
   - **Transparency**: Adjust the slider (50–255) to set window opacity.
   - **Blur Effect**: Toggle blur on/off and choose between **Standard Blur** or **Acrylic Blur**.
   - **Blur Settings**: Fine-tune blur opacity, intensity, and tint opacity using sliders.
   - Use **Undo** to revert the last change or **Reset** to restore the window’s original state.

4. **Manage Profiles**:
   - **Save Profile**: Save your current settings for a window.
   - **Load Profile**: Apply a saved profile to a matching window.

5. **Change Language**:
   - Select your preferred language from the sidebar dropdown (e.g., English, Українська, Русский).

6. **View About**:
   - Click the **About** button in the top bar to see program details, including version and developer info.

---

## About

- **Version**: 0.0.1
- **Developer**: Scody0
- **GitHub**: [https://github.com/Scody0](https://github.com/Scody0)
- **License**: MIT

Custom Blur is an open-source project designed to bring aesthetic window effects to Windows users. Contributions and feedback are welcome!

---

## Contributing

We love contributions! To contribute to Custom Blur:

1. **Fork the Repository**:
   Click the "Fork" button on GitHub to create your own copy.

2. **Create a Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Changes**:
   Implement your feature or bug fix, ensuring code quality and documentation.

4. **Test Thoroughly**:
   Test your changes on Windows 10/11 to ensure compatibility.

5. **Submit a Pull Request**:
   Push your branch to your fork and create a pull request with a clear description.

Please follow our [Code of Conduct](CODE_OF_CONDUCT.md) and ensure your changes align with the project’s goals.

---

## Troubleshooting

- **Blur Effects Not Working**:
  - Ensure Desktop Window Manager (DWM) is enabled (Windows 10/11).
  - Check if the selected window supports blur effects (some system windows may not).

- **Language Not Updating**:
  - Verify that `blur_config.json` is writable in the application directory.
  - Delete `blur_config.json` to reset to English.

- **Errors**:
  - Enable logging by uncommenting the logging setup in `custom_blur.py`.
  - Check `custom_blur.log` for detailed error messages.

For further assistance, open an issue on GitHub.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contact

- **Developer**: Scody0
- **GitHub**: [https://github.com/Scody0](https://github.com/Scody0)
- **Issues**: [https://github.com/Scody0/Custom-Blur/issues](https://github.com/Scody0/Custom-Blur/issues)

Feel free to reach out with questions, suggestions, or feedback!

---

*Built with ❤️ by Scody0*
