# Subtraction API -- MLOps Practical

Step-by-step procedure for the subtraction experiment using Python,
FastAPI, Pytest, Jenkins, and Evidently.

**Project folder:** `D:\MLDEVOPS_ExPoe`\
**Environment:** Windows, VS Code PowerShell

## 1. Project files

``` text
MLDEVOPS_ExPoe/
├── main.py
├── test_main.py
├── monitor.py
├── requirements.txt
└── venv/
```

## 2. Create and activate virtual environment

Run these commands from the project folder:

``` powershell
python -m venv venv
.env\Scripts\Activate.ps1
```

If PowerShell blocks activation in the current terminal session:

``` powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.env\Scripts\Activate.ps1
```

You should see `(venv)` at the start of the terminal prompt.

## 3. Verify Python and installed package versions

``` powershell
python --version
python -m pip --version
python -m pip show fastapi uvicorn pytest pandas evidently
```

Optional direct version checks:

``` powershell
python -c "import pandas; print('Pandas:', pandas.__version__)"
python -c "import evidently; print('Evidently:', evidently.__version__)"
```

## 4. Install requirements

Create `requirements.txt` with:

``` text
fastapi
uvicorn
pytest
pandas<3
evidently
```

Install the packages:

``` powershell
python -m pip install -r requirements.txt
```

### Pandas / Evidently import compatibility fix

If Evidently fails to import with an error such as
`cannot import name 'infer_dtype_from_object'`, install a Pandas version
below 3:

``` powershell
python -m pip install --force-reinstall "pandas<3"
```

Verify the version and Evidently import:

``` powershell
python -c "import pandas; print(pandas.__version__)"
python -c "from evidently import Report; print('Evidently imported successfully')"
```

## 5. Python subtraction program

The standalone Python program can use a function:

``` python
def subtract(num1, num2):
    return num1 - num2


num1 = float(input("Enter the first number: "))
num2 = float(input("Enter the second number: "))

result = subtract(num1, num2)
print("The subtraction is:", result)
```

For the integrated API project, `main.py` contains:

``` python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Numbers(BaseModel):
    num1: float
    num2: float

def subtract(num1, num2):
    return num1 - num2

@app.post("/subtract")
def subtraction(numbers: Numbers):
    result = subtract(numbers.num1, numbers.num2)
    return {
        "num1": numbers.num1,
        "num2": numbers.num2,
        "result": result
    }
```

The standalone program accepts keyboard input. The FastAPI version
accepts numbers in an HTTP request. Both use the same subtraction logic.

## 6. Run and test FastAPI

Start the server:

``` powershell
python -m uvicorn main:app --reload
```

Open the interactive documentation:

`http://127.0.0.1:8000/docs`

Test `POST /subtract` using this request body:

``` json
{
  "num1": 20,
  "num2": 8
}
```

Expected response:

``` json
{
  "num1": 20,
  "num2": 8,
  "result": 12
}
```

**Note:** Visiting `http://127.0.0.1:8000/` can show `404 Not Found`
because no root (`/`) route was defined. This does not mean the server
failed. Use `/docs` to test the API.

Keep the server running in one terminal. Use another VS Code terminal
for Pytest and Evidently. Stop the server with `Ctrl+C`.

## 7. Create and run Pytest tests

Create `test_main.py`:

``` python
from main import subtract

def test_positive_numbers():
    assert subtract(20, 8) == 12

def test_negative_result():
    assert subtract(5, 10) == -5

def test_zero():
    assert subtract(10, 10) == 0

def test_decimal_numbers():
    assert subtract(5.5, 2.5) == 3.0
```

Run the tests:

``` powershell
python -m pytest -v
```

Expected: all four tests pass. Pytest discovers test functions beginning
with `test_`; `assert` checks the actual result against the expected
result.

## 8. Configure Jenkins pipeline

