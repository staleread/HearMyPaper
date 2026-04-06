# 🎵 HearMyPaper

**Secure your course project, and only let the instructor listen!**

HearMyPaper is a cross-platform desktop application that lets students protect
their academic work with military-grade cryptography. Submit your projects with
confidence knowing only authorized instructors can access and listen to your
submissions.

The backend source code lives here 👉 [hmp-server](https://github.com/staleread/hmp-server)

## Development

Create and activate virtual environment

```bash
python -m venv .venv
. .venv/bin/activate
```

Install the dependencies

```bash
pip install .
```

Run the app in development mode

```bash
briefcase dev
```

---

## 📦 Supported Platforms

HearMyPaper runs on all major desktop operating systems:

| Platform | Status | Format |
|----------|--------|--------|
| **Windows** | ✅ Supported | `.msi` Installer |
| **Linux** (Ubuntu/Debian) | ✅ Supported | `.deb` Package |
| **Linux** (Arch) | ✅ Supported | Arch package |

---

## 🚀 Installation

### Windows
1. Download the `.msi` installer from [HearMyPaper Releases](https://github.com/staleread/hearmypaper/releases)
2. Run the installer and follow the setup wizard
3. Launch HearMyPaper from your Start Menu

### Linux (Ubuntu/Debian)
```bash
sudo apt install ./hearmypaper_1.0.x_amd64.deb
hearmypaper  # Launch from terminal or application menu
```

### Linux (Arch)
```bash
sudo pacman -U hearmypaper-1.0.x-x86_64.pkg.tar.zst
hearmypaper  # Launch from application menu
```

---

## 📄 License

HearMyPaper is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 👥 Credits

**Developed by:**
- Mykola Ratushniak
- Neholiuk Oleksandr

**Built with:**
- [BeeWare Toga](https://beeware.org/) - Native GUI framework
- [Briefcase](https://briefcase.readthedocs.io/) - Cross-platform packaging
- [cryptography](https://cryptography.io/) - Encryption library
