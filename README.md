
# pyhttpx

A lightweight, fast, and concurrent URL status checker built in pure Python — inspired by [httpx](https://github.com/projectdiscovery/httpx) from ProjectDiscovery.


---

## 🚀 Features

- ✅ Pure Python 3 — no compilation required
- 🌐 Supports HTTP and HTTPS
- ⚡ Fast concurrent requests (via `ThreadPoolExecutor`)
- 🧠 Useful for recon, bug bounty, and OSINT tasks

---

## 📥 Installation


From source:

```bash
git clone https://github.com/kirklan34/pyhttpx.git
cd pyhttpx
python pyhttpx.py -l urls.txt
```

---

## 🧪 Usage

Basic usage:

```bash
pyhttpx -l urls.txt
```

Example `urls.txt`:

```
https://example.com
http://test.com
https://nonexistent.tld
```

Example output:

```
[200] https://example.com
[404] http://test.com
[ERROR] https://nonexistent.tld - ConnectError
```

---

## 🔧 Options

| Option        | Description                      | Required |
|---------------|----------------------------------|----------|
| `-l, --list`  | File containing URLs to check    | ✅ yes   |

---

## 🛠️ Requirements

- Python 3.7+
- [`httpx`](https://www.python-httpx.org/)

Install dependencies manually (if needed):

```bash
pip install httpx
```

---

## 🤝 Contributing

Pull requests, issues, and forks are welcome!  
If you have ideas for new features or improvements, feel free to open a discussion.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 💬 About

`pyhttpx` was built as a minimal, pip-installable alternative to tools like `httpx`, ideal for scripting and cross-platform usage.

Created with ❤️ by kirklan34(https://github.com/kirklan34)
