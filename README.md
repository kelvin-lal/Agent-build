# Build my own Agent

## Description
A Python-based Agent that collects system metrics and sends them to Datadog via the Datadog API. The agent runs in the background with a command line menu to check the Agent Status as well as input an API key at to stop/exit the Agent

## Installation
- For US1 Site
    - install the project, and run 'python run.py' from the home /agent directory
- For all other sites
    - install the project
    - change the DD_SITE parameter in /agent/agent/config.py file
    - run 'python run.py' from the home /agent directory

## Key errors faced
- Retrieving metrics
    - psutil.disk_usage reuires a path
        https://psutil.readthedocs.io/en/latest/#psutil.disk_usage
        We can just use '/' for now, need to revisit this for a better solution, as a defined path configuration or maybe some kind of autodiscovery would be better here
- Dynamic class implimentation
    - Key error faced was attempting to populate the checks in the checkRun.py file with the correct check name, as the goal was to have the check class have the metric type attribute populated automatically with a check, similar to how the Datadog Agent automatically grabs the itnegration/check name. This was uncompleted and a hardcode for the check names was completed

# Design discussion

## Project Structure
```
Agent-build/
├── run.py                      # Entry point
├── __init__.py
├── agent/
│   ├── __init__.py
│   ├── agent.py                # Core Agent
│   ├── menu.py                 # CLI interface
│   ├── config.py               # Configuration file
│   └── settings.py             # Agent settings
├── metrics/
│   ├── metrics.py              # System metric collection
│   ├── metricSubmission.py     # Datadog API submission
│   ├── metricBuffer.py         # Metric buffering
│   ├── metricsConfig.py        # Metrics configuration
│   └── tags/
│       ├── __init__.py
│       ├── customTags.py       # Custom tag definitions
│       ├── tagEnricher.py      # Tag enrichment logic
│       └── tagProvider.py      # Tag provider interface
├── checks/
│   ├── __init__.py
│   ├── checkRun.py             # Status check implementation
│   ├── checkPrint.py           # Status check formatting
│   └── customCheck.py          # Custom check implementation
├── settings/
│   └── agent_settings.json     # Persistent agent settings
└── .gitignore
```
## Component Details

### 1. Entry Point (`run.py`)

Simple python file to be run at the CLI. It initializes the code by sending you to the main menu

### 2. Agent Module (`agent/`)

#### `agent.py`
- **Purpose**: Core Agent function that is on a constant loop to collect metrics
- **Function**:
  - Runs in a background thread
  - Collects metrics every 1 second
  - Increments `Check.metric_counts` for status check
  - Sets environment variables for Datadog API authentication
  - threaded in the background of the menu.py

#### `menu.py`
- **Purpose**: Command-line interface for user interaction
- **Function**:
  - Agent Stopped: Triggers user to Start, Enter API Key, and Exit
  - Agent Running: Triggers a Stop, Exit, and Status Check commands

#### `config.py`
- **Purpose**: Config class for API/Site variable needed to send metrics with getters/setters used in the menu.py to set the variable and used in the agent.py to set as a global variable

### 3. Metrics Module (`metrics/`)

#### `metrics.py`
- **Purpose**: Metric collection declarations using the psutil library
- **Function**:
  - `cpuMetrics()` → CPU usage %, CPU count
  - `memoryMetrics()` → Memory usage %, available memory
  - `diskMetrics()` → Disk usage %

#### `metricSubmission.py`
- **Purpose**: Sends metrics to Datadog via the metrics API: https://docs.datadoghq.com/api/latest/metrics

### 4. Checks Module (`checks/`)

#### `checkRun.py`
- **Purpose**: Status initialization, triggered from the meu.py once the user selects a status output, can only be run once the Agent is started. 


#### `checkPrint.py`
- **Purpose**: Formatted consoe output triggered from the checkRun.py file
- **Function**: `check_print(check)` — Prints metric type, count, and OK/Error status

#### `customCheck.py`
- **Purpose**: Base class for any user-defined custom checks/agent that will send metrics through the same API framework as the system metrics collected by the Agent

## Design Decisions
- Having this project run from the CLI rather than a start command was something I wanted to try, as the traditional Datadog Agent is shown to have some confusion with the initial configuration and checking its status. 
- Creating three separate modules for the three key primary functions was something needed for the organization/readability of this project. Some frustrations over calling each file/class were present, but this level of organization was key for a exercise like this
- Threading the Agent and running it in the background is simliar to the Datadog Agent's use of Concurrency, running multiple processes together via goroutines. For my simple project, it was just so the menu could be present while the Agent runs in the background
- Class variales were used for the Metrics and Check initializations, and should have also been used for the Agent as well, similar to the Datadog Agent's use of encapsulation and object-oriented design. They were used to group related functionality, and if this project was larger, they would allow for easier scaling by adding new metric types or checks without modifying existing code
- The Environment variable such as the API being set from the CLI rather than manually entering the code was a decision made to subvert the Datadog Agent's key annoyance from end users, the manual configuration. It was a fun idea and something I just wanted to do


## Future Improvements

- Dynamic Metric registration
    - In the Status Check, each metric type is hardcoded. Finding a dynamic way to have the class attributes set to both the out of the box metric types (CPU, System, Disk metric types) as well as the custom check. Key error faced as having the class attribute be able to find the metric type to set in the Status Check
- Dynamic Metric Collection
    - Currently, only a handful of system metrics are being collected. Although the Datadog Agent also uses the psutil library, and manually gathers the metrics similar to how this Agent is implimented, it would be nice to see an autodiscovery type of implimentation to find all metrics available through a library like psutil
- Complete Custom Check
    - Given more time, I would like to develop my own intergation/check, after some confusion for the Exercise requirements resulted in me completed a status.log type of check
    - Implimenting a full custom integration to collect and send metrics
- Error handling for API failures
    - There is currently no error handling for any errors recieved from the Datadog API other than setting the API key, which could still be incorrect. Given more time, it would nice to add some error handling, especially and the API is the crux of this exercise


