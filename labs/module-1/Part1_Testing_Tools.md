# Module 1 — Laboratory Activities: Part 1 — Installing Testing Tools

In this lab, we set up and configured local software testing tools to verify the BISIG ecosystem (our sign language translation platform). Instead of using expensive or cloud-dependent enterprise suites, we chose lightweight, open-source, and local-first alternatives that we can run directly in our terminal. 

This document explains why we chose each tool, how we installed them, and the steps to verify that they are working.

---

## 1. Functional / Manual Testing: Postman & Newman

For functional and manual API testing, we selected **Postman** along with its command-line runner, **Newman**. 

### Why we chose it
Postman is the standard tool for testing REST APIs. However, relying purely on a graphical interface makes automated or headless testing difficult. By using **Newman**, we can run our Postman test collections directly from the bash terminal. This makes our testing process scriptable and integration-ready.

### Setup and Installation
We installed Newman globally/locally using npm. Since this is a Node.js environment, we run it using `npx` to ensure the correct version is loaded without polluting global packages:
```bash
npx -y newman --version
```

### Local Test Configuration
We wrote a Postman Collection JSON file at `labs/module-1/bisig.postman_collection.json`. This collection contains three specific test requests targeting our local Python API backend (running on `http://localhost:8000`):
1. **API Root Check (`GET /`)**: Verifies the API server is alive and returning the welcome message.
2. **Translate Word (`GET /translate?text=hello&format=full_skeleton`)**: Confirms that a valid word query is accepted and resolved into sign language coordinates.
3. **Empty Input Validation (`GET /translate?text= `)**: Verifies the API's input sanitization by sending spaces and checking that it correctly returns a `400 Bad Request` with an error message.

### How to Run and Verify
Start the Python backend first, then run this command in your terminal:
```bash
npx newman run labs/module-1/bisig.postman_collection.json
```
Newman will execute the requests, run the embedded JavaScript assertions, and output a clean table showing the status of each test.

### What screenshot to include here
> [!TIP]
> **Screenshot 1 (functional_newman.png)**: Run the command in your terminal and take a screenshot of the Newman console output. Ensure the screenshot shows the checkmarks (`✓`) next to the three API requests and the summary table at the bottom showing 6 executed assertions and 0 failures.

---

## 2. Test Management: Verbose Terminal Runner (`pytest -v`)

For test management, we use the **PyTest Verbose Runner** (`pytest -v`) to track, catalog, and manage our test results directly in the terminal interface.

### Why we chose it
Traditional test management tools like TestLink (requires local PHP/MySQL servers) or Zephyr Squad (requires a paid Jira Cloud plugin) are heavy, proprietary, and run in the browser. Using the terminal-native verbose runner allows us to manage, filter, and inspect test suite outcomes directly in our shell, showing each individual test name and its pass/fail state in real-time.

### Setup and Installation
No external browser-based server is needed. The verbose runner is built into pytest. If needed, make sure pytest is installed:
```bash
.venv/bin/pip install pytest
```

### Local Configuration
When executing the test suite, we run pytest with the `-v` (verbose) flag:
```bash
.venv/bin/pytest -v labs/module-1/test_example.py
```
This reads the unit tests in `test_example.py`, runs them, and outputs a complete log of each test case name, its class context, execution percentage, and the result status (`PASSED`) directly to the console.

### What screenshot to include here
> [!TIP]
> **Screenshot 2 (test_management_terminal.png)**: Run the `.venv/bin/pytest -v labs/module-1/test_example.py` command in your terminal. Take a screenshot of the output, displaying the list of all 11 test cases and their green `PASSED` status labels printed directly in the shell.

---

## 3. Unit Testing: PyTest

For unit testing, we selected **PyTest**, the standard and most popular unit testing framework for Python.

### Why we chose it
PyTest is clean, easy to read, and handles test discovery automatically. It allows us to write basic assertions using Python's native `assert` statement instead of requiring boilerplate class setups.

### Setup and Installation
We activated our Python virtual environment and installed pytest:
```bash
.venv/bin/pip install pytest
```