1.  Open Jenkins, commonly at `http://localhost:8080`.
2.  Select **New Item**.
3.  Name it `Subtraction_API_Pipeline`.
4.  Select **Pipeline**, then click **OK**.
5.  Under **Pipeline**, set **Definition** to **Pipeline script**.
6.  Paste this script:

``` groovy
pipeline {
    agent any

    stages {
        stage('Install Dependencies') {
            steps {
                dir('D:\\MLDEVOPS_ExPoe') {
                    bat 'venv\\Scripts\\python.exe -m pip install -r requirements.txt'
                }
            }
        }

        stage('Run Pytest') {
            steps {
                dir('D:\\MLDEVOPS_ExPoe') {
                    bat 'venv\\Scripts\\python.exe -m pytest -v'
                }
            }
        }
    }
}
```

7.  Click **Save**, then **Build Now**.
8.  Open the build and select **Console Output**.
9.  Confirm both stages complete successfully and the four tests pass.

**Important:** Jenkins must run on a Windows agent that can access
`D:\MLDEVOPS_ExPoe` and its `venv` folder. Change the path in both
`dir(...)` blocks if your project is elsewhere. The Jenkins service
account must have permission to access the folder.

## 9. Generate Evidently data drift report

Create `monitor.py`:

``` python
import pandas as pd
from evidently import Report
from evidently.presets import DataDriftPreset

reference_data = pd.DataFrame({
    "num1": [10, 20, 30, 40, 50, 60, 70, 80],
    "num2": [2, 4, 6, 8, 10, 12, 14, 16]
})

current_data = pd.DataFrame({
    "num1": [100, 120, 130, 140, 150, 160, 170, 180],
    "num2": [20, 40, 60, 80, 100, 120, 140, 160]
})

report = Report([
    DataDriftPreset()
])

result = report.run(
    reference_data=reference_data,
    current_data=current_data
)

result.save_html("drift_report.html")
print("Data drift report generated successfully!")
```

Run the monitoring script:

``` powershell
python monitor.py
```

Expected terminal message:

``` text
Data drift report generated successfully!
```

Open the generated HTML report:

``` powershell
start .\drift_report.html
```

The report compares the reference input dataset with the current input
dataset and checks for changes in their statistical distributions.
Evidently monitors input data drift; it does not test whether the
subtraction result is mathematically correct.

## 10. Quick command reference

  --------------------------------------------------------------------------------------------------
  Task                                Command
  ----------------------------------- --------------------------------------------------------------
  Create virtual environment          `python -m venv venv`

  Activate environment                `.env\Scripts\Activate.ps1`

  Check Python version                `python --version`

  Check installed package versions    `python -m pip show fastapi uvicorn pytest pandas evidently`

  Install requirements                `python -m pip install -r requirements.txt`

  Fix Pandas compatibility            `python -m pip install --force-reinstall "pandas<3"`

  Run FastAPI                         `python -m uvicorn main:app --reload`

  Run Pytest                          `python -m pytest -v`

  Run Evidently                       `python monitor.py`

  Open HTML report                    `start .\drift_report.html`
  --------------------------------------------------------------------------------------------------

Jenkins is run through its web interface using **Build Now**, not as a
Python terminal command.

## 11. Tool roles

  Tool        Role in this experiment
  ----------- ---------------------------------------------------------
  Python      Performs subtraction
  FastAPI     Exposes subtraction through an HTTP API
  Pytest      Tests the subtraction function
  Jenkins     Automates dependency installation and test execution
  Evidently   Compares input datasets and creates a data drift report

## 12. Final verification checklist

-   [ ] Standalone Python subtraction program runs correctly.
-   [ ] FastAPI server starts.
-   [ ] `POST /subtract` returns the correct result.
-   [ ] All four Pytest tests pass.
-   [ ] Jenkins pipeline completes successfully.
-   [ ] Evidently monitoring script runs successfully.
-   [ ] `drift_report.html` is generated and opens in a browser.

------------------------------------------------------------------------

**End of practical guide.**