### Local Test Configuration
Instead of using mock data or hardcoded placeholders, we wrote a comprehensive unit and integration test suite in [test_example.py](file:///workspaces/BISIG/labs/module-1/test_example.py) that directly tests the live VM environments and crawls the actual project database:
1. **VM Filesystem Integrity (`TestVMFilesystemIntegrity`)**: Recursively walks the entire `Backend-API/videos` and `Backend-API/skeletons` folders on the VM disk using `os.walk` to assert that **every single** video file has a size > 0, and **every single** skeleton coordinates JSON is syntactically valid and structurally complete. It also audits the Google MediaPipe model binary paths.
2. **On-the-fly MediaPipe Extraction Verification**: Invokes the actual Google MediaPipe landmark model APIs on the VM CPU to decode `hello.mp4` and track pose, hand, and face joints frame-by-frame. This performs real-world, heavy CPU-based machine learning joint calculations on the VM and validates the extracted 33 pose joint coordinate arrays.
3. **Live VM Endpoint Integration (`TestLiveVMEndpoints`)**: Uses `httpx` to send live HTTP requests to the running FastAPI server in the VM (`http://127.0.0.1:8000`), verifying the root endpoint metadata, translation video mapping payloads, skeleton joint outputs, and 400 Bad Request error handlers against the live uvicorn server.
4. **CDN & Hosting Connectivity Verification**: Directly queries the remote ASL Amazon S3 CDN bucket (`https://pocketsign.s3-us-west-2.amazonaws.com/`) and FSL local hosting server port (`http://161.118.197.176:8080/`) defined in `config.json` to verify network routing and asset storage accessibility.
5. **Core Database Schema Checks (`TestCoreDictionaryFiles`)**: Validates the JSON array structure and keys of `Frontend/src/data/dictionary.json`, `fsl_dictionary.json`, and `verified_signs.json`.
6. **Logic Loop Validation (`TestLogicExecutionOnRealDictionaryWords`)**: Tests text cleaning, tokenization, and character cleaning loops on all items loaded from the actual dictionaries.

### How to Run and Verify
You can run these tests in two different ways depending on your preference:
* **Direct Execution (Standard Python)**:
  ```bash
  python3 labs/module-1/test_example.py
  ```
* **Framework Execution (pytest runner)**:
  ```bash
  .venv/bin/pytest labs/module-1/test_example.py
  ```

### What screenshot to include here
> [!TIP]
> **Screenshot 3 (unit_testing_pytest.png)**: Capture a screenshot of the terminal window after running the pytest command. It should show the Python and pytest version details, the test file execution bar, and the green `15 passed in 14.Xs` line.

---

## 4. Defect Tracking & Diagnostics: BISIG Codebase Quality Scanner (`bisig_scanner.py`)

For defect tracking and monitoring, we wrote our own custom diagnostic tool named **bisig_scanner.py** that dynamically scans our codebase to identify compiler errors and code smells, laying them out in a visual directory tree structure.

### Why we chose it
Jira is a proprietary cloud service, and Bugzilla is notoriously difficult to install locally. Rather than logging issues manually in a static, hardcoded table, our **BISIG Scanner** acts as an automated static analyzer and system monitor. It prints a full directory tree (similar to the standard `tree` command) but checks the syntax and readability of every single file dynamically as it builds the tree, indicating either `[Good]` or the exact compiler error and line number next to the file.

### Setup and Configuration
We wrote the script at `labs/module-1/bisig_scanner.py` and made it executable:
```bash
chmod +x labs/module-1/bisig_scanner.py
```

### Scanner Capabilities
The tool executes multiple checks dynamically:
1. **Visual Directory Tree Compilation**: Walks all directories recursively and outputs the structure.
2. **Python Syntax Verification**: Compiles all `.py` files using the Python compiler (`py_compile`) to discover and report syntax errors.
3. **JavaScript Syntax Verification**: Checks the syntax of all `.js` files using Node's built-in syntax compiler check (`node --check`).
4. **Interactive Status Output**: Annotates each file inline in the tree with its exact validation status (e.g., `[Good]` or `[Error: SyntaxError at line X]`).
5. **Report Exporter**: Writes the full annotated tree diagram directly to `labs/module-1/bisig_report.md` for offline viewing.

### How to Run and Verify
Run the tool to execute a complete diagnostic tree scan:
```bash
./labs/module-1/bisig_scanner.py
```

### What screenshot to include here
> [!TIP]
> **Screenshot 4 (defect_tracking_cli.png)**: Run the `./labs/module-1/bisig_scanner.py` command in your terminal. Take a screenshot showing the dynamic terminal output—specifically displaying the visual folder/file tree annotated with the green `[Good]` tags or red compiler error lines.
